import requests
import json
import bs4

#Build Database Structure
Stores = {}
link = "http://www.ikari.com.tw/store_detail.php?id="

#Loop Stores
for each in range(1, 118+1):
    #Fetch from Site
    Page = requests.get(link+str(each))
    Soup = bs4.BeautifulSoup(Page.text, "lxml")
    
    #Check Store Exist
    if Soup.body.h3 == None:
        continue
    
    #Gather Basic Info
    Store = {
        "ID":each,
        "Name":Soup.body.h3.string,
        "Tel":Soup.body.select(".tel")[0].string,
        "Address":Soup.body.select(".address")[0].string
    }
    
    #Get Seat#
    pos = str(Soup.body.select(".setNum")[0]).find("</span>")+7
    endpos = str(Soup.body.select(".setNum")[0]).find("</em>")
    Store["Seat#"]=str(Soup.body.select(".setNum")[0])[pos:endpos]
    
    #Get Open Hours
    pos = str(Soup.body.select(".openHours")[0]).find("</span>")+7
    endpos = str(Soup.body.select(".openHours")[0]).find("</em>")
    Store["Open Hours"]=str(Soup.body.select(".openHours")[0])[pos:endpos]
    
    #Append Store to List
    Stores[Soup.body.h3.string] = Store
    print("Saved:",Soup.body.h3.string)

#Export
with open("Ikari Stores.json", "w") as f:
    json.dump(Stores, f)