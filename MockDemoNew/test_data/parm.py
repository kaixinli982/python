# -*- coding: UTF-8 -*-
import time,ConfigParser

verification_code="mark"
Access_db=1#(1-访问，0-不访问)
Change_db=1#(1-变更，0-不变更，且只有Access_db=1时，此字段才有意义)

class URLs():
    def __init__(self,Environment):
        self.Environment=Environment

        self.boss_login="http://"+self.Environment+"/xxdai_sys_admin/employee/login.do;jsessionid=002625CA15B438EB6B7D1771FADE277B"
        # 登陆
        self.xxd_login = "http://"+self.Environment+"/user/loginActive.html"
        #发标
        self.xxd_borrow = "http://"+self.Environment+"/myloan/fill/borrow.html"
        #标的确认
        self.apply_borrow = "http://"+self.Environment+"/borrow/applyBorrow.html"
        #标的审核
        self.borrow_trial="http://"+self.Environment+"/xxdai_sys_admin/risk/control/approved/%s.do"
        #标的面签约
        self.signing_approved={
            "9":"http://"+self.Environment+"/xxdai_sys_admin/risk/control/signingApproved/%s.do",
            "10":"http://"+self.Environment+"/xxdai_sys_admin/risk/control/approved/%s.do",
            "14":"http://"+self.Environment+"/xxdai_sys_admin/risk/control/approved/%s.do",
            "13": "http://"+self.Environment+"/xxdai_sys_admin/risk/control/approved/%s.do",
        }
        #标的放款
        self.make_loan = "http://"+self.Environment+"/xxdai_sys_admin/account/cash/makeLoan/%s.do"
        #还款
        self.want_repayment = "http://"+self.Environment+"/account/wantRepayment.html"
        #用户类型变更
        self.change_user_type = "http://"+self.Environment+"/personal/basicSave.html"
class User:
    boss_username="guoxiaoli"
    boss_pwd="Aa111111"
class RequestBase(object):
    def __init__(self,Environment):
        self.Environment=Environment
        self.XXD_session = "XXD_front_SESSIONID"
        self.BOSS_session = "JSESSIONID"
        self.base_headers = {
            'accept': "application/json, text/javascript, */*; q=0.01",
            'origin': "http//"+self.Environment,
            'x-requested-with': "XMLHttpRequest",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            'content-type': "application/x-www-form-urlencoded",
            'referer': "http//"+self.Environment+"/user/ilogin.html",
            "cookie":"route=afbf93fb6b94ad97139cc7191098e600;"
        }
        self.user_type_change_headers = {
            'clientid': "XXD_INTEGRATION_PLATFORM",
            'clienttime': str(int(time.time()*1000)),
            's': "de42212bdc77b66092a9211cc08b2313",
            'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
            'cache-control': "no-cache",
            'postman-token': "fdde48ac-4ad8-b439-b412-5d604aaa04c9"
            }
class Sql:
    uesr_1001 = "SELECT usable,frozen FROM xxd_account where userid = '%s'and pcode='1001'"
    user_1000 = "SELECT * FROM xxd_fy_cap_acnt_mirror  where userid = '%s'"
    borrow_state = "SELECT status,loanaccount FROM xxd_borrow where  BORROWID='%s'"
    withdraw_deposit_log = "SELECT STATUS from GATEWAY_TRADEFLOW where ACTIONTYPE = 'DELEGATE_TO_WITHDRAW'  and BORROWID='%s'"
    borrow_id_message = "SELECT operatortype,workmoney FROM xxd_account_log where busiid='%s' order by addtime desc"
    borrow_repayment = "update XXD_BORROW_REPAYMENT  set REPAYMENTTIME=to_date('2017-08-30 11:54:30','yyyy-MM-dd:hh24:mi:ss') where BORROWID='%s' "
    repayment_Id = "SELECT REpaymentid FROM  XXD_BORROW_REPAYMENT  where BORROWID='%s'and status=0 and porder='%s' "
    user_type = "SELECT usertype FROM xxd_user_baseinfo where userid='%s'"
    borrow_account = "SELECT sum(EFFECTIVEMONEY) FROM XXD_BORROW_TENDER where BORROWID = '%s'"
    borrow_tender_sum = "SELECT account FROM XXD_BORROW WHERE BORROWID = '%s'"
    borrow_collection_sum = "SELECT sum(repaymentaccount) FROM XXD_BORROW_REPAYMENT where BORROWID = '%s'"
    borrow_repayment_account = "SELECT sum(REPAYACCOUNT) FROM XXD_BORROW_COLLECTION WHERE BORROWID = '%s'"
    repayment_check = "SELECT status FROM xxd_borrow_repayment where repaymentid = '%s'"
    repayment_state="SELECT status,sum(repaymentyesaccount) FROM  XXD_BORROW_REPAYMENT  where repaymentid='%s' group by status"
    collection_state="SELECT status,sum(REPAYYESACCOUNT)  FROM  xxd_borrow_collection  where BORROWID='%s' and porder='%s' group by status"

    database_user={"stage":{'username':'xxd_stage','password':'Bb919189','database':'192.168.31.225:1521/oragbst'},
                   "test":{'username':'xxd_v6_test','password':'Fc9a5cc','database':'192.168.31.225:1521/oragbst'},
                   "uat": {'username': 'XINXINDB', 'password': 'E08c555c123', 'database': '192.168.31.225:1521/v6trndg3'}
                   }
    sql = [
        "SELECT feeamount from GATEWAY_PAYMENT_FEE a,GATEWAY_PAYMENTINFO b where a.paymentid=b.id and b.borrowid='%s' and a.feetype='QA_SERVICE'and a.status='SUCCESS'",
        "SELECT operatortype,workmoney FROM xxd_account_log where userid='%s'and busiid='%s' order by addtime desc",  # 1-3
        "SELECT usable,frozen FROM xxd_account where userid = '%s'and pcode='1001'",
        "SELECT * FROM xxd_fy_cap_acnt_mirror  where userid = '%s'",
        "SELECT feeamount from GATEWAY_PAYMENT_FEE a,GATEWAY_PAYMENTINFO b where a.paymentid=b.id and b.borrowid='%s' and a.feetype='INTEREST_ON_RESERVES'and a.status='SUCCESS'",
        "SELECT STATUS from GATEWAY_TRADEFLOW where ACTIONTYPE = 'DELEGATE_TO_WITHDRAW'  and BORROWID='%s'",
    ]
