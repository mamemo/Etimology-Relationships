from tec.ic.ia.p2.g07.Relation import Relation
from pyDatalog import pyDatalog

pyDatalog.create_terms('X, Y, Z, PX, PY, X1, Y1, X2, Y2, X3, Y3, Ancestor, Siblings, Cousins, Cousins2, Son, Uncle, Lang_related, Lang_and_origin, List_Lang_related, Common_words, Relevant_lang')

def siblings_query(first, second):
    Siblings(X, Y) <= (Relation.parent[X] == Z) & (Relation.parent[Y] == Z) & (X!=Y)
    Siblings(X, Y, PX, PY) <= Siblings(X,Y) & (Relation.child[X]==PX) & (Relation.child[Y]==PY)
    return Siblings(X, Y, first, second)

def cousins_query(first, second):
    Siblings(X, Y) <= (Relation.parent[X] == Z) & (Relation.parent[Y] == Z) & (X!=Y)
    Siblings(X, Y, PX, PY) <= Siblings(X,Y) & (Relation.child[X]==PX) & (Relation.child[Y]==PY)

    Son(X, PX, PY) <= (Relation.child[X]==PX) & (Relation.parent[X] == PY)
    Ancestor(X,Y) <= Son(X1, X, Y)
    Ancestor(X,Y) <= Son(X1, X, Z) & Ancestor(Z,Y)

    (Cousins2[X,Y]==rank_(group_by=X, order_by=Z)) <= Ancestor(X1,Y1) & (X==X1) & (Y==Y1) & (X==Z)

    Cousins(X, Y) <= Siblings(X1, Y1, Relation.parent[X], Relation.parent[Y])  #la que funciona
    Cousins(X, Y, PX, PY, Z) <= Cousins(X, Y) & (Relation.child[X]==PX) & (Relation.child[Y]==PY) & (Z==-1)
    Cousins(X, Y, PX, PY, Z) <= Ancestor(X1,Y1) & Cousins(X2, Y2) & (Relation.child[X] == X1)\
         & (Relation.child[X2] == Y1) & (Y == Y2) & (Relation.child[X] == PX) & (Relation.child[Y] == PY)\
         & (Cousins2[X3,Y3]==Z) & (X3 == X1) & (Y3==Y1)
    Cousins(X, Y, PX, PY, Z) <= Cousins(X, Y, PY, PX, Z)

    temp = Cousins(X, Y, first, second, Z)
    answer = [[x,y,z+2] for x,y,z in temp]

    return answer

def son_query(son, parent):
    Son(X, PX, PY) <= (Relation.child[X]==PX) & (Relation.parent[X] == PY)
    return Son(X, son, parent)

def uncle_query(uncle, nephew):
    Siblings(X, Y) <= (Relation.parent[X] == Z) & (Relation.parent[Y] == Z) & (X!=Y)
    Siblings(X, Y, PX, PY) <= Siblings(X,Y) & (Relation.child[X]==PX) & (Relation.child[Y]==PY)

    Uncle(X, Y) <= Siblings(X1, Y1, Relation.child[X], Relation.parent[Y])
    Uncle(X, Y, PX, PY) <= Uncle(X, Y) & (Relation.child[X]==PX) & (Relation.child[Y]==PY)

    return Uncle(X, Y, uncle, nephew)

def language_related_query(language, word):
    Lang_related(X, PX, PY) <= (Relation.child_lang[X] == PX) & (Relation.child[X] == PY)
    Lang_related(X, PX, PY) <= (Relation.child_lang[X] == PX) & (Relation.parent[X] == PY)
    Lang_related(X, PX, PY) <= (Relation.parent_lang[X] == PX) & (Relation.child[X] == PY)
    Lang_related(X, PX, PY) <= (Relation.parent_lang[X] == PX) & (Relation.parent[X] == PY)

    return Lang_related(X, language, word)

def language_and_origin_query(language, word):
    Son(X, PX, PY) <= (Relation.child[X]==PX) & (Relation.parent[X] == PY)
    Ancestor(X,Y) <= Son(X1, X, Y)
    Ancestor(X,Y) <= Son(X1, X, Z) & Ancestor(Z,Y)
    Lang_and_origin(X, PX, PY) <= (Relation.child_lang[X] == PX) & Ancestor(X1, Y1) & (Relation.child[X] == X1) & (Y1==PY)

    return Lang_and_origin(X, language, word)

def list_languages_related_query(word):
    answer = language_related_query(Y, word)
    languages = set([y for x,y in answer])

    return languages, answer

def common_words_query(language1, language2):
    Common_words(X,Y, PX, PY, Z) <= (Relation.child[X] == Relation.child[Y]) & (X!=Y) & (Relation.child_lang[X] != Relation.child_lang[Y]) & \
                (Relation.child_lang[X] == PX) & (Relation.child_lang[Y] == PY) & (Relation.child[X] == Z)
    Common_words(X,Y, PX, PY, Z) <= (Relation.parent[X] == Relation.parent[Y]) & (X!=Y) & (Relation.parent_lang[X] != Relation.parent_lang[Y]) & \
                (Relation.parent_lang[X] == PX) & (Relation.parent_lang[Y] == PY) & (Relation.parent[X] == Z)

    return Common_words(X,Y, language1, language2, Z)

def cont_common_words_query(language1, language2):
    answer = common_words_query(language1, language2)
    words = set([z for x,y,z in answer])

    return len(words), answer

def list_common_words_query(language1, language2):
    answer = common_words_query(language1, language2)
    words = set([z for x,y,z in answer])

    return words, answer

def relevant_language_query(language):
    (Relevant_lang[X, Y, PX]==rank_(group_by=Y, order_by=Z)) <= (Relation.child_lang[X]==PX) & (Relation.parent_lang[X]==Y) & (Relation.parent_lang[X]==Z)

    return (Relevant_lang[X, Y,language]== Z)

def percentages_relevant_language_query(language):
    answer = relevant_language_query(language)
    amount = dict()
    for i in answer:
        if i[1] not in amount.keys():
            amount[i[1]] = i[2]+1
    total = sum(amount.values())
    percentages = [[k, v*100/total] for k, v in amount.items()]

    return percentages,answer

def most_relevant_language_query(language):
    percentages,answer = percentages_relevant_language_query(language)
    perc = max(percentages, key=lambda x: x[1])
    return perc,percentages, answer
