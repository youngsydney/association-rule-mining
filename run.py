"""
Main script which runs the Association Rule Mining program
"""
import time
import tqdm

from load import DataLoader
from fptree import FPTreeBuilder
from mine import Miner
from support import FPTreeSupportBuilder
from generator import Generator
from reporter import Reporter
import config

def main():
    """
    Controls the flow
    """
    # load the product list and transaction into memory
    loader = DataLoader()
    transactions, products = loader.return_p_t()

    reporter = Reporter()
    start_total = time.time()

    if config.ADDITIONAL:
        runs = config.runs_additional
    else:
        runs = config.runs

    for run in tqdm.tqdm(runs):
        start = time.time()
        config.SUPPORT = run['support']
        config.CONFIDENCE = run['confidence']
        # find the frequent items and build the ordered transactions
        support_builder = FPTreeSupportBuilder(transactions, products)
        L_list, o_transactions, min_support = support_builder.build()

        # build the FP tree
        tree_builder = FPTreeBuilder(L_list, o_transactions)
        tree, header_list = tree_builder.build_tree()

        miner = Miner(min_support, tree, header_list)
        frequent_patterns, frequent_patterns_count, K, K_freq = miner.run_miner()

        gen = Generator(frequent_patterns, frequent_patterns_count)
        gen.generate_rules(len(transactions))
        rules = gen.filter_correlations(len(transactions))
        end = time.time()
        values = {'sup': run['support'], 'conf': run['confidence'],
                  'freq': K_freq, 'K': K, 'rules': len(rules),
                  'time': (end - start)}
        reporter.add_run(values, rules)
    reporter.display()
    reporter.top_15_rules()
    end_total = time.time()
    print "Total Time: " + str(end_total-start_total)

if __name__ == "__main__":
    """
    Runs the control.
    """
    main()
