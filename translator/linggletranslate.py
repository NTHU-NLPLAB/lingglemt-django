#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import urllib2
from nltk.parse.stanford import StanfordParser
from bingslate import BingTranslator
import sys
VERBATIM = False

gtrans_url = 'http://translate.google.com/m?hl=%s&sl=%s&q=%s'


def gtrans(to_translate, to_langage='zh-TW', langage='en'):
    agents = {
        'User-Agent': ('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; '
                       'SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
                       '.NET CLR 3.0.04506.30)')
    }
    before_trans = 'class="t0">'
    link = gtrans_url % (to_langage, langage, to_translate.replace(' ', '+'))
    request = urllib2.Request(link, headers=agents)
    page = urllib2.urlopen(request).read()
    result = page[page.find(before_trans) + len(before_trans):]
    result = result.split('<')[0]
    return result


stanford_parser_path = '/usr/local/Cellar/stanford-parser/3.6.0/libexec/'
s_parser = StanfordParser(
    stanford_parser_path + 'stanford-parser.jar',
    stanford_parser_path + 'stanford-parser-3.6.0-models.jar'
)
SPGTable = {
    'consider ADJP': [u'認為 ADJP', {0: 0, 1: 1}],
    'contain NP': [u'含有 NP', {0: 0, 1: 1}],
    'contain S': [u'含有 S', {0: 0, 1: 1}],
    'harmful to NP': [u'對 NP 有害', {0: 0, 1: 2, 2: 2}],
    'happy about NP': [u'為 NP 感到高興', {0: 0, 1: 2, 2: 2}],
    'N1 S': [u'S 的 N1', {0: 1, 1: 1, 2: 0}],
    'NP SBAR': [u'SBAR 的 NP', {0: 1, 1: 1, 2: 0}],
    'NP ADJP': [u'ADJP 的 NP', {0: 1, 1: 1, 2: 0}],
    'NP NP VP': [u'NP VP 的 NP', {0: 1, 1: 2, 2: 2, 3: 0}],
    'AUX VP': [u'AUX VP', {0: 0, 1: 1}],
    'ADJP NP': [u'ADJP NP', {0: 0, 1: 1}],
    'ADJ PP': [u'PP ADJ', {0: 1, 1: 0}],
    'use for NP': [u'用於 NP', {0: 0, 1: 2}],
    'sorry for S': [u'對 S 感到 抱歉', {0: 0, 1: 2, 2: 2, 3: 3}],
    'dangerous S': [u'S 很 危險', {0: 1, 1: 1, 2: 2}],
    'angry with NP': [u'對 NP 生氣', {0: 0, 1: 2, 2: 2}],
    'RB angry with NP': [u'對 NP RB 生氣', {0: 0, 1: 3, 2: 0, 3: 3}],
    # go out yesterday -> yesterday go out
    'VB PRT PP': [u'PP VB PRT', {0: 2, 1: 0, 2: 1}],
    'VBZ ADJP S': [u'S VBZ ADJP', {0: 2, 1: 0, 2: 1}],
    # VB: go PP: to school NP: today -> today go to school
    'VB PP NP': [u'NP VB PP', {0: 2, 1: 0, 2: 1}],
    'JJ RB': [u'RB JJ', {0: 1, 1: 0}],
    'too JJ S': [u'太 JJ 以致於不能 S', {0: 0, 1: 1, 2: 2, 3: 2}],
    'impossible for NP': [u'對 NP 而言 是 不可能的', {0: 0, 1: 2, 2: 2, 3: 3, 4: 4}],
}


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

    if RULE == 'ADJP->JJ PP':
        res = '%s %s %s' % (node[0][0], node[1][0][0], node[1][1].label())
        RHS = [node[0][0], node[1][0][0], node[1][1]]
        # res is "harmful to NP"
        # print 'DEBUG 7 Pattern', res, RHS, (res and res in SPGTable)
    # (RB very) (JJ nice) (PP to foreign visitors)
    elif RULE == 'ADJP->RB JJ PP':
        res = '%s %s %s %s' % (node[0].label(), node[1][0], node[2][0][0], node[2][1].label())
        RHS = [node[0], node[1][0], node[2][0][0], node[2][1]]
    elif RULE == 'ADJP->JJ S':
        res = '%s %s' % (node[0][0], node[1].label())
        RHS = [node[0][0], node[1]]
    elif RULE == 'ADJP->RB JJ S':
        # two kinds of pattern : "adv. JJ S" or "RB adj. S"
        # too busy to spend time with their children
        res = '%s %s %s' % (node[0][0], node[1].label(), node[2].label())
        RHS = [node[0][0], node[1], node[2]]

        if res not in SPGTable:
            # so happy to hear your voice
            res = '%s %s %s' % (node[0].label(), node[1][0], node[2].label())
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
    elif RULE == 'NP->NP SBAR':
        res = '%s %s' % (node[0].label(), node[1].label())
        RHS = [node[0], node[1]]
        # res is "NP SBAR"
    elif RULE == 'VP->VBP ADJP':
        res = '%s %s' % (node[0][0], node[1].label())
        RHS = [node[0][0], node[1]]
        # res is "consider ADJP"
    elif RULE == 'VP->VB S':
        res = '%s %s' % (node[0][0], node[1].label())
        RHS = [node[0][0], node[1]]
        # res is "contain S"
    elif RULE == 'VP->VB NP':
        res = '%s %s' % (node[0][0], node[1].label())
        RHS = [node[0][0], node[1]]
        # print 'DEBUG', res
    elif RULE == 'VP->VB PP':
        res = '%s %s %s' % (node[0][0], node[1][0][0], node[1][1].label())
        RHS = [node[0][0], node[1][0][0], node[1][1]]
    elif RULE == 'VP->VBZ ADJP S':
        # is impossbile for sb to S
        res = '%s %s %s' % (node[0].label(), node[1].label(), node[2].label())
        RHS = [node[0], node[1], node[2]]
    elif RULE == 'VP->VB PRT PP':
        # go out on a typhoon day
        # two kinds of pattern : "v. rp. PP" or "VB PRT PP"
        res = '%s %s %s' % (node[0][0], node[1][0][0], node[2].label())
        RHS = [node[0][0], node[1][0][0], node[2]]

        if res not in SPGTable:
            res = '%s %s %s' % (node[0].label(), node[1].label(), node[2].label())
            RHS = [node[0], node[1], node[2]]

    elif RULE == 'VP->VB PP NP':
        # VB:go PP:to school NP:today
        res = '%s %s %s' % (node[0].label(), node[1].label(), node[2].label())
        RHS = [node[0], node[1], node[2]]
    # print RULE
    return (res, RHS,)


