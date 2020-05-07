import requests
from bs4 import BeautifulSoup
import re
import tkinter as tk
from PIL import Image, ImageTk
import urllib

import wordcloud
import jieba
img_open = None
img_png = None
img_open1 = None
img_png1 = None
country = []
city = []
view = []
comments = ""

def getCountry():
    global country
    # requests访问url爬取数据
    kv = {'user-agent':'Mozilla/5.0'}
    url = "https://you.ctrip.com/sitelist/europe120002.html"
    r = requests.get(url,headers = kv,timeout = 30)
    r.encoding = 'utf-8'
    txt = r.text

    # BeautifulSoup处理数据
    soup = BeautifulSoup(txt,'html.parser') #指定Beautiful的解析器为“html.parser”

    country_list = soup.find('div',attrs = {'class':'hot_destlist cf'})

    for i,v in enumerate(country_list.find_all('a')):
        country_name = v.find('dt')
        country_name = str(country_name)
        country_name=re.search(r'[\u4e00-\u9fa5]+',country_name).group()
        country_url = v['href']
        country.append([i+1,country_name,country_url])
        #print("{}\t{}\t{}".format(country[i][0],country[i][1],country[i][2]))
        
def getCity(num):
    global city
    global country
    kv = {'user-agent':'Mozilla/5.0'}
    url = "https:"+country[num][2]
    r = requests.get(url,headers = kv,timeout = 30)
    r.encoding = 'utf-8'
    txt = r.text

    soup = BeautifulSoup(txt,'html.parser') #指定Beautiful的解析器为“html.parser”

    city_list = soup.find('div',attrs = {'class':'hot_destlist cf'})
    city.clear()
    for i,v in enumerate(city_list.find_all('a')):
        city_name = v.find('dt')
        city_name = str(city_name)
        city_name=re.search(r'[\u4e00-\u9fa5]+',city_name).group()
        city_url = v['href']
        city.append([i+1,city_name,city_url])
        #print("{}\t{}\t{}".format(city[i][0],city[i][1],city[i][2]))

def getView(num):
    global view
    global city
    kv = {'user-agent':'Mozilla/5.0'}
    url = "https://you.ctrip.com"+city[num][2]
    url = url.replace('place','sight')
    r = requests.get(url,headers = kv,timeout = 30)
    r.encoding = 'utf-8'
    txt = r.text

    # BeautifulSoup处理数据
    soup = BeautifulSoup(txt,'html.parser') #指定Beautiful的解析器为“html.parser”

    view_list = soup.find('div',attrs = {'class':'list_wide_mod2'})
    view.clear()
    for i,v in enumerate(view_list.find_all('div',attrs = {'class':'list_mod2'})):
        #储存图片
        im = v.find('img')
        urllib.request.urlretrieve(str(im['src']),'D:\picture\%s.jpg'%i)
        #热度+分数
        s = v.find('ul',attrs = {'class':'r_comment'})
        hot = s.find('a',attrs = {'class':'recomment'})
        hot = re.search(r'[0-9]+',str(hot.string)).group()
        score = s.find('a',attrs = {'class':'score'}).find('strong')
        score = re.search(r'[0-9.]+',str(score.string)).group()
        #信息序号+名称+网页
        msg = v.find('div',attrs = {'class':'rdetailbox'})
        view_name = msg.find('a')
        view.append([msg.find('s').string,view_name['title'],view_name['href'],score,hot])
        #print("{}\t{}\t{}\t{}\t{}".format(view[i][0],view[i][1],view[i][2],view[i][3],view[i][4]))        

def getMessage(num):
    global view
    global comments
    kv = {'user-agent':'Mozilla/5.0'}
    url = "https://you.ctrip.com"+view[num][2]
    r = requests.get(url,headers = kv,timeout = 30)
    r.encoding = 'utf-8'
    txt = r.text
    soup = BeautifulSoup(txt,'html.parser')

    comments = soup.find('div',class_='normalbox boxsight_v1')
    if comments !=None:
        comments = comments.find('div',class_='text_style').string.strip()
    else:
        #重新访问
        url = "https://piao.ctrip.com/ticket/dest/t"+re.search(r'[0-9]+.html',view[num][2]).group()
        r = requests.get(url,headers = kv,timeout = 30)
        r.encoding = 'utf-8'
        txt = r.text
        soup = BeautifulSoup(txt,'html.parser')
        comments = soup.find('div',class_='introduce-content')
        comments = comments.find(lambda e:e.string == '景点介绍：' or e.string == '【景点介绍】'or e.string=='特色景点：')
        if comments != None:
            comments = comments.find_next('p').string.strip()#查找下一个为标签p
        else:
            comments = soup.find('div',class_='introduce-content')
            comments = str(comments.find_all('span')).replace('<br/>','')
            comments = re.search(r'>[\u4e00-\u9fa50-9，；。、]+',comments).group()

def wordcloud1():
    s = comments
    str1 = ' '.join(jieba.lcut(s))
    font = r'C:\Windows\Fonts\simhei.ttf'
    w = wordcloud.WordCloud(width=200,height=200, font_path=font,background_color = 'white')
    w.generate(str1)
    w.to_file("D:\picture\pywordcloud.png")