#校验结果表单
class response_list_old:
    response_list=('''{"resultCode":0}''',
                   '''{"statusCode":"200", "message":"操作成功", "navTabId":"appro", "rel":"", "callbackType":"closeCurrent", "forwardUrl":""}''',
                   '''{"statusCode":"200", "message":"操作成功", "navTabId":"bidRemit", "rel":"", "callbackType":"closeCurrent", "forwardUrl":""}''',
                   '''{"resultCode":0,"resultMes":"请求成功！[请求成功]","url":"http://"+Environment+":80/account/repaydetail.html"}''')

class response_list:
    response_list=('''{"resultCode":0}''',
                   '''"statusCode":"200", "message":"操作成功"''',
                   '''"resultCode":0,"resultMes":"请求成功！[请求成功]"''')


class interface_template:
    # 接口请求基础数据-发标
    create_borrow_data = {"account": "2222",
                          "apr": "60",
                          "citys": "110000",
                          "creditmanager": "160400111",
                          "effectiveTime": "60", "funds": "",
                          "mostTender": "0",
                          "name": "2221", "paymentMethod": "5",
                          "product": "", "provinces": "110000",
                          "timeLimit": "6", "type": "9", "use": "7",
                          "verifyCode": "mark",
                          "content":"1",
                          "lowestTender":"50"}

    # 发标确认,"fbComId":1674
    apply_borrow_data = {"borType": "9", "borrowId": ""}
    trial_borrow_data = {"blevel": "1", "borrowTimesType": "1", "borrowType": "9", "caltype": "1",
                         "isRevolving": "0", "loanAccount": "11",
                         "manageFee": "0.33", "mostTender": "0", "name": "ddd", "remark": "1", "status": "1","lowestTender":"50","content":"1","cashPosit":"1.1","accountMnangeFee":"0"}
    # 初审、复审、面签
    signing_approved_data = {"bankAccount": "",
                             "bankInfo": "6212262200013557002", "bankSubBranch": "", "blevel": "1","borrowSubType":"5",
                             "borrowTimesType": "1", "borrowType": "9",
                             "caltype": "1", "contractCode": "page",
                             "isRevolving": "0", "loanAccount": "11", "manageFee": "0.33","overdueLoanAccount":"1","overdueLoanMonth":"1","overdueLoanCardMonth":"1",
                             "mostTender": "0", "name": "ddd", "pchannelid": "", "remark": "1", "status": "1",
                             "borrowLoadType":"0","overdueLoanNum":"0","overdueLoanAccount":"0","overdueLoanMonth":"0","overdueLoanCardMonth":"0",
                             "cashPosit":"1.1","borrowStatus":"1","borrowUserId":"","accountMnangeFee":"0","lowestTender":"50","contractMode":"1","contractMode_temp":"1","content":"1"}
    # 放款
    make_loan_data = {"account": "11", "isPostpone": "0", "loanAccount": "11", "loanStatus": "待放款", "realName": "胡银湖",
                      "releaseAmount": "9.57", "userName": "18088888831"}
    # 还款
    want_repayment_data = {"borrowType": "9", "borrow_id": "", "porder": "1",

                           "repaymentId": "", "verifyCode": "mark","proPwd":""}
    # "proPwd": User.pro_password,
    option = {"step": "",
              "username":"",
              "pro_password":"",
              "borrowid":"",
              "password":"",
              "userid":"",
              }
    # 1-发标2-初审3-复审-4-面签-5-放款-6还款

    data_dict = {"create_borrow_data": create_borrow_data,
                 "apply_borrow_data": apply_borrow_data,
                 "trial_borrow_data": trial_borrow_data,
                 "signing_approved_data": signing_approved_data,
                 "make_loan_data": make_loan_data,
                 "want_repayment_data": want_repayment_data,
                 "option": option
                 }
class interface_corresponding:
    interface_corresponding = {'1': 'create_borrow_data', '2': 'apply_borrow_data', '3': 'trial_borrow_data',
                               '4': 'signing_approved_data', '5': 'make_loan_data', '6': 'want_repayment_data'}


