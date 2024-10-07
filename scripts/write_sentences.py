import csv
import random

def get_verbs(filename):
    verbs = []
    with open(filename, "r", encoding = "utf-8-sig") as file:
        lines = file.readlines()[1:]
        for line in lines:
            items = line.split(",")
            verb = []
            sing = items[1]
            plur = items[2]
            verb.append(sing)
            verb.append(plur)
            verbs.append(verb)
    return verbs

def distribute_verbs(verbs, contexts):
    verbs_per_context = len(verbs)//len(contexts)
    leftovers = len(verbs)%len(contexts)
    context_to_verb = {}
    random.shuffle(contexts) # shuffles the context list for every condition, so that the lemmas used for each context are rotated across conditions
    for context in contexts:
        context_to_verb[context] = verbs_per_context
        if leftovers >= 1:
            context_to_verb[context] += 1
            leftovers -= 1
    return context_to_verb

def write_sentences(verbs, contexts, condition):
    header = ["sentid", "contextid", "pairid", "comparison", "lemma", "condition", "sentence", "ROI"]
    data = []
    data.append(header)
    sentid = 0
    contextid = 0
    pairid = 0
    
    context_to_verb = distribute_verbs(verbs, contexts)
    curr_verb = 0

    if condition == "simple":
        for context in context_to_verb.keys():
            contextid += 1
            lemmas_limit = context_to_verb[context]

            for i in range(lemmas_limit):
                verb_pair = verbs[curr_verb]
                lemma = verb_pair[1]
                pairid += 1
                if context[-1] == "s": # NP is plural
                    setence = "The "+context+" "+verb_pair[0]
                    sentid += 1
                    row = [sentid, contextid, pairid, "unexpected", lemma, condition, setence, 2]
                    data.append(row)
                    
                    sentid += 1
                    setence = "The "+context+" "+verb_pair[1]
                    row = [sentid, contextid, pairid, "expected", lemma, condition, setence, 2]
                    data.append(row)
                    
                else: # NP is singular
                    setence = "The "+context+" "+verb_pair[1]
                    sentid += 1
                    row = [sentid, contextid, pairid, "unexpected", lemma, condition, setence, 2]
                    data.append(row)
                    
                    sentid += 1
                    setence = "The "+context+" "+verb_pair[0]
                    row = [sentid, contextid, pairid, "expected", lemma, condition, setence, 2]
                    data.append(row)
                
                curr_verb += 1
    
    elif condition == "sent_comp":
        for context in context_to_verb.keys():
            sbj = random.choice(contexts)
            mvs = ["say", "think", "know"]
            mv = random.choice(mvs)
            if sbj[-1] == "s":
                ms = "The "+sbj+" "+mv
            else: 
                ms = "The "+sbj+" "+mv+"s"
            
            contextid += 1
            lemmas_limit = context_to_verb[context]

            for i in range(lemmas_limit):
                verb_pair = verbs[curr_verb]
                lemma = verb_pair[1]
                pairid += 1

                if context[-1] == "s": # NP is plural
                    setence = ms+" the "+context+" "+verb_pair[0]
                    sentid += 1
                    row = [sentid, contextid, pairid, "unexpected", lemma, condition, setence, 5]
                    data.append(row)
                        
                    sentid += 1
                    setence = ms+" the "+context+" "+verb_pair[1]
                    row = [sentid, contextid, pairid, "expected", lemma, condition, setence, 5]
                    data.append(row)
                    
                else: # NP is singular
                    setence = ms+" the "+context+" "+verb_pair[1]
                    sentid += 1
                    row = [sentid, contextid, pairid, "unexpected", lemma, condition, setence, 5]                        
                    data.append(row)
                        
                    sentid += 1
                    setence = ms+" the "+context+" "+verb_pair[0]
                    row = [sentid, contextid, pairid, "expected", lemma, condition, setence, 5]
                    data.append(row)
                
                curr_verb += 1

    elif condition == "vp_coord":
        for context in context_to_verb.keys():
            contextid += 1
            lemmas_limit = context_to_verb[context]
            vp1 = random.choice(verbs)

            for i in range(lemmas_limit):
                verb_pair = verbs[curr_verb]
                lemma = verb_pair[1]
                pairid += 1
    
                if context[-1] == "s": # NP is plural
                    v1 = vp1[1] # first verb (before and) is always grammatical
                    setence = "The "+context+" "+v1+" and "+verb_pair[0]
                    sentid += 1
                    row = [sentid, contextid, pairid, "unexpected", lemma, condition, setence, 4]
                    data.append(row)
                    
                    sentid += 1
                    setence = "The "+context+" "+v1+" and "+verb_pair[1]
                    row = [sentid, contextid, pairid, "expected", lemma, condition, setence, 4]
                    data.append(row)
                    
                else: # NP is singular
                    v1 = vp1[0]
                    setence = "The "+context+" "+v1+" and "+verb_pair[1]
                    sentid += 1
                    row = [sentid, contextid, pairid, "unexpected", lemma, condition, setence, 4]
                    data.append(row)
                    
                    sentid += 1
                    setence = "The "+context+" "+v1+" and "+verb_pair[0]
                    row = [sentid, contextid, pairid, "expected", lemma, condition, setence, 4]
                    data.append(row)
                
                curr_verb += 1

    elif condition == "subj_rel":
        for context in context_to_verb.keys():
            contextid += 1
            lemmas_limit = context_to_verb[context]
            vp1 = random.choice(verbs)
            obj = random.choice(contexts)

            for i in range(lemmas_limit):
                verb_pair = verbs[curr_verb]
                lemma = verb_pair[1]
                pairid += 1

                if context[-1] == "s": # NP is plural
                    v1 = vp1[1]

                    setence = "The "+context+" that "+v1+" the "+obj+" "+verb_pair[0]
                    sentid += 1
                    row = [sentid, contextid, pairid, "unexpected", lemma, condition, setence, 6]
                    data.append(row)
                    
                    sentid += 1
                    setence = "The "+context+" that "+v1+" the "+obj+" "+verb_pair[1]
                    row = [sentid, contextid, pairid, "expected", lemma, condition, setence, 6]
                    data.append(row)
                    
                else: # NP is singular
                    v1 = vp1[0]

                    setence = "The "+context+" that "+v1+" the "+obj+" "+verb_pair[1]
                    sentid += 1
                    row = [sentid, contextid, pairid, "unexpected", lemma, condition, setence, 6]
                    data.append(row)
                    
                    sentid += 1
                    setence = "The "+context+" that "+v1+" the "+obj+" "+verb_pair[0]
                    row = [sentid, contextid, pairid, "expected", lemma, condition, setence, 6]
                    data.append(row)
                
                curr_verb += 1
    
    elif condition == "obj_rel":
        for context in context_to_verb.keys():
            contextid += 1
            lemmas_limit = context_to_verb[context]
            vp1 = random.choice(verbs)
            subj = random.choice(contexts)
            if subj[-1] == "s": # if subject of relative clause is plural
                v1 = vp1[1]
            else:
                v1 = vp1[0]
            rc = " that the "+subj+" "+v1+" "

            for i in range(lemmas_limit):
                verb_pair = verbs[curr_verb]
                lemma = verb_pair[1]
                pairid += 1

                if context[-1] == "s": # NP is plural
                    setence = "The "+context+rc+verb_pair[0]
                    sentid += 1
                    row = [sentid, contextid, pairid, "unexpected", lemma, condition, setence, 6]
                    data.append(row)
                    
                    sentid += 1
                    setence = "The "+context+rc+verb_pair[1]
                    row = [sentid, contextid, pairid, "expected", lemma, condition, setence, 6]
                    data.append(row)
                    
                else: # NP is singular
                    setence = "The "+context+rc+verb_pair[1]
                    sentid += 1
                    row = [sentid, contextid, pairid, "unexpected", lemma, condition, setence, 6]
                    data.append(row)
                    
                    sentid += 1
                    setence = "The "+context+rc+verb_pair[0]
                    row = [sentid, contextid, pairid, "expected", lemma, condition, setence, 6]
                    data.append(row)
                
                curr_verb += 1
    
    elif condition == "obj_rel_no_that":
        for context in context_to_verb.keys():
            contextid += 1
            lemmas_limit = context_to_verb[context]
            vp1 = random.choice(verbs)
            subj = random.choice(contexts)
            if subj[-1] == "s": # if subject of relative clause is plural
                v1 = vp1[1]
            else:
                v1 = vp1[0]
            rc = " the "+subj+" "+v1+" "

            for i in range(lemmas_limit):
                verb_pair = verbs[curr_verb]
                lemma = verb_pair[1]
                pairid += 1

                if context[-1] == "s": # NP is plural
                    setence = "The "+context+rc+verb_pair[0]
                    sentid += 1
                    row = [sentid, contextid, pairid, "unexpected", lemma, condition, setence, 5]
                    data.append(row)
                    
                    sentid += 1
                    setence = "The "+context+rc+verb_pair[1]
                    row = [sentid, contextid, pairid, "expected", lemma, condition, setence, 5]
                    data.append(row)
                    
                else: # NP is singular
                    setence = "The "+context+rc+verb_pair[1]
                    sentid += 1
                    row = [sentid, contextid, pairid, "unexpected", lemma, condition, setence, 5]
                    data.append(row)
                    
                    sentid += 1
                    setence = "The "+context+rc+verb_pair[0]
                    row = [sentid, contextid, pairid, "expected", lemma, condition, setence, 5]
                    data.append(row)
                
                curr_verb += 1

    return data

def main():
    verbs = get_verbs("combined_verb_list.csv")
    contexts = ["authors", "pilots", "surgeons", "farmers", "managers", "customers", "officers", "teachers", "senators", "consultants",
                "author", "pilot", "surgeon", "farmer", "manager", "customer", "officer", "teacher", "senator", "consultant"]
    conditions = ["simple", "sent_comp", "vp_coord", "subj_rel", "obj_rel", "obj_rel_no_that"]
    
    data = write_sentences(verbs, contexts, "obj_rel_no_that")
    with open("obj_rel_no_that_small.tsv", "w", newline="") as file:
        writer = csv.writer(file, delimiter="\t") # separate with tabs
        writer.writerows(data)

if __name__ == "__main__":
    main()