# -*- coding: UTF-8 -*-
import parm, requests, time, copy, sys,logging
import cx_Oracle, logging, hashlib
import ConfigParser

import decorat
import database
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf8')


# 查询用户账户信息
class UserAccount(object):
    def __init__(self):
        self.__account1001_useable_old = 0
        self.__account1001_useable = 0
        self.__account1001_frozen = 0
        self.__account1001_frozen_old = 0
        # self.__account1000_totalamount = 0
        # self.__account1000_availableamount = 0
        # self.__account1000_frozenamount = 0
        # self.__account1000_totalamount_old = 0
        # self.__account1000_availableamount_old = 0
        # self.__account1000_frozenamount_old = 0

    @property
    def account1001_useable(self):
        return self.__account1001_useable

    @account1001_useable.setter
    def account1001_useable(self, value):
        self.__account1001_useable_old = self.__account1001_useable
        self.__account1001_useable = value

    @property
    def account1001_frozen(self):
        return self.__account1001_frozen

    @account1001_frozen.setter
    def account1001_frozen(self, value):
        self.__account1001_frozen_old = self.__account1001_frozen
        self.__account1001_frozen = value

    '''
    金账户需到富有页面查询
    @property
    def account1000_frozenamount(self):
        return self.__account1000_frozenamount
    @account1000_frozenamount.setter
    def account1000_frozenamount(self,value):
        self.__account1000_frozenamount_old = self.__account1000_frozenamount
        self.__account1000_frozenamount = value
    @property
    def account1000_availableamount(self):
        return self.__account1000_availableamount
    @account1000_availableamount.setter
    def account1000_availableamount(self,value):
        self.__account1000_availableamount_old = self.__account1000_availableamount
        self.__account1000_availableamount = value
    @property
    def account1000_totalamount(self):
        return self.__account1000_totalamount
    @account1000_totalamount.setter
    def account1000_totalamount(self,value):
        self.__account1000_totalamount_old = self.__account1000_totalamount
        self.__account1000_totalamount = value

    '''

    # 账户变化数据展示
    def show(self):
        print u"1001: useable:%.2f(%.2f) frozen:%.2f(%.2f)" % (
            self.__account1001_useable, self.__account1001_useable - self.__account1001_useable_old,
            self.__account1001_frozen, self.__account1001_frozen - self.__account1001_frozen_old,)
        '''
        print u"1000: totalamount:%.2f(%.2f) availableamount:%.2f(%.2f) frozenamount:%.2f(%.2f)"%\
              (self.__account1000_totalamount,self.__account1000_totalamount-self.__account1000_totalamount_old,
               self.__account1000_availableamount, self.__account1000_availableamount - self.__account1000_availableamount_old,
               self.__account1000_frozenamount, self.__account1000_frozenamount - self.__account1000_frozenamount_old,)
        '''


