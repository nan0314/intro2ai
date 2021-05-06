import unittest
import read, copy
from logical_classes import *
from student_code import KnowledgeBase

class KBTest(unittest.TestCase):

    def setUp(self):
        # Assert starter facts
        file = 'statements_kb2.txt'
        self.data = read.read_tokenize(file)
        data = read.read_tokenize(file)
        self.KB = KnowledgeBase([], [])
        for item in data:
            if isinstance(item, Fact) or isinstance(item, Rule):
                self.KB.kb_assert(item)

    # Tests inferred facts and rules
    def test1(self):
        f1 = read.parse_input("fact: (isa Mammal Tall)")
        print(' Adding', f1)
        self.KB.kb_add(f1)
        ask1 = read.parse_input("fact: (isa Dog ?X)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer[0]), "?X : Mammal")
        self.assertEqual(str(answer[1]), "?X : Animal")
        self.assertEqual(str(answer[2]), "?X : Tall")

    # Remove children of asserted facts when asserted fact is removed
    def test2(self):
        f1 = read.parse_input("fact: (isa Dog Mammal)")
        print(' Retracting', f1)
        self.KB.kb_retract(f1)
        f2 = read.parse_input("fact: (isa Mammal Tall)")
        print(' Adding', f2)
        self.KB.kb_add(f2)
        ask1 = read.parse_input("fact: (isa Dog ?X)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(len(answer), 0)

    # Fail to remove supported fact
    def test3(self):
        f1 = read.parse_input("fact: (isa Dog Animal)")
        print(' Retracting', f1)
        self.KB.kb_retract(f1)
        ask1 = read.parse_input("fact: (isa Dog ?X)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer[0]), "?X : Mammal")
        self.assertEqual(str(answer[1]), "?X : Animal")

    # Fail to remove supported fact
    def test4(self):
        r1 = read.parse_input("rule: ((isa Mammal ?z)) -> (isa Dog ?z))")
        print(' Retracting', r1)
        self.KB.kb_retract(r1)
        f2 = read.parse_input("fact: (isa Mammal Tall)")
        print(' Adding', f2)
        self.KB.kb_add(f2)
        ask1 = read.parse_input("fact: (isa Dog ?X)")
        print(' Asking if', ask1)
        answer = self.KB.kb_ask(ask1)
        self.assertEqual(str(answer[0]), "?X : Mammal")
        self.assertEqual(str(answer[1]), "?X : Animal")
        self.assertEqual(str(answer[2]), "?X : Tall")



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
