"""
This is a module which handles rule generation
"""

import config

class Generator(object):
    """
    Generate rules which pass the confidence threshold
    """

    def __init__(self, freq_patt, freq_count):
        # pay careful attention because the indices match
        self.patterns = freq_patt
        self.convert_to_set()
        self.supports = freq_count
        self.min_confidence = config.CONFIDENCE
        # patterns that have more than one item (only gen. rules from these)
        self.mto = [k for k in self.patterns if len(k) > 1]
        self.rules = []
        self.count = 0

    def generate_rules(self, num_trans):
        """
        generate the rules
        conf = support itemset / support antecedent
        """
        #print "Generating rules from the frequent patterns..."
        for pattern in self.mto:
            variable = []
            for item in pattern:
                variable.append(item)
            for item in pattern:
                ant = variable[:]
                ant.remove(item)
                con = []
                con.append(item)
                sup_union = self.supports[self.pattern_supports.index(set(pattern))]
                sup_ant = self.supports[self.pattern_supports.index(set(ant))]
                confidence = float(sup_union) / sup_ant
                if confidence >= self.min_confidence:
                    self.rules.append({'ant': set(ant), 'con': set(con),
                                       'conf': confidence, 'cor': 0,
                                       'sup': (float(sup_union)/num_trans)})
                    self.count += 1
                    self.continue_rules(pattern, ant, con, num_trans)
        self.remove_duplicate_rules()
        return self.rules

    def continue_rules(self, pattern, ant, con, num):
        """
        if the rule passed the min conf with one on con side, then continue
        """
        if len(ant) == 1:
            return
        set_con = []
        variable = []
        for item in con:
            set_con.append(item)
        for item in ant:
            variable.append(item)
        for item in ant:
            c = set_con[:]
            a = variable[:]
            c.append(item)
            a.remove(item)
            sup_union = self.supports[self.pattern_supports.index(set(pattern))]
            sup_ant = self.supports[self.pattern_supports.index(set(a))]
            confidence = float(sup_union) / sup_ant
            if confidence >= self.min_confidence:
                self.rules.append({'ant': set(a), 'con': set(c), 'conf': confidence,
                                   'cor': 0, 'sup': (float(sup_union)/num)})
                self.count += 1
                self.continue_rules(pattern, a, c, num)

    def remove_duplicate_rules(self):
        """
        In case somehow any duplicate rules, remove them
        """
        fixed = []
        for rule in self.rules:
            if rule not in fixed:
                fixed.append(rule)
            else:
                pass
        for rule in fixed:
            rule['ant'] = list(rule['ant'])
            rule['con'] = list(rule['con'])
        self.rules = fixed

    def filter_correlations(self, num_transactions):
        """
        Filter out the rules for only those with positive correlation
        """
        num_tot = float(num_transactions)
        neg_correlation = []
        for rule in self.rules:
            item_set = rule['ant'] + rule['con']
            denom = 0
            for item in item_set:
                denom += self.supports[self.pattern_supports.index(set([item]))] / num_tot
            numer = self.supports[self.pattern_supports.index(set(item_set))] / num_tot
            correlation = numer/denom
            rule['cor'] = correlation
            if correlation  < 0:
                neg_correlation.append(rule)
        for rule in neg_correlation:
            del self.rules[rule]
        return self.rules

    def convert_to_set(self):
        """
        convert the frequent itemsets to a dictionary
        """
        self.pattern_supports = []
        for pattern in self.patterns:
            self.pattern_supports.append(set(pattern))
