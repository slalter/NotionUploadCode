from asyncio.windows_events import NULL
import requests
import os
import datetime
import json
import time
import flask
import bs4
from google.cloud import storage


#static list of exceptions
class eList:
    eString = ''

    @staticmethod
    def add(str):
        print(str)
        eList.eString = eList.eString + str

    @staticmethod
    def get():
        return eList.eString

    

#upload json to Notion. Returns http response. SHOULD: check to see if page already exists. If yes, archive old page and upload new one. If no, create new page.
#need to make a dictionary to connect the actual database ids in the workspace to ones that are read when making the pages as children of a main page on the backup. Any json with parent = workspace needs
#to be added to the parent directory as a new thing... and then all children need to point to the backupid of their fake parent. Abstracted, this will allow dynamic recovery options.
def jsonUpNotion(jsonfile, headers):
    f = jsonfile
    datajson = json.dumps(clean(f.read()))
    print(datajson)
    try:
        response = requests.post("https://api.notion.com/v1/databases",headers=headers, data=datajson)
        print(response.text + "code: " +response.status_code)
    except Exception as e:
        eList.add("failed to upload json "  + " due to " + e.__str__())
    try:
        return response
    except:
        eList.add("request failed.")
        return NULL

#pull only the data that we need to upload to notion
def clean(jsonFile):
    cleaned = json.loads(jsonFile)
    delCats = ['last_edited_time','rollup','created_by','created_time','last_edited_by','last_edited_time']
    for i in delCats:
        try:
            del cleaned[i]
        except:
            pass
    return cleaned


def main(request):

    #key
    #SECRET = os.environ.get('NOTION_KEY_BACKUP').__str__()
    SECRET = 'secret_dQsLC3pigquE7Q7SLZvo8evKxzxp8QLdsB4weQdvNSy'
    headers = {
    'Authorization': 'Bearer '+ SECRET,
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json',
    }
    #google stuff
    #storage_client = storage.Client()
    #bucket_name = "notionbackups"

    f = open("ee0ffb5c-dd32-4d15-8841-b965be51fd23.json", "r")
    

    jsonUpNotion(f,headers)

    print(eList.eString)
    #if(eList.eString == ''):
    #    print(flask.make_response('',200))
    #else:
    #    print(flask.make_response(eList.eString, 500))

main(NULL)