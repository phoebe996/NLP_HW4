Homework 4
Yu Wang (yw2684)

Expected time to run the whole program: 

Part A:
(1) ~ (2) Implement save_model_output(), create_ibm1(), and create_ibm2() as specified in the instruction.

(3) Implement compute_average_aer() and compute the AER over the first 50 sentences for IBMModel1 and IBMModel2. 
Here are the results:

IBM Model 1
---------------------------
Average AER: 0.665

IBM Model 2
---------------------------
Average AER: 0.650

Comparision of IBMModel1 and IBMModel2:
1.
For the following sentence pair
[u'Wie', u'Sie', u'sicher', u'aus', u'der', u'Presse', u'und', u'dem', u'Fernsehen', u'wissen', u',', u'gab', u'es', u'in', u'Sri', u'Lanka', u'mehrere', u'Bombenexplosionen', u'mit', u'zahlreichen', u'Toten', u'.']
[u'You', u'will', u'be', u'aware', u'from', u'the', u'press', u'and', u'television', u'that', u'there', u'have', u'been', u'a', u'number', u'of', u'bomb', u'explosions', u'and', u'killings', u'in', u'Sri', u'Lanka', u'.']
the correct alignment is 
0-0 1-0 2-1 2-2 3-4 4-5 5-6 6-7 7-8 8-8 9-3 10-9 11-10 11-11 11-12 12-10 13-20 14-21 15-22 16-14 16-15 17-16 17-17 17-18 17-19 19-13 21-23

The alignment result of IBMModel1 is:
0-19 1-0 2-19 3-4 4-15 5-19 6-18 7-19 8-19 9-19 10-2 11-22 12-22 13-20 14-22 15-22 16-19 17-19 18-19 19-19 20-19
and the error rate is 0.791666666667

The alignment result of IBMModel2 is:
0-6 1-0 2-16 3-3 4-4 5-17 6-18 7-22 8-19 9-8 10-2 11-16 12-22 13-20 14-19 15-22 16-19 17-8 18-17 19-19 20-8
and the error rate is 0.875


2. 
For the following sentence pair:
[u'Ich', u'bitte', u'Sie', u',', u'sich', u'zu', u'einer', u'Schweigeminute', u'zu', u'erheben', u'.']
[u'Please', u'rise', u',', u'then', u',', u'for', u'this', u'minute', u"'", u's', u'silence', u'.']
the correct alignment is 
0-0 1-0 2-0 3-4 4-1 5-5 6-6 7-7 7-8 7-9 7-10 8-10 9-10 10-11

The alignment result of IBMModel1 is:
0-1 1-1 2-1 3-4 4-10 5-10 6-10 7-10 8-10 9-1
and the error rate is 0.75

The alignment result of IBMModel2 is:
0-0 1-1 2-0 3-2 4-10 5-10 6-10 7-7 8-10 9-0
and the error rate is 0.666666666667


In the first sentence pair, IBMModel1 performs better than IBMModel2 and in the second sentence pair, IBMModel2 performs better than IBMModel1. 
This may because that in IBMModel1, distortion parameter is uniformly distributed over all possible positions, which means that for a word, the possibility of its corresponding translation in all positions of the target sentence is the same. IBMModel1's resulting alignments only base on the most probable translation of each word. However, in IBMModel2, distortion parameter is actually improving during EM iterations and its resulting alignment is based on both word translation and the position distortion of a word in the target sentence. As a result, in a sentence pair where position distortion is more randomly distributed over all positions, like the first sentence pair, IBMModel1 outperforms IBMModel2. While for sentence pairs whose position distortion is more fit to some rules between corresponding positions and position information can be used to get a better alignment, like the second sentence pair, IBMModel2 outperforms IBMModel1.

(4) I experiment on the AER on both IBMModel1 and IBMModel2 with respect to the number of iterations, and get the following result:
Iteration number:2
IBM Model 1
---------------------------
Average AER: 0.684

IBM Model 2
---------------------------
Average AER: 0.644

Total time: 57
Iteration number:3
IBM Model 1
---------------------------
Average AER: 0.641

IBM Model 2
---------------------------
Average AER: 0.644

Total time: 72
Iteration number:4
IBM Model 1
---------------------------
Average AER: 0.630

IBM Model 2
---------------------------
Average AER: 0.642

Total time: 82

Iteration number:5
IBM Model 1
---------------------------
Average AER: 0.627

IBM Model 2
---------------------------
Average AER: 0.644

Total time: 96

Iteration number:6
IBM Model 1
---------------------------
Average AER: 0.626

IBM Model 2
---------------------------
Average AER: 0.647

Total time: 112
Iteration number:7
IBM Model 1
---------------------------
Average AER: 0.629

IBM Model 2
---------------------------
Average AER: 0.646

Total time: 115
Iteration number:8
IBM Model 1
---------------------------
Average AER: 0.631

IBM Model 2
---------------------------
Average AER: 0.649

