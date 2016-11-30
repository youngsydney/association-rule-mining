"""
This is a module which supports mining frequent patterns and rule generation.
"""

from fptree import CondFPTreeBuilder

class Miner(object):
    """
    Run the recursive mining algorithm.
    """

    def __init__(self, min_support, tree, header_list):
        self.min_support = min_support
        self.frequent_patterns = []
        self.freq_patt_count = []
        self.fp_tree = tree
        self.header_list = header_list

    def run_miner(self):
        """
        Run the recursive mining algorithm
        """
        #print "Mining the FP Tree for frequent patterns..."
        self.mine_me(self.header_list, self.fp_tree, [], True)
        K_freq, largest_K = self.find_K()
        return self.frequent_patterns, self.freq_patt_count, largest_K, K_freq

    def mine_me(self, header_list, tree, items, first):
        """
        This is the recursive algorithm
        """
        for item in header_list:
            if first:
                self.frequent_patterns.append([item['item']])
                self.freq_patt_count.append(item['count'])
            items.append(item['item'])
            pattern_build = CondPatternBuilder(tree,
                                               item['head'],
                                               self.min_support)
            ordered_patterns, L_list = pattern_build.build()

            if L_list:
                tree = CondFPTreeBuilder(L_list, ordered_patterns)
                fp_tree, header_table = tree.build_tree()
                path = tree.type_path()
                if path == 'single_path':
                    new_patterns, counts = tree.enumerate_all(item['item'])
                    for pattern in new_patterns:
                        pattern.extend(items)
                        self.freq_patt_count.append(counts[0])
                    self.frequent_patterns.extend(new_patterns)
                elif path == 'multiple_path':
                    for it in header_table:
                        self.frequent_patterns.append(items + [it['item']])
                        self.freq_patt_count.append(it['count'])
                    self.mine_me(header_table, fp_tree, items, False)
            del items[-1]

    def find_K(self):
        """
        Find the longest itemset (K) from the frequent itemsets
        also report the number of itemsets for each K
        """
        K_freq = {'total': 0}
        max_current = 0
        current = 0
        for pattern in self.frequent_patterns:
            K_freq['total'] += 1
            current = len(pattern)
            if str(current) in K_freq:
                K_freq[str(current)] += 1
            else:
                K_freq[str(current)] = 1

            if current >= max_current:
                max_current = current
        return K_freq, max_current


class CondPatternBuilder(object):
    """
    Build the conditional pattern base for each item in the header list
    """

    def __init__(self, tree, item_nodes, min_support):
        self.tree = tree
        self.item_nodes = item_nodes
        self.conditional = []
        self.ordered_patterns = []
        self.min_support = min_support

    def build(self):
        """
        Run the building
        """
        self.find_conditional()
        self.find_frequent()
        self.order_patterns()
        return self.ordered_patterns, self.L_list

    def find_conditional(self):
        """
        Find the conditional patterns for an item and add to list
        """
        for node in self.item_nodes:
            self.conditional.append({'pattern': node.pattern,
                                     'freq': node.count})

    def find_frequent(self):
        """
        Find the frequent itemset in the conditional pattern base
        """
        # find all the frequent items in the conditional patterns
        counts = {}
        for pattern in self.conditional:
            for item in pattern['pattern']:
                if item in counts:
                    counts[item] += pattern['freq']
                else:
                    counts[item] = pattern['freq']
        self.L_list = {k: v for k, v in counts.iteritems() if v >= self.min_support}

    def order_patterns(self):
        """
        order the patterns in the set by conditional frequency
        """
        list_freq = self.L_list.keys()
        # for each transaction find which items are frequent
        for pattern in self.conditional:
            item_set = []
            for item in list_freq:
                # add the frequent items to the new item set in order of freq.
                if item in pattern['pattern']:
                    item_set.append(item)
            for x in range(0, pattern['freq']):
                self.ordered_patterns.append(item_set)
