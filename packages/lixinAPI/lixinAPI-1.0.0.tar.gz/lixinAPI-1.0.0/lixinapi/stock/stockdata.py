from lixinapi.login import *
# 创建数据库交互
metadata = MetaData(engine)  # 实例化数据库对象
# dbTable = Table('literature_copy', metadata, autoload=True)

#获取股票内部代码
def get_InnerCode(security):
    code=security.split('_')[1]
    market=security.split('_')[0]
    sql="select InnerCode from SecuMain where SecuCode='%s' and SecuMarket='%s'"%(code,market)
    table=pd.read_sql_query(sql, engine)
    inner=''
    if len(table)>0:
        inner=table['InnerCode'][0]
    return security,inner

#获取股票公司代码
def get_CompanyCode(security):
    code=security.split('_')[1]
    market=security.split('_')[0]
    sql="select CompanyCode from SecuMain where SecuCode='%s' and SecuMarket='%s'"%(code,market)
    table=pd.read_sql_query(sql, engine)
    inner=''
    if len(table)>0:
        CompanyCode=table['CompanyCode'][0]
        return security,CompanyCode

def get_Factor(security,date,fq):
    pass
    # try:
    #     if fq=='qfq':
    #     if len(inner) > 0:
    #         fember=session1.query(Factor).filter(Factor.InnerCode==inner[0].InnerCode).order_by(Factor.ExDiviDate.desc()).first()
    #         member=session1.query(Factor).filter(Factor.InnerCode==inner[0].InnerCode,Factor.ExDiviDate<=date).order_by(Factor.ExDiviDate.desc()).first()
    #         if member is not None:
    #             a=member.RatioAdjustingFactor
    #             b=fember.RatioAdjustingFactor
    #         else:
    #             a=1
    #             b=1
    # except:
    #     a=1
    #     b=1
    # return decimal.Decimal(str(a/b))

#A股日行情数据API
def get_history_data(security,startdate='',enddate='',fq='bfq'):
    # print(context.userid)
    #判断是否登陆
    # Islogin()
    #判断账户权限
    startdate,enddate,num,p_totalnum,p_id=query_permission(context.userid,'QT_DailyQuote',startdate,enddate)
    #获取股票内部编码
    innercode = []
    maplist={}
    for x in security.split(','):
        code,inner = get_InnerCode(x)
        if inner != '':
            maplist[str(inner)]=code
            innercode.append(str(inner))
    innercode=str(innercode).replace('[','(').replace(']',')')
    #获取复权因子
    if fq=='bfq':
        pass
    datasql="select top %s InnerCode as StockCode,TradingDay,PrevClosePrice,OpenPrice,HighPrice,LowPrice,ClosePrice,TurnoverVolume,TurnoverValue,TurnoverDeals from QT_DailyQuote where innercode in %s and TradingDay>='%s' and TradingDay<='%s' order by InnerCode,TradingDay desc"%(str(num),innercode,startdate,enddate)
    # print(datasql)
    table = pd.read_sql_query(datasql, engine)
    table['StockCode']=table['StockCode'].map(lambda x:maplist[str(x)])
    # print(table)
    Update_permission(p_id,  p_totalnum-num)
    return table

def get_Income_data(security,startdate='',enddate='',fileds=''):
    # 判断账户权限
    startdate, enddate, num,p_totalnum,p_id = query_permission(context.userid, 'LC_IncomeStatementAll', startdate, enddate)
    # 获取股票内部编码
    innercode = []
    maplist = {}
    for x in security.split(','):
        code, CompanyCode = get_CompanyCode(x)
        if CompanyCode != '':
            maplist[str(CompanyCode)] = code
            innercode.append(str(CompanyCode))
    innercode = str(innercode).replace('[', '(').replace(']', ')')
    if fileds=='':
        datasql="select top %s CompanyCode as StockCode,EndDate,OperatingRevenue,NetInterestIncome,PremiumsIncome,OtherOperatingRevenue,OperatingPayout,OperatingCost,FairValueChangeIncome,InvestIncome,NonoperatingIncome,NonoperatingExpense,NPParentCompanyOwners,BasicEPS,DilutedEPS from LC_IncomeStatementAll where CompanyCode in %s and EndDate>='%s' and EndDate<='%s' order by CompanyCode,EndDate desc"%(str(num),innercode,startdate,enddate)
        # print(datasql)
        table = pd.read_sql_query(datasql, engine)
        table['StockCode']=table['StockCode'].map(lambda x:maplist[str(x)])
        # print(table)
        Update_permission(p_id, p_totalnum - num)
        return table
    else:
        datasql = "select top %s CompanyCode as StockCode,EndDate,%s from LC_IncomeStatementAll where CompanyCode in %s and EndDate>='%s' and EndDate<='%s' order by CompanyCode,EndDate desc" % (str(num),fileds, innercode, startdate, enddate)
        # print(datasql)
        table = pd.read_sql_query(datasql, engine)
        table['StockCode'] = table['StockCode'].map(lambda x: maplist[str(x)])
        # print(table)
        Update_permission(p_id, p_totalnum - num)
        return table


