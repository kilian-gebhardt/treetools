"""
treetools: Tools for transforming treebank trees.

Unit tests (pytest) for tree operations

Author: Wolfgang Maier <maierw@hhu.de>
"""
import pytest
import io
import os
from trees import grammar, grammaroutput, grammarinput, grammarconst
from . import testdata


try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    def unicode(s): return str(s)


def test_cont_grammar(cont_grammar):
    """Test grammar extraction from non-discontinuous trees
    """
    assert len(cont_grammar.keys()) \
        == len(testdata.CONT_GRAMMAR_FUNCS)
    assert all([func in testdata.CONT_GRAMMAR_FUNCS
                for func in cont_grammar.keys()])
    lins = [lin for lin in cont_grammar[func] for func in cont_grammar]
    assert len(lins) == 6
    assert all([lin == (((0, 0),),) for lin in lins])


def test_discont_grammar(discont_grammar):
    """Test grammar extraction from discontinuous trees
    """
    assert len(discont_grammar.keys()) \
        == len(testdata.DISCONT_GRAMMAR_FUNCS)
    assert all([func in testdata.DISCONT_GRAMMAR_FUNCS
                for func in discont_grammar.keys()])
    lins = [lin for lin in discont_grammar[func] for func in discont_grammar]
    assert len(lins) == len(testdata.DISCONT_GRAMMAR_LINS)
    assert all([lin in testdata.DISCONT_GRAMMAR_LINS for lin in lins])


def test_discont_grammar_markov(discont_grammar):
    """Test binarized markovized grammar (discontinuous)
    """
    markov_opts = {'v': 1, 'h': 2}
    bin_grammar = grammar.binarize(discont_grammar,
                                   markov_opts=markov_opts)
    assert bin_grammar == testdata.DISCONT_GRAMMAR_LR_H2_V1_BTOP_BBOT
    markov_opts = {'v': 2, 'h': 1}
    bin_grammar = grammar.binarize(discont_grammar,
                                   markov_opts=markov_opts)
    assert bin_grammar == testdata.DISCONT_GRAMMAR_LR_H1_V2_BTOP_BBOT


def test_discont_grammar_markov_optimal(discont_grammar):
    """Test optimally binarized markovized grammar (discontinuous)
    """
    markov_opts = {'v': 1, 'h': 2}
    bin_grammar = grammar.binarize(discont_grammar,
                                   markov_opts=markov_opts,
                                   reordering=grammar.reordering_optimal)
    assert bin_grammar == testdata.DISCONT_GRAMMAR_OPTIMAL_H2_V1_BTOP_BBOT


def test_binarize_leftright(discont_grammar, cont_grammar):
    """Test left-to-right binarization
    """
    discont_grammar = grammar.binarize(discont_grammar)
    cont_grammar = grammar.binarize(cont_grammar)
    assert testdata.DISCONT_GRAMMAR_LEFT_RIGHT == discont_grammar
    assert testdata.CONT_GRAMMAR_LEFT_RIGHT == cont_grammar


def test_output_rcg(discont_grammar, discont_lex, cont_grammar, cont_lex):
    """Test grammar output (RCG format)
    """
    tempdest = os.path.join('.', 'tempdest')
    grammaroutput.rcg(discont_grammar, discont_lex, tempdest, 'utf8')
    lines = []
    with io.open("%s.rcg" % tempdest) as tempf:
        lines = [l.strip() for l in tempf.readlines()]
    assert len(lines) == len(testdata.DISCONT_GRAMMAR_OUTPUT_RCG)
    assert all([line in testdata.DISCONT_GRAMMAR_OUTPUT_RCG for line
                in lines])
    with io.open("%s.lex" % tempdest) as tempf:
        lines = [l.strip() for l in tempf.readlines()]
    assert len(lines) == len(testdata.GRAMMAR_OUTPUT_RCG_LEX)
    assert all([line in testdata.GRAMMAR_OUTPUT_RCG_LEX for line in lines])
    grammaroutput.rcg(cont_grammar, cont_lex, tempdest, 'utf8')
    lines = []
    with io.open("%s.rcg" % tempdest) as tempf:
        lines = [l.strip() for l in tempf.readlines()]
    assert len(lines) == len(testdata.CONT_GRAMMAR_OUTPUT_RCG)
    assert all([line in testdata.CONT_GRAMMAR_OUTPUT_RCG for line
                in lines])
    with io.open("%s.lex" % tempdest) as tempf:
        lines = [l.strip() for l in tempf.readlines()]
    assert len(lines) == len(testdata.GRAMMAR_OUTPUT_RCG_LEX)
    assert all([line in testdata.GRAMMAR_OUTPUT_RCG_LEX for line in lines])
    for ending in ['lex', 'rcg']:
        os.remove("tempdest.%s" % ending)


