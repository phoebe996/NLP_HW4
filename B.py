import nltk
import A
from collections import defaultdict
from nltk.align  import AlignedSent

class BerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)

    # TODO: Computes the alignments for align_sent, using this model's parameters. Return
    #       an AlignedSent object, with the sentence pair and the alignments computed.
    def align(self, align_sent):
        if self.t is None or self.q is None:
            raise ValueError("The model does not train.")
        alignment = []

        l_e = len(align_sent.words)
        l_f = len(align_sent.mots)

        for j, en_word in enumerate(align_sent.words):
            
            # Initialize the maximum probability with Null token
            max_align_prob = (self.t[None][en_word]*self.q[0][j+1][l_f][l_e], None)
            for i, fr_word in enumerate(align_sent.mots):
                # Find out the maximum probability
                max_align_prob = max(max_align_prob,
                    (self.t[fr_word][en_word]*self.q[i+1][j+1][l_f][l_e], i))

            # If the maximum probability is not Null token,
            # then append it to the alignment. 
            if max_align_prob[1] is not None:
                alignment.append((j, max_align_prob[1]))

        return AlignedSent(align_sent.words, align_sent.mots, alignment)

    # TODO: Implement the EM algorithm. num_iters is the number of iterations. Returns the 
    # translation and distortion parameters as a tuple.
    def train(self, aligned_sents, num_iters):
        t = {}
        q = {}

        fr_vocab = set()
        en_vocab = set()
        for alignSent in aligned_sents:
            en_set = alignSent.mots
            fr_set = alignSent.words
            fr_vocab.update(fr_set)
            en_vocab.update(en_set)

        possible_tran_ef = defaultdict(lambda : set())
        possible_tran_fe = defaultdict(lambda : set())
        t_ef = defaultdict(lambda: defaultdict(lambda: 0.0))
        t_fe = defaultdict(lambda: defaultdict(lambda: 0.0))
        q_ef = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
        q_fe = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))

        for alignSent in aligned_sents:

            en_set = alignSent.mots
            fr_set = alignSent.words

            l_f = len(fr_set) 
            l_e = len(en_set)
            ef_initial_value = 1.0 / (l_e + 1)
            fe_initial_value = 1.0 / (l_f + 1)
            for i in range(1, l_e+1):
                for j in range(1, l_f+1):
                    q_ef[i][j][l_e][l_f] = ef_initial_value
                    q_fe[j][i][l_f][l_e] = fe_initial_value
            for i in range(1, l_f+1):
                possible_tran_fe[fr_set[i-1]].update(en_set)
                q_ef[0][i][l_e][l_f] = ef_initial_value
            for i in range(1, l_e+1):
                possible_tran_ef[en_set[i-1]].update(fr_set)
                q_fe[0][i][l_f][l_e] = fe_initial_value


        for en_word in possible_tran_ef:
            for fr_word in possible_tran_ef[en_word]:
                t_ef[en_word][fr_word]=1.0/len(possible_tran_ef[en_word])
        for fr_word in possible_tran_fe:
            for en_word in possible_tran_fe[fr_word]:
                t_fe[fr_word][en_word]=1.0/len(possible_tran_fe[fr_word])
        for en_word in en_vocab:
            t_fe[None][en_word]=1.0/len(en_vocab)
        for fr_word in fr_vocab:
            t_ef[None][fr_word]=1.0/len(fr_vocab)

        for i in range(0, num_iters):
            count_ef = defaultdict(lambda: defaultdict(lambda: 0.0))
            count_fe = defaultdict(lambda: defaultdict(lambda: 0.0))
            total_f = defaultdict(float)
            total_e = defaultdict(float)
            delta_ef = defaultdict(float)
            delta_fe = defaultdict(float)

            count_align_ef = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
            total_align_ef = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

            count_align_fe = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0))))
            total_align_fe = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

            for alignSent in aligned_sents:
                en_set = [None] + alignSent.mots
                fr_set = alignSent.words
                l_f = len(fr_set) 
                l_e = len(en_set) -1

                # compute normalization
                for j in range(1, l_f+1):
                    fr_word = fr_set[j-1]
                    delta_ef[fr_word] = 0
                    for k in range(0, l_e+1):
                        delta_ef[fr_word] += t_ef[en_set[k]][fr_word] * q_ef[k][j][l_e][l_f]

                # collect counts
                for j in range(1, l_f+1):
                    fr_word = fr_set[j-1]
                    for k in range(0, l_e+1):
                        en_word = en_set[k]
                        c = t_ef[en_word][fr_word] * q_ef[k][j][l_e][l_f] / delta_ef[fr_word]
                        count_ef[en_word][fr_word] += c
                        total_e[en_word] += c
                        count_align_ef[k][j][l_e][l_f] += c
                        total_align_ef[j][l_e][l_f] += c


            for alignSent in aligned_sents:
                en_set = alignSent.mots
                fr_set = [None] + alignSent.words
                l_f = len(fr_set) - 1
                l_e = len(en_set) 

                # compute normalization
                for j in range(1, l_e+1):
                    en_word = en_set[j-1]
                    delta_fe[en_word] = 0
                    for k in range(0, l_f+1):
                        delta_fe[en_word] += t_fe[fr_set[k]][en_word] * q_fe[k][j][l_f][l_e]

                # collect counts
                for j in range(1, l_e+1):
                    en_word = en_set[j-1]
                    for k in range(0, l_f+1):
                        fr_word = fr_set[k]
                        c = t_fe[fr_word][en_word] * q_fe[k][j][l_f][l_e] / delta_fe[en_word]
                        count_fe[fr_word][en_word] += c
                        total_f[fr_word] += c
                        count_align_fe[k][j][l_f][l_e] += c
                        total_align_fe[j][l_f][l_e] += c


            for f in fr_vocab:
                for e in en_vocab:
                    t_ef[e][f] = (count_fe[f][e]+count_ef[e][f]) / (total_e[e]+total_f[f])
                    t_fe[f][e] = t_ef[e][f]
                   
            for alignSent in aligned_sents:
                en_set = [None]+alignSent.mots
                fr_set =  [None] + alignSent.words
                l_f = len(fr_set)-1
                l_e = len(en_set)-1
                for k in range(1, l_f+1):
                    for j in range(1, l_e+1):
                        if ((total_align_ef[k][l_e][l_f]+total_align_fe[j][l_f][l_e]))==0:
                            q_fe[k][j][l_f][l_e] = q_ef[j][k][l_e][l_f]=0
                        else:
                            q_ef[j][k][l_e][l_f] = (count_align_ef[j][k][l_e][l_f]+count_align_fe[k][j][l_f][l_e]) / (total_align_ef[k][l_e][l_f]+total_align_fe[j][l_f][l_e])
                            q_fe[k][j][l_f][l_e] = q_ef[j][k][l_e][l_f]

                for j in range(1, l_e+1):
                    q_fe[0][j][l_f][l_e] = count_align_fe[0][j][l_f][l_e]/total_align_fe[j][l_f][l_e]
                for k in range(1, l_f+1):
                    q_ef[0][k][l_e][l_f] = count_align_ef[0][k][l_e][l_f]/total_align_ef[k][l_e][l_f]
               
        t = t_ef
        q = q_ef
        return (t,q)

def main(aligned_sents):
    ba = BerkeleyAligner(aligned_sents, 10)
    A.save_model_output(aligned_sents, ba, "ba.txt")
    avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)
    print ('Berkeley Aligner')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
    
