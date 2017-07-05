#!/usr/bin/env python 3.5
#-*- coding:utf-8 -*-
"""
new price of futures
"""
import Tkinter as tk
import re
import urllib2
import urllib
import socket
import time
import threading
import winsound

price=''

url = 'https://hq.sinajs.cn/t=%s&list=' % time.time()#sina

parameter='I1709,RB1710,BU1706,PP1709,TA1709,MA1709'
forex='EURGBP'
stock='sz300048,sh600871'
#parameter='L1505'
class MyException(Exception):
    print('MyException:----'+time.strftime('%H:%M:%S'))
class Clock(threading.Thread):
    def __init__(self,num,interval):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False
    def time(self):
        #print('Clock is running')
        """
            类似闹钟功能

        """
        s=time.gmtime(time.time())
        if(s.tm_min%3==0 and (s.tm_sec<3)):
            print(s.tm_min)
            #winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
            #winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            #winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
            #winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            #winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
    def run(self):
        while not self.thread_stop:
            try:
                self.time()
            except Exception as e:
                print(e.message+'\t'+time.strftime('%H:%M:%S'))
            time.sleep(self.interval)
class Timer(threading.Thread):
    def __init__(self,num,interval):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False
    def getCode(self,url):
        """
        proxy = urllib2.ProxyHandler({'http':'127.0.0.1:8087'})
        opener=urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        #req = urllib2.urlopen(url) #wrong
        #"""
        req = urllib2.Request(url)
        try:
            fh = urllib2.urlopen(req,timeout=5)
        except socket.timeout:
            print('error in getcode')
            raise MyException('Timeout')
        except urllib.URLError as e:
            print('error in getcode')
            raise MyException('---')
        except Exception:
            raise MyException('Exception')
        try:
            respHtml = fh.read()
        except:
            print('error in getcode')
            raise MyException('---')
        fh.close()
        return respHtml
    def getstockprice(self,parameter):
        print(parameter)
        #单个现价
        url='https://hq.sinajs.cn/list=%s' % parameter
        resp = self.getCode(url)
        #print(str(resp))
        list = resp.split(";\n")[:-1]
        result = ''
        print(len(list))
        for i in list:
            if i=='':
                pass
            #print('i:%s'%i)
            #print(re.search(r'="(.*?)"',str(i)).groups(1)[0])
            p= (re.search(r'="(.*?)"',str(i)).groups(1)[0]).split(',')[7][0:5]
            result +=' '+p
        return result
    def getforex(self,parameter):
        url='https://hq.sinajs.cn/?rn=1420679359382&list=%s' % parameter
        try:
            resp = self.getCode(url)
        except:
            print('error in getforex\t'+time.strftime('%H:%M:%S'))
            raise MyException('Error')
        return re.search(r'="(.*?)"',str(resp)).groups(1)[0].split(',')[8][2:]
    def getXAG(self):
        url='https://quote.forex.hexun.com/2010/Data/FRunTimeQuote.ashx?code=XAGUSD'
        try:
            resp = self.getCode(url)
        except:
            print('error in getforex\t'+time.strftime('%H:%M:%S'))
            raise MyException('Error')
        return re.search(r'=\[(.*?)\]',str(resp)).groups(1)[0].split(',')[2][0:]
    def filterFg(self,p):
        #partten = re.compile(r'FG\d\d\d\d')
        #p=partten.sub(r'',p)
        return p
    def time(self):
        #print('Clock is running')
        #winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
        """
            类似闹钟功能
        """
        s=time.gmtime(time.time())
        print(s.tm_min)
        print(s.tm_sec)
        if(s.tm_min%2==0):
            print(s.tm_min)
            #winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
            #winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            #winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
            #winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            #winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
    def run(self):
        
        global parameter
        #parameter = self.filterFg(parameter)    #过滤FG这个垃圾品种
        
        global price
        while not self.thread_stop:
            try:
                #self.time();
                #a = self.getfbprice()
                #a = a + ' '+self.getPrice(url,parameter)#sina
                a=self.getPrice(url,parameter)
                #b=self.getstockprice(stock)
                """
                b=self.getforex('EURGBP')
                c=self.getXAG()
                #price = a+' '+b
                #price = price+' '+c
                #"""
                #price=a+' '+b
                price=a
                #price = self.getPriceHeXun(url,parameter)#hexun
                #price = price+'\n'+self.getPriceHeXun(url,'RM1409')+'\n'+self.getPriceHeXun(url,'RB1405')#hexun
                print(time.strftime('%H:%M:%S')+"\t"+price)
            except Exception as e:
                price='Time out'
                #print(e.message+'\t'+time.strftime('%H:%M:%S'))
            time.sleep(self.interval)
    def getPrice(self,url,parameter):
        try:
            resp = self.getCode(url+parameter)
        except:
            print('error in getPrice\t'+time.strftime('%H:%M:%S'))
            raise MyException('Error')
        #print(resp[:-1]+" "+time.strftime('%H:%M:%S'))
        list = str(resp).split(";")
        result = ''
        for i in range(len(list)):#-1,最后为hf_XAU
            p=list[i]
            if p=='':
                pass
            pp = p.split(",")
            if len(pp)>6:
                #print(pp[6])
                if result=='':
                    result=pp[6][-2:]#+'\t'+pp[13]
                    if len(pp[6])<4:
                        result=pp[6][-2:]#+'\t'+pp[13]
                    else:
                        if pp[6][2]=='.':
                            result=pp[6][1:]
                        else:
                            result=pp[6][2:]#+'\t'+pp[13]
                else:
                    if len(pp[6])<=4:
                        result=result+' '+pp[6][-3:]#+'\t'+pp[13]
                    elif pp[6].find(".")>=0:
                        result=result+' '+pp[6][-4:]
                    else:
                        if pp[6][2]=='.':
                            result=result+' '+pp[6][1:]
                        else:
                            result=result+' '+pp[6][2:]#+'\t'+pp[13]
                """
                if result=='':
                    result=parameter.split(',')[i]+'\t'+pp[6][2:4]
                else:
                    result=result+'\n'+parameter.split(',')[i]+'\t'+pp[6][2:4]
                """
        #return result+" "+list[len(list)-2][22:27]
        return result
    def getPriceHeXun(self,url,parameter):
        s='https://quote.futures.hexun.com/2010/JsData/FRunTimeQuote.aspx?code=%s&market=3&&time=%s' % (parameter,time.time())
        #print(s)
        resp = self.getCode(s)
        #print(resp[:-1]+" "+time.strftime('%H:%M:%S'))
        list = resp.split(";")
        result = ''
        for i in range(len(list)):
            p=list[i]
            if p=='':
                pass
            pp = p.split(",")
            if len(pp)>6:
                if result=='':
                    result=pp[3][3:5]+' '+pp[12]
                else:
                    result=result+' '+pp[3][2:4]+' '+pp[12]
                """
                if result=='':
                    result=parameter.split(',')[i]+'\t'+pp[6][2:4]
                else:
                    result=result+'\n'+parameter.split(',')[i]+'\t'+pp[6][2:4]
                """
        return result
    def getbbprice(self):
        #bb1409
        url='https://hq2gnqh.eastmoney.com/em_futures2010numericapplication/index.aspx?type=f&id=bb14093'
        resp = self.getCode(url)
        return re.search(r'extendedFutures:\["(.*?),',str(resp)).groups(1)[0][2:]#.split('.')[1]

