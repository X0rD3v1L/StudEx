import requests as r
from bs4 import BeautifulSoup as bs
import pandas as pd
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
# Ids = open("like.txt").read().split()
# main_list = []
# for Id in Ids:
# 	Id = Id.split(":")
# 	main_list.append(Request(Id[0],Id[1]))
# df = pd.DataFrame(main_list,columns=["Id","Name","Class","Gender","DOB","Category","Mobile","U_Mail","P_Mail","Father","Father_No","Addr","Adhar"])
# df.to_excel(r"CSE-1.xlsx",index=False)
print(Request("N160476","O0X8K"))