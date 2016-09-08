#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
from nltk.parse.stanford import StanfordParser
from translator.settings import STANFORD_PARSER_PATH, STANFORD_PARSER_MODEL_PATH
from translator.bingslate import BingTranslator
from translator.goslate import gtrans
from translator.SpgTable import SpgTable

s_parser = StanfordParser(STANFORD_PARSER_PATH, STANFORD_PARSER_MODEL_PATH)


def pattern(node, isLEAF, isTREE):
    if not isTREE(node):
        return ('', [], )
    res = ''
    try:
        LHS = node.label()
    except:
        LHS = '*'
    try:
        RHS = ' '.join(child if isLEAF(child) else child.label() for child in node)
    except:
        RHS = '* * *'
    RULE = LHS + '->' + RHS

    try:
        if RULE == 'ADJP->JJ PP':  # use ADJ pattern Grammar
            res = '%s %s %s' % (node[0][0], node[1][0][0], node[1][1].label())
            RHS = [node[0][0], node[1][0][0], node[1][1]]
            # res is "harmful to NP"
            # print 'DEBUG 7 Pattern', res, RHS, (res and res in SpgTable)
        elif RULE == 'ADJP->RB JJ PP':  # (RB very) (JJ nice) (PP to foreign visitors)
            res = '%s %s %s %s' % (node[0].label(), node[1][0], node[2][0][0], node[2][1].label())
            RHS = [node[0], node[1][0], node[2][0][0], node[2][1]]
        elif RULE == 'ADJP->JJ S':
            res = '%s %s' % (node[0][0], node[1].label())
            RHS = [node[0][0], node[1]]
        elif RULE == 'ADJP->RB JJ S':
            # two kinds of pattern : "adv. JJ S" or "RB adj. S"
            res = '%s %s %s' % (node[0][0], node[1].label(), node[2].label())  # too busy to spend time with their children
            RHS = [node[0][0], node[1], node[2]]

            if res not in SpgTable:
                res = '%s %s %s' % (node[0].label(), node[1][0], node[2].label())  # so happy to hear your voice
                RHS = [node[0], node[1][0], node[2]]

        elif RULE == 'ADJP->JJ RB':
            res = '%s %s' % (node[0].label(), node[1].label())
            RHS = [node[0], node[1]]
        elif RULE == 'ADJP->JJ RB S':  # big enough S
            res = '%s %s %s' % (node[0][0], node[1].label(), node[2].label())
            RHS = [node[0][0], node[1], node[2]]
        elif RULE == 'S->NP ADJP':
            res = '%s %s' % (node[0].label(), node[1].label())
            RHS = [node[0], node[1]]
            # res is "NP ADJP"
        elif RULE == 'SBAR->IN S':  # (IN After) (S we left the library)
            res = '%s %s' % (node[0][0], node[1].label())
            RHS = [node[0], node[1]]
        elif RULE == 'NP->NP SBAR':
            res = '%s %s' % (node[0].label(), node[1].label())
            RHS = [node[0], node[1]]
            # res is "NP SBAR"
        elif RULE == 'PP->IN NP':  # before 8 o'clock
            res = '%s %s' % (node[0][0], node[1].label())
            RHS = [node[0][0], node[1]]
        elif RULE == 'VP->VBP ADJP':
            res = '%s %s' % (node[0][0], node[1].label())
            RHS = [node[0][0], node[1]]
            # res is "consider ADJP"
        elif RULE == 'VP->VB S':
            res = '%s %s' % (node[0][0], node[1].label())
            RHS = [node[0][0], node[1]]
            # res is "contain S"
        elif RULE in ['VP->VB PP', 'VP->VBG PP', 'VP->VBD PP', 'VP->VBN PP', 'VP->VBP PP', 'VP->VBD PP', 'VP->VBZ PP']:  # use verb pattern grammar
            res = '%s %s %s' % (node[0][0], node[1][0][0], node[1][1].label())
            RHS = [node[0][0], node[1][0][0], node[1][1]]

        elif RULE == 'VP->VBZ ADJP S':  # is impossbile for sb to S
            res = '%s %s %s' % (node[0].label(), node[1].label(), node[2].label())
            RHS = [node[0], node[1], node[2]]

        elif RULE in ['VP->VB PRT PP', 'VP->VBZ PRT PP', 'VP->VBN PRT PP', 'VP->VBD PRT PP', 'VP->VBG PRT PP']:  # go out on a typhoon day
            res = '%s %s %s %s' % (node[0][0], node[1][0][0], node[2][0][0], node[2][1].label())
            RHS = [node[0][0], node[1][0][0], node[2][0][0], node[2][1]]

        elif RULE == 'VP->VB PP NP':  # VB:go PP:to school NP:today
            res = '%s %s %s' % (node[0].label(), node[1].label(), node[2].label())
            RHS = [node[0], node[1], node[2]]

        elif RULE in ['VP->VB NP PP', 'VP->VBN NP PP', 'VP->VBZ NP PP', 'VP->VBD NP PP', 'VP->VB NP PP', 'VP->VBG NP PP']:  # VB:send NP:my best wishes PP:to them
            res = '%s %s %s %s' % (node[0][0], node[1].label(), node[2][0][0], node[2][1].label())
            RHS = [node[0], node[1], node[2][0], node[2][1]]

            if res not in SpgTable:
                res = '%s %s %s' % (node[0].label(), node[1].label(), node[2].label())
                RHS = [node[0], node[1], node[2], node[2]]

        elif RULE == 'VP->VBP NP NP':  # I (VBP watch) (NP the basketball game) (NP yesterday)
            res = '%s %s %s' % (node[0].label(), node[1].label(), node[2].label())
            RHS = [node[0], node[1], node[2]]
        elif RULE == 'VP->VBD NP NP':
            res = '%s %s %s' % (node[0].label(), node[1].label(), node[2].label())
            RHS = [node[0], node[1], node[2]]
        elif RULE == 'VP->VBN ADVP':  # decided yet
            res = '%s %s' % (node[0].label(), node[1].label())
            RHS = [node[0], node[1]]
        elif RULE == 'VP->VBD ADVP':  # (VBD drove) (ADVP too fast)
            res = '%s %s' % (node[0].label(), node[1].label())
            RHS = [node[0], node[1]]
        elif RULE == 'VP->VBP ADVP PP':  # (VBP stay) (ADVP there) (PP with their families for several months)

            res = '%s %s %s %s' % (node[0][0], node[1].label(), node[2][0][0], node[2][1].label())  # use SPG first
            RHS = [node[0][0], node[1], node[2][0], node[2][1]]

            if res not in SpgTable:
                res = '%s %s %s' % (node[0].label(), node[1].label(), node[2].label())
                RHS = [node[0], node[1], node[2]]

        elif RULE in ['VP->VB NP ADVP', 'VP->VBN NP ADVP', 'VP->VBZ NP ADVP', 'VP->VBD NP ADVP', 'VP->VBP NP ADVP']:
            # VB:miss NP:you ADVP:very much
            res = '%s %s %s' % (node[0].label(), node[1].label(), node[2].label())
            RHS = [node[0], node[1], node[2]]
        elif RULE == 'VP->VB NP S':
            res = '%s %s %s' % (node[0].label(), node[1].label(), node[2].label())
            RHS = [node[0], node[1], node[2]]
        elif RULE == 'VP->VBD PRT NP':  # (VBD gave) (PRT up) (NP the idea of becoming a doctor)
            res = '%s %s %s' % (node[0][0], node[1][0][0], node[2].label())  # use SPG
            RHS = [node[0], node[1], node[2]]
        elif RULE in ['VP->VBD NP', 'VP->VB NP', 'VP->VBZ NP', 'VP->VBN NP', 'VP->VBP NP']:
            if node[1][0].label() == 'NP' and node[1][1].label() == 'PP':  # VB:take NP-NP:care NP-PP:of NP
                res = '%s %s %s %s' % (node[0][0], node[1][0][0][0], node[1][1][0][0], node[1][1][1].label())
                RHS = [node[0][0], node[1][0][0][0], node[1][1][0][0], node[1][1][1]]

        elif RULE in ['SBARQ->WHADJP SQ .', 'SBARQ->WHADJP SQ', 'SBARQ->WHADJP S .', 'SBAR->WHADJP S']:
            res = '%s %s' % (node[0][0][0], node[1].label())
            RHS = [node[0], node[1]]
        else:
            res = RHS
            RHS = [child for child in node]
    except:
        pass

    return (res, RHS,)


