from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json
import ssl

#some docu on google image search parameters
#https://stenevang.wordpress.com/2013/02/22/google-advanced-power-search-url-request-parameters/
#interesting
#http://stackoverflow.com/questions/15063091/python-clicking-a-button
#http://jeanphix.me/Ghost.py/


def get_soup(url,header):
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    req = urllib2.Request(url,headers=header)
    urlop = urllib2.urlopen(req, context=gcontext)
    return BeautifulSoup(urlop,'html.parser')


keywordsFile = open('keyword_list.txt','r')
keywords = keywordsFile.readlines()

for kw in keywords:
	query='+'.join(kw.split())
	url="http://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
	img_dir="imgs"
	image_filename = 'img_'
	
	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
	}
	print url,header
	soup = get_soup(url,header)


	scraped_images=[]# contains the link for Large original images, img_type of  image
	for a in soup.find_all("div",{"class":"rg_meta"}):
		link , img_type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
		scraped_images.append((link,img_type))

	print  "there are total" , len(scraped_images)," images"

	#create directories
	if not os.path.exists(img_dir):
	    os.mkdir(img_dir)
	img_dir = os.path.join(img_dir, query)

	if not os.path.exists(img_dir):
	    os.mkdir(img_dir)
	    
	#save images
	for i , (img , img_type) in enumerate( scraped_images):
		try:
			req = urllib2.Request(img, headers={'User-Agent' : header})
			gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
			raw_img = urllib2.urlopen(req,context=gcontext).read()

			cntr = len([a for a in os.listdir(img_dir) if image_filename in a]) + 1
			print cntr
			if len(img_type)==0:
				f = open(os.path.join(img_dir , image_filename + "_"+ str(cntr)+".jpg"), 'wb')
			else :
				f = open(os.path.join(img_dir , image_filename + "_"+ str(cntr)+"."+img_type), 'wb')


			f.write(raw_img)
			f.close()
		except Exception as e:
			print "could not load : "+img
			print e
