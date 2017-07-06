#目标：必应图片的桌面版；
#步骤：
# 1.分析图片url；
# 2.实现图片下载、保存；
# 3.实现图片读取、应用桌面；
# 4.打包为exe可执行文件;

import platform
import requests
import time
import os
import urllib.request
from bs4 import BeautifulSoup
import win32gui #win32的api
import win32con
from PIL import Image #处理图像库pillow
#!usr/bin/env Python
#coding=utf-8
class Desktop:
    #初始化
    def __init__(self ,name='',burl='',surl=''):
        self.name    = name
        self.baseUrl = burl
        self.fullUrl = ''
        self.data    = ''
        self.path    = 'E:/images/'+time.strftime("%Y-%m-%d")
        self.outpath = 'E:/images/outfile/'+time.strftime("%Y-%m-%d")
        self.jsonUrl = 'HPImageArchive.aspx?format=js&idx=0&n=1&nc=1498499725620&pid=hp&video=1'
        
    #定义系统信息
    def sysmsg(self):
        print('*'*32)
        print('脚本名称:', self.name)
        print('运行版本:', 'python'+platform.python_version())
        print('操作系统:', platform.platform())
        print('*'*32)

    #获取json文件        
    def getUrl(self):
        headers = {
            'Host':'cn.bing.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        try:
           print("正在获取链接...")    
           r        = requests.get(self.baseUrl+self.jsonUrl, headers = headers)
           resource = r.json()['images'][0]['url']
           return resource
        except ValueError as e:
               print('程序异常!!!,VauleError:', e)
               exit()  

    #下载、保存
    def downLoad(self):
               
        self.fullUrl = self.baseUrl[:-1]+str(self.getUrl())
        print("链接提取成功：\n"+self.fullUrl)
        
        #数据
        self.data = urllib.request.urlopen(self.fullUrl).read()

        with open(self.path+'.jpg','wb') as f:
             f.write(self.data)
        print("图片提取成功：\n"+self.path+'.jpg')             


    #格式转换    
    def transferImg(self):
        
        try:
           Image.open(self.path+'.jpg').save(self.outpath+'.bmp')
           print("格式转换完成:\n"+self.outpath+'.bmp')

        except BaseException as e:
           print("格式转换错误！")
           exit() 


    #读取、设置桌面背景
    def backGround(self):
        #格式转换
        self.transferImg()
        #设置背景
        try:
            win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, self.outpath+'.bmp', 0)
        except BaseException as e:
            print("设置背景失败！", e)
            exit()
        print("背景修改成功!!!")
        #删除原图
        if os.path.exists(self.path+'.jpg'):
           os.remove(self.path+'.jpg')
           print("原图删除成功")



    #运行总函数
    def runApp(self):
        self.sysmsg()
        if not os.path.exists(self.outpath+'.bmp'):       
            self.downLoad()
            self.backGround()
        else:
            print('文件已经存在,取消剩余操作.')

#实例
b = Desktop(name='必应图片抓取脚本 v1.0',burl='http://cn.bing.com/')
b.runApp()         
