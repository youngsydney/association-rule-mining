"""
This is a module which supports the construction of an FP-Tree.

Node is the node object for each node in the FP Tree.

FPTreeBuilder builds the actual tree from the F-List and ordered transactions.
"""

import itertools

class Node(object):
    """
    Node for the FP Tree
    """

    def __init__(self, item, count, pattern):
        # each node holds the item name, the count, a dictionary of children,
        # and the pattern that precedes it
        self.item = item
        self.count = count
        self.children = {}
        self.pattern = pattern

    def add_node(self, node):
        """
        Add a leaf to this node
        """
        self.children[node.get_item()] = node

    def update_count(self):
        """
        Increment the count by one
        """
        self.count += 1

    def get_item(self):
        """
        Return the name of the item in the node
        """
        return self.item

    def get_children(self):
        """
        Return the dictionary of children of this node
        """
        return self.children

class CondFPTreeBuilder(object):
    """
    Builds the FP Tree.
    """

    def __init__(self, L_list, o_patterns):
        self.L_list = L_list
        self.header_table = []
        self.build_header()
        self.helper = {}
        self.build_helper()
        self.patterns = o_patterns
        self.tree = Node('root', '0', [])
        self.item_set = []
        self.it_set = {}

    def build_tree(self):
        """
        Control the building of the FP Tree.
        """
        for pattern in self.patterns:
            # add the transactions to the tree one at a time
            self.add_transaction(pattern)
        return self.tree, self.header_table

    def add_transaction(self, itemset):
        """
        Add a transaction to the FP Tree.
        """
        for idx, item in enumerate(itemset):
            pattern = []
            # begin at the root of the tree
            node = self.tree
            #traverse down to the last leaf node in the transaction
            for x in range(0, idx):
                node = node.get_children()[itemset[x]]
                pattern.append(itemset[x])
            # if the item is already there, update the count
            if item in node.get_children():
                node = node.get_children()[item]
                node.update_count()
            # else create a new node and append it to the children
            else:
                new_leaf = Node(item, 1, pattern)
                node.add_node(new_leaf)
                node = node.get_children()[item]
                # append new item nodes to f_list
                self.header_table[self.helper[item]]['head'].append(node)

    def build_helper(self):
        """
        Build the helper dict <item: idx in f_list>
        """
        for idx, item in enumerate(self.header_table):
            self.helper[item['item']] = idx

    def build_header(self):
        """
        Build the header table
        """
        for item in self.L_list:
            self.header_table.append({'item': item, 'head': [],
                                      'count': self.L_list[item]})
        self.header_table.reverse()

    def type_path(self):
        """
        Returns single_path or multiple_path
        """
        node = self.tree
        if not node.children:
            return "empty"
        while len(node.children) == 1:
            for child in node.children:
                node = node.children[child]
                self.item_set.append(node.get_item())
        self.it_set[node.get_item()] = node.count
        if not node.children:
            return "single_path"
        if node.children > 1:
            return "multiple_path"

    def enumerate_all(self, item):
        """
        Tree is a single path and now enumerate all the different patterns
        """
        freq = []
        freq_count = []
        for it in range(0, len(self.item_set)+1):
            for subset in itertools.combinations(self.item_set, it):
                mini_list = []
                for sub in subset:
                    mini_list.append(sub)
                if mini_list:
                    freq.append(mini_list)
                    if len(mini_list) == 1:
                        freq_count.append(self.it_set[mini_list[0]])
        return freq, freq_count

class FPTreeBuilder(object):
    """
    Builds the FP Tree.
    """

    def __init__(self, L_list, o_transactions):
        self.L_list = L_list
        self.header_table = []
        self.build_header()
        self.helper = {}
        self.build_helper()
        self.transactions = o_transactions
        self.tree = Node('root', '0', [])

    def build_tree(self):
        """
        Control the building of the FP Tree.
        """
        #print "Building the FP Tree from the list of transactions..."
        for transaction in self.transactions:
            # add the transactions to the tree one at a time
            self.add_transaction(self.transactions[transaction])
        return self.tree, self.header_table

    def add_transaction(self, itemset):
        """
        Add a transaction to the FP Tree.
        """
        for idx, item in enumerate(itemset):
            pattern = []
            # begin at the root of the tree
            node = self.tree
            #traverse down to the last leaf node in the transaction
            for x in range(0, idx):
                node = node.get_children()[itemset[x]]
                pattern.append(itemset[x])
            # if the item is already there, update the count
            if item in node.get_children():
                node = node.get_children()[item]
                node.update_count()
            # else create a new node and append it to the children
            else:
                new_leaf = Node(item, 1, pattern)
                node.add_node(new_leaf)
                node = node.get_children()[item]
                # append new item nodes to f_list
                self.header_table[self.helper[item]]['head'].append(node)

    def build_helper(self):
        """
        Build the helper dict <item: idx in f_list>
        """
        for idx, item in enumerate(self.header_table):
            self.helper[item['item']] = idx

    def build_header(self):
        """
        Build the header table
        """
        for item in self.L_list:
            self.header_table.append({'item': item.keys()[0], 'head': [],
                                      'count': item.values()[0]})
        self.header_table.reverse()
