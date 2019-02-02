"""
Code in this module is very ugly, look at your own risk.

"""
import sys


def _output(result):
    """Common User interface"""
    print('='*34)
    print('WELCOME, Your search results are : ')
    print('='*34)
    for i,data in enumerate(result):
        num = i+1
        print('{index}. {data_name}'.format(index=num,data_name=data.get('name')))
    return 

def _selecting_anime():
    """One function interface to select anime"""
    
    while True:
        move_ahead = input("\nDownload or access anime info, [y/n]? ")
        
        if not move_ahead:  # nothing entered
            continue

        if move_ahead.casefold() == 'y':
            # It might be good to use some library, maybe textwrap ? o.O
            print('\n')
            print('+'*34)
            print('Available options are: ')
            print('+'*34)

            print('\n[anime number] ([i] | [d]) These are positional argument.')
            print('i: Show anime info')
            print('d: Download the season')
            print('q: Quit')
            print('\ne.g. 1 i (info of 1st anime) or 1 d (download) \n')
            
            available_options = {
                                'd',
                                'i'
                                }
            # check for EOFError: not added right now.
            while True:
                option = input('Enter your option: ')
                option_list = option.strip().split(' ',1)
                if option.casefold()=='q':
                    sys.exit('Bye')
                if len(option_list) == 2:
                    if not option_list[1] in available_options:
                        print("No argument {} available, please try again".format(option_list[1]))
                        continue
                    num,option = (  (int(option_list[0])), 
                                    (option_list[1])
                                )
                    break
                else:
                    print('{option} is wrong, please try again'.format(option=option))
                    continue
            break

        if move_ahead.casefold() == 'n':
            sys.exit('Okay will see you later.')
    return num,option
    
def _anime_extractor(s_result : list):
    '''
    It does something.
    '''
    _output(s_result)
    return _selecting_anime()
                
def _genre_extractor(g_result : list):
    _output(g_result)
    while True:
        move_ahead = input("Hey, want to see animes under specific genre? [y/n] (n for quit): ")
        if move_ahead.casefold() == 'n':
            sys.exit('Exiting')

        if move_ahead.casefold() == 'y':
            genre = input("Enter the genre\n")
            break
        else:
            continue
    return genre.casefold()

def extract(passed_result,extractor=None):
    """
    Extracts and outputs the text from the given list

    """
    # You have to ensure only one of the extractors are given,
    #  or as the arguments specify.
    if extractor=='anime':
        return _anime_extractor(passed_result)

    if extractor =='genres':
        return _genre_extractor(passed_result)
    
def _selecting_info(info : dict):
    """
    Used to select anime from the user, to show information
    """
    move_ahead = '' 
    while True:
        console_string = """Enter the info name: [[q] quit; [b] back; [d] download]\n\n"""
        option = input(console_string).strip()

        if not option:
            continue
        if option.casefold()=='q':
            sys.exit("Bye for now ;)")
        if option.casefold() not in info:
            if option.casefold() == 'd':
                move_ahead = 'download'
                break
            elif option.casefold() == 'b':
                move_ahead = 'back'
                break
            print("'{}' wrong info\n".format(option))
            continue

        value = info[option.casefold()]
        if not value:
            print("Sorry but information for {} is  not updated by site".format(option))
        print(value)
        continue
    return move_ahead
 
def anime_info_output(info : dict):
    
        print("\nWelcome to the info section of anime")
        print("Available info:")
        for i,val in enumerate(info.keys()):
            num = i + 1
            print("\t{index}. {val}".format(index=num,val=val))
        # sys will exit in _selecting_info if no info is selected
        return _selecting_info(info)

def download_info(episodes=None):
    """Interface to Download
    :return: a tuple of integers
    """
    if not episodes:
        # Indirect download invoked.
        episodes = input("Enter the episode numbers\ne.g. 45-47 will download episodes from 45 to 47(including)\n[q to quit]\n")
        if episodes.casefold() == 'q':
            sys.exit('Bye :D')
        
    # Stripping of white spaces
    stripped_episodes = episodes.strip()
    tupled_episodes = tuple(map(int,stripped_episodes.split('-')))
    #Get the *integer* indexes from stripped string
    try:
        ep_start,ep_end = tupled_episodes
    except ValueError: # if only one episode entered
        ep_start = tupled_episodes[0] # Only get the first episode.
        ep_end = ep_start
    return ep_start, ep_end


