import re

def extract_numbers(search_file):

    postwarning = ''
    
### Find and sort tiers and ranks

    searchfile = open(search_file,'r',encoding='utf-8', errors='ignore')
    scoreList = []
    peopleList = []

    for line in searchfile.readlines():
        if 'rank' in line:
            digits = re.findall('\d+',line)
            border = int(digits[len(digits)-1])
            rank = int(digits[len(digits)-2])
            if border not in scoreList:
                scoreList.append(border)
            if rank not in peopleList:
                peopleList.append(rank)
        
    scoreList = sorted(scoreList,reverse=True)
    finalScoreList = []
    
    for i in range(0,8,1):
        if i < len(scoreList):
            finalScoreList.append(str(scoreList[i]))
        else:
            finalScoreList.append('missing')

    peopleList = sorted(peopleList,reverse=True)
    finalScoreList.append(str(peopleList[0]))

    for n in range(0,len(finalScoreList)):
        print(finalScoreList[n])

    searchfile.close()
    return finalScoreList, postwarning

    