def test_output_pmcfg(discont_grammar, discont_lex, cont_grammar, cont_lex):
    """Test grammar output (PMCFG format)
    """
    tempdest = os.path.join('.', 'tempdest-pmcfg')
    grammaroutput.pmcfg(discont_grammar, discont_lex, tempdest, 'utf8')
    lines = []
    with io.open("%s.pmcfg" % tempdest) as tempf:
        lines = [l.strip() for l in tempf.readlines()]
    assert len(lines) == len(testdata.DISCONT_GRAMMAR_OUTPUT_PMCFG)
    assert all([line in testdata.DISCONT_GRAMMAR_OUTPUT_PMCFG for line
                in lines])
    with io.open("%s.lex" % tempdest) as tempf:
        lines = [l.strip() for l in tempf.readlines()]
    assert len(lines) == len(testdata.GRAMMAR_OUTPUT_RCG_LEX)
    assert all([line in testdata.GRAMMAR_OUTPUT_RCG_LEX for line in lines])
    grammaroutput.pmcfg(cont_grammar, cont_lex, tempdest, 'utf8')
    lines = []
    with io.open("%s.pmcfg" % tempdest) as tempf:
        lines = [l.strip() for l in tempf.readlines()]
    assert len(lines) == len(testdata.CONT_GRAMMAR_OUTPUT_PMCFG)
    assert all([line in testdata.CONT_GRAMMAR_OUTPUT_PMCFG for line
                in lines])
    with io.open("%s.lex" % tempdest) as tempf:
        lines = [l.strip() for l in tempf.readlines()]
    assert len(lines) == len(testdata.GRAMMAR_OUTPUT_RCG_LEX)
    assert all([line in testdata.GRAMMAR_OUTPUT_RCG_LEX for line in lines])
    for ending in ['lex', 'pmcfg']:
        os.remove("tempdest-pmcfg.%s" % ending)


def test_input_rcg(discont_grammar_novert, discont_lex):
    """Test grammar input (RCG format)
    """
    tempdestname = os.path.join('.', 'tempdest')
    with io.open(tempdestname + '.rcg', 'w') as tempdest:
        for line in testdata.DISCONT_GRAMMAR_OUTPUT_RCG:
            tempdest.write(unicode(line) + "\n")
    with io.open(tempdestname + '.lex', 'w') as tempdest:
        for line in testdata.GRAMMAR_OUTPUT_RCG_LEX:
            tempdest.write(unicode(line) + "\n")
    grammar, lexicon = grammarinput.rcg(tempdestname, 'utf-8')
    assert grammar == discont_grammar_novert
    assert lexicon == discont_lex
    for ending in ['lex', 'rcg']:
        os.remove("tempdest.%s" % ending)


@pytest.fixture(scope='function')
def cont_grammar(cont_tree):
    gram = {}
    lex = {}
    grammar.extract(cont_tree, gram, lex)
    return gram


@pytest.fixture(scope='function')
def cont_lex(cont_tree):
    gram = {}
    lex = {}
    grammar.extract(cont_tree, gram, lex)
    return lex


@pytest.fixture(scope='function')
def discont_grammar(discont_tree):
    gram = {}
    lex = {}
    grammar.extract(discont_tree, gram, lex)
    return gram


@pytest.fixture(scope='function')
def discont_grammar_novert(discont_tree):
    gram = {}
    lex = {}
    grammar.extract(discont_tree, gram, lex)
    for func in gram:
        for lin in gram[func]:
            gram[func][lin] = {grammarconst.DEFAULT_VERT:
                               sum(gram[func][lin].values())}
    return gram


@pytest.fixture(scope='function')
def discont_lex(discont_tree):
    gram = {}
    lex = {}
    grammar.extract(discont_tree, gram, lex)
    return lex
