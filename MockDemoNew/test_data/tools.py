# -*- coding: UTF-8 -*-
import copy
import parm

def data_interface_correspondence():
    tmp_correspondence={}
    tmp_correspondence["account"]={"create_borrow_data": "account", "trial_borrow_data": "loanAccount",
                                                 "signing_approved_data": "loanAccount",
                                                 "make_loan_data": ["loanAccount", "releaseAmount"]}
    tmp_correspondence["mobile"] = {"option": "username"}
    tmp_correspondence["loginpw"] = {"option": "password"}
    tmp_correspondence["proPwd"] = {"option": "pro_password"}
    tmp_correspondence["borrowtype"] = {"create_borrow_data": "type", "apply_borrow_data": "borType",
                                                   "trial_borrow_data": "borrowType",
                                                   "signing_approved_data": "borrowType",
                                                   "want_repayment_data": "borrowType"}
    tmp_correspondence["repaytype"] = {"create_borrow_data": "paymentMethod",
                                                  "signing_approved_data": "approborrow_paymentMethod", }
    tmp_correspondence["timelimit"] = {"create_borrow_data": "timeLimit"}
    tmp_correspondence["use"] = {"create_borrow_data": "use"}
    tmp_correspondence["step"] = {"option": "step"}
    tmp_correspondence["user_id"]={"option": "user_id"}
    tmp_correspondence["checkstatus"] = {"option": "checkstatus"}
    return tmp_correspondence
def request_data(config_data,data_interface_correspondence,tmp_data_dict=copy.copy(parm.interface_template.data_dict)):
    for key ,value in config_data.items():
        if key in data_interface_correspondence.keys():

            for k,v in data_interface_correspondence[key].items():
                if isinstance(v,str):
                    tmp_data_dict[k][v]=value
                else :
                    print v
                    for i in range(len(v)):
                        tmp_data_dict[k][i]=value
    return tmp_data_dict


def req_data_deal(req):
    config_data={}
    config_data['environment']  = req.GET['environment']+".xxd.com"
    config_data['mobile']  = req.GET['mobile']
    config_data['loginpw']  = req.GET['loginpw']
    config_data['proPwd']  = req.GET['paypw']
    config_data['borrowtype']  = req.GET['borrowtype']
    config_data['timelimit']  = req.GET['timelimit']
    config_data['repaytype']  = req.GET['repaytype']
    config_data['step']  = req.GET['step']
    config_data['use']  = req.GET['use']
    config_data['checkstatus']  = req.GET['checkstatus']
    config_data['user_id']  = req.GET['user_id']
    config_data['account']  = req.GET['account']
    return config_data

