from selenium import webdriver
import numpy as np
#import requests
import pandas as pd
from bs4 import BeautifulSoup
#from re import sub
import matplotlib.pyplot as plt
from scipy import stats
import time
import sys


def createUrl(keyword,n=None,pageitems=None,sold=False):
  Url=f"https://www.ebay.com/sch/i.html?_nkw={keyword}"
  if n:
    Url+=f"&_pgn={n}"
  if pageitems:
    if pageitems in [200,100,50,25,10,5]:
      Url+=f"&_ipgn={pageitems}"
    else:
      print("Error items perpage")
      print("Options: 200,100,50,25,10,5")
  if sold:
    Url+="&LH_Sold=1"
  return Url 

def ebay_SoldListingToPanda(listings,showprint=False):
    dictionary_list = []
    
    for i in range(0,len(listings)):
        dictionary_data = {}
        name=listings[i].find("h3",attrs={"class":f"s-item__title"})
        if name.text !="":
            name=name.text
            dictionary_data["name"]=name

            solddate=listings[i].find("div",attrs={"class":f"s-item__title--tag"}).text

            dictionary_data["sold_date"]=solddate.replace("Item","").replace("Sold","")

            condition=listings[i].find("span",attrs={"class":f"SECONDARY_INFO"}) #.text
            if condition==None:
                condition=""
            else:
                condition=condition.text
            dictionary_data["condition"]=condition

            #Sold price
            priceinfo=listings[i].find("div",attrs={"class":f"s-item__details clearfix"})
            #dictionary_data["price_info"]=priceinfo
            soldprice=priceinfo.find("span",attrs={"class":'s-item__price'}).text
            #Currany & cost 
            currency=soldprice.split(" ")[0]
            soldprice=soldprice.split(" ")[1].replace(",","")
            dictionary_data["price"]=int(soldprice)
            
            #Buynow
            Buytype=priceinfo.find("span",attrs={"class":'s-item__purchase-options-with-icon'})
            if Buytype==None:
                #Bid
                bids=priceinfo.find("span",attrs={"class":'s-item__bids s-item__bidCount'}).text
                Buytype=f"Bid ({bids})"
            else:
                Buytype=Buytype.text
            dictionary_data["Buytype"]=Buytype

            #Shipping info
            shippingprice=priceinfo.find("span",attrs={"class":'s-item__shipping'}).text
            shippinglocation=priceinfo.find("span",attrs={"class":'s-item__location'}).text[5:]

            dictionary_data["shipping_fee"]=shippingprice
            dictionary_data["shipping_location"]=shippinglocation
            #links 
            ref=listings[i].find("a").get("href")
            dictionary_data["ref"]=ref

            src=listings[i].find("img").get("src")
            dictionary_data["image_src"]=src

            dictionary_list.append(dictionary_data)
            
            if showprint:
                print(f"{'~'*10}")
                print(name)
                print(solddate)
                print(soldprice)
                print(Buytype)
                print(shippinglocation)
    df_final = pd.DataFrame.from_dict(dictionary_list)
    return df_final

