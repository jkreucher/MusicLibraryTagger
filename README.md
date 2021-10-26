# MusicLibraryTagger
2021 Jannik Kreucher


## What is MusicLibraryTagger?

This project uses the Spotify-Api and python library "spotipy" to get information about a specific song. The script tags the mp3 file based of the gathered information. The filename of the mp3 is used to search the song. Once song attributes are found the script tags the mp3 and renames it.



## Usage of MusicLibraryTagger

First of dependencies are needed. For Debian/Ubuntu users installing python3 wont be compicated at all:
```
$ sudo apt install python3 python3-pip
```

To communicate with the Spotify API and to tag the mp3s libraries are needed:
```
$ pip3 install mutegan
$ pip3 install spotipy
```

Before you run the script you must fill in the blank API access data consisting of your Spotify username and a API login. For that you need to change lines 10 to 12.
```
10 ClientUsr  = "username"
11 ClientID   = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
12 ClientScrt = "00000000000000000000000000000000"
```

Now is the time to run the script. Is requires at least one argument. Each argument of the script will be a mp3 file to be tagged:
```
$ python3 librarytagger.py <mp3_file_1> <mp3_file_2> <mp3_file_3> ... 
```



## Tagging a Library

Of course when having a rather large library you dont want to add each and every file by hand. For that a pipe is used to automate that. Just a single line to tag your entire library:
```
$ find . -name '*.mp3' -print0 | xargs -0 ./librarytagger.py
```
