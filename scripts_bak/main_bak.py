'''
Created on Dec 22, 2015

@author: wujz
'''
import zipfile,os,json,re,time
GITBASH = r"C:\Git\bin\sh.exe --login -i"
CLONEREPO_SH = r"./scripts/clone_repo.sh"
UPLOAD_FILES_SH=r"./scripts/upload_files.sh"
GET_RELEASE_INFO_SH=r"./scripts/get_release_info.sh"
CREATE_RELEASE_SH = r"./scripts/create_release.sh"
#RELEASE_MSG =r"\"min stats version: 18\""
RELEASE_MSG = "\"min modeler version: 18\""
RELEASE_NAME = r'{0}_{1}'

def zip_dir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
         
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        zf.write(tar,arcname)
    zf.close()

def cloneRepo():
    save_folder = r"C:\Users\wujz\Desktop"
    os.system(GITBASH+" "+CLONEREPO_SH+" "+save_folder+" ibmpredictiveanalytics"+" test_Stats_Release")

def createRelease(tar_zip, tag_index, ext_name):
    # create tag and release
    try:
        create_response = os.popen(GITBASH+" "+CREATE_RELEASE_SH+" "+tag_index+" "+RELEASE_NAME.format(ext_name,tag_index)+" "+RELEASE_MSG+" "+ext_name)
        time.sleep(5)
        print(create_response.read())
        
        # get release id
        
        reponse = os.popen(GITBASH+" "+GET_RELEASE_INFO_SH+" "+tag_index+ " "+ext_name)
        feedback = reponse.read()
        print(feedback)

        pat = re.compile(r'\n\n(\{.*\})', re.S)
        info = json.loads(re.findall(pat, feedback)[0])
        #file_name=ext_name+'.spe'
        file_name=ext_name+'.mpe'
        
        # upload asset
        os.system(GITBASH+" "+UPLOAD_FILES_SH+" "+tar_zip+" "+str(info["id"])+" "+file_name+" "+ext_name)
    except Exception as e:
        raise e

    #src_folder = r"C:\Users\wujz\Desktop\test_Stats_Release\src"
    #tar_zip = r"C:\Users\wujz\Desktop\test_Stats_Release.spe"
    #mf_file = r"C:\Users\wujz\Desktop\test_Stats_Release\src\META-INF\MANIFEST.MF"
    #fp = open(mf_file,'r')
    #version = ""
    #for line in fp.readlines():
    #    if ":" in line and line.split(":")[0]=="Version":
    #        version = line.split(":")[1].strip(' ').strip('\n')
    #        break
    #zip_dir(src_folder,tar_zip)
    #createRelease(tar_zip, version)

def calcVersion(mf_file):
    fp = open(mf_file,'r')
    version = ""
    for line in fp.readlines():
        if ":" in line and line.split(":")[0]=="Version":
            version = line.split(":")[1].strip(' ').strip('\n')
            break 
    return version  

if __name__ == '__main__':    
    src_folder = r"C:\Users\wujz\Desktop\modeler_ext"
    ext_stats_list = os.listdir(src_folder)
    print("total number:"+str(len(ext_stats_list)))
    #MF_FILE = r"C:\Users\wujz\Desktop\stats_repackage\{0}\ext\spe\META-INF\MANIFEST.MF"
    log = open(r"C:\Users\wujz\Desktop\logext",'w')
    logstr=""
    try:
        for ext in ext_stats_list:
            if ext.split('.')[0] == 'Cloudant' or ext.split('.')[0]=='Get_Coordinates_Esri':
                continue
            logstr+=ext+'\n'
            ext_name = ext.split('.')[0]
            #src_file = os.path.join(*([src_folder, ext , ext+'.spe']))
            src_file = os.path.join(*([src_folder, ext]))
            #mf_file = MF_FILE.format(ext)
            #tag_version = calcVersion(mf_file)
            tag_version = '1.0.0'
            print(ext+": "+tag_version)
            #createRelease(src_file, tag_version, ext_name)
            print(src_file)
    except Exception as e:
        print(str(e))
    finally:
        log.write(logstr)
        log.close()
        
        