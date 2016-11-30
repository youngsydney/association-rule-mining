"""
Holds constants and file paths for the whole program
"""

import os

# Root path for the project
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# filepath to the product list
PRODUCT_FP = ROOT_PATH + '/ar_test_data/products'

# filepath to the basket of transactions
BASKET_FP = ROOT_PATH + '/ar_test_data/small_basket.dat'

# output the results
OUTFILE = ROOT_PATH + '/results.txt'

# minimum support
SUPPORT = 0.2

# minimum confidence
CONFIDENCE = 0.75

# all the runs
runs = [{'support': 0.2, 'confidence': 0.75}]

ADDITIONAL = False
# runs with support 0.1 option, will greatly affect the rules printed
runs_additional = [{'support': 0.1, 'confidence': 0.75},
                   {'support': 0.2, 'confidence': 0.75},
                   {'support': 0.4, 'confidence': 0.75},
                   {'support': 0.5, 'confidence': 0.75},
                   {'support': 0.1, 'confidence': 0.60},
                   {'support': 0.2, 'confidence': 0.60},
                   {'support': 0.4, 'confidence': 0.60},
                   {'support': 0.5, 'confidence': 0.60}]