def lexicalizeTree(node, isLEAF, isTREE):
    if isLEAF(node):
        return
    # depth-first search
    for child in node:
        lexicalizeTree(child, isLEAF, isTREE)
    pat, RHS = pattern(node, isLEAF, isTREE)

    if pat and pat in SpgTable:
        for j in range(len(node)):
            del node[-1]
        for k, _ in enumerate(RHS):
            node.insert(k, RHS[k])
    return


def lexSynTree(node, parent, isLEAF, isTREE):
    if isLEAF(node):
        return
    tags = ['NP', 'PP', 'ADJP', 'VP', 'PRT', 'RB', 'JJ', 'S', 'SBAR']
    # reorder subtree
    pat, RHS = pattern(node, isLEAF, isTREE)
    if pat != '' and pat in SpgTable:
        print('-- %s %s' % (pat, SpgTable[pat]))
        global FIND_SPG
        FIND_SPG = True
        # print FIND_SPG
        # 'harmful to NP':[u'對 NP 有害', {0:0, 1:2, 2:2} ],
        RHSlabel, ALIGN = SpgTable[pat]
        RHSlabel = RHSlabel.split()
        # reorder
        RHSreo = [RHS[ALIGN[i]] if (RHSlabel[i][-1] == 'P' or RHSlabel[i][0] == 'S' or RHSlabel[i][0] == 'V' or RHSlabel[i] in tags) else
                  RHSlabel[i] for i in range(len(RHSlabel))]
        for j in range(len(node)):
            del node[-1]
        for k, child in enumerate(RHSreo):
            node.insert(k, child)

    # Depth-first search
    for child in node:
        lexSynTree(child, node, isLEAF, isTREE)


