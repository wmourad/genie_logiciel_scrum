import os
import shutil
import re
import pdftotext
import glob



def getFileName(pdfDir ,targetDir):
	l=os.listdir(pdfDir)
	for pdf in l:
		line1=pdf
		pdf = os.path.splitext(pdf)[0]
		file = open(targetDir+"/"+pdf+".txt",'w')
		file.write(line1+"\n")
		print (pdf)
		file.close()


def convertAll(pdfDir,convertedDir):
	l=os.listdir(pdfDir)
	for pdf in l:
		os.system("pdftotext -nopgbrk -raw "+pdfDir+"/"+pdf)
		shutil.move(pdfDir+"/"+os.path.splitext(pdf)[0]+".txt",convertedDir)
		#file=open(pdfDir+"/"+pdf,"rb")
		#pdf=pdftotext.PDF(convertedDir+"/"+file)


def getTitle(targetDir,convertedDir):
	l=os.listdir(convertedDir)
	for txt in l :
		tmp=open(convertedDir+"/"+txt)
		title=tmp.readline().rstrip("\n")
		#print(title)
		file_target=open(targetDir+"/"+txt,"a")
		file_target.write(title+"\n")
		file_target.close()

def getAbstract(targetDir,convertedDir):
	l=os.listdir(convertedDir)
	for txt in l :
		tmp=open(convertedDir+"/"+txt)
		abstract=tmp.read()
		btw="abstract(.*?)introduction"
		abstract=re.search(btw,abstract)#.group(1)
		print(abstract)
		#file_target=open(targetDir+"/"+txt,"a")
		#file_target.write(title+"\n")
		#file_target.close()
		exit(1)




def main():
	targetDir = 'parsed_files'
	if os.path.exists(targetDir):
	    shutil.rmtree(targetDir)
	os.makedirs(targetDir)
	pdfDir = 'CORPUS_APPRENTISSAGE'
	getFileName(pdfDir,targetDir)
	convertedDir = 'pdftotext'
	files = glob.glob('pdftotext/*.txt')
	for f in files:
		os.remove(f)
	convertAll(pdfDir,convertedDir)
	getTitle(targetDir,convertedDir)
	getAbstract(targetDir,convertedDir)

main()