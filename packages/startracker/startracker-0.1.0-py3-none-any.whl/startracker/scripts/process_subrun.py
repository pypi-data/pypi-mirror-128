#!/usr/bin/env python

'''
Helper script to process one subrun on a worker node.
'''

import argparse
import pickle

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pickle', help='File with pickled StarExtractor object',
                        required=True)
    parser.add_argument('-n', '--subrun-number', help='Subrun number to analyze', type=int,
                        default=0)
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    with open(args.pickle, 'rb') as f:
        star_extractor = pickle.load(f)
    star_extractor.produce(args.subrun_number)

if __name__ == '__main__':
    main()
