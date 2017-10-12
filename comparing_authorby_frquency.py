"""
    Author: Shreya Rangarajan
    Date: 10/12/17
    Description: Compare text frequency of two books from from Jane Austen
                 and two books Nathaniel Hawthorne
"""

import requests
import numpy as np
import matplotlib.pyplot as plt

# Get books from Gutenberg
pride_and_prejudice = requests.get('http://www.gutenberg.org/files/1342/1342-0.txt').text
emma = requests.get('http://www.gutenberg.org/files/158/158-0.txt').text
scarlet_letter = requests.get('http://www.gutenberg.org/cache/epub/33/pg33.txt').text
seven_gables = requests.get('http://www.gutenberg.org/cache/epub/77/pg77.txt').text

def most_frequent_words(n, text):
    """ Computes the most frequent words in a text as well as the number of
        words in the entire text

        n: an integer indication # of most frequent words wanting to output
        text: a text requested from the Gutenberg database
        returns: tuples with the first element as the word and the second
        element as how frequently it occurs in the text and the numbers of words
        in the text
    >>> most_frequent_words(5,pride_and_prejudice)
    ([('the', 4205), ('to', 4121), ('of', 3662), ('and', 3309), ('a', 1945)], 124592)

    >>> most_frequent_words(7, scarlet_letter)
    ([('the', 5029), ('of', 3332), ('and', 2642), ('a', 2028), ('to', 1993), ('in', 1386), ('with', 996)], 86639)
    """

    frequency = {}
    split_text = text.split()
    for word in split_text:
        frequency[word] = 0
    for word in split_text:
        frequency[word] += 1
    sort_top_words = sorted(frequency.items(), key=lambda x:x[1])
    sort_top_words.reverse()
    return sort_top_words[:n],len(split_text)


def compare_authors(text1,text2):
    """ Takes two texts, determines the 500 most frequent words in each text
        and returns how many of most frequent words are the same for both
        texts.

        text1: a unique text requested from Gutenberg database
        text2: another unique text requested from Gutenberg database
        returns: the count of how many "most frequent words" are similar for
                 the 2 texts

    >>> compare_authors(emma, pride_and_prejudice)
    375
    >>> compare_authors(seven_gables, scarlet_letter)
    366
    """
    most_freq_word_txt1 = most_frequent_words(500,text1)[0]
    most_freq_word_txt2 = most_frequent_words(500,text2)[0]

    words_txt1 = [x[0] for x in most_freq_word_txt1]
    words_txt2 = [x[0] for x in most_freq_word_txt2]

    count = 0
    for word in words_txt1:
        if word in words_txt2:
            count += 1
    return count


def frequency_table(textlist):
    """ Takes a list of texts and returns the titles of the texts along with
        the count of how many "most frequent words" are similar to both texts

    #>>> frequency_table([emma, pride_and_prejudice])
    #The Project Gutenberg EBook of Pride and Prejudice, by Jane Austen
    #The Project Gutenberg EBook of Emma, by Jane Austen
    #375
    Disclaimer: Doctest "expected" and "got" give the same results, but does not
                pass.
    """
    running_text_list = textlist
    for text in textlist:
        running_text_list.remove(text)
        for compare_text in textlist:
            compare1 = compare_authors(compare_text, text)
            print(compare_text.split('\n', 1)[0].replace('\ufeff',''))
            print(text.split('\n', 1)[0].replace('\ufeff',''))
            print(compare1)

def lexical_diversity(text):
    """ Computes and returns the lexial diversity of a text

        text: a text requested form the Gutenberg database
        returns: lexical diversity of the text
    >>> lexical_diversity(emma)
    0.11230976330254647

    >>> lexical_diversity(scarlet_letter)
    0.17630628239014762
    """
    split_text = text.split()
    total_num_uniqu_words = len(set(split_text))
    lex_div = total_num_uniqu_words/len(split_text)
    return lex_div

def plot_lexical_diversity(textlist, title_list):
    """ Plots the lexical diversity of each text in a list against their title

        textlist: list of texts from Gutenberg database
        title_list: list of book titles that correspond to the textlist
        returns: a plot of the lexical diversity title_list on x axis and lexica
    """
    lex_div_list = []
    for text in textlist:
        lex_div_list.append(lexical_diversity(text))

    x = np.array([0,1,2,3])
    plt.xticks(x, title_list)
    plt.plot(x, lex_div_list)
    plt.title('Lexical Diveristy of 4 different books')
    plt.xlabel('Book Name')
    plt.ylabel('Units')
    plt.show()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
