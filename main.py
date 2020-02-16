from bs4 import BeautifulSoup
import urllib.request as urllib
import requests

opener = urllib.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
url = 'https://www.mangapanda.com'
manga = "shingeki-no-kyojin"
response = opener.open("{}/{}".format(url,manga)).read()
soup = BeautifulSoup(response, 'html.parser')


def getSoup(url):
	response = opener.open(url).read()
	return BeautifulSoup(response, 'html.parser')

def getLength():
	return soup.find(id="latestchapters").ul.li.a.get('href').split("/")[-1]

def getLengthChapter(chapter):
	soup = getSoup("{}/{}/{}".format(url,manga,chapter))
	return int(soup.find(id="selectpage").find_all('option')[-1].string)

def getImageLocation(soup):
	return soup.find(id='imgholder').img['src']

def getImage(src,filePath,fileName):
	with open('{}/{}.jpg'.format(filePath,fileName),'wb') as file:
		file.write(requests.get(src).content)

def getChapter(chapter):
	lengthOfChapter = getLengthChapter(chapter)
	filePath = "{}/{}/".format(manga,chapter)
	for image in range(1,lengthOfChapter+1):
		soup = getSoup("{}/{}/{}/{}".format(url,manga,chapter,image))
		imageLocation = getImageLocation(soup)
		getImage(imageLocation,filePath,image)

getChapter(1)