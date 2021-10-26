#!/bin/python3
import spotipy
import os
import requests
#import mutagen
from mutagen.id3 import ID3, APIC, TRCK, TDRC, TIT2, TALB, TPE1, TPOS, USLT, TCOM, TCON, TSRC, COMM

# User must fill in these details:
# Spotify API access
ClientUsr  = ""
ClientID   = ""
ClientScrt = ""


class searcher:
	def __init__(self):
		# do spotify stuff
		token = spotipy.util.prompt_for_user_token(ClientUsr, "user-library-read", client_id=ClientID, client_secret=ClientScrt, redirect_uri='http://localhost/')
		self.sp = spotipy.Spotify(auth=token)
	

	def setFilename(self, filename):
		# check mp3 file
		if not os.path.isfile(filename):
			raise Exception('MP3 file not found !')
		# set it
		self.filename = filename


	def searchSong(self, text):
		result = self.sp.search(q=text, type="track", limit=1)
		if result["tracks"]["total"] == 0:
			return False
		else:
			return result["tracks"]["items"][0]


	def getArtists(self, result):
		artistsRaw = result['album']['artists']

		if len(artistsRaw) == 1:
			return artistsRaw[0]['name']

		artists = ""
		for artistraw in artistsRaw:
			artists += artistraw['name'] + ", "
		return artists[:-2] # remove last comma and space
	

	def getComment(self, result):
		if result['explicit']:
			return "Explicit"
		else:
			return ""
	

	def getGenre(self, result):
		# This solution is more like a botch. Most albums have no genre assigned.
		# To kind of fix this I just add the first genre of the first artist.
		# Not a great solution but it works fairly well.
		# get generes from song album
		album = self.sp.album(result["album"]["external_urls"]["spotify"])
		#print(album["genres"])
		if album["genres"]:
			return album["genres"][0]

		# get generes from artist
		album = self.sp.artist(result["artists"][0]["external_urls"]["spotify"])
		#print(album["genres"])
		if album["genres"]:
			return album["genres"][0]
		
		# no genre found
		return ""


	def generateFilename(self, result):
		# generates a new filename for the mp3 so very file is automatically
		# named with the same scheme
		artist = result["album"]["artists"][0]["name"].replace(" ","_")
		title  = result["name"].replace(" ","_").replace(".","")
		return artist + "-" + title
	

	def setAudioTags(self, result):
		# download cover art first
		coverUrl = result['album']['images'][0]['url']
		albumart = requests.get(coverUrl, allow_redirects=True).content
		# create new ID3 object. All necessary tags will be assigned.
		id3 = ID3()
		# set all tags
		id3.add(TRCK(encoding=3, text=str(result["track_number"]) ))
		id3.add(TDRC(encoding=3, text=result["album"]["release_date"][:4] ))
		id3.add(TIT2(encoding=3, text=result["name"] ))
		id3.add(TALB(encoding=3, text=result["album"]["name"] ))
		id3.add(TPE1(encoding=3, text=self.getArtists(result) ))
		id3.add(TPOS(encoding=3, text=str(result["disc_number"]) ))
		id3.add(TSRC(encoding=3, text=str(result["disc_number"]) ))
		#id3.add(USLT(encoding=3, text=lyric_data))
		#id3.add(TCOM(encoding=3, text=info['composer']))
		id3.add(TCON(encoding=3, text=self.getGenre(result) ))
		id3.add(COMM(encoding=3, desc=u'Comment', text=self.getComment(result) ))
		id3.add(APIC(encoding=3, mime=u'image/jpeg', type=3, desc=u'Front Cover', data=albumart ))
		# make it final
		id3.save(self.filename)



if __name__ == '__main__':
	# if this script is executed instead of imported.
	import json, sys

	if len(sys.argv) < 2:
		print("Usage:")
		print(sys.argv[0]+" <mp3file> <mp3file> ...")
		exit()
	
	# for each argument (mp3 file)
	for i in range(1, len(sys.argv)):
		# separate path and filename
		path, filename = os.path.split(sys.argv[i])
		# keep user happy
		print("[+] Tagging "+sys.argv[i])
		# set filename
		app = searcher()
		app.setFilename(sys.argv[i])
		# create a searchable string from filename
		search_string = filename.replace(".mp3","").replace("-", " ").replace("_", " ").replace("(","").replace(")","")
		# search song
		result = app.searchSong(search_string)
		#print(json.dumps(result, indent=4, sort_keys=True))
		# set tags
		app.setAudioTags(result)
		# rename file
		os.rename(sys.argv[i], path+"/"+app.generateFilename(result)+".mp3")