Total time: 125
Iteration number:9
IBM Model 1
---------------------------
Average AER: 0.628

IBM Model 2
---------------------------
Average AER: 0.649

Total time: 135
Iteration number:10
IBM Model 1
---------------------------
Average AER: 0.665

IBM Model 2
---------------------------
Average AER: 0.650
Total time: 146

Iteration number:11
IBM Model 1
---------------------------
Average AER: 0.666

IBM Model 2
---------------------------
Average AER: 0.649
Total time: 167

Iteration number:12
IBM Model 1
---------------------------
Average AER: 0.666

IBM Model 2
---------------------------
Average AER: 0.650
Total time: 190

Based on these experiments, we can see that when iteration number = 6, IBMModel1 has the lowest AER = 0.626, taking 112s. When iteration number = 5, IBMModel also performs well with AER = 0.627, taking 96s.
When iteration number = 4, IBMModel2 has the lowest AER = 0.642, taking 82s.
These two are the lower bounds of AER with respect to IBMModel1 and IBMModel2. For both of the two models, when iteration number is smaller, the AER is larger because there aren't enough feature information extracted for EM model to get a better result. While when iteration number is getting larger, AER hits a lower bound and it goes up again which may be because the feature information extracted is over calculated.


Part B:
(1) ~ (3)  Implement the functions according to the instruction.

(4) The average AER for the first 50 sentences is 0.574.

With both iteration number = 10, BerkeleyAligner model performs better than IBM model. 

(5)
Here's an example. For sentence pair
[u'Ich', u'erkl\xe4re', u'die', u'am', u'Freitag', u',', u'dem', u'17.', u'Dezember', u'unterbrochene', u'Sitzungsperiode', u'des', u'Europ\xe4ischen', u'Parlaments', u'f\xfcr', u'wiederaufgenommen', u',', u'w\xfcnsche', u'Ihnen', u'nochmals', u'alles', u'Gute', u'zum', u'Jahreswechsel', u'und', u'hoffe', u',', u'da\xdf', u'Sie', u'sch\xf6ne', u'Ferien', u'hatten', u'.']
[u'I', u'declare', u'resumed', u'the', u'session', u'of', u'the', u'European', u'Parliament', u'adjourned', u'on', u'Friday', u'17', u'December', u'1999', u',', u'and', u'I', u'would', u'like', u'once', u'again', u'to', u'wish', u'you', u'a', u'happy', u'new', u'year', u'in', u'the', u'hope', u'that', u'you', u'enjoyed', u'a', u'pleasant', u'festive', u'period', u'.']

Tne correct alignment is 
0-0 1-1 2-30 3-10 3-11 4-11 7-12 8-13 9-14 10-3 10-4 11-5 11-6 12-7 13-8 14-9 15-9 16-15 17-23 18-24 19-20 19-21 20-22 21-25 23-26 23-27 23-28 24-16 25-31 26-32 27-32 28-33 29-35 29-36 30-36 30-37 30-38 31-37 32-39

IBMModel1's alignment is 
0-17 1-37 2-30 3-21 4-37 5-15 6-23 7-37 8-37 9-37 10-4 11-37 12-7 13-37 14-27 15-37 16-15 17-37 18-37 19-20 20-37 21-37 22-37 23-37 24-16 25-31 26-15 27-32 28-33 29-37 30-37 31-37
and AER is 0.69014084507

IBMModel2's alignment is
0-17 1-37 2-30 3-21 4-37 5-15 6-23 7-37 8-37 9-37 10-4 11-37 12-7 13-37 14-27 15-37 16-15 17-37 18-37 19-20 20-37 21-37 22-37 23-37 24-16 25-31 26-15 27-32 28-33 29-37 30-37 31-37
and AER is 0.69014084507

BerkeleyAligner's alignment is 
0-17 1-26 2-30 3-21 4-26 5-15 6-22 7-26 8-26 9-26 10-4 11-37 12-7 13-8 14-10 15-26 16-15 17-26 18-33 19-20 20-37 21-26 22-37 23-26 24-16 25-31 26-15 27-32 28-33 29-26 30-26 31-37 32-39
and AER is 0.6388888888890

In this sentence pair, BerkeleyAligner model outperforms both IBM models. This may be becuase that both IBM model only uses one direction to train the parameters, while BerkeleyAligner model trains two models simultaneously, which are in different directions, to maximize a combination of data likelihood and agreement between these two models. As a result, BerkeleyAligner's two models can make up for each other's flaw by  finding predictions that both models agree on and can achieve a better performance on complex sentence pairs like the example.

(6) In this part, I tried to modify the way we quantify agreement between two models. I tried different methods to compute the average expected count of the two models. 
For example, I try to average the q, t parameters of these two models directly  with q' = (q1 + q2)/2, t' = (t1 + t2)/2. But this does not improve the AER.
I tried to average them with q' = 2/(1/q1+1/q2), t'=2/(1/t1+1/t2), but this does not improve the AER.



