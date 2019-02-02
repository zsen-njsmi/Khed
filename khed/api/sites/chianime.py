"""
This module provides API like service for the anime site chiaanime.tv
It used selenium for the final step in the process of getting information
if anime is to be downloaded, as the download link is rendered by
javascript.
This currently only supports Firefox headless versions.
Use of selenium creates an added overhead and may slow down the script
and thus it is recommended that you have atleast a moderate 
internet connection.

"""



import os 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests 
from bs4 import BeautifulSoup




class ChiaAnime():
    """API To chiaanime.tv site"""

    def __init__(self):
        self._base_url = 'http://ww2.chia-anime.tv'
        self.session = requests.Session()
   
  
    def search(self,anime):
        """
        Searches the anime 
        :param anime: anime name to be search
        :return: list of dictionaries, each consisting 'name' and 'url' as key or None. 
        """
        s = self.session 
        url = '{base_url}/search/{search_item}'.format(base_url=self._base_url,search_item=anime)

        res = s.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text,'lxml')   # add lxml to requirements.
        raw_result = soup.select('[class~=title] > a')       # Results.
        
        # if raw_result is empty, list will be empty, thus will evaluate to None
        result = [
                    {
                        'name':elem.text,
                        'url':elem.get('href',None),
                    }
                    for elem in raw_result
                ]
        return result


    def show_genres(self):
        """
        List all the genres available in the website

        :return: List of dictionaries with, 'name' and 'url'.
        """
        s = self.session
        url = '{base_url}/index'.format(base_url=self._base_url)

        res = s.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text,'lxml')
        #result in raw form (includes the tags also in the 
        # formed list).
        raw_result = soup.select('p[style] > a')
        
        
        result = [
                    {
                        'name':elem.text, #extracting the genre name
                        'url' :elem.get('href',None) #getting the url (None if not found)
                    }
                    for elem in raw_result
                ]
        return result
            

    def under_genre(self,genre_name):
        """
        Extract information under specific genres

        :param genre_name: name of the genre
        :return: list of dictionaries, with 'name' and 'url' of anime or None
        """
        s = self.session
        genre_name = genre_name.casefold() # case insensitive
        add_url = '?genre={genre_name}'.format(genre_name=genre_name)
        url = '{base_url}/{add_url}'.format(base_url=self.base_url,add_url=add_url)
        res = s.get(url)
        soup = BeautifulSoup(res.text,'lxml')
        
        raw_result = soup.select('h3 > a[style]')
        result = [
                    {
                        'name':elem.text,
                        'url' :elem.get('href',None)
                    }
                    for elem in raw_result
        ]
        return result


    def most_popular(self):
        """
        Lists the most-popular animes on the website

        :return: List of dictionaries, with 'name' and 'url'.
        """
        s = self.session
        popular = 'most-popular-anime-series/'
        url = '{base_url}/{added_info}'.format(base_url=self._base_url,added_info=popular)

        res = s.get(url)  
        res.raise_for_status()  # raises error with connectivity
        soup = BeautifulSoup(res.text,'lxml')
        raw_result = soup.select('div[style] h3 > a')

        result = [
                    {'name':elem.text,
                     'url' :elem.get('href',None),
                    }
                    for elem in raw_result
        ]
        return result


    def anime_info(self,url=None):
        """
        Provides the info available for an anime.

        :param url: Url to the anime info needed
        :return: dictionary of *'info', 'value', where info is the information
        """
        s = self.session
        res = s.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text,'lxml')


        # Due to ineffecient site building, and ineffecient coding, following is done :/
        anime_info = soup.select('blockquote > div')
        anime_plot = soup.select('blockquote > p')

        paired_values = [i.text.strip().split(':') for i in anime_info]
        paired_values.append(['plot',anime_plot[0].text.strip()])

        # The above give something like [['english','some value'],['another','another_value']
        
       
        result_dict = {
                    i[0].casefold():' '.join(i[1:]).strip() for i in paired_values
        }
        # The above converts the paired values to dict.

        return result_dict


    def get_episodes_link(self,anime_url,start,end):
        """
        Generator function yielding episodes_download_url

        :param anime_url: This is the main page url
        :param range: A string of number specifying the range
                      of episodes.
                      Default range is 1, only the first episode url
        :yield: episode_download_url
        """

        s = self.session
        res = s.get(anime_url)
        soup = BeautifulSoup(res.text,'lxml')
        all_episode_links = soup.select('h3[itemprop] > a')
        
        # Episode links are in reverse order
        all_episode_links.reverse()

        
        driver = self._get_browser()
        for i in all_episode_links[start-1: end]:
            '''
            This for loop do not check if the end range is valid.
            For end range beyond the links, all links are included uptill last link.
            '''
            episode_url = i.get('href')
            episode_download_urls = self._extract_download_url(episode_url,driver)
            yield episode_download_urls
        driver.quit()
    
    ########################################
    # Following functions are used only for# 
    # implementation details.              #
    #######################################

    def _url_to_anime_premium(self,episode_url):
        """Get the anime premium site links
        :param episode_url: (str) url of the episode
        :return: Download url of the episode 
        """
        s = self.session
        res = s.get(episode_url)
        soup = BeautifulSoup(res.text,'lxml')
        # Finding anime_premium download site link
        raw_result = soup.find(id='download')
        url = raw_result.get('href')
        return url


    # This is used to add support for multiple browsers.
    @staticmethod
    def _get_browser(browser='firefox'):
        """
        Internal usage, gets the browser to be used for scraping
        :return: A selenium webdriver
        """
        
        if browser.casefold() == 'firefox':
            driver_options = webdriver.FirefoxOptions()
            driver_options.add_argument('--headless')
            driver = webdriver.Firefox(options=driver_options)
            return driver


    def _extract_download_url(self,episode_url,browser):
        """Gets the download url for the episode
        :param episode_url: url (str) of the episode
        :param return: (str) of download url
        """
        
        anime_premium_link = self._url_to_anime_premium(episode_url)
        driver = browser
        driver.get(anime_premium_link)
        # There must be exception catching here 
        elements = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[target='_blank']"))
                            )
        name = os.path.basename(episode_url.strip('/'))
        # This gathers all the download links for episode
        # e.g. Server 0, server 1 etc.
        episode_download_urls = {
                                name : [elem.get_attribute('href') for elem in elements]
        }
        
        return episode_download_urls
    

    @property
    def base_url(self):
        return self._base_url


    @base_url.setter
    def base_url(self,url):
        #make it raise an exception if invalid url given
        self._base_url = url
    