#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     cluster.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-01-02 19:42:26
# MODIFIED: 2016-01-15 00:31:28
# USAGE: python cluster.py ../data/query.txt ../data/candidate/ 100 corpus.info.txt 1.77 0.23 ../data/result/ 0.9

import os
import sys
from os import listdir
from formulation import Distance
from textRank import Rank
from jaccard import Jaccard

class Cluster:
    def __init__(self, queryFile, candidatePath, mu, corpusFile, sigma, lamda):
        self.query = {}
        self.candidate = candidatePath
        self.tweet = {}  
        self.mu = mu
        self.sigma = sigma      #similarity threshold
        self.lamda = lamda      #cluster threshold     
        self.jaccInstance = Jaccard()
        self.klInstance = Distance(mu, corpusFile)
        print "corpus read done!"    
    
    def write(self, writePath, alpha, beta, yibuson):
        writeFile = writePath + "res.4.59S" + str(self.sigma) + ".L" + str(self.lamda) + ".a" + str(alpha) + ".b" + str(beta) + ".J" + str(yibuson)
        result = open(writeFile, "w+")
        log = open(writePath + "log.4.59S" + str(self.sigma) + ".L" + str(self.lamda) + ".a" + str(alpha) + ".b" + str(beta) + ".J" + str(yibuson), "w+")
        log.write("Qid\tclusterCount\ttweetCount\n")
        log1 = open(writePath + "qidWidKL.4.59S" + str(self.sigma) + ".L" + str(self.lamda) + ".a" + str(alpha) + ".b" + str(beta) + ".J" + str(yibuson), "w+")
        log2 = open(writePath + "widWidKL.4.59S" + str(self.sigma) + ".L" + str(self.lamda) + ".a" + str(alpha) + ".b" + str(beta) + ".J" + str(yibuson), "w+")
        log3 = open(writePath + "jaccScore.4.59S" + str(self.sigma) + ".L" + str(self.lamda) + ".a" + str(alpha) + ".b" + str(beta) + ".J" + str(yibuson), "w+")

        num = 1
        files = []
        while(num <= 55):
            files.append(str(num) + ".res.content.all")
            num += 1
        for file in files:
            #remember to make them initial on each query
            self.curQid = -1
            self.cluster = []
            self.qidWidKL = {}
            self.qidWidMax = 0
            self.qidWidMin = 999
            self.widWidKL = {}
            self.widWidMax = 0
            self.widWidMin = 999 
            self.widScore = {}
            self.jacc = {}
            self.jaccMax = 0
            self.jaccMin = 1
            self.resultList = []
            readPath = self.candidate + file  
            
            with open(readPath, "r") as fin:
                for i, line in enumerate(fin):
                    qid, Qid, wid, rank, score, runName, wcontent, qcontent = line.strip().split("\t")
                    self.query[qid] = qcontent
                    
                    #first time selection
                    if(float(score) < 4.59):
                        if not self.cluster:
                            print "break out of 4.59, ", file, " , empty cluster!"
                            exit()
                        break
                        
                    self.tweet[wid] = wcontent
                    self.curQid = qid
                    
                    #calculate qidWidKL
                    similarity = self.klInstance.kl(self.query[qid], wcontent)
                    
                    #calculate jaccard score
                    jaccScore = self.jaccInstance.jaccardScore(qcontent, wcontent)
                    
                    if similarity <= self.sigma and jaccScore >= yibuson:
                        
                        #set self.qidWidKL
                        self.qidWidKL[qid+"-"+wid] = similarity
                        if (similarity > self.qidWidMax):
                            self.qidWidMax = similarity

                        if (similarity < self.qidWidMin):
                            self.qidWidMin = similarity
                        
                        #set self.jacc       
                        self.jacc[qid+"-"+wid] = jaccScore
                        if self.jaccMax < jaccScore:
                            self.jaccMax = jaccScore
                        if self.jaccMin > jaccScore:
                            self.jaccMin = jaccScore    
                        
                        #calculate widWidKL
                        if not self.cluster:
                            self.cluster.append([wid])
                            self.widWidKL[wid] = []
                        else:
                            self.__clustering(wid)

                    
                    if (i % 100) == 0:
                        print file, " => ", i
                
            log1.write(str(self.qidWidMin) + "\t" + str(self.qidWidMax) + "\n")
            for key in self.qidWidKL:
                log1.write(key + "\t" + str(self.qidWidKL[key]) + "\n")
            log2.write(str(self.widWidMin) + "\t" + str(self.widWidMax) + "\n")
            for key in self.widWidKL:
                for i in range(len(self.widWidKL[key])):
                    for widKey in self.widWidKL[key][i]:
                        log2.write(key + "-" + widKey + "\t" + str(self.widWidKL[key][i][widKey]) + "\n")
            log3.write(str(self.jaccMin) + "\t" + str(self.jaccMax) + "\n")
            for key in self.jacc:
                log3.write(key + "\t" + str(self.jacc[key]) + "\n")
                        
            rankInstance = Rank(self.widWidKL, self.widWidMin, self.widWidMax, self.cluster, self.tweet)
            self.widScore = rankInstance.generate(0.85, 0.01, alpha, beta)
            
            #log info
            clusterCount = len(self.cluster)
            tweetCount = 0
            
            #select one wid from each cluster & log info 
            for i in range(len(self.cluster)):
                maxScore = 0
                bestWid = -1
                tweetCount += len(self.cluster[i])
                for wid in self.cluster[i]:
                    if self.widScore[wid] > maxScore:
                        maxScore = self.widScore[wid]
                        bestWid = wid
                self.resultList.append(bestWid)
            
            #write log info
            log.write("MB" + self.curQid + "\t" + str(clusterCount) + "\t" + str(tweetCount) + "\n")
            
                       
            #write result
            for wid in self.resultList:
                result.write("MB" + self.curQid + "\t" + "Q0\t" + wid + "\t1\t1\tYAO\n")
            
        
    def __clustering(self, wid):
        minScore = 999
        index = -1
        wcontent = self.tweet[wid]
        for i in range(len(self.cluster)):          
            for cwid in self.cluster[i]:
                ccontent = self.tweet[cwid]
                score = self.klInstance.kl(self.tweet[wid], self.tweet[cwid])
                #print i
                if wid in self.widWidKL:
                    self.widWidKL[wid].append({cwid: score})
                else:
                    self.widWidKL[wid] = [{cwid: score}]
                
                if cwid in self.widWidKL:
                    self.widWidKL[cwid].append({wid: score})
                else:
                    self.widWidKL[cwid] = [{wid: score}]
                    
                    
                #select miniScore, that is the most similar value
                if score < minScore:
                    minScore = score
                    index = i
                if score < self.widWidMin:
                    self.widWidMin = score

                if score > self.widWidMax:
                    self.widWidMax = score
                    
        #put wid into the cluster 
        #a new cluster
        if minScore > self.lamda:
            self.cluster.append([wid])
            #print self.cluster
        #add to a highest similarity cluster
        else:
            self.cluster[index].append(wid)
  

if __name__ == '__main__':
    if len(sys.argv) < 11:
        print "sys.argv[1]: input query file!"
        print "sys.argv[2]: input candidate file path!"
        print "sys.argv[3]: input smooth mu!"
        print "sys.argv[4]: input corpus file!"
        print "sys.argv[5]: input similarity threshold!"
        print "sys.argv[6]: input cluster threshold!"
        print "sys.argv[7]: output file path!"
        print "sys.argv[8]: input textRank alpha!"
        print "sys.argv[9]: input textRank beta!"
        print "sys.argv[10]: input jaccard yibuson!"
        exit()

    clusterInstance = Cluster(sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], float(sys.argv[5]), float(sys.argv[6]))
    clusterInstance.write(sys.argv[7], float(sys.argv[8]), float(sys.argv[9]), float(sys.argv[10]))
    
    

    
    
