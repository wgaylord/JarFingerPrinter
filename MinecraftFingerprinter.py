import FingerPrinter
import sys
import os
import urllib


MCUrl = """https://s3.amazonaws.com/Minecraft.Download/versions/<version>/<version>.jar"""

def DownloadJar(version):
    print 'Downloading'
    realUrl = MCUrl.replace('<version>', version)
    zip = urllib.urlopen(realUrl).read()
    open(str(version) + '.jar', 'wb+').write(zip)

if __name__ == "__main__":    
    version = sys.argv[1]
    DownloadJar(version)
    FingerPrinter.BuildClassFilesAndHash(version+".jar",ignoreDirs=["io","assets","com","it","org","javax","META-INF"],ignoreFiles=[".xsd",".xml",".dtd","der"])
    FingerPrinter.GenerateClassFingerPrint()
    FingerPrinter.ExportFingerPrint(version+".jar")