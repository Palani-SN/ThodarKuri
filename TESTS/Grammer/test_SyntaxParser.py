from ThodarKuri.Grammer.SyntaxParser import ThodarkuriParser
import pytest

def test_Template1():

    NodeList = [
             " R[Var_new_1] ",
             " R[Var_new_3] => files1.html ",
             " ( R[Var_new_4] => files2.html )* "
             ]

    NodeResult = [
             { 'VAR' : 'Var_new_1' },
             { 'Var_new_3' : 'files1.html' },
             [{ 'Var_new_4' : 'files2.html' },]
             ]

    for i in range(len(NodeList)):
    	# print(ThodarkuriParser(NodeList[i]));
        assert(ThodarkuriParser(NodeList[i]) == NodeResult[i]);