class Func_Apis(object):
    def __init__(self,Environment):
        self.Environment=Environment
        self.db=database.DB_oracle(parm.Sql.database_user[self.Environment[:-8]]['username'],
                                    parm.Sql.database_user[self.Environment[:-8]]['password'],
                                    parm.Sql.database_user[self.Environment[:-8]]['database'])
        self.RequestBase= parm.RequestBase(self.Environment)
        print 'Func_Apis_init'
    # 获取数据库内容
    def getDbData(self, solo):
        return self.db.select_all(solo)

    # 获取用户账户
    def getUserMessage(self, user_id):  # 增加第一次判断
        self.user_account.account1001_useable, self.user_account.account1001_frozen = \
        self.getDbData(str(parm.Sql.uesr_1001) % user_id)[0]
        self.user_account.show()

    # headr中sessionid增加
    def headersAddSession(self, headers, sessionid):
        headers_temp = copy.copy(headers)
        if isinstance(sessionid, str):
            headers_temp['cookie'] = '%s=%s;' % (self.RequestBase.BOSS_session, sessionid)
        elif isinstance(sessionid, list):
            for solo in sessionid:
                headers_temp["cookie"] += "%s=%s;" % (self.RequestBase.BOSS_session, solo)
        return headers_temp

    # 基础请求函数
    @decorat.checkprint()
    def baseRequestPost(self,dothing, url, payload, sessionid, r_type="POST"):
        headers = copy.copy(self.headersAddSession(self.RequestBase.base_headers, sessionid))

        response = requests.request(r_type, url, data=payload, headers=headers, verify=False)
        try:
            if 200 == response.status_code:
                for solo in parm.response_list.response_list:
                    if solo in str(response.text):
                        return True
            return False
        except:
            return False
        finally:
            print response.text

    # 确定及print
    def checkPrint(self, state, dothing, succeed="成功", faild="失败"):
        if state:
            print str(dothing) + succeed+'!!!!!!'
            logging.info(str(dothing) + succeed+'!!!!!!')
            return True
        else:
            print str(dothing) + faild + '!!!!!!'
            logging.info(str(dothing) + faild+'!!!!!!')
            return False


    # 日志配置
    def log_config(self, logfilename):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y %H:%M:%S', filename=logfilename, filemode='a+')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        logging.info("log success")

    # 日志整理
    def log_sort_out(self, logname, resultname, log_intercept_locat=int(37), borrowid_locat=int(5)):
        with open(logname, 'r') as f:
            new_list = []
            for index, i in enumerate(f.readlines()):
                if index != 0:
                    i = i.strip('\n')
                    new_list.append(i[log_intercept_locat:])
        statu = {'发标成功': 1, '发标失败': -1, '复审成功': 2, '复审失败': -2, '面签成功': 3, '面签失败': -3, '标的状态=3判断成功': 4, '标的状态=3判断失败': -4,
                 '标的金额校验成功': 5, '标的金额校验失败': -5, '放款成功': 6, '放款失败': -6, '标的状态=4判断成功': 7, '标的状态=4判断失败': -7, '还款成功': 8,
                 '还款失败': -8, '标的状态=5判断成功': 9, '标的状态=5判断失败': -9}
        opposite_statu = dict((value, key) for key, value in statu.iteritems())
        a = [i for i, x in enumerate(new_list) if x == 'start']
        new_dict = {}
        for index, value in enumerate(a):
            new_dict[new_list[value + borrowid_locat]] = {}
            if index == len(a) - 1:
                new_dict[new_list[value + borrowid_locat]]["data"] = new_list[value:]
            else:
                new_dict[new_list[value + borrowid_locat]]["data"] = new_list[value:a[index + 1]]
        for key in new_dict:
            bw_statu = 0
            for value in new_dict[key]["data"]:
                if value in statu.keys():
                    print value
                    if abs(statu[value]) > abs(bw_statu):
                        bw_statu = statu[value]
            new_dict[key]["statu"] = bw_statu
        with open(resultname, 'a') as f:
            for i in new_dict.keys():
                f.write(i + '\t' + new_dict[i]['data'][3] + '\t' + opposite_statu[new_dict[i]['statu']] + '\n')

    #一个字段在多接口中处理
    def interface_parm_deal(self,temp_data_dict,keys_split,solo,interface_corresponding):
        multi_key = keys_split[0].split("_")
        for i in list(multi_key[1]):
            temp_data_dict[interface_corresponding[i]][keys_split[1]] = solo

    # md5加密
    def md5(self, pwd):
        m = hashlib.md5()
        m.update(pwd)
        return m.hexdigest()
    def pwd_deal(self,pwd):
        if len(pwd) <= 16:
            pwd = self.md5(self.md5(pwd))
        else:
            pwd = pwd
        return pwd


