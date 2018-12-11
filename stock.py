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
                                proxies=minites_data.proxies,
                                headers=minites_data.headers)
        except :
            print("Error : grabbing() : failed at requests.get(server, , ,)")
            return ['0'] * 9
            #sys.exit(0)
        #
        if resp.status_code != 200 :
            print("Error : grabbing() : resp.status_code = ", resp.status_code)
            return ['0'] * 9
            #sys.exit(0)
        #

        r = resp.text.split('\n')
        r.pop()  # delete the last ''
        #print('==1==', r)

        n = 0
        for i in r :
            r[n] = i[11:-5]
            r[n] = r[n].replace('="', ',')
            r[n] = r[n].split(',')
            if len(r[n]) == 1 :
                r[n] = ['0'] * 9
            else :
                # Time format to int()
                r[n].append( r[n][31].replace('-', '') + r[n][32].replace(':', '') )

            n += 1
        #
        return r
    #


    def get_data( self, select, data ) :

        r = self.grab( select )
        #print('==r==', r)
        for i in range(len(r)):
            code = r[i][0]
            tm = int(r[i][-1])  # time
            open = float(r[i][2])
            close = float(r[i][3])
            curr = float(r[i][4]) # current price
            max = float(r[i][5])
            min = float(r[i][6])
            f = [tm, curr, open, close, max, min]

            if not data[i]: # Null List init
                data[i].append( f )
            elif data[i][-1][0] != tm : # Time refresh
                data[i].append( f )

            #print(i, data)

        return



if __name__ == '__main__':
    import time
    d = minites_data()
    select = 'n1,sh000001,n2,sz399006,n3'
    result = [[], [], [], [], []]
    d.get_data(select, result)
    print( result )
    time.sleep(2)
    d.get_data(select, result)
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
