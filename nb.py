import email.parser 
import os, sys, stat
import shutil
import math

def uniqueWords(sentence):
    return set("".join((char if char.isalpha() else " ") for char in sentence).lower().split())

def allWords(sentence):
    return "".join((char if char.isalpha() else " ") for char in sentence).lower().split()

def CreateCategories(bodyOfMsg,usual):
    # print "entered CreateCategories"
    totalHam =usual[0]
    totalSpam =usual[1]
    category_HAM =usual[2]
    category_SPAM =usual[3]
    spamList = usual[4]
    uniqueWordsInBody = list(uniqueWords(bodyOfMsg))
    allWordsInBody = list(allWords(bodyOfMsg))
    sizeOfBody = len(allWordsInBody)
    checkspam = int(spamList[totalHam+totalSpam].split(" ")[0])
    if checkspam == 1:
        totalHam = totalHam + 1
        # print "Reading Ham Mail ",totalHam
        for word in uniqueWordsInBody:
            if word in category_HAM:
                category_HAM[word] = category_HAM[word] + float(allWordsInBody.count(word))/sizeOfBody
            else:
                category_HAM[word] = float(allWordsInBody.count(word))/sizeOfBody
    else:
        totalSpam += 1
        # print "Reading Spam Mail ",totalSpam
        for word in uniqueWordsInBody:
            if word in category_SPAM:
                category_SPAM[word] = category_SPAM[word] + float(allWordsInBody.count(word))/sizeOfBody
            else:
                category_SPAM[word] = float(allWordsInBody.count(word))/sizeOfBody
    usual = [totalHam,totalSpam,category_HAM,category_SPAM,spamList]
    return usual

def GetBodyOfMsg (srcfilename,usual):
    if not os.path.exists(srcfilename): # dest path doesnot exist
        print "ERROR: input file does not exist:", filename
        os.exit(1)
    fp = open(srcfilename)
    msg = email.message_from_file(fp)
    payload = msg.get_payload()
    if type(payload) == type(list()) :
        payload = payload[0] # only use the first part of payload
    sub = msg.get('subject')
    sub = str(sub)
    if type(payload) != type('') :
        payload = str(payload)
    bodyOfMsg = sub+payload
    return CreateCategories(bodyOfMsg,usual)


def FindCategories(bodyOfMsg,usual):
    totalHam =usual[0]
    totalSpam =usual[1]
    category_HAM =usual[2]
    category_SPAM =usual[3]
    noOfHam = usual[4]
    noOfSpam = usual[5]
    uniqueWordsInBody = list(uniqueWords(bodyOfMsg))
    probOfHAM = 0.0
    probOfSPAM = 0.0
    for word in uniqueWordsInBody:
        if word in category_HAM:
            probOfHAM = probOfHAM + category_HAM[word]
        else:
            probOfHAM = probOfHAM - 10
    for word in uniqueWordsInBody:
        if word in category_SPAM:
            probOfSPAM = probOfSPAM + category_SPAM[word]
        else:   
            probOfHAM = probOfHAM - 10
    if (probOfSPAM > probOfHAM):
        noOfSpam = noOfSpam + 1
    else :
        noOfHam = noOfHam + 1
    usual = [totalHam,totalSpam,category_HAM,category_SPAM,noOfHam,noOfSpam]
    return usual

def GetBodyOfMsgForTesting (srcfilename,usual):
    if not os.path.exists(srcfilename): # dest path doesnot exist
        print "ERROR: input file does not exist:", filename
        os.exit(1)
    fp = open(srcfilename)
    msg = email.message_from_file(fp)
    payload = msg.get_payload()
    if type(payload) == type(list()) :
        payload = payload[0] # only use the first part of payload
    sub = msg.get('subject')
    sub = str(sub)
    if type(payload) != type('') :
        payload = str(payload)
    bodyOfMsg = sub+payload
    return FindCategories(bodyOfMsg,usual)    


def ExtractBodyFromDir ( srcDir,dstDir):
    
    totalSpam = 0
    totalHam = 0
    category_HAM = {"assignment":0.0}
    category_SPAM = {"purchase":0.0}
    spamTrainPath = "/home/yooo/Documents/Indix/CSDMC2010_SPAM/CSDMC2010_SPAM/SpamTrain/SPAMTrain.txt"
    spamfp = open(spamTrainPath)
    spamList = spamfp.readlines()
    usual = [totalHam,totalSpam,category_HAM,category_SPAM,spamList]
    srcfiles = os.listdir(srcDir)
    for file in srcfiles:
        srcPath = os.path.join(srcDir, file)
        usual = GetBodyOfMsg (srcPath,usual)

    print totalHam,totalSpam
    totalHam =usual[0]
    totalSpam =usual[1]
    category_HAM =usual[2]
    category_SPAM =usual[3]
    category_HAM.update((x,math.log10(y/totalHam)) for x,y in category_HAM.items())
    category_SPAM.update((x,math.log10(y/totalSpam)) for x,y in category_SPAM.items())
    noOfSpam = 0
    noOfHam = 0
    # print category_SPAM
    usual = [totalHam,totalSpam,category_HAM,category_SPAM,noOfHam,noOfSpam]
    dstfiles = os.listdir(dstDir)
    for file in dstfiles:
        dstPath = os.path.join(dstDir, file)
        usual = GetBodyOfMsgForTesting (dstPath,usual)
    print usual[4],usual[5]

srcDir = "/home/yooo/Documents/Indix/CSDMC2010_SPAM/CSDMC2010_SPAM/Destination/"
# srcDir = "/home/yooo/Documents/Indix/CSDMC2010_SPAM/CSDMC2010_SPAM/trial/"
print 'Input source directory: ',srcDir #ask for source and dest dirs
dstDir = "/home/yooo/Documents/Indix/CSDMC2010_SPAM/CSDMC2010_SPAM/TESTING/"
# dstDir = "/home/yooo/Documents/Indix/CSDMC2010_SPAM/CSDMC2010_SPAM/trailtest/"
print 'Input source directory: ',dstDir #ask for source and dest dirs
ExtractBodyFromDir (srcDir,dstDir) 
