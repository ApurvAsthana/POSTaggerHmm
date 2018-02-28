import time
import json
import sys

class LearnModel:
    transition_probabilities = dict()
    emmission_probabilities = dict()
    lines = []
    INIT_STATE = "InitState"

    def learnProbabilities(self):
        tagCountsForTr = dict()
        tagCountsForEm = dict()
        for line in self.lines:
            words = line.rstrip('\n').strip().split(" ")
            for i in range(0,len(words)):
                wordPrev = ""
                tagPrev = ""
                wordCurr = ""
                tagCurr = ""
                # to use an end state or not??
                if i != 0:
                    items = words[i-1].rstrip('\n').strip().rsplit("/", 1)
                    wordPrev = items[0]
                    tagPrev = items[1]
                    items = words[i].rstrip('\n').strip().rsplit("/", 1)
                    wordCurr = items[0]
                    tagCurr = items[1]

                else:
                    tagPrev = self.INIT_STATE
                    items = words[i].rstrip('\n').strip().rsplit("/", 1)
                    wordCurr = items[0]
                    tagCurr = items[1]

                if self.transition_probabilities.__contains__(tagPrev):
                    if self.transition_probabilities.get(tagPrev).__contains__(tagCurr):
                        self.transition_probabilities.get(tagPrev)[tagCurr] = self.transition_probabilities.get(tagPrev)[tagCurr] + 1
                    else:
                        self.transition_probabilities.get(tagPrev)[tagCurr] = 1
                else:
                    self.transition_probabilities[tagPrev] = dict()
                    self.transition_probabilities.get(tagPrev)[tagCurr] = 1
                if tagCountsForTr.__contains__(tagPrev):
                    tagCountsForTr[tagPrev] = tagCountsForTr[tagPrev] + 1
                else:
                    tagCountsForTr[tagPrev] = 1

                if self.emmission_probabilities.__contains__(wordCurr):
                    if self.emmission_probabilities.get(wordCurr).__contains__(tagCurr):
                        self.emmission_probabilities.get(wordCurr)[tagCurr] = self.emmission_probabilities.get(wordCurr)[
                                                                                  tagCurr] + 1
                    else:
                        self.emmission_probabilities.get(wordCurr)[tagCurr] = 1
                else:
                    self.emmission_probabilities[wordCurr] = dict()
                    self.emmission_probabilities.get(wordCurr)[tagCurr] = 1
                if tagCountsForEm.__contains__(tagCurr):
                    tagCountsForEm[tagCurr] = tagCountsForEm[tagCurr] + 1
                else:
                    tagCountsForEm[tagCurr] = 1

        # Smoothen the transition probabilities
        keys = self.transition_probabilities.keys()
        for key in keys:
            currDict = self.transition_probabilities.get(key)
            for checkKey in keys:
                if checkKey != self.INIT_STATE:
                    if not currDict.__contains__(checkKey):
                        currDict[checkKey] = 0.1
                    else:
                        currDict[checkKey] = currDict[checkKey] + 0.1
                    tagCountsForTr[key] = tagCountsForTr.get(key) + 0.1*len(keys)
            self.transition_probabilities[key] = currDict

        for key in keys:
            countForKeyTr = tagCountsForTr[key]
            currDictTr = self.transition_probabilities[key]
            for iterKeyTr in keys:
                if iterKeyTr!=self.INIT_STATE:
                    currDictTr[iterKeyTr] = currDictTr[iterKeyTr]/countForKeyTr
            self.transition_probabilities[key] = currDictTr

        keys = self.emmission_probabilities.keys()
        for key in keys:
            currDictEm = self.emmission_probabilities[key]
            for iterKeyEm in currDictEm.keys():
                currDictEm[iterKeyEm] = currDictEm[iterKeyEm] / tagCountsForEm[iterKeyEm]
            self.emmission_probabilities[key] = currDictEm

        # print("----------------------------")
        # print(self.transition_probabilities)
        # print(tagCountsForTr)
        # print("***********")
        # print(self.transition_probabilities['VBD'])
        # # print(tagCountsForTr.__len__())
        # print(self.emmission_probabilities)
        # print(tagCountsForEm)
        # # print(tagCountsForEm.__len__())

path = 'C:\\Users\\sunny\\Desktop\\assignments\\NLP\\Assignment1\\en_train_tagged.txt'
Learner = LearnModel()
f_in = open(path,'r',encoding="utf-8")
Learner.lines = f_in.readlines()
f_in.close()
startTime = time.time()
Learner.learnProbabilities()
result = dict()
result['TR'] = Learner.transition_probabilities
result['EM'] = Learner.emmission_probabilities
f_out = open('hmmmodel.txt','w',encoding="utf-8")
jsonStr = json.dump(result,f_out,ensure_ascii=False)
f_out.close()
print(time.time()-startTime)
