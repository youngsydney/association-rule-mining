"""
This is a module which handles reporting all the runs
"""

import os
from tabulate import tabulate

import config

class Reporter(object):
    """
    Reports the results of all the runs
    """

    def __init__(self):
        self.sup = []
        self.conf = []
        self.freq = []
        self.K = []
        self.rules = []
        self.time = []
        self.all_rules = {}
        self.rules_strings = []
        self.count = 0

    def add_run(self, values, r):
        """
        Add a run
        """
        self.count += 1
        self.sup.append(values['sup'])
        self.conf.append(values['conf'])
        new_K_freq = 'total: ' + str(values['freq']['total'])
        for x in range(0, len(values['freq'])-1):
            new_K_freq += ', ' + str(x+1) + 'K: ' + str(values['freq'][str(x+1)])
        self.freq.append(new_K_freq)
        self.K.append(values['K'])
        self.rules.append(values['rules'])
        self.time.append(values['time'])
        self.add_rules(r)

    def display(self):
        """
        Display the results of the runs
        """
        try:
            os.remove(config.OUTFILE)
        except:
            pass
        row1 = ['REPORT 1', '-', '-', '-', '-', '-']
        row2 = ['Min. Support', 'Min. Confidence', 'Num Freq. Item sets',
                'Largest K', 'Num. Rules', 'Run Time']
        rows = []
        rows.append(row1)
        rows.append(row2)
        for idx, run in enumerate(self.sup):
            with open(config.OUTFILE, 'a') as out:
                my_string =  'Combination -  Min. Support: ' + str(self.sup[idx]) + ' Min. Confidence: ' + str(self.conf[idx])
                out.write(my_string + '\n')
                print my_string
                for rule in self.rules_strings[idx]:
                    print rule
                    out.write(rule)
                    out.write('\n')
                print '\n'
                out.write('\n')
            row = [self.sup[idx], self.conf[idx], self.freq[idx],
                   self.K[idx], self.rules[idx], self.time[idx]]
            rows.append(row)
        print tabulate(rows, tablefmt='grid')
        with open(config.OUTFILE, 'a') as out:
            out.write(tabulate(rows, tablefmt = 'grid'))
            out.write('\n\n')

    def add_rules(self, r):
        """
        Add new rules to the collection
        """
        self.all_rules[str(self.count)] = r
        self.make_rule_strings(r)

    def top_15_rules(self):
        """
        Find the top 15 rules by confidence and correlation
        """
        index_largest = 0
        max_rules = 0
        for x in range(1, self.count+1):
            if len(self.all_rules[str(x)]) > max_rules:
                max_rules = len(self.all_rules[str(x)])
                index_largest = x

        top = []
        for rule in self.all_rules[str(index_largest)]:
            top.append(rule)

        confid = sorted(top, key=lambda k: k['conf'], reverse=True)
        correl = sorted(top, key=lambda k: k['cor'], reverse=True)
        self.display_rules(confid, correl)

    def make_rule_strings(self, r):
        """
        Turn the ant and con into a nice rule string for displaying
        """
        my_rules = []
        for rule in r:
            ant = ''
            con = ''
            for item in rule['ant']:
                if item != rule['ant'][-1]:
                    ant += item + ' + '
                else:
                    ant += item
            for item in rule['con']:
                if item != rule['con'][-1]:
                    con += item + ' + '
                else:
                    con += item
            rule = ant + '-->' + con
            my_rules.append(rule)
        self.rules_strings.append(my_rules)

    def display_rules(self, confid, correl):
        """
        Display the top 15 rules
        """
        rows = []
        row1 = ['REPORT 2', 'By Confidence', '-', '-', '-']
        row2 = ['Rank', 'Rule', 'Support', 'Confidence', 'Correlation']
        rows.append(row1)
        rows.append(row2)
        for x in range(0, 15):
            if x < len(confid):
                ant_f = ''
                con_f = ''
                for item in confid[x]['ant']:
                    if item != confid[x]['ant'][-1]:
                        ant_f += item + ' + '
                    else:
                        ant_f += item
                for item in confid[x]['con']:
                    if item != confid[x]['con'][-1]:
                        con_f += item + ' + '
                    else:
                        con_f += item
                rule_cof = ant_f + '-->' + con_f
                row = [str(x+1), rule_cof, str(confid[x]['sup']),
                       str(confid[x]['conf']), str(confid[x]['cor'])]
                rows.append(row)
        rows_2 = []
        row3 = ['REPORT 2', 'By Correlation', '-', '-', '-']
        row4 = ['Rank', 'Rule', 'Support', 'Confidence', 'Correlation']
        rows_2.append(row3)
        rows_2.append(row4)
        for x in range(0, 15):
            if x < len(correl):
                ant_r = ''
                con_r = ''
                for item in correl[x]['ant']:
                    if item != correl[x]['ant'][-1]:
                        ant_r += item + ' + '
                    else:
                        ant_r += item
                for item in correl[x]['con']:
                    if item != correl[x]['con'][-1]:
                        con_r += item + ' + '
                    else:
                        con_r += item
                rule_cor = ant_r + '-->' + con_r
                row = [str(x+1), rule_cor, str(correl[x]['sup']),
                       str(correl[x]['conf']), str(correl[x]['cor'])]
                rows_2.append(row)

        print tabulate(rows, tablefmt='grid')
        with open(config.OUTFILE, 'a') as out:
            out.write(tabulate(rows, tablefmt = 'grid'))
            out.write('\n\n')
        print tabulate(rows_2, tablefmt='grid')
        with open(config.OUTFILE, 'a') as out:
            out.write(tabulate(rows_2, tablefmt = 'grid'))
            out.write('\n\n')
