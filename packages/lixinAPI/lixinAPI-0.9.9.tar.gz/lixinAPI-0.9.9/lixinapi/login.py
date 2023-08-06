import hashlib
from lixinapi.__config import *

def md5x(pwd):
    try:
        # 或者可以这样
        mpwd=hashlib.md5(pwd).hexdigest()
    except:
        mpwd=hashlib.md5(pwd.encode(encoding='UTF-8')).hexdigest()
    return mpwd

def ressetLogin(loginname,loginpwd):
    pwd=md5x(loginpwd)
    sql="select id from rs_account where login_name='%s' and login_pwd='%s' "%(loginname,pwd)
    # print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    id=cursor.fetchone()
    cursor.close()
    if id is not None:
        context.userid=id[0]
        print("登录成功！！")
    else:
        print('账户或密码错误！！')
if __name__ == '__main__':

    thsLogin = ressetLogin("zhangq", "123")
#     if (thsLogin == 0 or thsLogin == -201):