def ebay_CurrentListingToPanda(listings,showprint=False):
  dictionary_list = []
  for i in range(0,len(listings)):

      dictionary_data = {}
      try:
        name=listings[i].find("h3",attrs={"class":f"s-item__title"})
        if name.text !="":
            name=name.text
            dictionary_data["name"]=name
            condition=listings[i].find("span",attrs={"class":f"SECONDARY_INFO"}) #.text
            if condition==None:
                condition=""
            else:
                condition=condition.text
            dictionary_data["condition"]=condition

            priceinfo=listings[i].find("div",attrs={"class":f"s-item__details clearfix"})
            
            if priceinfo==None:
              print("Price Error")
              print(name)
              print(priceinfo)

            else:
              price=priceinfo.find("span",attrs={"class":'s-item__price'}).text
              dictionary_data["price"]=price

              #Buynow
              Buytype=priceinfo.find("span",attrs={"class":'s-item__purchase-options-with-icon'})
              if Buytype==None:
                  #Bid
                  bids=priceinfo.find("span",attrs={"class":'s-item__bids s-item__bidCount'}).text
                  Buytype=f"Bid ({bids})"
              else:
                  Buytype=Buytype.text
              dictionary_data["Buytype"]=Buytype

              #Watch type    
              watchers=priceinfo.find("span",attrs={"class":'s-item__hotness s-item__itemHotness'})
              if watchers !=None:
                  watchers=(watchers.text)[:watchers.text.find("w")-1]
                 # print(watchers)
                  dictionary_data["watchers"]=watchers
              else:
                  dictionary_data["watchers"]=0

              #Shipping info
              shippingprice=priceinfo.find("span",attrs={"class":'s-item__shipping'}).text
              shippinglocation=priceinfo.find("span",attrs={"class":'s-item__location'}).text[5:]

              dictionary_data["shipping_fee"]=shippingprice
              dictionary_data["shipping_location"]=shippinglocation
              #links 
              ref=listings[i].find("a").get("href")
              dictionary_data["ref"]=ref

              src=listings[i].find("img").get("src")
              dictionary_data["image_src"]=src

              dictionary_list.append(dictionary_data)
              
              if showprint:
                  print(f"{'~'*10}")
                  print(name)
                  print(price)
                  print(Buytype)
                  print(shippinglocation)

      except Exception as e:
            print(f"{'='*10} Error {'='*10}")
            print("Lisitng item error")
            print(i)
            if name:
              print(name)
           
            print(e)


  df_final = pd.DataFrame.from_dict(dictionary_list)  
  return df_final
  
def Ebay_MarketData(URL,pagenumbers,browser,sold=False,test=False): 
  
  itemclass="s-item"
 
  MarketData=pd.DataFrame()
  for i in range(1,pagenumbers):
      if "_pgn" in URL:
        pgnloc=URL.find("_pgn")
        URL[pgnloc+6]=str(i)
        ebayUrl=URL
      else:
        ebayUrl=URL+f"&_pgn={i}"
      browser.get(ebayUrl)
      #time.sleep(1)
      #Catch 対策
      first=True
      while browser.title=='Security Measure':
        if first:
          print("waiting for human help")
          first=False
          print(browser.title)
      else:
        pass
     # print(r.raise_for_status())
      data=browser.page_source
      soup=BeautifulSoup(data)
      if test:
        return soup
      listings = soup.find_all('li', attrs={'class': itemclass})
      L=len(listings) 
      print(f" page listing number {L}")
      if i==1:
        Lsave=L

      if sold:
        page_df=ebay_SoldListingToPanda(listings)
      else:
        page_df=ebay_CurrentListingToPanda(listings)
       
      MarketData=pd.concat([MarketData,page_df],axis=0,ignore_index=True)
      
      if L < Lsave: #Hit result item limit 
        print(f"page data items {len(MarketData)}")
        return MarketData
  return MarketData
      
def start_browser(driverpath="chromedriver.exe",brave="C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"):
    driverpath="chromedriver.exe"
    brave="C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    option = webdriver.ChromeOptions()
    option.binary_location = brave
    browser = webdriver.Chrome(executable_path=driverpath, chrome_options=option)
    return browser

def main():
    browser=start_browser()
    #inputs 
    args = sys.argv
    title="EbayScarpper"
    if len(args)<2:
        item="Katsuragi Misato"
        page=5
        sold=False
    else:
        try:
            item=args[1]
            page=int(args[2])
            sold=args[3]
          
        except Exception as e:
            print(f"{'='*10} Error {'='*10}")
            print("Check inputs are correct")
            print("Args item(str) itemsperpage(int) sold(True/False)" )
            print(e)
    URL=createUrl(item,pageitems=page,sold=sold)
    Data=Ebay_MarketData(URL,page,browser)
  
    title+=item.replace(" " ,"_")
    if sold:
        title+="_sold"
    else:
        title+="_lisiting"
    title+=f"_{len(Data)}"
    Data.to_csv(title+".csv",index=False)
    print(f"{'X'*10} 完成 {'X'*10}") 
    print(f"item {item}")
    print(f"URL {URL}")
    print(f"file items {len(Data)}")
    print(Data["price"].describe())
    print(f"{'X'*10} xxxx {'X'*10}") 

if __name__ =="__main__":
    main()