import pandas as pd 
import csv

def same_char(word1:str, word2:str)->int:
    """ 
        This function calculates how many characters in word1 are 
        equals in word2 and returns your equivalence. The occurrence 
        of the characters is important. 

        Parameters
        ----------
        word1 : str
        Word that will be compared 

        word2 : str
        Base word, that will be the target of comparade

        Returns
        -------
        percent : double
        correlation between word1 and word2

        Examples
        --------
        >>>same_char('fy','fly')
        0.6666666666666666
        >>>same_char('fly','fly')
        1.0
    """
    word1_size = len(word1)
    word2_size = len(word2)
    initial_word2 = 0
    equals = 0
    for i in range(0,word1_size):
        local = word2[initial_word2:word2_size].find(word1[i])
        if  local != -1:
            initial_word2 += local + 1
            equals += 1
    percent = equals/word2_size
    return percent

def complete_word(word:str):
    """
        This function is used to standardise 'geographical words'
        (in portugues)
        
        Parameters
        ----------
        word: str
        The word that will be transformed

        Results
        -------
        word_return : str
        Word standardized

        Examples
        --------
        >>>word = complete_word('av')
        >>>print(word)
        AVENIDA
        >>>word = complete_word('aneida')
        >>>print(word)
        AVENIDA

    """
    data_path = "GeoAPI/Data/Tabela_abreviações.csv"
    file_ = open(data_path, 'r')
    data = csv.reader(file_)
    columns = next(data)
    values = []
    for row in data :
        len_row = len(row)
        for i in range(0,len_row):
            row[i] = row[i].upper()
        values.append(row)
    word = word.upper()
    count_equals = 0
    word_return = None
    for row in values:
        if((word == row[2]) or (word == row[1])):
            word_return = row[1]
    if word_return == None:
        for row in values:
            count_aux = same_char(word, row[1])
            if count_aux > count_equals:
                count_equals = count_aux
                word_return = row[1]
    return word_return
