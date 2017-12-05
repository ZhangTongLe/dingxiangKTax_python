#_*_ coding:utf-8 _*_


from selenium import webdriver
import time
import os
import time
import sys
import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys  #需要引入keys包
from selenium.webdriver.support.wait import WebDriverWait
import pymysql
from selenium.webdriver.support.select import Select


#登陆网站
def login(driver):
    # 登陆界面
    driver.get('http://web.china12366.org/Login.aspx')
    # 通过使用选择器选择到表单元素进行模拟输入和点击按钮提交
    driver.find_element_by_id('txtUserName').clear()
    driver.find_element_by_id('txtUserName').send_keys('用户名')  #用户名需要输入
    driver.find_element_by_id('txtUserPwd').clear()
    driver.find_element_by_id('txtUserPwd').send_keys('密码') #密码需要输入
    driver.find_element_by_id('ibtnLogin').click()
    time.sleep(2)
#到了搜索列表，页面切换
def nextPage(driver,url,itemPage):
    driver.get(url)
    switchBool = True
    while switchBool:
        str1 = str(driver.find_element_by_id("lblPage").get_attribute('innerHTML')).split(" ")
        if str(str1[6])!=itemPage:
            print(str1[6])
            driver.find_element_by_id("lbtnNext").click()
            time.sleep(1.5)
            driver.page_source
        else:
            search(driver)
            print("----------")
            switchBool=False
    #time.sleep(20000)
    switchBool=True

    while switchBool:
        #print(driver.get_attribute('innerHTML'))
        str1 = str(driver.find_element_by_id("lblPage").get_attribute('innerHTML')).split(" ")
        #print(str1[6])  #总页数
        #print(str1[4])  #当前页码
        if str1[4]!=str1[6]:
            driver.find_element_by_id("lbtnNext").click()  #点击下一页按钮
            time.sleep(2)
            driver.page_source  #重新获取页面资源
            time.sleep(0.5)
            search(driver)
        else:
            switchBool=False



#点击每个搜索页面
def search(driver):
    pageItem=driver.find_elements_by_class_name("Black14")  #获取每项链接
    secondPageList=[]
    for pageOne in pageItem:
        urlString= str(pageOne.get_attribute('href'))  #判断其是不是我们需要的链接
        if urlString.find('?') != -1:
            #print(urlString)
            secondPageList.append(urlString)
    for item in secondPageList:
         #print("序号：%s   值：%s" % (list.index(i) + 1, i))
        click(driver,item)
        #driver.back()
        handles = driver.window_handles  # 获取当前窗口句柄集合（列表类型）
        driver.switch_to_window(handles[0])  # 切换首页

#找到目标连接，获取内容
def click(driver,url):
    #driver.get(url)
    js = 'window.open("'+url+'");'
    driver.execute_script(js)
    driver.title.encode("utf-8")
    handles = driver.window_handles  # 获取当前窗口句柄集合（列表类型）
    driver.switch_to_window(handles[1])  # 切换新开的页面窗口
    time.sleep(1)
    driver.page_source
    #print("写入数据库----")
    tables=driver.find_elements_by_tag_name("table")
    for table in tables:
        convent=str(table.get_attribute("width"))
        if(convent=="93%"):
            #print(table.get_attribute('innerHTML'))
            #wirteTxt(table.get_attribute('innerHTML'))

            # lblTitle  标题
            # lblInfo   出处
            # lblContent 内容
            lblTitle= table.find_element_by_id("lblTitle").get_attribute('innerHTML')
            lblInfo=table.find_element_by_id("lblInfo").get_attribute('innerHTML')
            lblContent=table.find_element_by_id("lblContent").get_attribute('innerHTML')
            #print(lblTitle)
            if "失效日期" in str(lblInfo):
                lblInfoType = str(lblInfo).replace("源自[中税答疑网]", "").split("：")
                wirteTxt(lblTitle, lblInfoType[1].replace("状态", "").strip(),
                         lblInfoType[2].replace("发文日期", "").strip(),lblInfoType[3].replace("失效日期", "").strip(), lblInfoType[4].strip(), lblContent)
            else:
                lblInfoType=str(lblInfo).replace("源自[中税答疑网]","").split("：")
                wirteTxt(lblTitle,lblInfoType[1].replace("状态","").strip(),
                         lblInfoType[2].replace("日期", "").strip(),lblInfoType[3].strip(),"2099-1-1",lblContent)
            #print(lblContent)
            #print("正在写入数据--------"+str(datetime.datetime.now())+">>>>>>>>")


    driver.close()  # 关闭当前窗口


#写入数据库
def wirteTxt(Country_Title,Country_Location,Country_Type,Country_Data,Country_Somefailure_Time,Country_Info):
    #Country_Title(标题),Country_Location（位置）,Country_Type（类型）,Country_Data（日期）,Country_Info（内容）
    #print("11")
    # 打开数据库连接
    print(Country_Somefailure_Time)
    #print(Country_Title)
    conn = pymysql.connect(host="localhost", user="root",password="root", db="dingxiangktax", port=3306,charset="utf8")
    # 使用cursor()方法获取操作游标
    #sql="""INSERT INTO `countrytax` (`Country_Title`, `Country_Location`, `Country_Data`, `Country_Type`, `Country_Info`) VALUES ('"+Country_Title+"', '"+Country_Location+"',' "+Country_Data+"','"+Country_Type+"','"+Country_Info+"')"""
    sql_insert = """INSERT INTO `countrytax` (`Country_Title`, `Country_Location`, `Country_Data`, `Country_Type`,`Country_Somefailure_Time`, `Country_Info`) VALUES (Country_Title.encode('utf-8'), Country_Location.encode('utf-8'), Country_Data.encode('utf-8'),Country_Type.encode('utf-8'), Country_Info.encode('utf-8'))"""
    cur = conn.cursor()
    Country_Title = str(Country_Title).encode('utf-8').decode()
    Country_Location = str(Country_Location).encode('utf-8').decode()
    Country_Type = str(Country_Type).encode('utf-8').decode()
    Country_Data = str(Country_Data).encode('utf-8').decode()
    Country_Somefailure_Time= str(Country_Somefailure_Time).encode('utf-8').decode()
    Country_Info = str(Country_Info).encode('utf-8').decode().replace("'","^")
    sql = u"INSERT INTO `countrytax` (`Country_Title`, `Country_Location`, `Country_Data`, `Country_Type`,`Country_Somefailure_Time`, `Country_Info`) VALUES ('"+Country_Title+"', '"+Country_Location+"',' "+Country_Data+"','"+Country_Type+"','"+Country_Somefailure_Time+"','"+Country_Info+"')"
    sta = cur.execute(sql)
    if sta == 1:
        print('Done')
    else:
        print('Failed')
    conn.commit()
    cur.close()
    conn.close()

#---
driver = webdriver.Firefox()
#登陆
login(driver)

#搜索1949-01-1到2017-12-02的所有法规，从第一页开始
nextPage(driver,"http://web.china12366.org/Search.aspx?type=121&c1=&c2=&c3=&bt=&wh=&nr=&rq=True&ksrq=1949-01-01&jsrq=2017-12-02","1")
