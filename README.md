#TTG
tweet timeline generation

#Usage
python cluster.py ../data/query.txt ../data/candidate/ 100 corpus.info.txt 1.77 0.23 ../data/result/ 0.9978 0.022

#Format of files
../data/query.txt
    qid \t qcontent
../data/candidate/
    The directory includes 55 candidate files: qid \t Qid \t wid \t rank \t score \t runTag \t wcontent \t qcontent
corpus.info.txt
    First line contains the total number of words in corpus. And the format of the following each line is: word \t tfValue
    
#Notice
In the usage command, 100 stands for mu in Dirichlet smoothing. And 
1.77, 0.23, 0.9978 are the relevance, novelty and coverage threshold respectively. Although 0.022 the threshold for Jaccard, it is not applied in 
the best performance, which means the file "jaccard.py" is useless here. Likewise, the usage of embedding doesn't work for our TTG system, so I leave out the file "w2v.py".
