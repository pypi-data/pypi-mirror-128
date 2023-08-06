import pandas as pd
import datetime
import pymssql
from lixinapi.secret import *
from sqlalchemy import *
#solr地址
# titlesolr='http://106.75.219.243:8080/solrTA/title'
contentsolr=decrypt('36L39dqK+Yw2KxA8UiV39/smikvm7emHTaip6qjuUfdYXKLukGwaNjQQ9fb8Eap2')
# chaptersolr='http://106.75.219.243:8080/solrTA/chapter'
#TXT存储路径
PATH=u'E:/RESSET/Report'

#数据库链接
dburl=decrypt('BV4L6rzB5zITUPK+IeApvrgHUR96H64NfDz92potAnZ/DjtxXnSEoTk3h6oyaq12mxZdGUyN0sKorBeZ4SKnwQxIWDgYt+23IXRhHaD5CvY')
db=pymssql.connect(decrypt('bjEZOBs+qZypI4pUfjstfOP8q0zj8XVSYbkOikC6Zpg'), decrypt('QKQ4RAXfyse0+iqLFWewYA'), decrypt('p58sxNFfd1e4l1Eu66ZonA'), decrypt('lIPA8Yl8wzzwWDf9FdQe4g'), charset='utf8')
jydburl=decrypt('BV4L6rzB5zITUPK+IeApvkXu++2pLno6nj3cXSPKyha1t+vkWeZ5VGBdNb5KpnGtVKHMl/Tq73EqPtWA5AnPIg')
# jydburl=decrypt('BV4L6rzB5zITUPK+IeApvpvmOQtRCiaqYMAhYBBbah9iFZxrSm/WCfN17VuQIC3Ogha/Zj/w2ix1YldeDGe+5Q')
engine = create_engine(jydburl, echo=False, pool_size=1000)
dbengine=create_engine(dburl, echo=False, pool_size=1000)
# 持久化对象
class Context():
    def __init__(self):
        # 账户信息
        self.permission = pd.DataFrame()
        self.userid = ''
    def __repr__(self):
        return "Context({'userid':%s})"\
               %(self.userid)
context = Context()

#判断是否登陆，剩余流量
def query_permission(id,tablename,startdate,enddate):
    persql = "select * from permission where userid='%s' and tablename='%s'"% (id,tablename)
    # print(persql)
    context.permission = pd.read_sql_query(persql, dbengine)
    if len(context.permission)>0:
        p_id=context.permission['id'][0]
        p_start=context.permission['startdate'][0]
        p_enddate=context.permission['enddate'][0]
        p_totalnum=context.permission['totalnum'][0]
        p_eachnum=context.permission['eachnum'][0]
        if startdate != '':
            startdate_T = datetime.datetime.strptime(startdate, '%Y-%m-%d')
            if startdate_T >= p_start:
                startdate = startdate
            else:
                startdate = p_start.strftime("%Y-%m-%d %H:%M:%S")[:10]
        else:
            startdate = p_start.strftime("%Y-%m-%d %H:%M:%S")[:10]
        if enddate!='':
            enddate = enddate
        else:
            enddate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")[:10]
        if p_totalnum > p_eachnum:
            num = p_eachnum
        else:
            num = p_totalnum
        return startdate,enddate,num,p_totalnum,p_id
    else:
        print('该账号没有此表权限！！')
        exit()

def Update_permission(id,totalnum):
    persql = "update permission set totalnum='%s' where id='%s' " % (totalnum, id)
    # print(persql)
    cursor = db.cursor()
    cursor.execute(persql)
    db.commit()
    cursor.close()


def Islogin():
    if context.userid=='':
        print('请先登录账号！！')
        exit()