def LinearizeTree(node, isLEAF, isTREE):
    if isLEAF(node):
        return node
    res = []
    for child in node:
        res1 = LinearizeTree(child, isLEAF, isTREE)
        res += res1 if type(res1) == list else [res1]
    return res


def spg_translate(sent):
    parseTree = [tree for tree in s_parser.raw_parse(sent)]
    lexTree = copy.deepcopy(parseTree[0])
    # lexTree.draw()

    lexicalizeTree(lexTree, lambda x: type(x) != type(lexTree), lambda x: type(x) == type(lexTree))
    # lexTree.draw()

    synTree = copy.deepcopy(parseTree[0])
    lexSynTree(synTree, None, lambda x: type(x) != type(synTree), lambda x: type(x) == type(synTree))
    # synTree.draw()

    string = LinearizeTree(synTree, lambda x: type(x) != type(synTree), lambda x: type(x) == type(synTree))

    spg_sent = ' '.join(string)

    res = {
        'SPG': spg_sent,
        'Google Translate': gtrans(sent, 'zh-TW'),
        'Bing Translator': bingmt.translate_one(sent),
        'GLinggle': gtrans(spg_sent, 'zh-TW'),
        'BLinggle': bingmt.translate_one(spg_sent),
    }
    return res


bingmt = BingTranslator()

if __name__ == '__main__':
    sents = ['harmful to environment', 'harmful to brain', 'leave from Seatle']

    for sent in sents:
        print('Input:', sent)
        result = spg_translate(sent)
        for key, res in result.items():
            print(key, '==>', res)
