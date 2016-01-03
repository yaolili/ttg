#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     cluster.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-01-02 19:42:26
# MODIFIED: 2016-01-02 19:42:38
# USAGE: python cluster.py ../data/query.txt ../data/candidate/ 0.85 /index14/plain/origin.corpus ../data/result.txt

import os
import sys
from os import listdir
from formulation import Distance

def clustering(wid, cluster, tweet, klInstance, lamda, widWidKL, widWidMax, widWidMin):
    maxScore = 999
    index = -1
    wcontent = tweet[wid]
    for i in range(len(cluster)):
        for cwid in cluster[i]:
            ccontent = tweet[cwid]
            score = klInstance.kl(tweet[wid], tweet[cwid])
            widWidKL[wid+"-"+cwid] = score
            if score < maxScore:
                maxScore = score
                index = i
            if score < widWidMin:
                widWidMin = score
            if score > widWidMax:
                widWidMax = score
                
    #put wid into the cluster 
    #a new cluster
    if maxScore > lamda:
        cluster.append([wid])
    #add to a highest similarity cluster
    else:
        cluster[index].append(wid)
    return widWidMax, widWidMin   
    
def normalize(origin, max, min):
    return (origin - min) / (max - min)

if __name__ == '__main__':
    if len(sys.argv) < 8:
        print "sys.argv[1]: input query file!"
        print "sys.argv[2]: input candidate file path!"
        print "sys.argv[3]: input smooth mu!"
        print "sys.argv[4]: input corpus file!"
        print "sys.argv[5]: input similarity threshold!"
        print "sys.argv[6]: input cluster threshold!"
        print "sys.argv[7]: output file path!"
        exit()
    
    query = {}
    tweet = {}
    cluster = []
    qidWidKL = {}
    widWidKL = {}
    sigma = float(sys.argv[5])      #similarity threshold
    lamda = float(sys.argv[6])      #cluster threshold
    qidWidMax = 0
    qidWidMin = 999
    widWidMax = 0
    widWidMin = 999
    
    klInstance = Distance(sys.argv[3], sys.argv[4])
    print "corpus read done!"

    
    #read query info
    f1 = open(sys.argv[1], "r")
    for line in f1:
        qid, qcontent = line.strip().split("\t")
        query[qid] = qcontent
    
    #candidate files
    files = [f for f in listdir(sys.argv[2])]
    for file in files:
        readPath = sys.argv[2] + file
        writePath = sys.argv[7] + file + ".cluster"
        result = open(writePath, "w+")
        log1 = open(writePath + ".qidWidKL" , "w+")
        log2 = open(writePath + ".widWidKL" , "w+")
        with open(readPath, "r") as fin:
            for i, line in enumerate(fin):
                qid, Qid, wid, rank, score, runName, content = line.strip().split("\t")
                tweet[wid] = content
                
                #calculate qidWidKL
                similarity = klInstance.kl(query[qid], content)
                

                if similarity <= sigma:
                    qidWidKL[qid+"-"+wid] = similarity
                    if (similarity > qidWidMax):
                        qidWidMax = similarity
                    if (similarity < qidWidMin):
                        qidWidMin = similarity
                    
                    #calculate widWidKL
                    if not cluster:
                        cluster.append([wid])                    
                    else:
                        widWidMax, widWidMin = clustering(wid, cluster, tweet, klInstance, lamda, widWidKL, widWidMax, widWidMin)
                
                if (i % 100) == 0:
                    print i
            
            #write log file
            log1.write(str(qidWidMin) + "\t" + str(qidWidMax) + "\n")
            for key in qidWidKL:
                score = normalize(qidWidKL[key], qidWidMax, qidWidMin)
                log1.write(key + "\t" + str(score) + "\n")
            log2.write(str(widWidMin) + "\t" + str(widWidMin) + "\n")
            for key in widWidKL:
                score = normalize(widWidKL[key], widWidMax, widWidMin)
                log2.write(key + "\t" + str(score) + "\n")
                
            #write cluster    
            for i in range(len(cluster)):
                for wid in cluster[i]:
                    result.write(wid + "\t" + tweet[wid] + "\n\n")
                result.write("----------------------------\n")
            result.close()   
            exit()    
    f1.close()
