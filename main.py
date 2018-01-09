import pymorphy2, copy
from nltk.tokenize import word_tokenize, sent_tokenize
from idf_info import words_count, read_for_chapters
from tf_idf_coef_count import tf_idf_count


def read_text(file):
    '''
    file -> (list, list)
    file: input text you want to summarize
    return: sentences - list with sentences(type == str)
            separated - list with sentences(type == list) divided
            into words (type == str)
    '''
    with open(file, 'r', encoding='utf-8') as file:
        sentences = ""
        punctuation = ['.', '!', '?', '—', "...", '–', ',', "…",
                       ':', '*', "—", '(', ')', ';', '``']
        for line in file:
            sentences += line.strip() + ' '
        sentences = sent_tokenize(sentences)
        separated, index = copy.copy(sentences), 0
        for sentence in separated:
            sentence = word_tokenize(sentence)
            for i in sentence:
                if i in punctuation:
                    sentence.remove(i)
            if len(sentence) > 1:
                separated[index] = sentence
                index += 1
    return sentences, separated


def count_sentence(text, idf_tf_normal, text1):
    '''
    (list, dictionary, list) -> tuple(float, string)
    text: list with sentences divided into words
    idf_tf_normal: dictionary with normal form of word as key, tf-idf coef
    as value
    text1: text, divided only into sentences
    return: list with 6 the most important sentences; float - tf-idf coeff,
    str - sentence
    '''
    values, morph = [], pymorphy2.MorphAnalyzer(lang='uk')
    for sentence in text:
        value, len = 0, 0
        for word in sentence:
            len += 1
            value += idf_tf_normal[morph.parse(word)[0].normal_form]
        if len > 1:
            values.append(value/len)
    important = (list(zip(values, text1)))
    # finding of middle value
    mid = (max(important)[0]+min(important)[0])/2
    summary = [x for x in important if x[0] >= mid]


    return summary


your_text, whole = read_text('part.txt'), words_count('Potter.txt')
words_coefficient = tf_idf_count(whole, your_text[1])
important = count_sentence(your_text[1], words_coefficient, your_text[0])

# saving of summary into the file
with open('summary', 'w', encoding='utf-8') as file:
    for part in important:
        file.write(part[1])
print(important)












