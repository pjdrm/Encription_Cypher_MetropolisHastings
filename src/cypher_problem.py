import math
import random
import string
import numpy as np


def gen_rnd_cypher():
    position_cypher = range(26)
    random.shuffle(position_cypher)
    rnd_cypher = gen_cypher(position_cypher)
    return rnd_cypher

def gen_cypher(position_cypher):
    alphabet_list = list(string.ascii_uppercase)
    cypher_dic = {}
    for i in range(26):
        cypher_dic[alphabet_list[i]] = alphabet_list[position_cypher[i]]
    return cypher_dic

def get_cypher(cypher_dic):
    cypher = ""
    for char in string.ascii_uppercase:
        cypher += cypher_dic[char]
    return cypher

def cypher_txt(txt, cypher):
    char_list = list(txt)
    cypher_txt = ""
    for char in char_list:
        if char.upper() in string.ascii_uppercase:
            cypher_txt += cypher[char.upper()]
        else:
            cypher_txt += char
    return cypher_txt

def decypher_txt(txt, cypher):
    inv_cypher = {v: k for k, v in cypher.items()}
    char_list = list(txt)
    decypher_txt = ""
    for char in char_list:
        if char.upper() in string.ascii_uppercase:
            decypher_txt += inv_cypher[char.upper()]
        else:
            decypher_txt += " "
    return decypher_txt

def r_score_params(txt_path):
    with open(txt_path) as f:
        return score_params(f.read())
    
def score_params(txt):
    score_params_dic = {}
    for i in range(len(txt)-1):
        char_i = txt[i].upper()
        char_j = txt[i+1].upper()
        if char_i not in string.ascii_uppercase:
            char_i = " "
        if char_j not in string.ascii_uppercase:
            char_j = " "
        
        param = char_i + char_j
        if param in score_params_dic:
            score_params_dic[param] += 1
        else:
            score_params_dic[param] = 1
    return score_params_dic

def new_state_proposal(current_state_cypher):
    #the number of existing ascii letters is 26
    pos1 = random.randint(0, 25)
    pos2 = random.randint(0, 25)
    while pos1 == pos2:
        pos2 = random.randint(0, 25)
    proposed_state = dict(current_state_cypher)
    old_pos1_val = proposed_state[string.ascii_uppercase[pos1]]
    proposed_state[string.ascii_uppercase[pos1]] =  proposed_state[string.ascii_uppercase[pos2]]
    proposed_state[string.ascii_uppercase[pos2]] =  old_pos1_val
    return proposed_state
    

def cypher_score(txt, r_score_dic, cypher):
    dec_txt = decypher_txt(txt, cypher)
    f_score_dic = score_params(dec_txt)
    cypher_score = 0.0
    for param in f_score_dic:
        if param in r_score_dic:
            cypher_score += f_score_dic[param] * math.log(r_score_dic[param])
    return cypher_score

def MCMC_decrypt(n_iter, cipher_text, r_score_dic):
    current_state = gen_rnd_cypher()
    current_state_score = cypher_score(cipher_text, r_score_dic, current_state)
    for i in range(n_iter):
        print "Iteration %d" % (i)
        proposed_state = new_state_proposal(current_state)
        proposed_state_score = cypher_score(cipher_text, r_score_dic, proposed_state)
        coin_weight = min(1,math.exp(proposed_state_score-current_state_score))
        coin_flip = np.random.binomial(1, coin_weight)
        if coin_flip == 1:
            current_state = proposed_state
            current_state_score = proposed_state_score
    return current_state
            
        
    

txt = "As Oliver gave this first proof of the free and proper action of his lungs, \
the patchwork coverlet which was carelessly flung over the iron bedstead, rustled; \
the pale face of a young woman was raised feebly from the pillow; and a faint voice imperfectly \
articulated the words, Let me see the child, and die. \
The surgeon had been sitting with his face turned towards the fire: giving the palms of his hands a warm \
and a rub alternately. As the young woman spoke, he rose, and advancing to the bed's head, said, with more kindness \
than might have been expected of him: "

cypher = gen_rnd_cypher()
cypher_txt = cypher_txt(txt, cypher)
r_score_dic = r_score_params("war_and_peace.txt")
tru_cypher_score = cypher_score(cypher_txt, r_score_dic, cypher)
discovered_cypher = MCMC_decrypt(50000, cypher_txt, r_score_dic)
decipher_txt = decypher_txt(cypher_txt, discovered_cypher)


print decipher_txt
print "True cypher\n%s\nPredicted cypher\n%s" % (get_cypher(cypher), get_cypher(discovered_cypher))
