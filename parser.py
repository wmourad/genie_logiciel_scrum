import os
import shutil
import re
import glob
import sys
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
from io import BytesIO


def getDirConvert():
    directory = "converted_pdf_pdftotext"
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
    return "converted_pdf_pdftotext"


# convertie tout les pdf existant dans un dossier dans un nouveau dossier
def convertAll(pdfDir,convertionDir):
    l = os.listdir(pdfDir)
    for pdf in l:
        if pdf.endswith('.pdf'):
            os.system("pdftotext -enc UTF-8 -y 60 -H 640 -W 1000 -nopgbrk -layout -raw -eol unix '" +os.path.join(pdfDir, pdf)+"' '"+os.path.join(convertionDir, os.path.splitext(pdf)[0]+".txt'"))
        

def parseText(parsedDir,convertionDir):
    l=os.listdir(parsedDir)
    for fichier in l:
        with open(os.path.join(parsedDir,fichier),"w") as f:
            data = getData(fichier,convertionDir)
            f.write("file name      : "+getFileName(fichier))
            
            f.write("\ndocument title : "+getTitle(data))
            
            f.write("\nauteur         : "+getAuthor(data))
            
            f.write("\nabstract       : "+getAbstract(data))
            
            f.write("\nintroduction   : "+getIntro(data))

            f.write("\ncorps   : "+getCorps(data))
            
            f.write("\nbiblio         : "+getBiblio(data))
            
            


def parseXml(parsedDir,convertionDir):
    l=os.listdir(parsedDir)
    for fichier in l:
        with open(os.path.join(parsedDir,fichier),"wb") as f:
            data = getData(fichier,convertionDir)
           
            root = ET.Element('article')

            name = ET.SubElement(root,'preamble')
            name.text=getFileName(fichier)

            title = ET.SubElement(root,'titre')
            title.text = getTitle(data)
            
            auteur = ET.SubElement(root,'auteur')

            abstract = ET.SubElement(root,'abstract')
            abstract.text = getAbstract(data)

            introduction = ET.SubElement(root,'introduction')
            introduction.text = getIntro(data)
            
            biblio = ET.SubElement(root,'biblio')
            biblio.text=getBiblio(data)

            et = ET.ElementTree(root)
            tmp= BytesIO()
            et.write(tmp, encoding='utf-8', xml_declaration=True) 
            tree = ET.tostring(root)
            f.write(tmp.getvalue())

#get tout le text du fichier
def getData(textFile,convertionDir):
    with open(os.path.join(convertionDir,os.path.splitext(textFile)[0]+".txt"),"r") as f:
        data=f.readlines()
    return data

#get le nom du fichier pdf
def getFileName(pdf):
    return os.path.splitext(pdf)[0]+".pdf"


#get title of the document
def getTitle(data):
    text= data[0]+data[1]
    return re.sub('\n'," ",text)


#get authors of the paper
def getName(data):
    pattern = re.compile(r'[A-Z][a-zA-Z]+[\s-][A-Z][a-zA-Z]+\s[A-Z][a-zA-Z]+[\s-][A-Z][a-zA-Z]+')
    text=""
    cpt=0
    for line in data:
        text = text+re.sub('\n'," ",line)
        cpt+=1
        if cpt == 10:
            break
    text2 = re.findall(pattern,text)
    if  text2:
        print (text2)
        #for matche in text2:
            #print(matche)
    
    else:
        return "pas d'auteur trouver"

#get abstract of the paper
def getAbstract(data):
    pattern = re.compile(r'([Aa]\s?b\s?s\s?t\s?r\s?a\s?c\s?t|A\s?B\s?S\s?T\s?R\s?A\s?C\s?T)\.?\-?\s?(.*?)1\.?-?\s?(I\s?n\s?t\s?r\s?o\s?d\s?u\s?c\s?t\s?i\s?o\s?n|I\s?N\s?T\s?R\s?O\s?D\s?U\s?C\s?T\s?I\s?O\s?N)?') #[1|I.]\
    text=""
    for line in data:
        text = text+re.sub('\n'," ",line)
        
    text2= re.search(pattern,text)
    
    if  text2 != None:
        if text2.group(1) != None:
            return text2.group(2)
    return "pas d'abstract trouver"


def getAuthor(data):
    text=""
    i=2
    while i<=15 :
        text=text+data[i]
        i+=1
    return re.sub('\n'," ",text)

#get biblio of the paper
def getBiblio(data):
    #pattern = re.compile(r'([Rr]eferences?|REFERENCES?)(.*)')
    text=""
    for line in data:
        text = text+re.sub('\n'," ",line)
    
    text=text.lower()

    textS=text.rsplit("references",1)
    if len(textS)== 2:
        return textS[1]
    return "pas de bilio trouver"

def getIntro(data):
    text=""
    pattern = re.compile(r'^1?\.?\s?(introduction)\s?:?',re.IGNORECASE)
    patternBis= re.compile(r'^2\.?\s[A-Z]')    
    stop=False 
    for line in data:
        if re.match(pattern,line) :
            stop=True
        elif re.match(patternBis,line):
            if " ." not in line:
                return text    
        elif stop:
            text = text+re.sub('\n'," ",line)           
    return "pas d'introduction"    



def getCorps(data):
    text=""
    pattern = re.compile(r'(^(II|2)\.?\s)[A-Z].*')
    patternBis = re.compile(r'^[A-Z]?\d{0,2}\.?\d?\s?(Conclusions?|results?|Discussion?|summary):?\s?(\b\s)*$',re.IGNORECASE)  
    stop=False 
    for line in data:
        if re.match(pattern,line) :
            text = text+re.sub('\n'," ",line)
            stop=True
        elif re.match(patternBis,line):
            if " ." not in line:
                return text    
        elif stop:
            text = text+re.sub('\n'," ",line)           
    return "pas de corps"    


def getConclusion(data):
    return null

def getDisc(data):
    return null




    


def dirParse(command,convertionDir):
    #create directory où pn vas parser
    directory = "parsed_files"
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
    #list files in dir
    files=os.listdir(convertionDir)
    for f in files:
        #create files txt/xml
        if command == "xml":
            f=open(os.path.join(directory,os.path.splitext(f)[0]+".xml"),"x")
            
        elif command == "text":
            f=open(os.path.join(directory,f),"x")
        f.close()
    return directory


# recupere la commande passer par l'utilisateur
def getCommand():
    if sys.argv[2] == "-t":
        return "text"
    elif sys.argv[2] == "-x":
        return "xml"
    else:
        sys.exit(
            "\n### Commande incorrect !! ###\n -t | pour convertion en texte.\n -x | pour convertion en xml.\n")


# recupere le dossier a convertir
def getTargetDir():
    exist = os.path.exists(sys.argv[1])
    if exist == False:
        sys.exit("\n### Le dossier n'existe pas! ###\n")
    else:
        return sys.argv[1]


def main():
    pdfDir = ""
    lenSys = len(sys.argv)
    command = "text"
    if lenSys == 2:
        pdfDir = getTargetDir()
    elif lenSys == 3:
        pdfDir = getTargetDir()
        command = getCommand()
    else:
        sys.exit(
            "\n### Le programme attend un dossier existant a convertir +[optionnel](commande de convetion) ###\n")
    convertionDir = getDirConvert()
    convertAll(pdfDir,convertionDir)
    parsedDir = dirParse(command,convertionDir)
    if command == "text":
        parseText(parsedDir,convertionDir)
    elif command == "xml" :
        parseXml(parsedDir,convertionDir)


# lance le programme
if __name__ == '__main__':
    main()






