# coding: utf-8
import urllib
import shutil
import zipfile
from jawa import ClassFile
import hashlib
import jawa
import json
import os
import sys

MCUrl = """https://s3.amazonaws.com/Minecraft.Download/versions/<version>/<version>.jar"""

FingerPrintPath = '/web/www/minecraft'

ClassFiles = {}
Hashes = {}
FingerPrint = {}


def DownloadJar(version):
    print 'Downloading'
    realUrl = MCUrl.replace('<version>', version)
    zip = urllib.urlopen(realUrl).read()
    open(os.getcwd() + '/jars/' + str(version) + '.jar', 'wb+').write(zip)


def ExtractJar(version):
    print 'Extracting'
    zipfile.ZipFile(os.getcwd()+'/jars/'+str(version)+'.jar').extractall(os.getcwd()+'/class_files/'+version)
    shutil.rmtree(os.getcwd()+'/class_files/'+version+'/assets',ignore_errors=True)
    shutil.rmtree(os.getcwd()+'/class_files/'+version+'/META-INF',ignore_errors=True)
    for root, dirs, files in os.walk("./class_files/"+version, topdown=False):
        for name in files:
            if not name.endswith('.class'):
                os.remove(root+'/'+name)

  
def BuildClassFiles(version):
    print 'Building ClassFiles'
    for root, dirs, files in os.walk("./class_files/"+version, topdown=False):
        for name in files:
            if name.endswith('.class'):
                hasher = hashlib.md5()
                t = open(os.path.join(root,name),'rb')
                temp = ClassFile(t)
                ClassFiles[temp.this.name.value]=temp
                t.seek(0)
                hasher.update(t.read())
                Hashes[temp.this.name.value]=hasher.hexdigest()
                t.close()


def GenerateFingerPrint():
    global FingerPrint
    print 'Profiling Strings and Numbers'
    for key in ClassFiles.keys():
        FingerPrint[key] = {}
        # Get all string constants
        FingerPrint[key]["constants"] ={}
        FingerPrint[key]["access_flags"] = ClassFiles[key].access_flags.flags
        for x in ClassFiles[key].constants.find(type_=jawa.constants.ConstantString):
            if(FingerPrint[key].has_key('string')):
                FingerPrint[key]["constants"]['string'].append(x.string.value)
            else:
                FingerPrint[key]["constants"]['string'] = []
                FingerPrint[key]["constants"]['string'].append(x.string.value)
        # Get all number constants        
        for x in ClassFiles[key].constants.find(type_=jawa.constants.ConstantNumber):
            if(FingerPrint[key].has_key('number')):
                FingerPrint[key]["constants"]['number'].append(str(x.value))
            else:
                FingerPrint[key]["constants"]['number'] = []
                FingerPrint[key]["constants"]['number'].append(str(x.value))
        # Get the super class        
        FingerPrint[key]['super'] = ClassFiles[key].super_.name.value
        # Get all interfaces
        for x in ClassFiles[key].interfaces:
            if(FingerPrint[key].has_key('interfaces')):
                FingerPrint[key]['interfaces'].append(ClassFiles[key].constants[x].name.value)
            else:
                FingerPrint[key]['interfaces'] = []
                FingerPrint[key]['interfaces'].append(ClassFiles[key].constants[x].name.value)
        #Get all field data
        for x in ClassFiles[key].fields:
            if(FingerPrint[key].has_key('fields')):
                FingerPrint[key]['fields'].append((x.name.value,x.descriptor.value,x.access_flags.value))
            else:
                FingerPrint[key]['fields'] = []
                FingerPrint[key]['fields'].append((x.name.value,x.descriptor.value,x.access_flags.value))
        
        #Get all method data
        for x in ClassFiles[key].methods:
            if(FingerPrint[key].has_key('methods')):
                FingerPrint[key]['methods'].append((x.name.value,x.descriptor.value,x.access_flags.value))
            else:
                FingerPrint[key]['methods'] = []
                FingerPrint[key]['methods'].append((x.name.value,x.descriptor.value,x.access_flags.value))
        
        FingerPrint[key]['hash'] = Hashes[key]

        
def ExportFingerPrint(version):
    print 'Exporting Profile'
    out = json.dumps(FingerPrint)
    open(FingerPrintPath+'/jar_fingerprints/'+version+'.json','w+').write(out)

    
def Cleanup(version):
    print 'Cleaning up'
    shutil.rmtree(os.getcwd()+'/class_files/'+version,ignore_errors=True)
    os.remove(os.getcwd()+'/jars/'+version+'.jar')
    

if __name__ == "__main__":
    version = sys.argv[1]
    DownloadJar(version)
    ExtractJar(version)
    BuildClassFiles(version)
    GenerateFingerPrint()
    ExportFingerPrint(version)
    Cleanup(version)
