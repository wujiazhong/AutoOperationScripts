'''
Created on Dec 28, 2015

@author: wujz
'''
from GithubOperation.release import createRelease,releaseInfoObj,uploadAssets,OWNER
from optparse import OptionParser
import os,json

def calcVersion(mf_file):
    fp = open(mf_file,'r')
    version = ""
    for line in fp.readlines():
        if ":" in line and line.split(":")[0]=="Version":
            version = line.split(":")[1].strip(' ').strip('\n')
            break 
    return version  

def getExtInfoList(ext_file):
    if not os.path.isfile(ext_file):
        print("Cannot find index file")
        exit(1)
    fp = open(ext_file,'r')
    ext_info_list = json.loads(fp.read())["extension_index"]
    return ext_info_list

if __name__ == '__main__':  
    usage = "usage: %prog [options] arg1 arg2"  
    parser = OptionParser(usage)  
    parser.add_option("-o", "--outdir", dest="outdir", action='store', help="Directory to work")
    parser.add_option("-p", "--product", dest="productName", action='store', help="Choose license index for which product: 1. modeler 2. stats.")
    (options, args) = parser.parse_args() 
    
    # --- check params
    productName = options.productName.lower()
    tail = ''
    if productName == 'modeler':
        tail = '.mpe'
    elif productName == 'stats':
        tail = '.spe'
    else:  
        parser.error(productName+" is not a legal parameter. "+"Please input valid product name 'modeler' or 'stats' for your index file")
        
    workdir = options.outdir
    if os.path.isdir(workdir):
        parser.error(workdir+" does not exist!")
    
    # start
    ext_package_file = ''
    ext_file = ''
    ext_list = getExtInfoList(ext_file)
    for item in ext_list:
        repo_name = item["repository"]
        version = item["extension_detail_info"]["Version"]
        min_pro_version = item["extension_detail_info"]["Product-Version"]
        if createRelease(OWNER, repo_name, version, item["repository"]+'_'+version, "min "+productName+" version: "+min_pro_version):
            obj2 = releaseInfoObj(OWNER, repo_name) 
            latest_release_id = obj2.getLatestReleaseID()
            uploadAssets(OWNER, repo_name,str(latest_release_id),ext_package_file, dict({"Content-Type":"application/zip"}))
            