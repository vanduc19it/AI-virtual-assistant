import json 

import handleData
import constants

url_user  = constants.URL_File + "ahihi.json"


def addUserName(username):
    handleData.addData({"username": username }, url_user)

def addPass(passw):
    handleData.addData({"pass": passw }, url_user)

def getInfor():
    return handleData.getData(url_user)