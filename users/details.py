import requests as r
from bs4 import BeautifulSoup as bs
import pandas as pd
import smtplib
r = r.Session()
h = {"X-Requested-With": "XMLHttpRequest"}
def Request(Id,Pass):
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
