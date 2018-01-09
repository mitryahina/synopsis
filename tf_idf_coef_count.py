import pymorphy2, math



def tf_count(separated):
    '''
    list(list(str)) -> dict
    text1: list with lists as sentence and str - words
    return: dictionary with word as key and TF as value
    '''
    term_frequency_normal, length = {}, 0
    morph = pymorphy2.MorphAnalyzer(lang='uk')
    for sentence in separated:
        length += len(sentence)
        for word in sentence:
            word1 = morph.parse(word)[0].normal_form
            if word1 not in term_frequency_normal:
                term_frequency_normal[word1] = 1
            else:
                term_frequency_normal[word1] += 1
    for key in term_frequency_normal:
        term_frequency_normal[key] /= length
    return term_frequency_normal


def tf_idf_count(whole, separated):
    '''
    (dict, list) -> dict
    whole: dictionary with information from whole file, chapter as key,
    text in chapter as value. document (for idf) == chapter.
    separated: list with lists as sentences divided into words as string
    return: dictionary with normal form of the word as key, tf-idf coeff as
    value
    '''
    D, idf_tf_normal = 18, tf_count(separated)
    for word in idf_tf_normal:
        count = 0
        for chapter in whole:
            if word in whole[chapter]:
                count += 1
        try:
            idf_tf_normal[word] *= math.log2(D/count)
        except ZeroDivisionError:
            idf_tf_normal[word] = 0.02

    return idf_tf_normal