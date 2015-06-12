#!/usr/bin/env python
# coding=utf8

import requests
import ConfigParser

# import curses
import os, time




def clear_display():
    # printf "\ec"
    os.system('printf "\033c"')

def show_template(hq):

    # 0：”大秦铁路”，股票名字；
    # 1：”27.55″，今日开盘价；
    # 2：”27.25″，昨日收盘价；
    # 3：”26.91″，当前价格；
    # 4：”27.55″，今日最高价；
    # 5：”26.20″，今日最低价；
    # 6：”26.91″，竞买价，即“买一”报价；
    # 7：”26.92″，竞卖价，即“卖一”报价；
    # 8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
    # 9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
    # 10：”4695″，“买一”申请4695股，即47手；
    # 11：”26.91″，“买一”报价；
    # 12：”57590″，“买二”
    # 13：”26.90″，“买二”
    # 14：”14700″，“买三”
    # 15：”26.89″，“买三”
    # 16：”14300″，“买四”
    # 17：”26.88″，“买四”
    # 18：”15100″，“买五”
    # 19：”26.87″，“买五”
    # 20：”3100″，“卖一”申报3100股，即31手；
    # 21：”26.92″，“卖一”报价
    # (22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四的情况”
    
    _range = float(hq[3]) - float(hq[2])
    _range_rate = _range/float(hq[2]) * 100
    
    _res = []
    _res.append("name: %s, n: %s, t: %s, y: %s, r: %s(%.2f)" % (hq[0], hq[3], hq[1], hq[2], str(_range), _range_rate) )

    _res.append("sale: %s(%s),  %s(%s),  %s(%s),  %s(%s),  %s(%s)" % (hq[21],hq[20],hq[23], hq[22],hq[25],hq[24],hq[27],hq[26],hq[29],hq[28]) )
    _res.append(" buy: %s(%s),  %s(%s),  %s(%s),  %s(%s),  %s(%s)" % (hq[11],hq[10],hq[13], hq[12],hq[15],hq[14],hq[17],hq[16],hq[19],hq[18]) )

    return "\n".join(_res)


def stock():
    runpath = os.path.realpath(__file__)

    cf = ConfigParser.SafeConfigParser()
    cf.read("%s/setting.conf" % os.path.dirname(runpath))
    sh = cf.get("stock", "SH").split(',')
    sz = cf.get("stock", "SZ").split(',')

    stock = []
    for k, v in enumerate(sz):
        stock.append("sz%s" % v)
    for k, v in enumerate(sh):
        stock.append("sh%s" % v)

    

    while True:
        _print = []
        for k, v in enumerate(stock):
            try:
                res = requests.get(url="http://hq.sinajs.cn/list=%s" % v)
                hq = res.text.split("=")[1].replace('"', '').replace(";", '').split(",")
                _print.append(show_template(hq))
            except Exception, e:
                print e
            _print.append("---------------------------------------------------------------")
        
        clear_display()
        print "\n".join(_print)
        time.sleep(1)




if __name__ == '__main__':
    stock()