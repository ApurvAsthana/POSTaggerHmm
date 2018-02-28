import json
import time

class HMMDecode:
    transitionMatrix = dict()
    emmissionMatrix = dict()
    INIT_STATE = "InitState"
    FINAL_STATE = "FinalState"
    correct = 0
    total = 0

    def viterbi(self,line,checkLine):
        path_matrix = dict()
        backpointers = dict()
        stepCounter = 0
        words = line.rstrip("\n").strip().split(" ")
        checkWords = checkLine.rstrip("\n").strip().split(" ")
        states = list(self.transitionMatrix.keys())
        states.remove(self.INIT_STATE)
        path_matrix[stepCounter] = dict()
        backpointers[stepCounter] = dict()
        if self.emmissionMatrix.__contains__(words[0]):
            wordTagDict = self.emmissionMatrix[words[0]]
        else:
            wordTagDict = None
        pathDictCurr = path_matrix[stepCounter]
        backPtrCurr = backpointers[stepCounter]
        for tagState in states:
            pathDictCurr[tagState] = self.transitionMatrix.get(self.INIT_STATE)[tagState]
            if wordTagDict is None:
                pathDictCurr[tagState] = pathDictCurr[tagState] * 1
            elif wordTagDict.__contains__(tagState):
                pathDictCurr[tagState] = pathDictCurr[tagState] * wordTagDict[tagState]
            else:
                pathDictCurr[tagState] = pathDictCurr[tagState] * 0
            backPtrCurr[tagState] = self.INIT_STATE
        for i in range(1,len(words)):
            stepCounter = stepCounter + 1
            path_matrix[stepCounter] = dict()
            backpointers[stepCounter] = dict()
            pathDictCurr = path_matrix[stepCounter]
            backPtrCurr = backpointers[stepCounter]
            if self.emmissionMatrix.__contains__(words[i]):
                wordTagDict = self.emmissionMatrix[words[i]]
            else:
                wordTagDict = None
            for prevState in states:
                prevStateTransitions = self.transitionMatrix[prevState]
                prevPathMatrix = path_matrix[i-1]
                for tagState in states:
                    # print(prevState)
                    if prevPathMatrix.__contains__(prevState):
                        tempPathVal = prevPathMatrix[prevState]*prevStateTransitions[tagState]
                        if wordTagDict is None:
                            tempPathVal = tempPathVal * 1
                        elif wordTagDict.__contains__(tagState):
                            tempPathVal = tempPathVal * wordTagDict[tagState]
                        else:
                            tempPathVal = tempPathVal * 0
                        if tempPathVal > pathDictCurr.get(tagState,0):
                            pathDictCurr[tagState] = tempPathVal
                            backPtrCurr[tagState] = prevState
        maxFinal = 0
        maxFinalState = None
        for key in path_matrix[stepCounter].keys():
            temp = path_matrix[stepCounter][key]
            if temp>maxFinal:
                maxFinal = temp
                maxFinalState = key

        resultStr = ""
        for i in range(stepCounter,-1,-1):
            if checkWords[i].rsplit("/",1)[1]==maxFinalState:
                self.correct = self.correct + 1
                self.total = self.total + 1
            else:
                self.total = self.total + 1
            if maxFinalState==None:
                resultStr = words[i] + "/" + "" + " " + resultStr
                break
            else:
                resultStr = words[i]+"/"+maxFinalState + " " + resultStr
            maxFinalState = backpointers[i][maxFinalState]
        resultStr = resultStr.strip()
        return resultStr

Tagger = HMMDecode()
startTime = time.time()
f_in = open('hmmmodel.txt','r',encoding="utf-8")
modelDict = json.load(f_in)
f_in.close()
Tagger.emmissionMatrix = modelDict['EM']
Tagger.transitionMatrix = modelDict['TR']
f_in = open('C:\\Users\\sunny\\Desktop\\assignments\\NLP\\Assignment1\\en_dev_raw.txt','r',encoding="utf-8")
# print(time.time()-startTime)
lines = f_in.readlines()
f_in = open('C:\\Users\\sunny\\Desktop\\assignments\\NLP\\Assignment1\\en_dev_tagged.txt','r',encoding="utf-8")
checkLines = f_in.readlines()
taggedResult = ""
# for line in lines:
#     taggedResult = taggedResult + Tagger.viterbi(line) + "\n"

for i in range(0,len(lines)):
    taggedResult = taggedResult + Tagger.viterbi(lines[i],checkLines[i]) + "\n"

print(taggedResult)
# f_out = open('hmmoutput.txt','w',encoding="utf-8")
# f_out.write(taggedResult)
# f_out.close()
print(time.time()-startTime)
print("Acc: ")
print(Tagger.correct/Tagger.total)