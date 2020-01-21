import FingerPrinter
import sys
import os
import urllib.request
import requests


versionData = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

def getVersionURL(version):
    data = requests.get(versionData).json()
    versions = data["versions"]
    for x in versions:
        if x["id"] == version:
            return x["url"]
        
    

def DownloadJar(version,side):
    print('Downloading')
    data = requests.get(getVersionURL(version)).json()["downloads"]
    url = data[side]["url"]
    zip = urllib.request.urlopen(url).read()
    open(str(version)+"_"+side + '.jar', 'wb+').write(zip)

if __name__ == "__main__":    
    version = sys.argv[1]
    side = sys.argv[2]
    DownloadJar(version,side)
    FingerPrinter.BuildClassFilesAndHash(str(version)+"_"+side + '.jar',ignoreDirs=["commons-logging","ca","oshi-project","it","commons-io","io","org","net","com","commons-codec"],ignoreFiles=[".xsd",".xml",".dtd","der"],keepDirs=["net/minecraft","com/mojang"])
    FingerPrinter.GenerateClassFingerPrint()
    FingerPrinter.ExportFingerPrint(version+".jar")