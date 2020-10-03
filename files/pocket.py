import requests as r
from bs4 import BeautifulSoup as bs
url = input()
responce = r.get(url)
b = bs(responce.content,'html.parser')
title = b.find('title').text
image = ""
m = b.findAll('meta')
for i in m:
	try:
		if i["property"].strip() == "og:image":
			image = i["content"].strip()
			if image[0] == "/":
				image = url + image
				break
	except:
		pass
if image == "":
	l = b.findAll('link')
	for i in l:
		try:
			if i["rel"][0] == "icon" :
				image = i["href"].strip()
				if image[0] == "/":
					image = url + image
					break
		except:
			pass
responce = r.get(image)
name = url.split("//")[1].split("www.")[-1].split(".")[0] + "." + image.split(".")[-1]
file = open( name ,"wb")
file.write(responce.content)
file.close()
print(title)
print(image)
print(name)