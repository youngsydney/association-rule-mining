"""
This is a module which supports the loading of the market
basket transactions and item types.
"""

import config

class DataLoader(object):
    """
    Loads the data from the files into memory
    """

    def __init__(self):
        self.products = []
        self.load_products()
        self.transactions = {}
        self.load_transactions()

    def return_p_t(self):
        """
        returns the product list and transaction dict
        """
        return self.transactions, self.products

    def load_products(self):
        """
        Load the product list into memory
        """
        with open(config.PRODUCT_FP, 'r') as in_file:
            for line in in_file:
                # split the line into the name of the product and its price
                item_cost = line.split(',')
                item_cost[1] = item_cost[1].replace('\r\n', '')
                item_cost[1] = float(item_cost[1].replace(' ', ''))
                # Note: at this point not tracking the cost of the products
                self.products.append({'item': item_cost[0],
                                      'cost': item_cost[1]})

    def load_transactions(self):
        """
        Load the transactions into memory
        """
        transaction_count = 0
        with open(config.BASKET_FP, 'r') as in_file:
            for line in in_file:
                # split the line, the first index will be 200003011105
                items = line.split(',')
                items[-1] = items[-1].replace('\r\n', '')
                del items[0]
                # Note: at this point not capturing the quanity purchased
                self.transactions[transaction_count] = []
                for idx, item in enumerate(self.products):
                    if items[idx] != ' 0':
                        self.transactions[transaction_count].append(item['item'])
                transaction_count += 1
