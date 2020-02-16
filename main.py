from bs4 import BeautifulSoup
import urllib.request as urllib
import requests
import os

opener = urllib.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

manga = "dr-stone"


class Manga(object):
    """docstring for Manga"""
    url = ''

    def __init__(self, manga):
        self.manga = manga
        self.mangaURL = "{}/{}".format(self.url, self.manga)
        self.soup = self.getSoup(self.mangaURL)
        self.filePath = manga
        self.lengthOfManga = self.getLengthOfManga()

    def getSoup(self, url):
        response = opener.open(url).read()
        return BeautifulSoup(response, 'html.parser')

    def getImage(self, src, filePath, fileName):
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        with open('{}/{}.jpg'.format(filePath, fileName), 'wb') as file:
            file.write(requests.get(src).content)

    def getChapter(self, chapter):
        lengthOfChapter = self.getLengthOfChapter(chapter)
        filePath = "{}/{}/".format(self.manga, chapter)
        for image in range(1, lengthOfChapter + 1):
            imageLocation = self.getImageLocation(chapter, image)
            print(filePath, image)
            # self.getImage(imageLocation, filePath, image)

    def getManga(self):
        self.getChapters(1, self.lengthOfManga)

    def getChapters(self, start=1, numOfChapters=1):
        for chapter in range(numOfChapters):
            try:
                self.getChapter(start + chapter)
            except:
                print("Chapter {} is unavalible".format(chapter))


class MangaPanda(Manga):
    """docstring for MangaPanda"""
    url = 'https://www.mangapanda.com'

    def getLengthOfManga(self):
        return int(self.soup.find(id="latestchapters").ul.li.a.get('href').split("/")[-1])

    def getLengthOfChapter(self, chapter):
        soup = self.getSoup("{}/{}".format(self.mangaURL, chapter))
        return int(soup.find(id="selectpage").find_all('option')[-1].string)

    def getImageLocation(self, chapter, image):
        soup = self.getSoup("{}/{}/{}".format(self.mangaURL, chapter, image))
        return soup.find(id='imgholder').img['src']

manga = MangaPanda(manga)
manga.getManga()