#!/usr/bin/env python3

# G.enerate A.nd S.core P.asswords
# password generator that sorts and serializes output by zxcvn score
# 11APR20


import argparse
import os
import time
import math

from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from itertools import permutations
from zxcvbn import zxcvbn


_CHARS_LIST = list(' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~')

_CPU_COUNT = cpu_count()

_RESULTS_FILENAME_TEMPLATE = 'passwords_length_{}_scored_{}'


# because permutations returns an iterable of tuples
def get_passwords_generator(n, k):
    passwords_iter = permutations(n, k)
    passwords_generator = (''.join(password) for password in passwords_iter)
    return passwords_generator


# scores are 0->4. Zero is shite and four is good.
def get_score(pw):
    results = zxcvbn(pw)
    score = results['score']
    password = results['password']
    return [score, password]


def get_results_directory():
    epoch_time = int(time.time())
    results_directory = './results_{}/'.format(epoch_time)
    os.mkdir(results_directory)
    return results_directory


def get_binomial_coefficient(n, k):
    bc = math.factorial(n) / math.factorial(k) / math.factorial(n - k)
    return bc

# ty stack exchange https://math.stackexchange.com/a/221041
def get_permutation_count(n, k):
    pc = math.factorial(n) / math.factorial(n - k)
    return pc


def main(args):
    results_directory = get_results_directory()
    pool = Pool(_CPU_COUNT)
    floor = args.floor
    ceiling = args.ceiling
    n = _CHARS_LIST
    for k in range(floor, ceiling):
        expected_total = get_permutation_count(len(n), k)
        passwords_generator = get_passwords_generator(n, k)
        results_iter = pool.imap_unordered(get_score, passwords_generator)
        with tqdm(total=expected_total) as pbar:
            for result in results_iter:
                score = result[0]
                password = result[1]
                filename = _RESULTS_FILENAME_TEMPLATE.format(k, score)
                path = results_directory + filename
                with open(path, 'a') as f:
                    f.write(password + '\n')

                pbar.update(1)


if __name__ == "__main__":
    description_text = "generates all possible combinations of printable characters, " \
        "rates them with zxcvbn, and serializes by length and rating."

    parser = argparse.ArgumentParser(description=description_text)
    parser.add_argument("floor", help="floor of password size to generate.", type=int)
    parser.add_argument("ceiling", help="non-inclusive ceiling of password size to generate", type=int)
    args = parser.parse_args()
    main(args)
