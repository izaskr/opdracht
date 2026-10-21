from parse_items_responses import StimuliItems
import stanza
import json
import wn

def add_lemma_to_list(words):
    """
    :param words: list of words whose lemma should be added
    :return: extended list of words
    """
    # example: words: ["wortelharen"]
    # extended words: ["wortelharen", "wortelhaar"]
    words = [w.lower() for w in words]
    extended_words = words.copy()
    nlp = stanza.Pipeline(lang="nl", processors="tokenize,pos,lemma")
    for one_word in words:
        # if the teachers' answer is a multi-word phrase, do not add lemmas of individual words
        if len(one_word.split()) > 1:
            continue
        #extended_words.append(one_word)
        doc = nlp(one_word)
        for sent in doc.sentences:
            for word in sent.words:
                lemma = word.lemma
                extended_words.append(lemma.replace("_", "")) # wortel_haar --> wortelhaar
    extended_words = set(extended_words)
    extended_words = list(extended_words)
    return extended_words


def add_synonyms_to_list(words):
    """"
    :param words: list of words whose synonyms should be added
    :return: extended list of words, including synonyms extracted from WordNet
    """
    words = [w.lower() for w in words]
    extended_words = words.copy()
    for one_word in words:
        # skip synonym search for multi-word answers
        if len(one_word.split()) > 1:
            continue
        word_info = wn.words(one_word, lang="nl", lexicon="omw-nl:2.0")[0]
        for synset in word_info.synsets():
            for syn in synset.words():
                if syn.lemma() not in extended_words:
                    extended_words.append(syn.lemma())
    return extended_words



def write_extended_into_file():
    d = {"i03": [], "i04": []}

    stimuli = StimuliItems("/home/skrjanec/cito_opdracht/data/items.txt")
    item_i03 = stimuli.item("i03")
    item_i04 = stimuli.item("i04")

    # item 3
    teacher_answers = item_i03['voorbeelden']
    first_answer, second_answer = [teacher_answers[0].split(":")[-1].strip()], [teacher_answers[1].split(":")[-1].strip()]

    # extend the list of teachers' answers with lemmas
    first_answer = add_lemma_to_list(first_answer)
    second_answer = add_lemma_to_list(second_answer)

    d["i03"] = [first_answer, second_answer]

    # item 4
    answers = item_i04['voorbeelden']
    answers = add_lemma_to_list(answers)
    answers = add_synonyms_to_list(answers)
    d["i04"] = answers

    with open("/home/skrjanec/cito_opdracht/data/extended_answers.json", "w") as f:
        json.dump(d, f)

write_extended_into_file()