def updatelabel(label):
    """
    用最新price更新label显示
    """
    def update():
        label.config(text=str(price))
        label.after(100, update)#单位 毫秒
    update()




root = tk.Tk()
'''
def on_closing():
    root.destory()
root.protocol('WM_DELETE_WINDOW',on_closing)
'''
root.wm_attributes('-topmost',1)    #置顶显示
#root.wm_overrideredirect(True)  #去掉标题等,仅仅显示label内容.
#root.overrideredirect(True) #隐藏窗口边框与标题栏.

#root.attributes("-transparentcolor","white")#白色透明掉.
#root["background"] = "white"

root.title("")
label = tk.Label(root,text='0000')
label.pack(side="right")
Timer(1,10).start() #更新价格频率 单位 秒
Clock(1,1).start()
#winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
curWidth = root.winfo_reqwidth() # get current width
curHeight = root.winfo_height() # get current height
scnWidth,scnHeight = root.maxsize() # get screen width and height
# now generate configuration information
#tmpcnf = '%dx%d+%d+%d'%(100,10,0,scnHeight-60)#scnWidth-110#带边框位置
tmpcnf = '%dx%d+%d+%d'%(150,10,scnWidth-160,scnHeight-80)#scnWidth-110#精简位置.
#tmpcnf = '%dx%d+%d+%d'%(100,20,scnWidth/2-55,scnHeight-45)
root.geometry(tmpcnf)
updatelabel(label)
root.mainloop()




