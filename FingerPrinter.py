# coding: utf-8
import shutil
import zipfile
from jawa import ClassFile
import hashlib
import jawa
import json
import os
import sys


FingerPrintPath = '/web/www/minecraft'

ClassFiles = {}
Hashes = {}
FingerPrint = {}
FingerPrint["other"] = {}


  
def BuildClassFilesAndHash(jarfile,ignoreDirs = [],ignoreFiles = []):
    print 'Building ClassFiles'
    zip = zipfile.ZipFile(jarfile)
    #print zip.namelist()
    files = []
    for name in zip.namelist():
        isokay = True
        for x in ignoreDirs:
            #print name.startswith(x)
            if name.startswith(x):
                isokay = False
                break
        for x in ignoreFiles:
            if name.endswith(x):
                isokay = False
                break
        if isokay == True:
            files.append(name)
    for name in files:
        if name.endswith('.class'):
            #print name
            hasher = hashlib.md5()
            t = zip.open(name)
            temp = ClassFile(t)
            ClassFiles[name.replace(".class","")]=temp
            t = zip.open(name)
            hasher.update(t.read())
            Hashes[name.replace(".class","")]=hasher.hexdigest()
            t.close()
        elif not name.endswith("/"):
            t = zip.open(name)
            hasher = hashlib.md5()
            hasher.update(t.read())
            FingerPrint["other"][name] = hasher.hexdigest()


def GenerateClassFingerPrint():
    global FingerPrint
    FingerPrint["class"] = {}
    print 'Profiling Strings and Numbers'
    for key in ClassFiles.keys():
        FingerPrint["class"][key] = {}
        # Get all string constants
        FingerPrint["class"][key]["constants"] ={}
        FingerPrint["class"][key]["constants"]['string'] = []
        FingerPrint["class"][key]["constants"]['number'] = []
        FingerPrint["class"][key]["access_flags"] = ClassFiles[key].access_flags.value
        for x in ClassFiles[key].constants.find(type_=jawa.constants.ConstantString):
            FingerPrint["class"][key]["constants"]['string'].append(x.string.value)
        # Get all number constants        
        for x in ClassFiles[key].constants.find(type_=jawa.constants.ConstantNumber):
            FingerPrint["class"][key]["constants"]['number'].append(str(x.value))

        # Get the super class        
        FingerPrint["class"][key]['super'] = ClassFiles[key].super_.name.value
        # Get all interfaces
        for x in ClassFiles[key].interfaces:
            if(FingerPrint["class"][key].has_key('interfaces')):
                FingerPrint["class"][key]['interfaces'].append(ClassFiles[key].constants[x].name.value)
            else:
                FingerPrint["class"][key]['interfaces'] = []
                FingerPrint["class"][key]['interfaces'].append(ClassFiles[key].constants[x].name.value)
        #Get all field data
        for x in ClassFiles[key].fields:
            if(FingerPrint["class"][key].has_key('fields')):
                FingerPrint["class"][key]['fields'].append((x.name.value,x.descriptor.value,x.access_flags.value))
            else:
                FingerPrint["class"][key]['fields'] = []
                FingerPrint["class"][key]['fields'].append((x.name.value,x.descriptor.value,x.access_flags.value))
        
        #Get all method data
        for x in ClassFiles[key].methods:
            if(FingerPrint["class"][key].has_key('methods')):
                FingerPrint["class"][key]['methods'].append((x.name.value,x.descriptor.value,x.access_flags.value))
            else:
                FingerPrint["class"][key]['methods'] = []
                FingerPrint["class"][key]['methods'].append((x.name.value,x.descriptor.value,x.access_flags.value))
        
        FingerPrint["class"][key]['hash'] = Hashes[key]

        
def ExportFingerPrint(jarfile):
    print 'Exporting Profile'
    out = json.dumps(FingerPrint,indent=1)
    open(jarfile.replace(".jar","")+".json",'w+').write(out)

    
    

if __name__ == "__main__":
    BuildClassFilesAndHash(sys.argv[1])
    GenerateClassFingerPrint()
    ExportFingerPrint(sys.argv[1])
