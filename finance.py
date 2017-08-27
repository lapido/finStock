"""This is a python program for financial data"""

#import libraries
from urllib2 import urlopen
import json
import sys
import time
from bs4 import BeautifulSoup as soup
import re
class FetchNse:
    
    #urls
    profile_url = 'http://www.nse.com.ng/rest/api/issuers/companydirectory?$filter=Symbol%20eq'
    details_url = 'http://www.nse.com.ng/Issuers-section/listed-securities/company-details?symbol='
    historical_url = 'http://www.nse.com.ng/rest/api/issuers/historicaltrade/7/NG7UP0000004'
    
    stock_price_monthly_url = 'http://www.nse.com.ng/rest/api/stockchartdata/'
    
    
    def __init__(self, company_ticker):
        self.company_ticker = company_ticker
        
        #joining the url to the company's ticker
        self.profile_url = FetchNse.profile_url + '%27'+self.company_ticker + '%27'
        self.profile = {}
        
        uClient = urlopen(self.profile_url)
        page = uClient.read()
        uClient.close()
        
        all_data = json.loads(page)
        self.profile = all_data[0]
    
    """Gets company profile data from nse"""
    def getProfile(self): 
        
        for i, y in self.profile.items():
            print('%s=%s' %(i,y))
            
    def printName(self):
        print self.profile['CompanyName']
        
    """method to print company stock price for the last 7 days trades""" 
#    def trade_7_prices(self):
        
    
#    def check_if_exist(self,post_title, cmp_name):
#        post_title = post_title.lower()
#        cmp_name = cmp_name.lower()
#        if cmp_name in post_title
#            return True
#        return False
    def monthlyDate(self):
        isin = self.profile['InternationSecIN']
        full_url = FetchNse.stock_price_monthly_url + str(isin)
        uClient = urlopen(full_url)
        data = json.loads(uClient.read())
        for datum in data:
            print str(datum[0]) + '--' + str(datum[1])
        
    def findNewsUtill(self, com, ticker, title):

        findRegex = re.compile(r'(\w+)\s+(\w+)\s*\w*')  
        find_g = findRegex.match(com)

        group_1 = find_g.group(1)
        group_2 = find_g.group(2)

        groups = group_1 + ' ' + group_2

        if (group_1 in title) or (group_2 in title) or (groups in title) or (ticker in title):
            return True

        return False

    def getNews(self):
        urls = ["http://nairametrics.com/page/{}".format(i) for i in range(1, 3)]
        
        posts = []
        for url in urls:
            uClient = urlopen(url)
            page_html = uClient.read()
            page_soup = soup(page_html, "html.parser")
            per_entry = page_soup.findAll('div', {'class':'post-grid'})

            for per_post in per_entry:
                post = {}
                #md_7_div = per_post.find('div', {'class': 'col-md-7'})
                title_area = per_post.find('div', {'class': 'post-title'})
                post['post_title'] = title_area.find('h3').a.text

                #check if name exist in title post
                post_title = post['post_title'].lower()
                company_name = self.profile['CompanyName'].lower()
                ticker = self.company_ticker.lower()
#                print post_title;
                
                if self.findNewsUtill(company_name, ticker, post_title):
                        post['link'] = title_area.a['href']
                        post['post_desc'] = per_post.find('div', {'class': 'post-exc'}).p.text
                        posts.append(post)
                else:
                    pass
            #take a rest buddy
            #time.sleep(1)

            uClient.close()
        print(posts)                            
                                        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
def main():
    if len(sys.argv) != 2:
        print "Insert Company/'s Ticker"
        sys.exit()
    ticker = str(sys.argv[1]).strip()
    data = FetchNse(ticker)
    data.printName()
    # data.getProfile()
    data.getNews()
    #data.monthlyDate()


    
if __name__ == '__main__':
    main()
