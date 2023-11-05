from grammar.non_terminal import NonTerminal
from grammar.terminal import Terminal
from collections import deque

class FirstFollow:
    def __init__(self, grammar) -> None:
        self.grammar = grammar
    
    def get_possible_strings(self, rule, k, prev_first_k):
        possible_strings = []
        queue = deque()
        queue.append(list(rule))
        while queue:
            current_rule = queue.popleft()
            if all(isinstance(c, Terminal) for c in current_rule[:k]):
                possible_strings.append(tuple(current_rule[:k]))
                continue
            for i, c in enumerate(current_rule):
                if isinstance(c, NonTerminal):
                    for nt_first in prev_first_k[c]:
                        new_rule = current_rule.copy()
                        if all(nt_c.is_empty() for nt_c in nt_first) and len(current_rule) > 1:
                            new_rule[i:i+1] = []
                        else:
                            new_rule[i:i+1] = nt_first 
                        queue.append(new_rule)
                    break
        return possible_strings

    def tuples_to_strings(self, table):
        result = {}
        for key, value in table.items():
            result[key] = set()
            for v in value:
                result[key].add(''.join([str(c) for c in v]))
        return result

    def first_k(self, k):
        first = {}
        prev_first = {}
        for n in self.grammar.non_terminals:
            first[n] = set()
        
        while first != prev_first:
            prev_first = first.copy()
            for key, value in prev_first.items():
                prev_first[key] = value.copy()

            for n in self.grammar.non_terminals:
                for rule in n.rules:
                    possible_strings = self.get_possible_strings(rule, k, first)
                    first[n] |= set(possible_strings)

        return first
    
    def follow_k(self, k, first_k):
        follow = {}
        prev_follow = {}

        for n in self.grammar.non_terminals:
            follow[n] = set()
        follow[self.grammar.non_terminals[0]].add((self.grammar.get_epsilon(),))

        seen_nonterminals = set()
        seen_nonterminals.add(self.grammar.non_terminals[0])

        while follow != prev_follow:
            prev_follow = follow.copy()
            for key, value in prev_follow.items():
                prev_follow[key] = value.copy()

            seen_nonterminals_buf = []
            for nt in seen_nonterminals:
                for rule in nt.rules:
                    for i, c in enumerate(rule):
                        if isinstance(c, NonTerminal):
                            seen_nonterminals_buf.append(c)
                            after = rule[i+1:]
                            first_of_after = self.concat_k(k, [ps[:k] for ps in self.get_possible_strings(after, k, first_k)], follow[nt])
                            for s in first_of_after:
                                if len(s) == 0:
                                    follow[c].add((self.grammar.get_epsilon(),))
                                else:
                                    follow[c].add(s)
                            
            seen_nonterminals |= set(seen_nonterminals_buf)

        return follow
        
    def concat_k(self, k, first_set, second_set):
        result = set()
        for s1 in first_set:
            for s2 in second_set:
                s1_empty = all(c.is_empty() for c in s1)
                s2_empty = all(c.is_empty() for c in s2)
                if s1_empty and s2_empty:
                    result.add((self.grammar.get_epsilon(),))
                    continue
                elif s1_empty:
                    result.add(s2)
                    continue
                elif s2_empty:
                    result.add(s1)
                    continue

                result.add((s1 + s2)[:k])
        return result
