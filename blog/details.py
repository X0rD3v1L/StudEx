import requests as r
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
from datetime import timedelta
from googleapiclient.discovery import build
def Request(Id,Pass):
	r = r.Session()
	h = {"X-Requested-With": "XMLHttpRequest"}
	g = r.post("https://intranet.rguktn.ac.in/SMS/logic/login.php",data={"user1": Id,"passwd1": Pass,"uri":""},headers=h)
	d = r.get("https://intranet.rguktn.ac.in/SMS/profile.php")
	soup = bs(d.text,"html.parser")
	d = soup.find("div",class_="box-body box-profile")
	details = [Id]
	details.append(d.find("h4").text.strip())
	details.append(d.find("p").text.split(",")[-1].strip())
	a = d.findAll("a")
	for i in a:
		details.append(i.text.strip())
	del details[6]
	a = soup.find("div",class_="col-md-7")
	p = a.findAll("p")
	details.append(p[-2].text.split(" ( Mobile: ")[0])
	details.append(p[-2].text.split(" ( Mobile: ")[1][:-1])
	details.append(p[-1].text.strip())
	details.append(a.findAll("span")[-3].text.strip())
	details.append(a.findAll("span")[-2].text.strip())
	details.append(a.findAll("span")[-1].text.strip())
	return details

def totaltime(ID):
	
	api_key = 'AIzaSyBDvpT2IKIAx3R82COTdbEFtCO2KWMtbqE'
	youtube = build('youtube','v3',developerKey=api_key)
	hours_pattern = re.compile(r'(\d+)H')
	minutes_pattern = re.compile(r'(\d+)M')
	seconds_pattern = re.compile(r'(\d+)S')
	nextPageToken = None
	total_seconds = 0

	while True:
		pl_request = youtube.playlistItems().list(
			part='contentDetails',
			playlistId=ID,
			maxResults = 50,
			pageToken=nextPageToken)

		pl_response = pl_request.execute()

		vid_ids = []
		for item in pl_response['items']:
			vid_ids.append(item['contentDetails']['videoId'])


		vid_request = youtube.videos().list(
			part = "contentDetails",
			id = ','.join(vid_ids)
			)
		vid_response = vid_request.execute()

		for item in vid_response['items']:
			duration = item['contentDetails']['duration']
			
			hours = hours_pattern.search(duration)
			minutes = minutes_pattern.search(duration)
			seconds = seconds_pattern.search(duration)

			minutes = int(minutes.group(1)) if minutes else 0
			hours = int(hours.group(1)) if hours else 0
			seconds = int(seconds.group(1)) if seconds else 0

			video_seconds = timedelta(
				hours = hours,
				minutes = minutes,
				seconds = seconds).total_seconds()
			total_seconds += video_seconds

		nextPageToken = pl_response.get('nextPageToken')
		if not nextPageToken:break

	total_seconds = int(total_seconds)
	final = []
	d = 1
	px = []
	while d<=2:
		px.append(d)
		total_seconds = total_seconds/d
		minutes,seconds = divmod(total_seconds,60)
		hours,minutes = divmod(minutes,60)
		final.append(f'{int(hours)}H:{int(minutes)}M:{int(seconds)}S')
		d += 0.25
	return (final,px)

def videos(word):
	api_key = "AIzaSyBDvpT2IKIAx3R82COTdbEFtCO2KWMtbqE"

	youtube = build('youtube', 'v3', developerKey=api_key)

	hours_pattern = re.compile(r'(\d+)H')
	minutes_pattern = re.compile(r'(\d+)M')
	seconds_pattern = re.compile(r'(\d+)S')
	videos = []
	nextPageToken = None
	while True:
	    pl_request = youtube.search().list(
	        part='snippet , id',
	        q=word,
	        maxResults=50,
	        pageToken=nextPageToken,
	        type="video",
	    )

	    pl_response = pl_request.execute()

	    vid_id = []
	    title = []
	    pub_date = []
	    for item in pl_response['items']:
	        vid_id.append(item["id"]["videoId"])
	        title.append(item["snippet"]["title"])
	        pub_date.append(item["snippet"]["publishTime"])

	    pl_request = youtube.videos().list(
	        part='statistics,contentDetails',
	        id =",".join(vid_id)
	    )

	    pl_response = pl_request.execute()
	    for item,i in zip(pl_response["items"],range(len(vid_id))):
	        duration = item["contentDetails"]["duration"]
	        hours = hours_pattern.search(duration)
	        minutes = minutes_pattern.search(duration)
	        seconds = seconds_pattern.search(duration)

	        hours = int(hours.group(1)) if hours else 0
	        minutes = int(minutes.group(1)) if minutes else 0
	        seconds = int(seconds.group(1)) if seconds else 0

	        viewCount = item["statistics"]["viewCount"]
	        likes = item["statistics"]["likeCount"]
	        dislikes = item["statistics"]["dislikeCount"]
	        videoId = item["id"]
	        url = f'youtu.be/{videoId}'
	        videos.append(
	                        {
	                            "url":url,
	                            "views":int(viewCount),
	                            "likes":int(likes),
	                            "dislikes":int(dislikes),
	                            "title":title[i],
	                            "pub_date":pub_date[i],
	                            "total_time":f'{hours}H:{minutes}M:{seconds}S'
	                        }
	                    )
	    nextPageToken = pl_response.get('nextPageToken')
	    if not nextPageToken:
	        break
	videos.sort(key=lambda vid:vid["views"],reverse=True)
	for vid in videos[:10]:
		l = ["views","likes","dislikes"]
		for i in l:
			print(vid[i],end=",")
			if vid[i] >= 1000000:
				vid[i] = f'{vid[i]/1000000:0.1f}M'
			elif vid[i] >= 1000:
				vid[i] = f'{vid[i]/1000:0.1f}K'

	return videos[:10]

def getpocket(url):
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
			except:
				pass
	responce = r.get(image)
	name = url.split("//")[1].split("www.")[-1].split(".")[0] + "." + image.split(".")[-1]
	print(name)
	file = open("/home/s0m3_7h1ng/Documents/py7h0n/django/RGUKTN/media/pocket_pics/" + name ,"wb")
	file.write(responce.content)
	file.close()
	return {"title":title,"image":image,"name":name}