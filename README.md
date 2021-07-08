# Ebay selenium  WEBSCRAPPER FOR SOLD AND CURRENT LISTINGS 

* [X] Base scapper for sold and current listing   
* [X] jupyiter notebook test (Test_Scrapper)
* [ ] Sales Anaylsis 
* [ ] メリカりやヤフオク!の機能
 

## Ebay Scapper 

Functions Ebay_scapper.py
*  createUrl(keyword,n=None,pageitems=None,sold=False)  
<p> Create URL for Ebay_MarketData, from keyword (item name), n - pagenumber ,pageitems - items per page , sold - True (sold data) or False (Currrent listing)  
</p>

*  start_browser(driverpath="chromedriver.exe",other_Browser="C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe")
> <p> start Selenium browser, returns running browers to be uses in Ebay_MarketData. If other_Browers is set then other browers can be used bar crome (Here brave is used)</P>

*  Ebay_MarketData(URL,pagenumbers,browser,sold=False,test=False)
> <p>Create the Market data from the URL, thats in URL, pagenumbers, browser created from start_browser and options for sold and test case. This code looks through page numbers and gets the listing for each page, and used the two functions bellow to get the data into a pandas data fromat. If test is True this function wont return data but will return the page html source code. </P>

*  ebay_SoldListingToPanda(listings,showprint=False)
> <p> Convert page listing data into Panda data frame for Sold lisintgs. If showprint=True each items name, and infromation about the item will be printed</p>
*  ebay_CurrentListingToPanda(listings,showprint=False)
> <p> Convert page listing data into Panda data frame for Current lisintgs </p>

### Catch stratagy 
<p>When making web scrappers you will soon come into a Catch robot blocker. For ebay there is one of theses what runs mainly for Sold items.
To deal with this problem this code has a while statment to stop the code when the Catch security page pops up. 
Then you can manly complete the questsion and once done the code continuess again. 
 </p>


```python
first=True
while browser.title=='Security Measure':
if first:
    print("waiting for human help")
    first=False
    print(browser.title)
else:
    pass
```



