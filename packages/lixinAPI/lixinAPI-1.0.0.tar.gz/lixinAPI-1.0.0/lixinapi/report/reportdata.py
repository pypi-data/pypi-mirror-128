from lixinapi.login import *
import requests

def get_report(content_type,code, type, year):
    startdate, enddate, num, p_totalnum, p_id = query_permission(context.userid, 'Year_Report', '', '')


    if content_type != 'part':
        content_type = 'all'
    query = contentsolr + '/select?fl=id,title,code,name,releaseTime,type,charnum,year,%s_content&rows=%s&q=code:"%s"AND type:"%s"AND year:%s' % (content_type, str(num), code, type, year)
    # print(query)
    r = requests.get(query, verify=False, headers={'Connection': 'close'})
    report_list = r.json()['response']['docs']
    # print(report_list)
    if num >= len(report_list):
        num = len(report_list)
    Update_permission(p_id, p_totalnum - num)
    return report_list

if __name__ == '__main__':
    thsLogin = ressetLogin("zhangq", "123")
    print(get_report('part', '002462', '年度报告', '2011'))