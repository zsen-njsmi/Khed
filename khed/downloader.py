"""
Downloader interface
Class is used to ease the process of adding features such as
archiving the file, and using database, multithreaded downloading
asynch download.

"""
import os

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
 
class Downloader():
    '''
    Sequentially downloads.
    '''

    def __init__(self,folder):
        self.session = requests.Session()
        self.download_folder_path = folder
    
    
    def run(self,url):
        '''
        Main function that downloads the url.
        '''
        session = self.session
        file_name = list(url.keys())[0]
        file_path = '{folder}/{episode_name}'.format(
                                folder = self.download_folder_path,
                                episode_name=file_name
        )
        current_ep_url = url[file_name][0] # First server is used
        print("Episode: {}".format(file_name))
        try:
            downloaded_file_size = os.path.getsize(file_path)
        except FileNotFoundError:
            downloaded_file_size = 0
        headers = {
                "Range":"bytes={}-".format(downloaded_file_size)
        }
        with open(file_path,'ab') as f:
            with session.get(current_ep_url,stream=True,headers=headers) as s:
                current_file_size = int(s.headers['Content-Length'])
                total_file_size = current_file_size + downloaded_file_size 
                print('\nTotal size of file: {}B'.format(total_file_size))
                bars = int(total_file_size)//1024
                pos = downloaded_file_size//1024
                for chunk in tqdm( 
                                iterable = s.iter_content(chunk_size=1024),
                                initial=pos,
                                total = bars,
                                unit = 'KB',
                                unit_scale=True,
                                unit_divisor=1024,
                                 ):
                    if chunk:
                        f.write(chunk)










                
