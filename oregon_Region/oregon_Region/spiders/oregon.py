import scrapy
import selenium
from selenium import webdriver
import csv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")

path = R"E:\Desktop\oregon_bills\chromedriver.exe"
driver = webdriver.Chrome(path,options=chrome_options)
a_list = []
b_list = []
c_list = []
pdf_list = []
url = "https://gov.oregonlive.com/bill/intro/2021/"
def crawl():
        for ur in range(23,26):
            new_url = url + "page-"+str(ur) + "/"
            driver.get(new_url)

            a = driver.find_elements_by_xpath('//div[@class="indvote"]/a')
            for new in  a:
                a_list.append(new.text)
            l = driver.find_elements_by_xpath("//div[@class='indvote']/a")
            for item in l:
                b_list.append(item.get_attribute('href'))
        for c in b_list:
            try:
                driver.get(c)

                pdf = driver.find_element_by_xpath("//div[@class='billtext']/ul/li/a").get_attribute('href')
                pdf_list.append(pdf)
                status = driver.find_element_by_xpath("//div[@class='activity']//li[last()]").text
                c_list.append(status)
            except NoSuchElementException:
                c_list.append("No Activity yet")
                continue


        with open(R"E:\Desktop\oregon_bills\out_7.csv",'w', newline="", encoding='utf8') as my_file:
                csv_writer = csv.writer(my_file,delimiter=",")
                csv_writer.writerow(["bill_no.","Doc URL","Status"])
                for m,n,o in zip(a_list,pdf_list,c_list):
                # for m in pdf_list:
                    csv_writer.writerow([m,n,o])
                my_file.close()
        driver.quit()




crawl()



