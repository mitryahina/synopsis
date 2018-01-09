from nltk.tokenize import word_tokenize
import pymorphy2


def read_for_chapters(file):
    '''
    file -> dict
    return: dictionary with name of chapter as key, words in chapter as value
    '''
    with open(file, 'r', encoding='utf-8') as file:
        punctuation = ['.', '!', '?', "-", '—', "...", '–', ',', "— ", "…",
                       ':', '*', "—", '(', ')', ';', '``']
        text = {}
        line = file.readline().strip()
        for i in range(19):
            chapter, name = "", file.readline().strip()
            line = file.readline().strip()
            while not line.startswith('РОЗДІЛ'):
                if line:
                    for x in line:
                        if x in punctuation: line = line.replace(x, "")
                    chapter += line + ' '
                line = file.readline().strip()
            chapter = word_tokenize(chapter)
            text[name] = chapter
    return text


def words_count(file):
    '''
    dict -> {dict}
    file: file with all documents
    return: dictionary with chapter as key, value - dictionary with
    word as key, count as value
    '''
    text = read_for_chapters(file)
    morph = pymorphy2.MorphAnalyzer(lang='uk')
    text1, count  = {}, 0
    for chapter in text:
        text1[chapter] = {}
        for word in text[chapter]:
            word = morph.parse(word)[0].normal_form
            if word not in text1[chapter]:
                text1[chapter][word] = 1
            else:
                text1[chapter][word] += 1
    return text1






