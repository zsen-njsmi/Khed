"""
Arguments collection from the CLI
"""

import argparse

default_folder = 'DownloadedAnimes'


def get_args():
    """
    Function to get arguments passed from cli.
    """

    ###########################################
    # Support for mutuallyexclusive           #
    # arguments currently not provided        #
    ###########################################
    parser = argparse.ArgumentParser(
                            description="Download,search and enjoy your animes."
                            ) 
                                    
    parser.add_argument('-d','--download',
                        dest="download_anime",
                        help="Downloads the anime, if found."
                        )
    parser.add_argument('-s','--search',
                        help="Searches the anime name",
                        )
    parser.add_argument('-l','--list-genres',
                        dest='genres',
                        action='store_true',
                        help="List the available genres",
                        )
    parser.add_argument('-p','--most-popular',
                        dest='most_popular',
                        action='store_true',
                        help="Get the most popular animes",
                        )
    
    parser.add_argument('-f','--folder',
                        dest='folder',
                        help="Download folder path.",
                        default=default_folder
                        )
    # I know the short form is ugly here,please look away.  

    parser.add_argument('-a','--archive',
                        help="Uses the archived folder",
                        )
    parser.add_argument('-r','--range',
                        help="range of episodes\
                              e.g. 45-30",
                        dest='episode_range',
                        default='1'
                        )
    parser.add_argument('-si','--search-index',
                        help="Index of anime to be used",
                        dest='search_index',
                        type = int,
                        default=1
                        )
    parser.add_argument('-i','--info',
                        help="Information for a particular anime",
                    )

    

    ####################
    # Feature dependent#
    ####################
    
    

    args = parser.parse_args()
    
    return args

if __name__=="__main__":
    r = get_args()
    print(r.search)
    