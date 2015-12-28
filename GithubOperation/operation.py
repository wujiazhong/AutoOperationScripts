'''
Created on Dec 26, 2015

@author: wujz
'''
import os,time
OWNER = 'ibmpredictiveanalytics'
CLONE_REPO_SH = r'./clone_repo.sh'
DELETE_REPO_TAG_SH = r'./delete_repo_tag.sh'
GITBASH = r"C:\Git\bin\sh.exe --login -i"

def cloneRepo(save_folder,owner, repo_name):
    try:
        res = os.system(GITBASH+" "+CLONE_REPO_SH+" "+save_folder+" "+owner+" "+repo_name)
        time.sleep(5)
        if res==0:
            print("Get "+repo_name+" successfully!")
        else:
            print("Fail to get "+repo_name)
            
    except Exception as e:
        raise e

def delRemoteTag(repo_folder, tag_name, branch_name='master'):
    if not os.path.isdir(repo_folder) or not os.path.isdir(os.path.join(repo_folder, '.git')):
        print(repo_folder+" is not a Git repository!")
        exit(1)
    
    try:
        res = os.system(GITBASH+" "+DELETE_REPO_TAG_SH+" "+repo_folder+" "+tag_name+" "+branch_name)
        time.sleep(5)
        if res==0:
            print("Delete tag "+tag_name+" in "+repo_folder+" successfully!")
        else:
            print("Fail to delete "+tag_name+" in "+repo_folder)
            
    except Exception as e:
        raise e

if __name__=='__main__':
    cloneRepo(r'C:\Users\wujz\Desktop','ibmpredictiveanalytics','test_Stats_Release')
    delRemoteTag(r'C:\Users\wujz\Desktop\test_Stats_Release', '1.1.1')