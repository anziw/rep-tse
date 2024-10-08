import pandas as pd

def calculate_ew_mw(file_path):
    
    file = pd.read_csv(file_path, sep='\t')

    # Initialize counts
    correct_count = 0
    total_count = 0
    correct_prob_sum = 0  
    total_prob_sum = 0    

    # Group by lemma and pairid
    grouped = file.groupby(['lemma', 'pairid'])

    for (lemma, pairid), group in grouped:
        expected = group[group['comparison'] == 'expected']
        unexpected = group[group['comparison'] == 'unexpected']

        if not expected.empty and not unexpected.empty:
            expected_prob = expected['probsum'].values[0]
            unexpected_prob = unexpected['probsum'].values[0]

            # EW addition
            if expected_prob > unexpected_prob:
                correct_count += 1 

            total_count += 1 

            # MW Calculation:
            correct_prob_sum += expected_prob
            total_prob_sum += (expected_prob + unexpected_prob)

    # Calculate EW score
    ew_score = (correct_count / total_count) if total_count > 0 else 0

    # MW = (Sum of expected probabilities) / (Sum of expected + unexpected probabilities)
    mw_score = (correct_prob_sum / total_prob_sum) if total_prob_sum > 0 else 0

    return ew_score, mw_score

# Files to run
file_paths = [
    '/home/bkherlen/NLPScholar/Midterm_Replication/rep-tse/bert_cased_analysis/simple_small_analysis_bert_byROI.tsv',
    '/home/bkherlen/NLPScholar/Midterm_Replication/rep-tse/bert_cased_analysis/vp_coord_small_analysis_bert_byROI.tsv',
    '/home/bkherlen/NLPScholar/Midterm_Replication/rep-tse/bert_cased_analysis/subj_rel_small_analysis_bert_byROI.tsv',
    '/home/bkherlen/NLPScholar/Midterm_Replication/rep-tse/bert_cased_analysis/sent_comp_small_analysis_bert_byROI.tsv',
    '/home/bkherlen/NLPScholar/Midterm_Replication/rep-tse/bert_cased_analysis/obj_rel_small_analysis_bert_byROI.tsv',
    '/home/bkherlen/NLPScholar/Midterm_Replication/rep-tse/bert_cased_analysis/obj_rel_no_that_small_analysis_bert_byROI.tsv'
]

for file_path in file_paths:
    ew_score, mw_score = calculate_ew_mw(file_path)
    print(f"File: {file_path}")
    print(f"Equally Weighted (EW) Score: {ew_score:.4f}")
    print(f"Model-Weighted (MW) Score: {mw_score:.4f}")
    print("-" * 40)