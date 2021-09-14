import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# This class crawls a website and takes search information from website
def crawler(url,searchKey,nameOfClass):
    req = webdriver.Chrome(ChromeDriverManager().install())       # open chrome
    req.get(url + searchKey)                    # go to the url + search key

    # if it is an infinite scroll then keep scrolling untill no more scroll
    lenOfPage = req.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while (match == False):            # while not at end of page
        lastCount = lenOfPage           # get last count of page height
        time.sleep(3)                   # wait 3 seconds
        lenOfPage = req.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")     # keep scrolling
        if lastCount == lenOfPage:      # if at the bottom of page
            match = True                # set match to true and end while loop


    sourceData = req.page_source        # source of data
    soup = BeautifulSoup(sourceData,'html.parser')          # parser
    product = soup.find_all("div", {'class': nameOfClass})  # find all classes of nameOfClass

    shoeDict = {}                                       # create a dictionary
    counter = 0
    for shoe in product:                                    # for each shoe in the products
        shoeD = {}
        productPhoto = shoe.find('img').get('src')                                              # get the image
        productPrice = shoe.find("div",{'class':'product-price'}).text.replace('$','').strip()  # strip out the $ and get price
        productName = shoe.find("div",{'class':'product-title'}).text.strip()                   # get name of product
        shoeD['name'] = productName
        shoeD['price'] = productPrice
        shoeD['photo'] = productPhoto

        shoeDict[counter] = shoeD
        counter += 1
    return shoeDict                                          # return results


def main():
    brands = ["Jordan", "Adidas", "Nike"]
    # brands = ["Adidas"]

    url = "https://vicesltd.com/collections/vendors?q="            # Enter name of website
    print("Updating Shoe Database, Please Wait...")
    for i in brands:
        searchKey = i                                              # Enter search Key
        res = crawler(url,searchKey,'product-container')           # change class name

        with open("E:/Github Repos/ShoeCollectionApp/webCrawl/" + i + ".json", 'w') as writeFile:
            json.dump(res, writeFile)                                       # dump results into jsonfile
        print("Crawling Done for " + i)

main()
