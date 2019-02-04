Khed
---
Khed is an easy to use, **Free anime downloader**, supporting episodes playlists and resumable downloads. At present it only supports *nix* like Operating System. Although its free, it is recommended that you don't abuse this program. 
Currently supported site is [chia-anime](http://ww2.chia-anime.tv/) 

![upload_content1](https://user-images.githubusercontent.com/45007276/52194145-a4f1b000-2878-11e9-9fe1-59a3595e46a3.png) 
![upload_content2](https://user-images.githubusercontent.com/45007276/52194160-b5a22600-2878-11e9-904d-959da9d5e2fe.png)

## Features

1. Searching of anime by name.
2. Downloading anime.
3. Episodes playlist.
4. Resuming downloads.
5. Download progress.
6. User-defined output folder.

## Dependencies

Currently only *nix* like Operating Systems are supported.

Requires Python 3.4+ and pip3 for installing and running.

It relies on Firefox headless mode, so make sure you have Firefox version > 56.0 installed, also **geckodriver** is needed, you can follow [Install geckodriver for firefox](https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu) to see how to download and configure it.

*NOTE: This program is tested on Ubuntu 18.04 with Python 3.6*

## Installation

1.`$ pip3 install khed` : Recommended way to install, as it installs all the requirements.

 OR 
 
2. `$ git clone https://github.com/bnu123/Khed`: First clone this repository.

   `$ pip3 install . `: Then install it.

## Usage

This script requires arguments to run, passing script arguments is easy and this script does not have too many arguments.
It would be helpful for you if you remember that the backbone of this program is its searching functionality, almost every argument uses search internally.

### Searching 

`-s` or `--search` argument is used for searching an anime.
e.g.
```
$ khed --search=Boku
                          
==================================
WELCOME, Your search results are : 
==================================
1. Boku dake ga Inai Machi
2. Boku no Hero Academia
3. Boku no Hero Academia 2nd Season
4. Boku no Hero Academia 3rd Season
5. Boku no Kanojo ga Majimesugiru Sho-bitch na Ken
6. Boku no Kanojo ga Majimesugiru Sho-bitch na Ken OVA
7. Boku wa Tomodachi ga Sukunai
8. Boku wa Tomodachi ga Sukunai Next
9. Bokura ga Ita
10. Bokura wa Minna Kawaisou
11. Bokurano
12. Bokusatsu Tenshi Dokuro

Download or access anime info, [y/n]? 
```
From here you can also move-ahead and download any anime or get anime info.

*NOTE: Sometimes the search will tell that no anime was found, you can try and then enter the Japanese name of the anime or try to shorten the name , e.g. use Bok instead of Boku no.*

### Downloading

`-d` or `--download` along with *other arguments* make for a powerful downloader.

#### Basic usage 
For downloading:  `$ khed -d=anime name`. Now as download uses search internally to lookup for the anime name, the first episode of the first anime (if found) will be downloaded.
e.g. following the above example
```
$ khed --download=Boku
```
This will download the first episode of `Boku dake ga Inai Machi` which is the anime at 1st index.

#### Advanced usage
Gives a fine grained control over download. This script provides extra arguments along with the `--download` argument to get anime and episodes specifically.
e.g.
```
$ khed --download=Boku --search-index=8 --range=3-5           : This will fetch the 8th (search-index) anime from the search
                                                                result, and download episodes: 3, 4 and 5.
                                                               
                                                              : --search-index MUST be correct, if not, a huge error list will
                                                                be shown, so it is recommended that you run --search on the 
                                                                anime name before downloading to see the --search-index.
                                                                
$ khed -d Boku -si 8 -r 3-4                                    : Short form for the above.

$ khed -d Boku --folder=folder name                            : This specifies the folder to be downloaded to. folder 
                                                                 does not need to exist, but either must be an *absolute path*
                                                                 or just a name.
                                                                 e.g. /home/user/FOLDER_NAME OR Anime, and corresponding 
                                                                 folder will be created if they does not exist.
                                                        
$ khed -d Boku -r 3-4                                          : --search-index default is 1, so first anime selected.

$ khed -d Boku -si 4                                           : --range default is 1, only 1st episode is downloaded.

$ khed -d Boku                                                 : This is the basic usage, --range,--search-index default to 1.

default folder is "DownloadedAnime" which will be create in your current directory, which is the directory you invoked the command with.

```
*NOTE `--range` specifies Episode numbers, i.e. `--range=10-20` will include Episode-10,11,12...20*

### Information

This script also allows you to get the anime information. Getting information is similar to downloading an anime.

```
$ khed --info=Boku

Welcome to the info section of anime
Available info:
	1. english
	2. synonyms
	3. japanese
	4. type
	5. episodes
	6. status
	7. aired
	8. premiered
	9. genres
	10. duration
	11. rating
	12. plot
Enter the info name: [[q] quit; [b] back; [d] download]
```
As shown above, the available info can be used
*Note: Unlike `--search` here the info name has to be typed to get the info e.g. `plot` will give the info rather than `12`.
Also, there is no use of `--range` as information is only about anime not about episodes, which is what range is for.*

Using info:
```
$ khed --info=Boku --search-index=4                   : Use the 4th anime result from search.
$ khed -i Boku -si 4                                  : Short form

Helpful if you wan't to know the durations of episodes, or number of episodes.
```

FOR THE FOLLOWING, NO EXTRA ARGUMENT MUST BE GIVEN, IT MAY RESULT IN ERROR.

### Listing Genres
You can see the available genres and download under specific genres.

### Most-popular
You can see and download the most-popular animes, although its subjective to website.

e.g

```
$ khed --list-genres        OR      $ khed -l

==================================
WELCOME, Your search results are : 
==================================
1. Adventure
2. Comedy
3. Drama
4. Erotica
5. Fantasy
6. Horror
7. Mystery
8. Psychological
9. Romance
10. Science fiction
11. Thriller
12. Tournament
13. Adventure
... and many more
```

## Issues

If you get an error or have any feature request, go ahead and drop an issue. If you would like to work on the issues see the following.

## Development

Don't commit to master branch, instead create a branch and then open a new pull requests specifying in short what did you change. Also it is recommended to have single commit per file rather than single commit to multiple files, it helps in reviewing.
Also install the program as editable.
```
$ git clone https://github.com/bnu123/Khed
$ pip3 install -e .
```
So that *no* re-installing has to be done if you made a change to the program.

## Motivation And Future

I made this program to learn about python programming and development in general, currently I am working on making it compatible with other Operating Systems.
This program is purely for education purpose, you are responsible for its use.




