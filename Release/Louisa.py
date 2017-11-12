import requests
import json
import bs4

#Fetch from Site
link = "http://www.louisacoffee.com.tw/visit_result"
Form = {"data[name]":"","data[county]":"","data[district]":"","data[zipcode]":"","data[address]":""}
Page = requests.post(link, data=Form)
Soup = bs4.BeautifulSoup(Page.text, "lxml")

#Build Database Structure
Stores = {}
Infos = {"Tel":"電話/","Address":"地址/ ","Open Hours":"營業時間/","Meal Hours":"供餐時間/"}
Features = {"Breakfast":"輕食早午餐","Cake":"手做蛋糕","Bread":"麵包","WiFi":"免費Wifi","MoreSeats":"座位10席以上","Holiday":"國定假日照常營業"}

#Loop for each store
for each in Soup.body.select(".col-md-6.store_info"):
    Store = {"Name":each.h4.string}
    
    #Fetch Text Info
    for info in Infos:
        pos = str(each).find(Infos[info])+len(Infos[info])
        endpos = str(each).find("</p>", pos)
        Store[info]=str(each)[pos:endpos]
    
    #Fetch Boolean Info
    for feature in Features:
        if Features[feature] in str(each):
            Store[feature]=True
        else:
            Store[feature]=False
    
    #Append Store Data to List
    Stores[each.h4.string] = Store
    print("Saved:",each.h4.string)

#Export
with open("Louisa Stores.json", "w") as f:
    json.dump(Stores, f)