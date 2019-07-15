"""
A Library for Crawling Tawan Starbucks Stores.
import this library or run as script which will output all stores in a json file.
"""
import re
import requests
import bs4

BASE_URL = "https://www.starbucks.com.tw/stores/storesearch.jspx"
FEATURES = {
    "wifi": "icon_wifi.jpg",
    "reserve": "icon_reserve.jpg",
    "pour_over": "icon_pour-over-coffee.jpg",
    "nitro": "icon_nitor-coffee.jpg", # Somebody check this Typo ?
    "drive": "icon_drive.jpg",
    "fizzio": "icon_fizzio.jpg"
}

def get_cities():
    """
    Use to get cities' id which can be used as param to seach for region and stores.

    :param None
    :returns: A Dictionary of available cities in structure of {name, id}
    :raises None
    """
    page = requests.get(BASE_URL)
    soup = bs4.BeautifulSoup(page.text, "lxml")
    results = []
    for each in soup.select("#selCity option")[1:]:
        results.append(each.string)
    return {each.string: each["value"] for each in soup.select("#selCity option")[1:]}

def get_region(city_id):
    """
    Use to get regions' id which can be used as param to seach for stores.

    :param city_id: city's id which can be obtain from get_cities()
    :returns: A Dictionary of available regions in structure of {name, id}
    :raises None
    """
    page = requests.post("https://www.starbucks.com.tw/member/region.serx", data={"cid": city_id})
    return {each["regionName"]: each["regionId"] for each in page.json()[0]["region"]}

def get_stores(city_id, region_id="ALL"):
    """
    The main function to fetch stores infos.

    :param city_id: city's id which can be obtain from get_cities()
    :param region_id: region's id which can be obtain from get_region(city_id),
                      if not provided, all stores in the city will be return
    :returns: A List of stores in a structure of Dictionary
    :raises None
    """
    blank_page = requests.get(BASE_URL)
    blank_soup = bs4.BeautifulSoup(blank_page.text, "lxml")
    page = requests.post("{};jsessionid={}".format(BASE_URL, blank_page.cookies["JSESSIONID"]),
                         data={
                             "AJAXREQUEST": "j_id_jsp_1422024916_0",
                             "selCity": city_id,
                             "selRegion": region_id,
                             "sbForm:reserve": "",
                             "sbForm:pour": "",
                             "sbForm:nitro": "",
                             "sbForm:drive": "",
                             "sbForm:fizzio": "",
                             "sbForm_SUBMIT": "1",
                             "javax.faces.ViewState": blank_soup.find(
                                 "input", {"name":"javax.faces.ViewState"})["value"],
                             "as_fid": blank_soup.find("input", {"name":"as_fid"})["value"],
                             "sbForm:doFindByRegion": "sbForm:doFindByRegion"})
    soup = bs4.BeautifulSoup(page.text, "lxml")
    results = []
    for store in soup.select("#search_store")[0].find_all("li"):
        item = {
            "id": re.search(r"javascript:checkStoreMap\((\d*)\);", str(store)).group(1),
            "name_zhTW": store.find_all("h4")[0].string,
            "name_en": store.find_all("h4")[1].string,
            "coordinate": store.find_all("span")[1].string,
            "address": store.select(".address")[0].string,
            "tel": store.select(".tel")[0].string,
            "hours": store.select(".hours")[0].string
        }
        for feature, checker in FEATURES.items():
            item[feature] = bool(checker in str(store))
        results.append(item)
    return results

if __name__ == "__main__":
    RESULTS = []
    for city_name, city_code in get_cities().items():
        print("{}\t{}".format(city_name, len(get_stores(city_code))))
        for region_name, region_code in get_region(city_code).items():
            stores = get_stores(city_code, region_code)
            print("{}\t{}\t{}".format(city_name, region_name, len(stores)))
            RESULTS += stores

    import json
    with open("starbucks.json", "w") as f:
        json.dump(RESULTS, f)