class APIS(Func_Apis):
    def __init__(self, Environment,LoginBoss=True):
        super(APIS, self).__init__(Environment)
        self.URLs=parm.URLs(self.Environment)
        # 是否访问数据库
        self.Access_db = parm.Access_db
        # 是否变更数据
        self.Change_db = parm.Change_db
        if LoginBoss:
            self.boss_cookie = self.get_boss_login_session(self.URLs.boss_login, parm.User.boss_username,parm.User.boss_pwd)
            self.boss_session = self.boss_cookie[0]
            self.route = self.boss_cookie[1]
        else:
            self.boss_cookie = None
            self.boss_session = None
            self.route = None
        self.user_account = UserAccount()

    # 获取boss后台登录session
    def get_boss_login_session(self, url, username, password):
        driver = webdriver.Chrome()
        driver.get(url)
        driver.find_element_by_name("username").send_keys(username)
        driver.find_element_by_name("password").send_keys(password)
        if url[:5] == 'http:':
            driver.find_element_by_name("captcha").send_keys(parm.verification_code)
        else:
            time.sleep(10)
        driver.find_element_by_id("btn_login").click()
        boss_sessionid_list = []
        route = "route="
        time.sleep(1)
        for i in range(len(driver.get_cookies())):
            # print driver.get_cookies()[i]['value']
            if driver.get_cookies()[i]['name'] == 'JSESSIONID':
                boss_sessionid_list.append(driver.get_cookies()[i]['value'])
            else:
                route += driver.get_cookies()[i]['value'] + ";"
        return (boss_sessionid_list, route)

    # 获取订单状态
    # def getBorrowState(self, status1, borrow_id, time_limit=20):
    #     try:
    #         start = time.time()
    #         while time.time() - start < time_limit:
    #             status = self.getDbData(parm.Sql.borrow_state % (borrow_id))
    #             if status[0][0] == status1:
    #                 return True
    #     except:
    #         return False

    def getBorrowState(self, sql,status1, time_limit=20,*args):
        try:
            start = time.time()
            while time.time() - start < time_limit:
                status = self.getDbData(sql)
                if status[0][0] == status1:
                    return True
        except:
            return False
    #判断企业还是个人,确认标的参数变更
    def getUserType(self,data_dict,stage,user_id):
        if self.getDbData(parm.Sql.user_type % user_id)[0][0]==str(2):
            if stage=='test.xxd.com':
                data_dict["apply_borrow_data"]['fbComId']=1701
            elif stage=='stage.xxd.com':
                data_dict["apply_borrow_data"]['fbComId'] = 1674
    # 登陆
    def getXXDSessionID(self, Environment='', username='', passwd='', verify_code='mark'):
        try:
            payload = {"password": passwd, "username": username, "verifyCode": verify_code}
            headers = self.RequestBase.base_headers
            headers['cookie'] = self.route
            response = requests.request("POST", self.URLs.xxd_login, data=payload, headers=headers)
            session_id = response.cookies._cookies[Environment]["/"]["JSESSIONID"].value
            return session_id
        except:
            return False

    # 查询匹配金额
    def borrowTenderCheck(self, borrowid):
        try:
            # if "%.2f"%self.getDbData(parm.Sql.borrow_account % borrowid)[0][0] != "%.2f"%self.getDbData(parm.Sql.borrow_tender_sum % borrowid)[0][0]:
            #     print "borrow_account:", self.getDbData(parm.Sql.borrow_account % borrowid)[0][0], "borrow_tender_sum:", self.getDbData(parm.Sql.borrow_tender_sum % borrowid)[0][0]
            #     return False
            assert "%.2f"%self.getDbData(parm.Sql.borrow_account % borrowid)[0][0]=="%.2f"%self.getDbData(parm.Sql.borrow_tender_sum % borrowid)[0][0]
            assert "%.2f"%self.getDbData(parm.Sql.borrow_collection_sum % borrowid)[0][0]=="%.2f"%self.getDbData(parm.Sql.borrow_repayment_account % borrowid)[0][0]
            print "borrow_collection_sum:", self.getDbData(parm.Sql.borrow_collection_sum % borrowid)[0][0], "borrow_repayment_account", self.getDbData(parm.Sql.borrow_repayment_account % borrowid)[0][0]
            print "borrow_account:", self.getDbData(parm.Sql.borrow_account % borrowid)[0][0], "borrow_tender_sum:", self.getDbData(parm.Sql.borrow_tender_sum % borrowid)[0][0]
            print "borrow_collection_sum:", self.getDbData(parm.Sql.borrow_collection_sum % borrowid)[0][0], "borrow_repayment_account", self.getDbData(parm.Sql.borrow_repayment_account % borrowid)[0][0]
            return True
        except:
            return False

    # 1-发标2-初审3-复审4-面签-5放款6-还款,0-单独放款，-1单独放款，还款
    def run(self, data_dict, borrow_id=''):
        try:
            logging.info(data_dict['option']['username'])
            pwd=self.pwd_deal(data_dict['option']['password'])
            self.sessionid = self.getXXDSessionID(Environment=self.Environment, username=data_dict['option']['username'],
                                                  passwd=pwd, verify_code=parm.verification_code)
            self.user_id = data_dict['option']['user_id']
            step_dict = {
                0: ["self.createMBorrow(data_dict)"],
                1: ["self.first_trial(data_dict)"],
                2: ["self.recheck(data_dict)"],
                3: ["self.visa_interview(data_dict)"],
                4: ["self.getUserMessage(self.user_id)",
                    "time.sleep(2)",
                    "self.borrowLoan(data_dict)",
                    "self.getUserMessage(self.user_id)"],
                5: ["self.borrowRepayment(data_dict)",
                    "self.getUserMessage(self.user_id)"],
            }
            self.borrow_id = data_dict["option"]["borrowid"]
            self.porder=data_dict["want_repayment_data"]["porder"]

            if "" != data_dict["option"]["checkstatus"]:
                checkstatus = data_dict["option"]["checkstatus"].split("|")
            # 标的状态判断
            # step_dict[int(checkstatus[0])].append(
            #     'self.checkPrint(self.getBorrowState((parm.Sql.borrow_state %self.borrow_id),%s), "标的状态=%s判断")' % (
            #     checkstatus[1], checkstatus[1]))


            step = data_dict['option']['step'].split("|")
            for i in range(int(step[0]), int(step[1])):
                print i, ":", "*" * 20
                for thing in step_dict[i]:
                    eval(thing)
        except:
            return False
    #发标
    def createMBorrow(self, data_dict):
        logging.info('发标金额:' + data_dict["create_borrow_data"]['account'])
        self.borrow_id = self.createBorrow(data_dict["create_borrow_data"], self.sessionid)  # 发标
        logging.info(self.borrow_id)
        if not self.checkPrint(self.borrow_id, "发标"):
            return False
        data_dict["apply_borrow_data"]["borrowId"] = self.borrow_id
        self.getUserType(data_dict,self.Environment,self.user_id)
        if not self.baseRequestPost('标的确认',self.URLs.apply_borrow, data_dict["apply_borrow_data"], self.sessionid):
            return False
        data_dict["trial_borrow_data"]["name"] = "autotest" + str(self.borrow_id)
        data_dict["signing_approved_data"]["name"] = "autotest" + str(self.borrow_id)

    # 初审
    def first_trial(self, data_dict):
        if not self.baseRequestPost('初审',self.URLs.borrow_trial % self.borrow_id, data_dict["trial_borrow_data"],self.boss_session):
            return False


    # 终审
    def recheck(self, data_dict):
        if not self.baseRequestPost('复审',self.URLs.borrow_trial % self.borrow_id, data_dict["trial_borrow_data"],self.boss_session):
            return False
    #面签
    def visa_interview(self, data_dict):
        if not self.baseRequestPost('面签',self.URLs.signing_approved[data_dict["signing_approved_data"]["borrowType"]] % self.borrow_id, data_dict["signing_approved_data"], self.boss_session):
            return False
    #放款
    def borrowLoan(self, data_dict, borrow_id=''):
        if borrow_id == '':
            borrow_id = self.borrow_id
        if str(self.Access_db) == str(1):
            # 临时修改
            # if not self.checkPrint(self.getBorrowState(3, borrow_id), "标的状态=3判断"):
            #     return False
            if not self.checkPrint(self.getBorrowState(parm.Sql.borrow_state %borrow_id, 3), "标的状态=3判断"):
                return False
            if not self.checkPrint(self.borrowTenderCheck(self.borrow_id), "标的金额校验"):
                return False
        else:
            print '配置不需要访问数据库,标的状态=3判断、标的金额校验无需操作'

        if not  self.baseRequestPost('放款',self.URLs.make_loan % borrow_id, data_dict["make_loan_data"], self.boss_session):
            return False
        if str(self.Access_db) == str(1):
            if not self.checkPrint(self.getBorrowState(parm.Sql.borrow_state %borrow_id, 4), "标的状态=4判断"):
                return False
            self.checkPrint(self.getDbData(parm.Sql.withdraw_deposit_log % borrow_id),
                            self.getDbData(parm.Sql.withdraw_deposit_log % borrow_id), "存在提现记录", "无提现记录")
            self.borrow_id_message = self.getDbData(parm.Sql.borrow_id_message % (borrow_id))
        else:
            print '配置不需要访问数据库,标的状态=4判断、提现记录查询 无需操作'
        self.borrowAmount()

    # 还款操作
    def borrowRepayment(self, data_dict, borrow_id=''):
        if str(self.Access_db) != str(1):
            print '没有数据库访问权限不能还款'
            return False
        try:
            if borrow_id == '':
                borrow_id = self.borrow_id
            self.repayment_id = self.getDbData(parm.Sql.repayment_Id % (borrow_id,self.porder))[0][0]
            if not self.checkPrint(self.repayment_id, str(self.repayment_id) + "还款ID查找"):
                return False
            data_dict["want_repayment_data"]["borrow_id"] = borrow_id
            data_dict["want_repayment_data"]["repaymentId"] = self.repayment_id
            data_dict["want_repayment_data"]['proPwd']=self.pwd_deal(data_dict['option']['pro_password'])
            if not self.baseRequestPost('还款',self.URLs.want_repayment, data_dict["want_repayment_data"], self.sessionid):
                return False
            if not self.checkPrint(self.getBorrowState(parm.Sql.repayment_state %self.repayment_id,1,time_limit=40), "标的待还记录=1判断"):
                return False
            if not self.checkPrint(self.getBorrowState(parm.Sql.collection_state %(borrow_id,self.porder),1), "标的待收记录=1判断"):
                return False
            if int(data_dict["create_borrow_data"]["timeLimit"])==1:
                if not self.checkPrint(self.getBorrowState(parm.Sql.borrow_state %borrow_id, 5), "标的状态=5判断"):
                    return False
        except:
            logging.info("还款失败")

    def borrowAmount(self):
        if self.Access_db != str(1):
            return False
        borrow_success = 0
        for solo in self.borrow_id_message:
            if "borrow_success" in solo:
                borrow_success = solo[1]
        calc_ = borrow_success
        calc_string = "borrow_success" + str(calc_)
        for solo in self.borrow_id_message:
            if "borrow_success" not in solo:
                calc_string += " - " + solo[0] + str(solo[1])
                calc_ -= solo[1]
        print calc_string, "=", calc_

    # 创建标的请求
    def createBorrow(self, payload, sessionid):
        headers = self.headersAddSession(self.RequestBase.base_headers, sessionid)
        response = requests.request("POST", self.URLs.xxd_borrow, data=payload, headers=headers)
        if 200 == response.status_code:
            return eval(response.text)["map"]["borrowId"]
        return False


