import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_rule):
        """Retract a fact from the KB

        Args:
            fact (Fact) - Fact to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_rule])
        ####################################################
        # Student code goes here
        if fact_rule not in self.facts and fact_rule not in self.rules:
            return

        if isinstance(fact_rule,Rule):
            if fact_rule in self.rules:
                ind = self.rules.index(fact_rule)
                fact_rule = self.rules[ind]

            if fact_rule.asserted or fact_rule.supported_by:
                pass
            else:
                ind = self.rules.index(fact_rule)
                del self.rules[ind]

                for supported_rule in fact_rule.supports_rules:
                    if supported_rule not in self.rules:
                        fact_rule.supports_rules.remove(supported_rule)
                        continue

                    ind = self.rules.index(supported_rule)
                    for pair in self.rules[ind].supported_by:
                        if fact_rule in pair:
                            self.rules[ind].supported_by.remove(pair)

                    self.kb_retract(supported_rule)
                for supported_fact in fact_rule.supports_facts:
                    if supported_fact not in self.facts:
                        fact_rule.supports_facts.remove(supported_fact)
                        continue
                    ind = self.facts.index(supported_fact)
                    for pair in self.facts[ind].supported_by:
                        if fact_rule in pair:
                            self.facts[ind].supported_by.remove(pair)

                    self.kb_retract(supported_fact)

        else:
            if fact_rule in self.facts:
                ind = self.facts.index(fact_rule)
                fact_rule = self.facts[ind]


            if fact_rule.supported_by:
                pass 
            else:
                ind = self.facts.index(fact_rule)
                del self.facts[ind]

                for supported_rule in fact_rule.supports_rules:
                    if supported_rule not in self.rules:
                        fact_rule.supports_rules.remove(supported_rule)
                        continue
                    ind = self.rules.index(supported_rule)
                    for pair in self.rules[ind].supported_by:
                        if fact_rule in pair:
                            self.rules[ind].supported_by.remove(pair)
                            

                    self.kb_retract(supported_rule)
                for supported_fact in fact_rule.supports_facts:
                    if supported_fact not in self.facts:
                        fact_rule.supports_facts.remove(supported_fact)
                        continue
                    ind = self.facts.index(supported_fact)
                    for pair in self.facts[ind].supported_by:
                        if fact_rule in pair:
                            self.facts[ind].supported_by.remove(pair)

                    self.kb_retract(supported_fact)




class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here

        # Simple Rules (single conditions)
        if len(rule.lhs) < 2:

            # Unify fact with lhs of rule
            bindings = match(rule.lhs[0],fact.statement)

            # If we can unify, make new facts
            if bindings:

                # Make substitutions
                statement = instantiate(rule.rhs,bindings)

                # Make new fact
                new_fact = Fact(statement,[[fact,rule]])
                new_fact.asserted = False

                # Update support information
                fact.supports_facts.append(new_fact)
                rule.supports_facts.append(new_fact)

                # Assert fact
                kb.kb_assert(new_fact)


        # Complex Rules (multiple conditions)
        else:
            
            # Unify fact with first sentence in lhs
            bindings = match(rule.lhs[0],fact.statement)

            if bindings:

                new_rule = Rule([[],[]],[])
                new_rule.asserted = False
                new_rule.rhs = instantiate(rule.rhs,bindings)
                for i in range(1,len(rule.lhs)):
                    new_rule.lhs.append(instantiate(rule.lhs[i],bindings))
                
                new_rule.supported_by.append([fact,rule])

                fact.supports_rules.append(new_rule)
                rule.supports_rules.append(new_rule)

                kb.kb_assert(new_rule)