def get_Balance_data(security,startdate='',enddate='',fileds=''):
    # 判断账户权限
    startdate, enddate, num,p_totalnum,p_id = query_permission(context.userid, 'LC_BalanceSheetAll', startdate, enddate)
    # 获取股票内部编码
    innercode = []
    maplist = {}
    for x in security.split(','):
        code, CompanyCode = get_CompanyCode(x)
        if CompanyCode != '':
            maplist[str(CompanyCode)] = code
            innercode.append(str(CompanyCode))
    innercode = str(innercode).replace('[', '(').replace(']', ')')
    if fileds=='':
        datasql="select top %s CompanyCode as StockCode,EndDate,CashEquivalents,AccountReceivable,AdvancePayment,TotalCurrentAssets,LongtermReceivableAccount,FixedAssets,TotalNonCurrentAssets,SettlementProvi,DerivativeAssets,FixedDeposit,ShortTermLoan,TotalCurrentLiability,LongtermLoan,OtherLiability,TotalLiability from LC_BalanceSheetAll where CompanyCode in %s and EndDate>='%s' and EndDate<='%s' order by CompanyCode,EndDate desc"%(str(num),innercode,startdate,enddate)
        # print(datasql)
        table = pd.read_sql_query(datasql, engine)
        table['StockCode']=table['StockCode'].map(lambda x:maplist[str(x)])
        # print(table)
        Update_permission(p_id, p_totalnum - num)
        return table
    else:
        datasql = "select top %s CompanyCode as StockCode,EndDate,%s from LC_BalanceSheetAll where CompanyCode in %s and EndDate>='%s' and EndDate<='%s' order by CompanyCode,EndDate desc" % (str(num),fileds, innercode, startdate, enddate)
        # print(datasql)
        table = pd.read_sql_query(datasql, engine)
        table['StockCode'] = table['StockCode'].map(lambda x: maplist[str(x)])
        # print(table)
        Update_permission(p_id, p_totalnum - num)
        return table

def get_CashFlow_data(security,startdate='',enddate='',fileds=''):
    # 判断账户权限
    startdate, enddate, num,p_totalnum,p_id = query_permission(context.userid, 'LC_CashFlowStatementAll', startdate, enddate)
    # 获取股票内部编码
    innercode = []
    maplist = {}
    for x in security.split(','):
        code, CompanyCode = get_CompanyCode(x)
        if CompanyCode != '':
            maplist[str(CompanyCode)] = code
            innercode.append(str(CompanyCode))
    innercode = str(innercode).replace('[', '(').replace(']', ')')
    if fileds=='':
        datasql="select top %s CompanyCode as StockCode,EndDate,SubtotalOperateCashInflow,SubtotalOperateCashOutflow,NetOperateCashFlow,SubtotalInvestCashInflow,SubtotalInvestCashOutflow,NetInvestCashFlow,SubtotalFinanceCashInflow,SubtotalFinanceCashOutflow,NetFinanceCashFlow,ExchanRateChangeEffect,CashEquivalentIncrease,EndPeriodCashEquivalent,NetProfit from LC_CashFlowStatementAll where CompanyCode in %s and EndDate>='%s' and EndDate<='%s' order by CompanyCode,EndDate desc"%(str(num),innercode,startdate,enddate)
        # print(datasql)
        table = pd.read_sql_query(datasql, engine)
        table['StockCode']=table['StockCode'].map(lambda x:maplist[str(x)])
        # print(table)
        Update_permission(p_id, p_totalnum - num)
        return table
    else:
        datasql = "select top %s CompanyCode as StockCode,EndDate,%s from LC_CashFlowStatementAll where CompanyCode in %s and EndDate>='%s' and EndDate<='%s' order by CompanyCode,EndDate desc" % (str(num),fileds, innercode, startdate, enddate)
        # print(datasql)
        table = pd.read_sql_query(datasql, engine)
        table['StockCode'] = table['StockCode'].map(lambda x: maplist[str(x)])
        # print(table)
        Update_permission(p_id, p_totalnum - num)
        return table

if __name__ == '__main__':
    thsLogin = ressetLogin("zhangq", "123")
    get_history_data('83_600519,90_000001','2018-09-10','2021-09-16')
    get_Balance_data('83_600519,90_000001', '2018-09-10', '2021-09-16')
    get_CashFlow_data('83_600519,90_000001', '2018-09-10', '2021-09-16')