class runtest(APIS):
    def run(self, data_dict, borrow_id=''):
        try:
            logging.info(data_dict['option']['username'])
            pwd=self.pwd_deal(data_dict['option']['password'])
            self.sessionid = self.getXXDSessionID(Environment=parm.Environment, username=data_dict['option']['username'],
                                                  passwd=pwd, verify_code=parm.verification_code)
            self.user_id = data_dict['option']['user_id']
            step_dict = {
                0: ["self.createMBorrow(data_dict)"],
                1: ["self.first_trial(data_dict)"],
                2: ["self.recheck(data_dict)"],
                3: ["self.visa_interview(data_dict)"],
                4: ["self.getUserMessage(self.user_id)",
                    "time.sleep(2)",
                    "self.borrowLoan(data_dict)",
                    "self.getUserMessage(self.user_id)"],
                5: ["self.borrowRepayment(data_dict)",
                    "self.getUserMessage(self.user_id)"],
            }
            self.borrow_id = data_dict["option"]["borrowid"]
            self.porder=data_dict["want_repayment_data"]["porder"]
            if "" != data_dict["option"]["checkstatus"]:
                checkstatus = data_dict["option"]["checkstatus"].split("|")
            # 标的状态判断
            # step_dict[int(checkstatus[0])].append(
            #     'self.checkPrint(self.getBorrowState(%s,self.borrow_id), "#####标的状态=%s判断")' % (
            #         checkstatus[1], checkstatus[1]))
            step_dict[int(checkstatus[0])].append(
                'self.checkPrint(self.getBorrowState(parm.Sql.borrow_state %%self.borrow_id,%s), "标的状态=%s判断")' % (checkstatus[1], checkstatus[1]))
            step = data_dict['option']['step'].split("|")
            for i in range(int(step[0]), int(step[1])):
                print i, ":", "*" * 20
                for thing in step_dict[i]:
                    eval(thing)

        except:
            return False