def lexicalizeTree(node, isLEAF, isTREE):
    if isLEAF(node):
        return
    # depth-first search
    for child in node:
        lexicalizeTree(child, isLEAF, isTREE)
    pat, RHS = pattern(node, isLEAF, isTREE)

    if pat and pat in SPGTable:
        for j in range(len(node)):
            del node[-1]
        for k, _ in enumerate(RHS):
            node.insert(k, RHS[k])
    return


def lexSynTree(node, isLEAF, isTREE):
    if isLEAF(node):
        return
    tags = {'NP', 'PP', 'ADJP', 'VP', 'PRT', 'RB', 'JJ', 'S', 'SBAR'}
    # reorder subtree
    pat, RHS = pattern(node, isLEAF, isTREE)
    if pat != '' and pat in SPGTable:
        print '\n%s %s' % (pat, str(SPGTable[pat]).decode('unicode_escape'))
        # 'harmful to NP':[u'對 NP 有害', {0:0, 1:2, 2:2} ],
        RHSlabel, ALIGN = SPGTable[pat]
        RHSlabel = RHSlabel.split()
        # reorder
        RHSreo = [RHS[ALIGN[i]] if (RHSlabel[i][-1] == 'P' or
                  RHSlabel[i][0] == 'S' or RHSlabel[i][0] == 'V' or
                  RHSlabel[i] in tags) else RHSlabel[i]
                  for i in range(len(RHSlabel))]
        for j in range(len(node)):
            del node[-1]
        for k, child in enumerate(RHSreo):
            node.insert(k, child)

    # Depth-first search
    for child in node:
        lexSynTree(child, isLEAF, isTREE)


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
    if VERBATIM:
        print >> sys.stderr, '\nStanford parse output:'
        print >> sys.stderr, str(lexTree).decode('unicode_escape')
    # lexTree.draw()

    lexicalizeTree(lexTree, lambda x: type(x) != type(lexTree), lambda x: type(x) == type(lexTree))
    if VERBATIM:
        print >> sys.stderr, '\nLexicalized Tree (based on pattern grammar)'
        print >> sys.stderr, str(lexTree).decode('unicode_escape')
    # lexTree.draw()

    synTree = copy.deepcopy(parseTree[0])
    lexSynTree(synTree, lambda x: type(x) != type(synTree), lambda x: type(x) == type(synTree))
    if VERBATIM:
        print >> sys.stderr, '\nReordered Tree (based on SPG synchronous pattern grammar)'
        print >> sys.stderr, str(synTree).decode('unicode_escape')
    # synTree.draw()

    string = LinearizeTree(synTree, lambda x: type(x) != type(synTree), lambda x: type(x) == type(synTree))
    if VERBATIM:
        print >> sys.stderr, '\nString from tree'
        print >> sys.stderr, str(string).decode('unicode_escape')

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
    sents = map(lambda x: x.strip(), open('sents.txt'))
    sents = [sent for sent in sents if sent]

    for sent in sents:
        print 'Input:', sent
        res = spg_translate(sent)
