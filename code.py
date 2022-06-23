from re import A
import time
import csv
from tracemalloc import start
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

start_url = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser  = webdriver.Chrome("C:/Users/VIVEK KHANNA/Desktop/WhitehatJr/Module-3/CW C127/chromedriver.exe")
browser.get(start_url)
time.sleep(10)
headers = [
'V Mag. (mV)','Proper name','Bayer designation','Distance (ly)','Spectral class	Mass (M☉)','Radius (R☉)	Luminosity (L☉)'
]

star_data = []

def scraping():
    for i in range(0,202):
        soup = BeautifulSoup(browser.page_source,"html.parser")
        
        for ul_tag in soup.find_all("ul" , attrs = {"class" , "star"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index , li_tag in enumerate(li_tags):
                if index ==0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else : 
                    try : 
                        temp_list.append(li_tag.contents[0])
                    
                    except : 
                        temp_list.append("")
                    
            hyperlink_li_tag = li_tags[0]
            link = hyperlink_li_tag.find_all("a" , href = True)[0]["href"]
            temp_list.append("" + link)
            star_data.append(temp_list)

        browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()


new_stars_data = []

def scrape_more_data(hyperlink):
    try:

        page = requests.get(hyperlink)
      
        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []

        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
          
            for td_tag in td_tags:
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")

        new_temp_list = []
        for item in temp_list:
            new_item = item.replace("\n" , "")
            new_temp_list.append(new_item)

        new_temp_list = new_temp_list[:7]
        new_stars_data.append(new_temp_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

scraping()

for index , data in enumerate(star_data):
    scrape_more_data(data[5])

star_data_final = []
for index , data in enumerate(star_data):
    new_stars_data_element = new_stars_data[index]
    star_data_final.append(data + new_stars_data_element)

with open("scraping.csv" , "w") as f :
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)
    csv_writer.writerows(star_data_final)

print(new_stars_data)

            


