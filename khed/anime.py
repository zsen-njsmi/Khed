#!usr/bin/env python3

"""
The Driver program
Currently the only site supported is chiaanime.tv
""" 

import sys
from pathlib import Path

from .api import ChiaAnime 
from .args import get_args 
from .interface import (extract, 
                        anime_info_output,
                        download_info)

from .downloader import Downloader
 

class Anime:
    ''' 
    Main Class
    '''

    def __init__(self):
        self.chiaanime = ChiaAnime()
        self.args = get_args()
        # used to store anime search result.
        self.result = None


    def _anime_processing(self, anime_result, anime_num=None, option=None):
        """
        Common interface for processing anime
        result.
        """

        if not anime_num and not option:
            anime_num, option = extract(anime_result, extractor='anime')
        url = anime_result[anime_num-1].get('url')
        if option=='i':
            self.anime_info(url)
        
        if option=='d':
            self.anime_download(url)


    def _searcher(self,anime_name, index=None, choice=None):
        """
        A common interface for downloading,info and searching
        This is used only for implementation details.

        :param anime_name: A str of anime name to be searched
        :param index: Search index to be used.
        :param choice: Used to direct the flow of program from either
                       info or download.
        """

        anime_result = self.chiaanime.search(anime_name)
        # Temporary storing anime_result for further processing.
        self.result = anime_result

        if not anime_result:
            sys.exit("Sorry,no results found for {anime_name}, maybe try its japanese name ".format(anime_name=anime_name))
        self._anime_processing(anime_result, index, choice)


    def _create_download_folder(self):
        """
        A single channel to create a folder.
        Provides easy interface for scalable folder operations
        """

        folder = self.args.folder
        cur_dir = Path.cwd() # Consider replacing this with Path(__file__).parent
        folder_path = cur_dir / folder
        
        if not folder_path.exists():
            folder_path.mkdir()
            
        return folder_path


    def anime_download(self, anime_url): 
        """Download anime
        :param anime_url: Url to animes main page
        
        """
        
        folder = self._create_download_folder()
        
        print("+"*34)
        print("Downloaded folder is: {}".format(folder))
        print("To change rerun the program with --folder option")
        print('+'*34)

        if self.args.download_anime:
        # Download is directly invoked, hence use the --range
        # argument.
            ep_range = download_info(self.args.episode_range)

        else:
        # Download is indirectly invoked, give 
        # user an interface for specifying range
            ep_range = download_info()
          
        anime_name = Path(anime_url.strip('/')).parent
        print('\nDownloading {}, please wait'.format(anime_name))

        #extracting episode ranges
        download_url_generator = self.chiaanime.get_episodes_link
        downloader = Downloader(folder)
        
        for url in download_url_generator(anime_url, *ep_range):
            downloader.run(url)
        sys.exit('Bye :D')


    def anime_info(self, anime_url):
        '''
        Provides the information about an anime, 
        :param anime_url: main url of the anime
        ''' 
        
        result_info = self.chiaanime.anime_info(url=anime_url)
        option = anime_info_output(result_info)
        
        if option == 'download':
            self.anime_download(anime_url)

        if option == 'back':
            # move back to the displayed list of animes
            # Thus, imitating the _searcher, but instead of again getting the
            # search result, use the temporary search result
            self._anime_processing(self.result)
        sys.exit('Bye :D')


    def run(self):
        """
        Main function
        """
        
        args = self.args
        
        if args.search: # add a waiting message, probably use the threading.(could be fun :D)
            anime = args.search
            self._searcher(anime)

        if args.download_anime:
            anime = args.download_anime
            index = args.search_index
            self._searcher(anime, index, choice='d')
        
        if args.info:
            anime = args.info
            index = args.search_index
            self._searcher(anime, index, choice='i')
        
        if args.genres: 
            genres_result = self.chiaanime.show_genres()
            genre_name = extract(genres_result, extractor='genres')
            under_genre_result = self.chiaanime.under_genre(genre_name=genre_name)
            self._anime_processing(under_genre_result)

        if args.most_popular:
            anime_result = self.chiaanime.most_popular()
            self._anime_processing(anime_result)
            

def main():
    """
    Main console_scipt entry point 
    """
    
    anime = Anime()
    anime.run()
