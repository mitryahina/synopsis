import nltk
import math
import string
from nltk.collocations import *
from nltk.tokenize import word_tokenize, sent_tokenize, TweetTokenizer


def read_file(file_name):
    """
    Returns a string of text from file.
    :param string file_name: The name of the file.
    :return string text: Parsed text from the file.
    """
    text_file = open(file_name, encoding='utf-8')
    text = text_file.read().replace('\n', ' ')
    return text


def parse_file(file_name):
    """
    Returns list of lists of sentences and words.
    :param string file_name: The name of the file.
    :return list sentences: List of lists of sentences of words.
    """
    punctuations = list(string.punctuation)
    punctuations += ["...", "–", "''", "``", '—', '..', '”']
    text_file = open(file_name, encoding='utf-8')
    text = text_file.read().replace('…', '...')
    sentences = sent_tokenize(text)
    for i, sentence in enumerate(sentences):
        sentences[i] = [word for word in word_tokenize(sentence) if word not in punctuations]
    return sentences


def list_words(sentences):
    """
    Returns list of words from list of sentences.
    :param list sentences: List of lists of sentences of words.
    :return list wordlist: List of words.
    """
    wordlist = []
    for i in range(len(sentences)):
        for word in sentences[i]:
            word = word.lower()
            if word not in set(stop_words):
                wordlist.append(word)
    return wordlist


def create_freqtable(wordlist):
    """
    Returns a frequency dictionary with words as keys and frequencies as values.
    :param list wordlist: List of words.
    :return dictionary freq_table: Words and their frequencies.
    """
    freq_table = dict()
    for word in wordlist:
        word = word.lower()
        if word in set(stop_words):
            continue
        if word in freq_table:
            freq_table[word] += 1
        else:
            freq_table[word] = 1
    return freq_table


def find_sent_value(sentlist):
    """
    Returns a dictionary of sentence values, sum of all values.
    :param list sentlist: List of sentences.
    :return dictionary sentence_value: sentences as keys and their values as values.
    :return integer sum_values: Sum of all sentence values.
    """
    sentence_value = dict()
    for sentence in sentlist:
        for key in freq_table:
            if key in sentence.lower():
                if sentence in sentence_value:
                    sentence_value[sentence] += freq_table[key]
                else:
                    sentence_value[sentence] = freq_table[key]
        for bigram in top_bigrams:
            if bigram[0][0] and bigram[0][1] in sentence.lower():
                if sentence in sentence_value:
                    sentence_value[sentence] += math.ceil(bigram[1])
                else:
                    sentence_value[sentence] = math.ceil(bigram[1])
    sum_values = 0
    for sentence in sentence_value:
        sum_values += sentence_value[sentence]

    return sentence_value, sum_values


def print_summary(sentlist, sum_values, sentence_value, file_output=True):
    """
    Prints the most popular sentences from the list to console or to "Summary.txt" file.
    :param list sentlist: List of sentences.
    :param integer sum_values: Sum of all sentence values.
    :param dictionary sentence_value: Dictionary with sentences and their values.
    :param file_output: if True, result is printed to file.
    """
    k = 1 # summary size coeficient
    average = int(sum_values/ len(sentence_value))
    summary = ''
    for sentence in sentlist:
        if sentence in sentence_value and sentence_value[sentence] > (k * average):
            summary +=  " " + sentence
    if file_output:
        output_file_name = file_name.replace(".txt", "_summary.txt")
        with open(output_file_name, "w", encoding="utf-8") as f:
            print(summary, file=f)
    else:
        print(summary)


file_name = "example_text.txt"
sentlist = sent_tokenize(open(file_name, encoding="utf-8").read())
sentences = parse_file(file_name)
stop_words = word_tokenize(read_file("stopwords.txt"))
wordlist = list_words(sentences)

bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(wordlist)
scored = finder.score_ngrams(bigram_measures.raw_freq)
#sorted_bigrams = sorted(bigram for bigram, score in scored)
top_bigrams = scored[:20]

freq_table = create_freqtable(wordlist)
sentence_value, sum_values = find_sent_value(sentlist)

print_summary(sentlist, sum_values, sentence_value)
