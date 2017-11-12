import requests
import json
import bs4

#Build Database Structure
Stores = {}
Features = {"WiFi":".in01","NearMetro":".in02","NCCC":".in03","CreditCard":".in04","KingCarSelling":".in05","Booking":".in06","NearParking":".in07","OutdoorArea":".in08"}
link = "https://www.mrbrown.com.tw/Stores/InquiryDetail.aspx?ID="

#Loop Stores
for each in range(1, 76+1):
    #Fetch from Site
    Page = requests.get(link+str(each))
    Soup = bs4.BeautifulSoup(Page.text, "lxml")
    
    #Check Store Exist
    if len(Soup.select(".introB")[0].string[22:]) == 0:
        continue
    
    #Gather Basic Info
    Store = {
        "ID":each,
        "Name":Soup.select(".introB")[0].string[22:],
        "Tel":Soup.select(".introL")[1].string[22:],
        "Fax":Soup.select(".introL")[2].string[22:],
        "Address":Soup.select(".introL")[3].string[22:],
        "Open Hours":str(Soup.select(".introL")[0])[42:str(Soup.select(".introL")[0]).find("</div>")].replace("<br/>","").replace(" ","")
    }
    
    #Check Features
    for feature in Features:
        if len(Soup.select(Features[feature])) != 0:
            Store[feature] = True
        else:
            Store[feature] = False
    
    #Append Store to List
    Stores[Soup.select(".introB")[0].string[22:]] = Store
    print("Saved:",Soup.select(".introB")[0].string[22:])

#Export
with open("Mr.Brown Stores.json", "w") as f:
    json.dump(Stores, f)