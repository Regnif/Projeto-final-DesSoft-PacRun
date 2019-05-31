# -*- coding: utf-8 -*-
"""
Created on Fri May 31 10:34:01 2019

@author: Erick
"""

def high_score(score):
    with open("high_score.txt", "r") as arquivo:
        conteudo = arquivo.read()
        
    numero = int(conteudo)
    
    if score > numero:
        with open("high_score.txt", "w") as arquivo:
            arquivo.write(str(score))
        return score
    else:
        return numero
