#
# Copyright (C) 2018 tobalanx@qq.com
#

import sys
import requests

class minites_data():

    #server = 'http://qt.gtimg.cn/q='
    server = 'http://hq.sinajs.cn/list='

    headers = {'Accept':'text/html', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    #proxies = {'http': '127.0.0.1:80', 'https': '127.0.0.1:80'}
    proxies = {}

    def grab( self, codes ) :
        '''
        e.g. codes = 'sz300389,sz002371,sz300523,sz300620,sh600807,sh000001,sz399006'
        '''
        if not codes : return []

        try :
            resp = requests.get(minites_data.server + codes,
                                timeout=0.5, # second
                                proxies=minites_data.proxies,
                                headers=minites_data.headers)
        except ReadTimeout :
            print("Error : requests() timeout")
            return [[0] * 9]
        except :
            print("Error : grabbing() : failed at requests.get(server, , ,)")
            return [[0] * 9]
            #sys.exit(0)
        #
        if resp.status_code != 200 :
            print("Error : grabbing() : resp.status_code = ", resp.status_code)
            return [[0] * 9]
            #sys.exit(0)
        #

        r = resp.text.split('\n')
        r.pop()  # delete the last ''
        #print('==1==', r)

        for i in range(len(r)):
            r[i] = r[i][11:-4]
            r[i] = r[i].replace('="', ',')
            r[i] = r[i].split(',')
            if len(r[i]) == 1 :
                r[i] += [0] * 8
            else :
                r[i].pop()
                # Time format to int()
                r[i].append( r[i][31].replace('-', '') + r[i][32].replace(':', '') )

        #
        return r
    #

    def arrange( self, r ) :

        code = r[0]
        tm = 0 if not r[-1] else int(r[-1])  # time
        open = float(r[2])
        close = float(r[3])
        curr = float(r[4]) # current price
        max = float(r[5])
        min = float(r[6])
        f = [code, tm, curr, open, close, max, min]

        return f

    def get_one( self, codes ) :

        r = self.grab( codes )
        #print('==r==', r)
        t = []
        for i in range(len(r)):
            f = self.arrange(r[i])
            t.append(f)

        return t


    def gets( self, select, data ) :

        r = self.grab( select )
        #print('==r==', r)
        t = len(data)
        for i in range(len(r)):
            f = self.arrange(r[i])
            #print('==d==', n, f, data[n])

            if data[i][0][0] != f[0]: continue # code mismatch
            if data[i][-1][0] != f[1]: # Time refresh
                data[i].append( f[1:] )
                if i >= t: break

        return



if __name__ == '__main__':
    import time
    d = minites_data()

    select = 'n1,sh000001,n2,sz399006,n3'
    '''
    #select = 'sh000001,sz399006'
    #result = [[['sh000001']], [['sz399006']]]
    result = [[['n1']], [['sh000001']], [['n2']], [['sz399006']], [['n3']]]
    d.gets(select, result)
    print( result )
    #print( '\n\n' )
    time.sleep(3)
    d.gets(select, result)
    print( result )
    '''
    result = d.get_one(select)
    print( result )




'''
-1: sh601006, 添加一个元素
0：”大秦铁路”，股票名字；
1：”27.55″，今日开盘价；
2：”27.25″，昨日收盘价；
3：”26.91″，当前价格；
4：”27.55″，今日最高价；
5：”26.20″，今日最低价；
6：”26.91″，竞买价，即“买一”报价；
7：”26.92″，竞卖价，即“卖一”报价；
8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
10：”4695″，“买一”申请4695股，即47手；
11：”26.91″，“买一”报价；
12：”57590″，“买二”
13：”26.90″，“买二”
14：”14700″，“买三”
15：”26.89″，“买三”
16：”14300″，“买四”
17：”26.88″，“买四”
18：”15100″，“买五”
19：”26.87″，“买五”
20：”3100″，“卖一”申报3100股，即31手
21：”26.92″，“卖一”报价
(22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四的情况”
30：”2008-01-11″，日期
31：”15:05:32″，时间
'''
