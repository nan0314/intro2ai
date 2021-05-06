import unittest
import read, copy
from logical_classes import *
from student_code import KnowledgeBase

class KBTest(unittest.TestCase):

    def setUp(self):
        # Assert starter facts
        file = 'geography.txt'
        self.data = read.read_tokenize(file)
        data = read.read_tokenize(file)
        self.KB = KnowledgeBase([], [])
        for item in data:
            if isinstance(item, Fact) or isinstance(item, Rule):
                self.KB.kb_assert(item)

    def test1(self):
        ask1 = read.parse_input("fact: (cityof chicago ?y)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer[0]), "?Y : illinois")
        ask2 = read.parse_input("fact: (capitalof ?x newyork)")
        print(' Asking if', ask2)
        answer = self.KB.kb_ask(ask2)
        self.assertEqual(str(answer[0]), "?X : albany")
        ask3 = read.parse_input("fact: (stateof illinois ?y)")
        print(' Asking if', ask3)
        answer = self.KB.kb_ask(ask3)
        self.assertEqual(str(answer[0]), "?Y : usa")

    def test2(self):
        ask0 = read.parse_input("fact: (cityof springfield ?y)")
        print(' Asking if', ask0)
        answer = self.KB.kb_ask(ask0)
        self.assertEqual(str(answer[0]), "?Y : illinois")
        ask1 = read.parse_input("fact: (cityincountry albany ?y)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer[0]), "?Y : usa")
        r1 = read.parse_input("fact: (cityof albany newyork)")
        print(' Retracting', r1)
        self.KB.kb_retract(r1)
        answer2 = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer[0]), "?Y : usa")
        r2 = read.parse_input("fact: (capitalof albany newyork)")
        print(' Retracting', r2)
        self.KB.kb_retract(r2)
        answer2 = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer[0]), "?Y : usa") #still supported by rule for capitols and citys
        ask2 = read.parse_input("fact: capitalof albany newyork")
        answer3 = self.KB.kb_ask(ask2)
        self.assertEqual(answer3, [])

    def test3(self):
        r1 = read.parse_input("fact: (cityof nyc newyork)")
        r2 = read.parse_input("fact: (cityof manhattan newyork)")
        r3 = read.parse_input("fact: (capitalof albany newyork)")
        print(' Retracting', r1)
        self.KB.kb_retract(r1)
        print(' Retracting', r2)
        self.KB.kb_retract(r2)
        print(' Retracting', r3)
        self.KB.kb_retract(r3)
        ask1 = read.parse_input("fact: cityincountry nyc ?Y")
        answer1 = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer1[0]), "?Y : usa")


def pprint_justification(answer):
    """Pretty prints (hence pprint) justifications for the answer.
    """
    if not answer: print('Answer is False, no justification')
    else:
        print('\nJustification:')
        for i in range(0,len(answer.list_of_bindings)):
            # print bindings
            print(answer.list_of_bindings[i][0])
            # print justifications
            for fact_rule in answer.list_of_bindings[i][1]:
                pprint_support(fact_rule,0)
        print

def pprint_support(fact_rule, indent):
    """Recursive pretty printer helper to nicely indent
    """
    if fact_rule:
        print(' '*indent, "Support for")

        if isinstance(fact_rule, Fact):
            print(fact_rule.statement)
        else:
            print(fact_rule.lhs, "->", fact_rule.rhs)

        if fact_rule.supported_by:
            for pair in fact_rule.supported_by:
                print(' '*(indent+1), "support option")
                for next in pair:
                    pprint_support(next, indent+2)



if __name__ == '__main__':
    unittest.main()
