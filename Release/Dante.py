import requests
import json
import bs4

#Build Database Structure
Stores = {}
Infos = {"Tel":"電話：</b>","Address":"地址：</b>","Open Hours":"營業時間：</b>"}
Features = {"WiFi":"無線上網","FreeParking":"免費停車場","Delivery":"外送服務","ConferenceRoom":"室內會議區","NearMetro":"捷運週邊","ChargeParking":"收費停車場","OutdoorSeat":"戶外桌椅"}
link = "http://www.dante.com.tw/store_10_1_2.php?no="

#Loop Stores
for each in range(1, 257+1):
    #Fetch from Site
    Page = requests.get(link+str(each))
    Soup = bs4.BeautifulSoup(Page.text, "lxml")
    
    #Check Store Exist
    if len(Soup.select(".store_block04")) == 0:
        continue
    
    #Gather Basic Info
    Store = {
        "ID":each,
        "Name":Soup.select(".store_block04")[0].string[12:],
    }
    
    #Fetch Text Info
    for info in Infos:
        pos = str(Soup.select(".store_block05")).find(Infos[info])+len(Infos[info])
        endpos = str(Soup.select(".store_block05")).find("<br/>", pos)
        Store[info]=str(Soup.select(".store_block05"))[pos:endpos]
    
    #Fetch Boolean Info
    for feature in Features:
        if Features[feature] in str(Soup.select(".store_block05")):
            Store[feature]=True
        else:
            Store[feature]=False
    
    #Append Store to List
    Stores[Soup.select(".store_block04")[0].string[12:]] = Store
    print("Saved:",Soup.select(".store_block04")[0].string[12:])

#Export
with open("Dante Stores.json", "w") as f:
    json.dump(Stores, f)