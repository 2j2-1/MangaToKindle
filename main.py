from bs4 import BeautifulSoup
import urllib.request as urllib
import requests
import os

opener = urllib.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
url = 'https://www.mangapanda.com'
manga = "shingeki-no-kyojin"

class Manga(object):
	"""docstring for Manga"""
	def __init__(self, url ,manga):
		self.url = url
		self.manga = manga
		self.mangaURL = "{}/{}".format(self.url,self.manga)
		self.soup = self.getSoup(self.mangaURL)
		self.filePath = manga

	def getSoup(self,url):
		response = opener.open(url).read()
		return BeautifulSoup(response, 'html.parser')

	def getLengthOfManga(self):
		return self.soup.find(id="latestchapters").ul.li.a.get('href').split("/")[-1]

	def getLengthOfChapter(self,chapter):
		soup = self.getSoup("{}/{}".format(self.mangaURL,chapter))
		return int(soup.find(id="selectpage").find_all('option')[-1].string)

	def getImageLocation(self,soup):
		return soup.find(id='imgholder').img['src']

	def getImage(self,src,filePath,fileName):
		if not os.path.exists(filePath):
		    os.makedirs(filePath)
		with open('{}/{}.jpg'.format(filePath,fileName),'wb') as file:
			file.write(requests.get(src).content)

	def getChapter(self,chapter):
		lengthOfChapter = self.getLengthOfChapter(chapter)
		filePath = "{}/{}/".format(self.manga,chapter)
		for image in range(1,lengthOfChapter+1):
			soup = self.getSoup("{}/{}/{}".format(self.mangaURL,chapter,image))
			imageLocation = self.getImageLocation(soup)
			self.getImage(imageLocation,filePath,image)
