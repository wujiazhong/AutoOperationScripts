'''
Created on Dec 25, 2015

@author: wujz
@version: 1.0
'''
import urllib.request,json,traceback,os
from GithubOperation import operation

# --- params
OWNER = 'ibmpredictiveanalytics'
TOKEN = ''
RELEASE_URL = r'https://api.github.com/repos/{0}/{1}/releases'
LATEST_RELEASE_INFO_URL = r'https://api.github.com/repos/{0}/{1}/releases/latest'
TAR_RELEASE_URL = r"https://api.github.com/repos/{0}/{1}/releases/{2}"
UPLOAD_URL = r"https://uploads.github.com/repos/{0}/{1}/releases/{2}/assets?name={3}"

class releaseInfoObj:
    def __init__(self, owner, repo_name):
        try: 
            self.owner = owner
            self.repo = repo_name
            self.release_json_info = json.loads(sendRequest(OWNER, self.repo,RELEASE_URL.format(self.owner, self.repo)))
            self.latest_release_json_info = json.loads(sendRequest(OWNER, self.repo,LATEST_RELEASE_INFO_URL.format(self.owner, self.repo)))
        except Exception as e:
            raise e
    
    def getLatestReleaseID(self): 
        return self.latest_release_json_info['id']   
    
    def getLatestTagName(self): 
        return self.latest_release_json_info['tag_name']     
  
def sendRequest(owner, repo_name, url, method='GET', data=None, headers={}):  
    try:
        if data!=None:
            data = data.encode('utf-8')
        request = urllib.request.Request(url, data)
        request.method = method
        request.add_header("Authorization", "token "+TOKEN)
        for key in headers.keys():
            request.add_header(key, headers[key])
            
        response = urllib.request.urlopen(request,timeout=20)
        
        feedback_info = None 
        if str.upper(method)=='GET':
            if 200 <= response.status < 300:
                print("GET info successfully!")
                feedback_info = response.read().decode('utf-8')
            else:
                raise Exception("Cannot get release information from api.github.com!")
        elif str.upper(method)=='POST':
            if 200 <= response.status < 300:
                print(response.status)
                print("POST info successfully!")
            else:
                raise Exception("Cannot get post data to api.github.com!")  
        elif str.upper(method) == 'DELETE': 
            if 200 <= response.status < 300: 
                print("request is done!")
                print(response.status)
            else:
                raise Exception("request to api.github.com failed!")  
        else:
            print("Wrong method!")
    except Exception as e:
        raise e
    return feedback_info

def createRelease(owner, repo_name,tag_name, release_name, release_note, branch_name="master"):
    tar_url = RELEASE_URL.format(owner,repo_name)
    try:
        data=json.dumps(dict({"tag_name": tag_name,"target_commitish":branch_name,\
                              "name": release_name,"body": release_note}))
        if sendRequest(owner, repo_name, tar_url, 'POST', data)==None:
            return True
    except Exception as e:
        raise e

def uploadAssets(owner, repo_name, release_id, file_path, headers):
    tar_url = UPLOAD_URL.format(owner,repo_name,release_id,os.path.basename(file_path))
    try:
        if sendRequest(owner, repo_name, tar_url, 'POST',file_path, headers)==None:
            return True
    except Exception as e:
        raise e
    

def delRelease(owner, repo_name, release_id):
    tar_url = TAR_RELEASE_URL.format(owner, repo_name,release_id)
    try:
        if sendRequest(owner, repo_name, tar_url, method='DELETE')==None:
            return True
    except Exception as e:
        raise e
            
if __name__ == '__main__':
    try: 
        path = r'C:\Users\wujz\Desktop'
        repo_name = 'test_Stats_Release'
        obj2 = releaseInfoObj(OWNER, 'test_Stats_Release') 
        print(obj2.getLatestReleaseID())
        print(obj2.getLatestTagName())
        print(json.dumps(obj2.release_json_info))
        delRelease(OWNER, repo_name,obj2.getLatestReleaseID())
        print("start to clone repo")
        operation.cloneRepo(path,OWNER,repo_name)
        print("start to del repo")
        operation.delRemoteTag(os.path.join(path,repo_name), obj2.getLatestTagName())
        
        if createRelease(OWNER, 'test_Stats_Release', '1.1.5', 'test_Stats_Release_1.1.5', 'it is a test'):
            obj2 = releaseInfoObj(OWNER, 'test_Stats_Release') 
            latest_release_id = obj2.getLatestReleaseID()
            uploadAssets(OWNER, 'test_Stats_Release',str(latest_release_id),r'C:\Users\wujz\Desktop\test.zip', dict({"Content-Type":"application/zip"}))

    except Exception as e:
        print(str(traceback.format_exc()))