def gui():

    global view
    global comments
    window = tk.Tk()
    window.title('马蜂窝旅游景点信息爬取')
    window.geometry('800x500')

    getCountry()

    l1 = tk.Label(window,text = '选择要查询国家',
                  font = ("Arial, 12")).place(x=10,y=10)
    l3 = tk.Label(window,text = '选择要查询的城市',
                  font = ("Arial, 12")).place(x=160,y=10)
    l5 = tk.Label(window,text = '选择要查询的景点',
                  font = ("Arial, 12")).place(x=310,y=10)
    l7 = tk.Label(window,text = '景点Top 10',
                  font = ("Arial, 12")).place(x=500,y=10)
    var4 = tk.StringVar()
    l8 = tk.Label(window,font = ("SimHei, 18"),textvariable = var4).place(x=20,y=280)
    var5 = tk.StringVar()
    l8 = tk.Label(window,font = ("Arial, 11"),wraplength = 270,textvariable = var5).place(x=200,y=300,w = 410)

    var1 = tk.StringVar()
    l2 = tk.Label(window,bg = 'white',width = 8, height = 2,
                  font = ("Arial, 12"),textvariable = var1).place(x=30,y=160)
    var2 = tk.StringVar()
    l4 = tk.Label(window,bg = 'white',width = 16, height = 2,
                  font = ("Arial, 12"),textvariable = var2).place(x=150,y=160)
    
    def print_selection1():
        value = lsbox1.get(lsbox1.curselection())
        x = lsbox1.curselection()
        var1.set(value)
        getCity(x[0])
        lsbox2.delete(0,tk.END)
        for i in city:
            lsbox2.insert(tk.END,i[1])

    def print_selection2():
        value = lsbox2.get(lsbox2.curselection())
        var2.set(value)
        x = lsbox2.curselection()
        getView(x[0])
        lsbox3.delete(0,tk.END)
        for i in view:
            lsbox3.insert(tk.END,i[1])
        #显示top10表格
        columns = ("名次", "景点名","评分","热度")
        treeview = ttk.Treeview(window, height=10, show="headings", columns=columns)
 
        treeview.column("名次", width=50, anchor='center') # 表示列,不显示
        treeview.column("景点名", width=150, anchor='center')
        treeview.column("评分", width=40, anchor='center')
        treeview.column("热度", width=50, anchor='center')
 
        treeview.heading("名次", text="名次") # 显示表头
        treeview.heading("景点名", text="景点名")
        treeview.heading("评分", text="评分")
        treeview.heading("热度", text="热度")
        treeview.place(x=480,y =30)
        
        for i in range(len(view)): # 写入数据
            if i <10 :
                treeview.insert('', i, values=(view[i][0], view[i][1],view[i][3],view[i][4]))

    def print_selection3():
        global img_open
        global img_png
        global img_open1
        global img_png1
        l9 = tk.Label(window,text = '景点介绍：',
                  font = ("Arial, 12")).place(x=300,y=270)
        value = lsbox3.get(lsbox3.curselection())
        x = lsbox3.curselection()
        getMessage(x[0])
        #在画布上显示对应图片、介绍和名称
        var4.set(view[x[0]][1])
        img_open = Image.open('D:\picture\%s.jpg'%x[0])
        img_png = ImageTk.PhotoImage(img_open)
        canvas.create_image(0,0,anchor = 'nw',image = img_png)
        var5.set(comments)
        #显示生成的wordcloud
        wordcloud1()
        img_open1 = Image.open('D:\picture\pywordcloud.png')
        img_png1 = ImageTk.PhotoImage(img_open1)
        canvas1.create_image(0,0,anchor = 'nw',image = img_png1)
        
            
    bl = tk.Button(window,text = '确定',width = 10,font = ("Arial, 12"),
               height = 2,command = print_selection1).place(x=20,y=220)
    
    b2 = tk.Button(window,text = '确定',width = 10,font = ("Arial, 12"),
               height = 2,command = print_selection2).place(x=170,y=220)
    b3 = tk.Button(window,text = '确定',width = 10,font = ("Arial, 12"),
               height = 2,command = print_selection3).place(x=340,y=180)

    #国家列表框
    ls = ['法国','意大利','英国','希腊','德国','瑞士','西班牙','俄罗斯','荷兰',
          '奥地利','捷克','葡萄牙']
    lsbox1 = tk.Listbox(window,height = 5,width = 15,font = ("Arial, 11"))

    for i in ls:
        lsbox1.insert(tk.END,i)

    scrl1 = tk.Scrollbar(window)
    scrl1.place(x = 115,y = 40,height = 110)
    lsbox1.configure(yscrollcommand=scrl1.set)
    #指定Listbox的yscrollbar的回调函数为Scrollbar的set，表示滚动条在窗口实时更新
    lsbox1.place(x = 15,y = 40,width = 100,height = 110)

    scrl1['command'] = lsbox1.yview
    #指定Scrollbar的command的回调函数是Listbox的yview
    
    #城市列表框
    lsbox2 = tk.Listbox(window,height = 5,width = 15,font = ("Arial, 11"))

    scrl2 = tk.Scrollbar(window)
    scrl2.place(x = 265,y = 40,height = 110)
    lsbox2.configure(yscrollcommand=scrl2.set)
    lsbox2.place(x = 165,y = 40,width = 100,height = 110)
    scrl2['command'] = lsbox2.yview

    #景点列表框
    lsbox3 = tk.Listbox(window,height = 5,width = 15,font = ("Arial, 11"))

    scrl3 = tk.Scrollbar(window)
    scrl3.place(x = 455,y = 40,height = 110)
    lsbox3.configure(yscrollcommand=scrl3.set)
    lsbox3.place(x = 315,y = 40,width = 140,height = 110)
    scrl3['command'] = lsbox3.yview

    canvas = tk.Canvas(window,height = 140,width = 220)
    canvas.place(x=20,y=330)

    canvas1 = tk.Canvas(window,height = 200,width = 200)
    canvas1.place(x=570,y=270)

    window.mainloop()        
        
if __name__ == '__main__':
    #getCountry()
    gui()
