import time
import json
import os
from threading import Thread
import concurrent.futures
from datetime import datetime,timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import ActionChains
chromedriver=os.path.join(os.getcwd(),'chromedriver','chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument('--disable-dev-shm-usage')


def scrapper1(message):
    #options.add_argument("user-data-dir=C:\\Users\\ASUS\\AppData\\Local\\Google\\Chrome\\User Data\\")
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
    driver.quit()
    try :
        proxlis.remove('Proxy address:port')
    except:
        pass
    
    return check_create_file(list(proxlis),"spys.one")

def scrapper2(message):
    proxlis=set()
    driver = webdriver.Chrome(executable_path=chromedriver,options =options)
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
    driver.quit()
    return check_create_file(list(proxlis),'free-proxy.cz')

def scrapper3(message):
    proxlis=set()
    driver = webdriver.Chrome(executable_path=chromedriver,options =options)
    driver.get("https://free-proxy-list.net/")
    proxlis=set()
    for k in range(0,15):
            
        table=[[col.text for col in i.find_elements_by_tag_name('td')] for i in driver.find_elements_by_xpath('//*[@id="proxylisttable"]/tbody/tr')]
        for i in table:
                z=str(i[0])+":"+str(i[1])
                proxlis.add(z)
                
        driver.find_element_by_xpath('/html/body/section[1]/div/div[2]/div/div[3]/div[2]/div/ul/li[10]/a').click()
    driver.quit()
    return check_create_file(list(proxlis),'free-proxy-list.net')

def scrapper4(message):
    proxlis=set()
    driver = webdriver.Chrome(executable_path=chromedriver,options =options)    
    for k in range(1,10):
        driver.get("http://nntime.com/proxy-list-0{}.htm".format(k))
        e=driver.find_element_by_id('proxylist')
        t=[[col.text for col in i.find_elements_by_tag_name('td') if len(col.text)>5 ] for i in e.find_elements_by_tag_name('tr')]
        for j in t:
            if len(j)>3:
                proxlis.add(j[0])
    driver.quit()
    # read the list of proxy IPs in proxyList
    return check_create_file(list(proxlis),'nntime.com')

def scrapper5(message):
    proxlis=set()
    driver = webdriver.Chrome(executable_path=chromedriver,options =options)
    driver.get('https://www.proxynova.com/proxy-server-list/')
    e=driver.find_element_by_id('tbl_proxy_list')
    table=[[col.text for col in i.find_elements_by_tag_name('td')] for i in e.find_elements_by_tag_name('tr')]
    driver.quit()
    for i in table:
	    if len(i)>5:
		    prox=i[0]+":"+i[1]
		    proxlis.add(prox)

    return check_create_file(list(proxlis),"www.proxynova.com")

def scrapper6(message):
    driver = webdriver.Chrome(executable_path=chromedriver,options =options)
    driver.get('https://proxyscrape.com/free-proxy-list')
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,"proxytable")))
    url=str(driver.find_element_by_id('downloadhttp').get_property('href'))
    driver.quit()
    import requests
    r=requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all')
    proxlis=r.content.decode("utf-8").split("\r\n")

    return check_create_file(list(proxlis),"proxyscrape.com")

def scrapper7(message):
    driver = webdriver.Chrome(executable_path=chromedriver,options =options)
    table=[]
    proxlis=set()
    for k in range(1,8):

        driver.get('https://premproxy.com/list/0{}.htm'.format(k))   #1-7
        e=driver.find_element_by_id('proxylist')
        temp=[[col.text for col in i.find_elements_by_tag_name('td')] for i in e.find_elements_by_tag_name('tr')]
        table+=temp
    driver.quit()
    for i in table:
	    if len(i)>4:
		    proxlis.add(i[0])    
    return check_create_file(list(proxlis),"Premproxy")

def scrapper8(message):
    driver = webdriver.Chrome(executable_path=chromedriver,options =options)
    table=[]
    proxlis=set()

    for k in range(1,27):
        
        driver.get('https://free-proxy-list.com/?search=1&page={}&port=&type%5B%5D=http&type%5B%5D=https&up_time=0&search=Search'.format(k))  #  1-5
        e=driver.find_elements_by_xpath('/html/body/div[2]/div[1]/div/div/div[3]/table/tbody')[0]
        temp=[[col.text for col in i.find_elements_by_tag_name('td')] for i in e.find_elements_by_tag_name('tr')]
        table+=temp
    driver.quit()
    for i in table:
        if len(i)>4:
            temp=i[0]+":"+i[2]
            proxlis.add(temp)

            
    return check_create_file(list(proxlis),"free-proxy-list.com")


def is_bad_proxy(pip,website):
    import urllib.request , socket
    socket.setdefaulttimeout(180)
    try:        
        proxy_handler = urllib.request.ProxyHandler({'https': pip,'http':pip})        
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)        
        sock=urllib.request.urlopen('http://www.google.com', timeout=6)  # change the url address here
        #sock=urllib.urlopen(req)
    except urllib.error.HTTPError as e:        
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:

        print( "ERROR:", detail,website)
        return 1
    return 0

def check_create_file(proxyList,website):
    working=[]
    for item in proxyList:
        if is_bad_proxy(item,website):
            print ("Bad Proxy"+ ":"+ item + str(website))    
        else:
            print (item, "is working")
            working.append(item)
    return working
    

def write_file(working,name):
    date=(datetime.now()+timedelta(30)).strftime("%d_%m_%Y")
    filename='./output/file_{name}_{date}.txt'.format(date=date,name=name)
    file=open(filename,'a')
    for i in working:
        file.writelines(i+"\n")

    file.close()

def final_file():
    filename=['./output/file_s{name}_{date}.txt'.format(date=date,name=i) for i in range(1,9)]
    date=(datetime.now()+timedelta(30)).strftime("%d_%m_%Y")
    final_file='./output/file{name}_{date}.txt'.format(date=date,name="_final")
    file=open(final_file,'a')

    for k in filename:
        temp=open(filename,'r')
        while True:
            line = temp.readline()
            if not line:
                temp.close()
                break
            file.writelines(line)
    file.close()
    print("file final is created\n")
    return filname

def remove_temp(name):
    for i in name:
        os.remove("i")
        print("File Removed!",i)
    print("execution completed")
    return "ok"

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers = 8) as executor:
        
        future1=executor.submit(scrapper1,("scrapper1"))
        future2=executor.submit(scrapper2,("scrapper2"))
        future3=executor.submit(scrapper3,("scrapper"))
        future4=executor.submit(scrapper4,("anythinh"))
        future5=executor.submit(scrapper5,("scrapper1"))
        future6=executor.submit(scrapper6,("scrapper2"))
        future7=executor.submit(scrapper7,("scrapper"))
        future8=executor.submit(scrapper8,("anythinh"))
        write_file(future1.result(),"s1")
        write_file(future2.result(),"s2")
        write_file(future3.result(),"s3")
        write_file(future4.result(),"s4")
        write_file(future5.result(),"s5")
        write_file(future6.result(),"s6")
        write_file(future7.result(),"s7")
        write_file(future8.result(),"s8")
        names=final_file()
        remove_temp(names)

if __name__ == '__main__':
    main()
