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
    dataDict = clean(f.read()) #cleaned returns a dictonary
    try:
        response = requests.post("https://api.notion.com/v1/pages",headers=headers, data=json.dumps(dataDict))
        print(response.text + "code: " + response.status_code.__str__())
    except Exception as e:
        eList.add("failed to upload json "  + " due to " +  e.__str__())
    try:
        return response
    except:
        eList.add("request failed.")
        return flask.make_response("http request failed ", 532)

#delete data that cannot be uploaded
def clean(jsonFile):
    #delete data that cannot be uploaded
    cleaned = json.loads(jsonFile)
    delCats = ['last_edited_time','rollup','created_by','created_time','last_edited_by','last_edited_time']
    for i in delCats:
        try:
            del cleaned[i]
        except:
            pass
    
    #if parent is workspace, make parent the BACKUPS page
    if(cleaned["parent"].__str__()=="{'type': 'workspace', 'workspace': True}"):
        cleaned["parent"] = {"page_id": "f33994e861a14f6fae8cee8cb6b15bdf"}
        print("parent changed from workspace to BACKUPS.")

    #set icon to smiley face becuase dynamically loaded ones aren't supported here
    cleaned["icon"]={"emoji": "😀"}

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


    #path to backup jsons
    backuppath = os.path.join(os.getcwd(), "backuptest/")

    #dynamic nextFolders list containing paths to folders
    nextFolders = [backuppath]

    #upload all jsons layer by layer
    while(len(nextFolders)!=0):
        for filename in os.listdir(nextFolders[0]):
            if(os.path.isfile(os.path.join(backuppath, filename))):
                try:
                    f = open(os.path.join(backuppath, filename),"r")
                    if(jsonUpNotion(f, headers).status_code != 200):
                        eList.add("failed to upload file: " + filename)
                except Exception as e:
                    eList.add("exception uploading file " + filename + e.__str__())
                try:
                    f.close()
                except:
                    pass
            else:
                nextFolders.append(os.path.join(backuppath, filename))
            nextFolders.remove(nextFolders[0])

    
    


    print(eList.eString)
    #if(eList.eString == ''):
    #    print(flask.make_response('',200))
    #else:
    #    print(flask.make_response(eList.eString, 500))

main(NULL)