import nltk
from nltk.align.ibm1 import IBMModel1
from nltk.align.ibm2 import IBMModel2
import datetime

NUM_ITERS = 10

# TODO: Initialize IBM Model 1 and return the model.
def create_ibm1(aligned_sents):
    ibm1 = IBMModel1(aligned_sents, NUM_ITERS)
    return ibm1

# TODO: Initialize IBM Model 2 and return the model.
def create_ibm2(aligned_sents):
    ibm2 = IBMModel2(aligned_sents, NUM_ITERS)
    return ibm2

# TODO: Compute the average AER for the first n sentences
#       in aligned_sents using model. Return the average AER.
def compute_avg_aer(aligned_sents, model, n):
    error_sum = 0.0
    for sample_sent in aligned_sents[:n]:
        sample_sent_result = model.align(sample_sent)
        error_sum = error_sum + sample_sent_result.alignment_error_rate(sample_sent)
    return error_sum/n

# TODO: Computes the alignments for the first 20 sentences in
#       aligned_sents and saves the sentences and their alignments
#       to file_name. Use the format specified in the assignment.
def save_model_output(aligned_sents, model, file_name):
    output_file = open(file_name, "w")
    for sample_sent in aligned_sents[:20]:
        sample_sent_result = model.align(sample_sent)
        output_file.write(str(sample_sent_result.words) + "\n")
        output_file.write(str(sample_sent_result.mots) + "\n")
        output_file.write(str(sample_sent_result.alignment) + "\n\n")
    output_file.close()

def main(aligned_sents):
    ibm1 = create_ibm1(aligned_sents)
    save_model_output(aligned_sents, ibm1, "ibm1.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm1, 50)

    print ('IBM Model 1')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))

    ibm2 = create_ibm2(aligned_sents)
    save_model_output(aligned_sents, ibm2, "ibm2.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm2, 50)
    
    print ('IBM Model 2')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))