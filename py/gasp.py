#!/usr/bin/env python3

# G.enerate A.nd S.core P.asswords
# password generator that sorts and serializes output by zxcvn score
# 12AUG20


import argparse
import os
import time
import math

from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from itertools import product
from zxcvbn import zxcvbn


#_CHARS_LIST = list(' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
_CHARS_LIST = list('ABC')
_CPU_COUNT = cpu_count()

_RESULTS_FILENAME_TEMPLATE = 'passwords_length_{}_scored_{}'

_FLUSH_THRESHOLD = 100000000


# because permutations returns an iterable of tuples
def get_passwords_generator(n, k):
    #passwords_iter = permutations(n, k)
    passwords_iter = product(n, repeat=k)
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


# ty internets 
# https://study.com/academy/answer/how-many-elements-are-in-the-cartesian-product-axb.html
# https://mathhelpforum.com/threads/cardinality-of-a-cartesian-product.217325/
#
def get_cartesian_product_cardinality(n, k):
    # we're squaring 'n' because the set of things to choose from can be repeated n times
    return (n**2) * k


def serialize_results_dict(results_dict):
    for k, v in results_dict.items():
        for e in v:
            with open(k, 'a') as f:
                f.write(e + '\n')

    results_dict = {}


def main(args):
    results_directory = get_results_directory()
    pool = Pool(_CPU_COUNT)
    floor = args.floor
    ceiling = args.ceiling
    n = _CHARS_LIST
    for k in range(floor, ceiling):
        expected_total = get_cartesian_product_cardinality(len(n), k)
        passwords_generator = get_passwords_generator(n, k)
        results_iter = pool.imap_unordered(get_score, passwords_generator)
        results_dict = {}
        buffer_size = 0
        with tqdm(total=expected_total) as pbar:
            for result in results_iter:
                score = result[0]
                password = result[1]
                filename = _RESULTS_FILENAME_TEMPLATE.format(k, score)
                path = results_directory + filename
                pbar.update(1)

                # we only want to serialize passwords scored lower than four. the reason is
                # we can infer that anything not serialized has a score of four and the set of
                # passwords scored 1, 2, or 3 is much smaller than the set of things scored
                # 4 (and thus is more manageable list).
                if score == 4:
                    continue

                if path in results_dict.keys():
                    results_dict[path].append(password)
                else:
                    results_dict[path] = [password]

                if buffer_size > _FLUSH_THRESHOLD:
                    serialize_results_dict(results_dict)
                    buffer_size = 0

                buffer_size+= 1

        serialize_results_dict(results_dict)



if __name__ == "__main__":
    description_text = "generates all possible combinations of printable characters, " \
        "rates them with zxcvbn, and serializes by length and rating."

    parser = argparse.ArgumentParser(description=description_text)
    parser.add_argument("floor", help="floor of password size to generate.", type=int)
    parser.add_argument("ceiling", help="non-inclusive ceiling of password size to generate", type=int)
    args = parser.parse_args()
    main(args)
