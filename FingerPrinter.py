# coding: utf-8
import shutil
import zipfile
from jawa.cf import ClassFile
import hashlib
import jawa
import json
import os
import sys
from tqdm import tqdm


ClassFiles = {}
Hashes = {}
FingerPrint = {}
FingerPrint["other"] = {}


  
def BuildClassFilesAndHash(jarfile,ignoreDirs = [],ignoreFiles = [],keepDirs=[]):
    print('Building ClassFiles')
    zip = zipfile.ZipFile(jarfile)
    files = []
    for name in zip.namelist():
        isokay = True
        for x in ignoreDirs:
            if name.startswith(x):
                for y in keepDirs:
                    if not name.startswith(y):
                        isokay = False
                        break
        for x in ignoreFiles:
            if name.endswith(x):
                isokay = False
                break
        if isokay == True:
            files.append(name)
    for name in tqdm(files):
        if name.endswith('.class'):
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
    print('Profiling Strings and Numbers')
    for key in tqdm(ClassFiles.keys()):
        FingerPrint["class"][key] = {}
        # Get all string constants
        FingerPrint["class"][key]["constants"] ={}
        FingerPrint["class"][key]["constants"]["classes"] = []
        FingerPrint["class"][key]["constants"]['strings'] = []
        FingerPrint["class"][key]["constants"]['numbers'] = []
        FingerPrint["class"][key]["access_flags"] = ClassFiles[key].access_flags.value
        for x in ClassFiles[key].constants.find(type_=jawa.constants.String):
            FingerPrint["class"][key]["constants"]['strings'].append(x.string.value)
        # Get all number constants        
        for x in ClassFiles[key].constants.find(type_=jawa.constants.Number):
            FingerPrint["class"][key]["constants"]['numbers'].append(str(x.value))
        #Get Classes in constant poll
        for x in  ClassFiles[key].constants.find(type_=jawa.constants.ConstantClass):
            if not x.name.value == key:
                FingerPrint["class"][key]["constants"]["classes"].append(str(x.name.value))
        # Get the super class        
        FingerPrint["class"][key]['super'] = ClassFiles[key].super_.name.value
        # Get all interfaces
        for x in ClassFiles[key].interfaces:
            if('interfaces' in FingerPrint["class"][key].keys()):
                FingerPrint["class"][key]['interfaces'].append(x.name.value)
            else:
                FingerPrint["class"][key]['interfaces'] = []
                FingerPrint["class"][key]['interfaces'].append(x.name.value)
        #Get all field data
        for x in ClassFiles[key].fields:
            if('fields' in FingerPrint["class"][key].keys()):
                FingerPrint["class"][key]['fields'].append((x.name.value,x.descriptor.value,x.access_flags.value))
            else:
                FingerPrint["class"][key]['fields'] = []
                FingerPrint["class"][key]['fields'].append((x.name.value,x.descriptor.value,x.access_flags.value))
        
        #Get all method data
        for x in ClassFiles[key].methods:
            if('methods' in FingerPrint["class"][key].keys()):
                FingerPrint["class"][key]['methods'].append((x.name.value,x.descriptor.value,x.access_flags.value))
            else:
                FingerPrint["class"][key]['methods'] = []
                FingerPrint["class"][key]['methods'].append((x.name.value,x.descriptor.value,x.access_flags.value))
        
        FingerPrint["class"][key]['hash'] = Hashes[key]

        
def ExportFingerPrint(jarfile):
    print('Exporting Profile')
    out = json.dumps(FingerPrint)
    open(jarfile.replace(".jar","")+".json",'w+').write(out)

    
    

if __name__ == "__main__":
    BuildClassFilesAndHash(sys.argv[1])
    GenerateClassFingerPrint()
    ExportFingerPrint(sys.argv[1])
