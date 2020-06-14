import time
import json
import os
from datetime import datetime,timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import ActionChains

def scraper():
    chromedriver=os.path.join(os.getcwd(),'chromedriver','chromedriver.exe')
    options = webdriver.ChromeOptions()
    #options.add_argument("user-data-dir=C:\\Users\\ASUS\\AppData\\Local\\Google\\Chrome\\User Data\\")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=chromedriver,options =options)

    driver.get("http://spys.one/en/anonymous-proxy-list/")
    select=Select(driver.find_element_by_id('xpp'))
    select.select_by_value('5')
    table = [[col.text
              for col in row.find_elements_by_tag_name('td')]
             for row in driver.find_elements_by_xpath('//tr[contains(@class, "spy1x")]')]

    proxlis=set()
    for i in table:
        proxlis.add(i[0])
        
    for i in range(1,6):
        
        driver.get("http://free-proxy.cz/en/proxylist/country/all/https/date/all/{}".format(i))
        driver.find_element_by_id('clickexport').click()
        z=driver.find_element_by_id('zkzk').text
        for k in z.split('\n'):
            proxlis.add(k)


    for i in range(1,6):
        
        driver.get("http://free-proxy.cz/en/proxylist/country/all/http/ping/all/{}".format(i))
        driver.find_element_by_id('clickexport').click()
        z=driver.find_element_by_id('zkzk').text
        for k in z.split('\n'):
            proxlis.add(k)

    driver.get("https://free-proxy-list.net/")

    for k in range(0,15):
            
        table=[[col.text for col in i.find_elements_by_tag_name('td')] for i in driver.find_elements_by_xpath('//*[@id="proxylisttable"]/tbody/tr')]
        for i in table:
                z=str(i[0])+":"+str(i[1])
                proxlis.add(z)
                
        driver.find_element_by_xpath('/html/body/section[1]/div/div[2]/div/div[3]/div[2]/div/ul/li[10]/a').click()

    driver.get('http://nntime.com/')
    driver.find_element_by_xpath('//*[@id="formname"]/div[1]/a[1]').click()
    e=driver.find_element_by_xpath('//*[@id="form1"]/div[1]/textarea')
    for i in e.get_attribute("value").split("\n"):
        proxlis.add(i)

    for i in range(2,10):
        driver.get("http://nntime.com/proxy-list-0{}.htm".format(i))
        driver.find_element_by_xpath('//*[@id="formname"]/div[1]/a[1]').click()
        e=driver.find_element_by_xpath('//*[@id="form1"]/div[1]/textarea')
        for j in e.get_attribute("value").split("\n"):
            proxlis.add(j)
    driver.quit()

    # read the list of proxy IPs in proxyList
    try :
        proxlis.remove('Proxy address:port')
    except:
        pass

    return list(proxlis)

def is_bad_proxy(pip):
    import urllib.request , socket
    socket.setdefaulttimeout(180)
    try:        
        proxy_handler = urllib.request.ProxyHandler({'https': pip,'http':pip})        
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)        
        sock=urllib.request.urlopen('http://www.google.com', timeout=4)  # change the url address here
        #sock=urllib.urlopen(req)
    except urllib.error.HTTPError as e:        
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:

        print( "ERROR:", detail)
        return 1
    return 0

def check_create_file(proxyList):
    working=[]
    for item in proxyList:
        if is_bad_proxy(item):
            print ("Bad Proxy", item)
            
            
        else:
            print (item, "is working")
            working.append(item)
    date=(datetime.now()+timedelta(30)).strftime("%d_%m_%Y")

    filename='./output/file_{}.txt'.format(date)
    file=open(filename,'w')
    for i in working:
        file.writelines(i+"\n")

    file.close()

if __name__ == '__main__':
    proxli=scraper()
    check_create_file(proxli)
