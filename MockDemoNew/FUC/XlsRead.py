# -*- coding: UTF-8 -*-
import xlrd
from collections import OrderedDict
import logging
import logging.handlers


class XlsRead():
    def __init__(self,path,bodyindex=11,long = 2,id_sign = "CASEID"):
        self.path = path
        self.bodyindex=bodyindex
        self.data = xlrd.open_workbook(path)
        self.sheets = self.data.sheet_names()
        self.long = long
        self.id_sign = id_sign
    def getAllSheetSrc(self):
        if len(self.sheets)<2:
            logging.info("Sheet number less than 2")
            return self.getSheetSrc(self.sheets[0])
        dict = {}
        logging.info("Sheet number more than 2")
        for sheet in self.sheets:
            dict[sheet] = self.getSheetSrc(sheet)
        return dict
    def getAllSheetByHeader(self):
        all_dict = {}
        for i in self.sheets:
            sheet_data = self.getSheetSrc(i)
            all_dict[i] = self.dictByHeader(sheet_data)
        return all_dict
    def getAllSheet(self):
        all_dict={}
        for i in self.sheets:
            sheet_data = self.getSheetSrc(i)
            all_dict[i]=self.dictSrcBody(sheet_data,self.dictSrcHead(sheet_data))
        return all_dict
    def getSheetSrc(self,sheetname):
        table = self.data.sheet_by_name(sheetname)
        nrows = table.nrows
        ncols = table.ncols
        sheet_data = []
        for nrow in xrange(nrows):
            sheet_data.append(table.row_values(nrow))
        return sheet_data
    def dictSrcHead(self,sheet_data):
        dict={}
        dict["url"] = sheet_data[0][2]+sheet_data[0][0]
        dict["name"] = sheet_data[0][1]
        dict["method"] = sheet_data[1][0]
        dict["Chinese notes"] = sheet_data[1][1]
        dict["parms_num"] = sheet_data[2][0]
        return dict
    def dictByHeader(self,sheet_data,header_long=2):
        header_dict = self.dictHeader(sheet_data,long=self.long)
        all_dict = self.dictBody(sheet_data,header_dict,long=self.long,id_sign=self.id_sign)
        # all_dict = {"header":header_dict,"body":body_dict}
        return all_dict
    def dictBody(self,sheet_data,header_dict,id_sign,long=2):
        body_dict = OrderedDict({})
        body_data = sheet_data[long:]
        header = body_data[0]
        for index,data in enumerate(body_data[1:]):
            solo_dict = OrderedDict(zip(header,data))
            solo_dict = OrderedDict(header_dict,**solo_dict)
            body_dict[solo_dict[id_sign]] = solo_dict
        return body_dict
    def dictHeader(self,sheet_data,long=2):
        header_dict = OrderedDict({})
        header_data = sheet_data[:long]
        for row in range(0,long,2):
            for index in range(len(header_data[row])):
                if "" != header_data[row][index]:
                    header_dict[header_data[row][index]] = header_data[row+1][index]
        return header_dict
    def dictSrcBody(self,sheet_data,dict):
        parms=sheet_data[3:self.bodyindex]
        parms = map(list,zip(*parms))#行列互换
        dict["parms"]=parms
        return dict
    def listSrcData(self,sheet_data):
        src_data=sheet_data[self.bodyindex:]
        return src_data