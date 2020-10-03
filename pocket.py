import requests as r
from bs4 import BeautifulSoup as bs
def getpocket(url):
	responce = r.get(url)
	b = bs(responce.content,'html.parser')
	description = ""
	image = ""
	m = b.findAll('meta')
	for i in m:
		try:
			if "property" in i.attrs:
				if i["property"].strip() == "og:image":
					image = i["content"].strip()
					if image[0] == "/":
						image = url + image

				if i["property"].strip() == "og:description":
					description = i["content"].strip()

				if i["property"].strip() == "og:title":
					description = i["content"].strip()

			if "name" in i.attrs :
				if description == ""  and i["name"].strip() == "description":
					description = i["content"].strip()

		except:
			pass
		if image and description:
			break
	if image == "":
		l = b.findAll('link')
		for i in l:
			try:
				if i["rel"][0] == "icon" :
					image = i["href"].strip()
					if image[0] == "/":
						image = url + image
			except:
				pass
	if description=="":
		description = b.find('title').text  # getting title
	responce = r.get(image)
	name = url.split("//")[1].split("www.")[-1].split(".")[0] + "." + image.split(".")[-1]
	file = open( name ,"wb")
	file.write(responce.content)
	file.close()
	return {"description":description,"image":image,"name":name}

print(getpocket(input()))