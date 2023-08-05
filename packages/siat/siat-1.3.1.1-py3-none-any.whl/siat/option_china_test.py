# -*- coding: utf-8 -*-

# 绝对引用指定目录中的模块
import sys
sys.path.insert(0,r'S:\siat\siat')
from option_china import *
#==============================================================================
def option_fin_china():
    """
    查找中国金融期权列表
    """
    option_fin_list=['华夏上证50ETF期权','华泰柏瑞沪深300ETF期权', \
                     '嘉实沪深300ETF期权','沪深300股指期权']
    num=len(option_fin_list)

    print("  There are",num,"financial options in China mainland at present:")
    for i in option_fin_list:
        print(' ',i)
        
    return option_fin_list



import akshare as ak
#横截面数据
df1 = ak.option_finance_board(symbol="华夏上证50ETF期权", end_month="2112")
list(df1)
#['合约交易代码', '当前价', '涨跌幅', '前结价', '行权价', '数量']

df2 = ak.option_finance_board(symbol="嘉实沪深300ETF期权", end_month="2112")
list(df2)
['合约编码', '合约简称', '标的名称', '类型', '行权价', '合约单位', '期权行权日', '行权交收日']

df3 = ak.option_finance_board(symbol="华泰柏瑞沪深300ETF期权", end_month="2112")
list(df3)
#['合约交易代码', '当前价', '涨跌幅', '前结价', '行权价', '数量']

df4 = ak.option_finance_board(symbol="沪深300股指期权", end_month="2112")
list(df4)
#['instrument',
 'position',
 'volume',
 'lastprice',
 'updown',
 'bprice',
 'bamount',
 'sprice',
 'samount']








#沪深300指数期权
df10 = ak.option_sina_cffex_hs300_list()
#实时行情
df11 = ak.option_sina_cffex_hs300_spot(contract="io2112")
df12 = ak.option_sina_cffex_hs300_daily(contract="io2004C4450")

#==============================================================================
#查找中国商品期权的常见品种
df1=option_comm_china()

#查找中国黄金期权的可用合约
df2=option_comm_china('黄金')

#查找中国黄金期权au2112和au2202的具体合约（看涨/看跌合约）
df3=option_comm_china('黄金','au2112')
df3b=option_comm_china('黄金','au2202')
#同一时刻行权价对期权合约的影响：行权价越高，看涨期权合约价格越低，看跌期权合约价越高

#单一期权合约价格的运动趋势：默认不带趋势线
df4=option_comm_trend_china('au2202C364','2021-9-1','2021-9-30',power=4)

#期权方向对合约价格走势的影响：看涨/看跌期权合约的价格走势正好相反
df5=option_comm_trend_china(['au2202C364','au2202P364'],'2021-8-1','2021-9-30')

#行权价对合约价格时间序列走势的影响：看涨期权，行权价低者合约价高
df6=option_comm_trend_china(['au2112C328','au2112C364'],'2021-8-1','2021-9-30')
#行权价对合约价格时间序列走势的影响：看跌期权，行权价低者合约价低，与看涨期权正好相反
df6b=option_comm_trend_china(['au2112P328','au2112P364'],'2021-8-1','2021-9-30')

#到期时间对合约价格走势的影响：看涨期权，到期日近者合约价低（时间价值少）
df7=option_comm_trend_china(['au2112C364','au2202C364'],'2021-8-1','2021-9-30')
#到期时间对合约价格走势的影响：看跌期权，到期日近者合约价低，与看涨期权一致
df7b=option_comm_trend_china(['au2112P364','au2202P364'],'2021-8-1','2021-9-30')



#==============================================================================
