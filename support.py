"""
FPTreeSupportBuilder finds the frequent items, buils the L-list and
the ordered transaction list.
"""

import config

class FPTreeSupportBuilder(object):
    """
    Constructs the F-List and the ordered transactions.
    """

    def __init__(self, transactions, products):
        # list of the <item:support> which have passed the min support threshold
        self.L_list = []
        # dictionary of <transaction id : [freq, ordered items in the trans.]>
        self.ordered_transactions = {}
        # dictionary of <transaction id : [list of items in the transaction]>
        self.transactions = transactions
        # list of all the products
        self.products = products
        self.min_support = 0

    def build(self):
        """
        runs the construction of the f-list and ordered transactions
        """
        #print "Finding frequent items and ordering the transactions..."
        self.find_frequent()
        #sort the L list by frequency of item
        self.L_list = sorted(self.L_list, key=lambda k: k.values()[0],
                             reverse=True)
        self.build_ordered_transactions()
        return self.L_list, self.ordered_transactions, self.min_support

    def find_frequent(self):
        """
        Find the frequent items in all the transactions and build L list
        """
        num_transactions = len(self.transactions)
        self.min_support = config.SUPPORT * num_transactions
        min_support = self.min_support
        # round the support minimum up
        if int(min_support) != min_support:
            min_support = int(min_support + 1)
        # first build the dictionary to hold the count of the items
        item_counts = {}
        for product in self.products:
            item_counts[product['item']] = 0
        # scan the transaction DB and count occurences of each item
        for transaction in self.transactions:
            for product in self.transactions[transaction]:
                item_counts[product] += 1
        # scan through the item counts and add only ones that pass support
        for item in item_counts:
            if item_counts[item] >= min_support:
                self.L_list.append({item: item_counts[item]})

    def build_ordered_transactions(self):
        """
        Build the transaction list with only the frequent items, in order
        """
        list_freq = [k.keys()[0] for k in self.L_list]
        # for each transaction find which items are frequent
        for transaction in self.transactions:
            item_set = []
            for item in list_freq:
                # add the frequent items to the new item set in order of freq.
                if item in self.transactions[transaction]:
                    item_set.append(item)
            self.ordered_transactions[transaction] = item_set