"""
不得妄动

"""
'''
bihu

即使某天有着比较好的走势，结果往往只是一个陷阱。
在主品种无序波动期，保持关注，精力/资金准备。
最重要的是持续作战能力！！！持续关注！！！

垃圾最大的危害，是在最短的时间内剥夺你所有的创造力与灵气。
垃圾名单：
FG PP L P CS C BU PP TA

再次强调：不要更换品种，否则会与所有品种节奏脱节，陷入追涨杀跌的灾难之中！

设置保存利益多的止损，才有意义！

看法不重要，入场才重要！
每一次，因为幻想的走势+当下的错误走势+看一眼就入场/已经大幅波动了再入场，
然后或有短期浮盈，或直接多在最高点。不变的是后面逆转，而被深套。

不要钻到野区去面对未知的遭遇战

出现过的情况，往往还会出现。

---------------------------------------------------------
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>白天靠岸！！！
---------------------------------------------------------
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>加仓是魔鬼！！
---------------------------------------------------------
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>PP垃圾！！！
---------------------------------------------------------
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>机会更代表着无谓的风险！！！
---------------------------------------------------------
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>制造业 格力？？？？？？？？？？！！！
---------------------------------------------------------
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>白天靠岸！！！
---------------------------------------------------------
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>白天靠岸！！！
---------------------------------------------------------
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>白天靠岸！！！
---------------------------------------------------------
2017.2.28
上上周，赚了80%，运气可谓好到极点。然而上周，又倒亏了一些，比盈利的速度还快。初始时是谨小慎微，盈利就跑，都是止盈后再追的，碰到了好行情。后来是想做大行情，放大止损，反而一笔几千地亏损。亏损之后更想着抓住一波大行情，加快亏损。或者陷入过量交易的绞肉机中。

早上听旁人谈论，贪婪，开始赚了钱，但是最后肯定全部赔光。虽然已经听过无数次类似话语，这次却显得格外引人深思。

白天继续追多矿，一度有4600浮盈。然而最终高抛低吸反被套止损。来回做几次都是止损出局，损失惨重。

今晚看电影《赌命法则》,讲的其实是运气（当然只是主角的运气）。真的存在运气这个东西吧，有运气时自然得意，更应该及时收手。

我是看多黄金的，日线也是非常漂亮强势的阳线。如果是从底部拿上来，做长线，自然是一笔丰厚的利润。然而，自己是做不到的。
那么短线呢？白天一天也不怎么涨，矿螺却大涨，怎么选择？顺势做多，今晚开始时也是一度浮亏一千多，还好后来涨上来变成浮盈一千多。然后呢，选择持仓待涨？缩水到六七百。最终反手空，反而盈利一千。

是否顺大趋势，好像并不是那么重要。想着顺大趋势就持仓待涨，尤其因为“顺势”而追涨杀跌，想赚一笔大的，反而更容易成为被坑杀。
反而不如安安静静等待行情逆转，赚点小钱，来的安逸，轻松。

既然想要好的运气，还是只做夜盘，能时时盯着盘才好。

=========再次犯错
被诱敌深入.

交易,根本没有顺势逆势之说.
就是因为顺势,才造成了大概率亏损.

相比势,根本在于在有利的位置发动攻击,让对手止损.
修道,本就是逆天改命.

临收盘的反弹,再之后下午的走弱.此时,才是入场狙杀的唯一机会!!!
不留隔夜
========= 贵,是首要标准
预案

Sort: 时间因素最高。

跳出眼前，
相比一维，二维层面才是核心！只有在二维做好，大概率不犯错，不冲动，一维才有意义。



不要做乱七八糟的品种,参与乱七八糟的交易,
使用BAR线，不要使用K线。根据均线，形态做交易。
分析当前周期的趋势，决定多空方向。反弹，就不要期待幅度有多大。
不要追逐。先保证不亏损。
轻仓，才能持续追踪趋势。



'''