#!/usr/bin/env python3

# G.enerate A.nd S.core P.asswords
# password generator that sorts and serializes output by zxcvn score
# 12AUG20


import argparse
import os
import time
import math
import json

from stopwatch import Stopwatch
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from itertools import product
from zxcvbn import zxcvbn


_CHARS_LIST = list(' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~')

_CPU_COUNT = cpu_count()

_RESULTS_FILENAME_TEMPLATE = 'passwords_length_{}_scored_{}.json'

_FLUSH_THRESHOLD = 1000000

_TARGET_CHUNK_SIZE = 1000


# because permutations returns an iterable of tuples
def get_passwords_generator(n, k):
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
    return n**k


def serialize_results_dict(results_dict, print_message=True):
    if print_message:
        print("serializing password buffer to disk...")

    # *!* this has a bug in it - this will concat valid json blocks together to form one big invalid json file

    for k, v in results_dict.items():
        with open(k, 'a') as f:
            json.dump(v, f)


# *!* ONLY WORKS IF IMAP IS SET TO RETURN AN ORDERED SET OF RESULTS 
#
# assumes the following method of generating the cartesian product
#   GIVEN   
#   - a set of choices 'n'
#   - a number of things 'k' to select from 'n'
#   - multiple instances of the same member of 'n' can be selected
#   - each selection from 'n' is denoted by a pointer 
#   - each pointer is uniquely identified with a number (the first choice is pointer(1), the second,  pointer(2)...)
#   - each pointer starts at index 0 of 'n'
#   THEN FOR EACH ITERATION
#   - shift pointer with the highest identifier to the right one place
#   - if shifted pointer is out of bounds
#     - reset that pointer's position to index 0
#     - shift pointer with the next highest identifier to the right one place
#     - if that pointer goes out of bounds, repeat 
#
# in effect, what happens is that the pointer with the highest identifier
#   - shifts every (len(n) **0) time steps
#   - resets to index 0 every (len(n) ** 1) time steps 
# for the pointer with the next highest identifer
#   - shifts every (len(n) **1) time steps (the reset period for the pointer with the next highest identifier)
#   - resets to index - every (len(n) ** 2) time steps
# etc... 
# 
# another way to think of this is that the pointer with the highest identifier moves every time step. the pointers 
# will reset to index zero every time the fully traverse 'n'. the pointer with the second-highest identifier can't 
# move until the pointer with the highest identifer traverses the list. the pointer with the third-highest identifier
# can't move until the pointer with the second-highest identifier traverses the list. etc etc etc. therefore, every
# pointer's movements (except the pointer with the highest identifier) can be computed  as a function of the movement 
# pattern of the pointer with an identifer one greater than itself. 
# 
# hope this helps you remember, future me. 
# https://youtu.be/fHAOWLhrxhQ?t=47
# 
def get_k_indexes_for_iteration(iteration, n, k):
    results_dict = {}
    shift_period_exponent = 0
    reset_period_exponent = 1
    for i in range(k, 0, -1):
        shift_period = n**shift_period_exponent
        reset_period = n**reset_period_exponent
        time_steps_since_last_reset = iteration % reset_period
        shifts_since_last_reset = time_steps_since_last_reset // shift_period
        results_dict[i] = shifts_since_last_reset
   
        shift_period_exponent += 1
        reset_period_exponent += 1
       
        # print('for pointer number: ', i)
        # print('shift_period is: ', shift_period)
        # print('reset_period is: ', reset_period)
        # print('time_steps_since_last_reset is: ', time_steps_since_last_reset)
        # print('shifts_since_last_reset is: ', shifts_since_last_reset)
        # print('---')
    
    return results_dict


def get_k_indexes_for_iteration_generator(floor, ceiling, n, k):
    for i in range(floor, ceiling):
        yield get_k_indexes_for_iteration(i, n, k)


def get_password_for_indexes_dict(indexes_dict):
    password_iterable = [
        _CHARS_LIST[indexes_dict[i]]
        for i
        in range(1, len(indexes_dict) + 1)
    ]
    
    return ''.join(password_iterable)   


def main(args):
    results_directory = get_results_directory()
    pool = Pool(_CPU_COUNT)
    floor = args.floor
    ceiling = args.ceiling
    n = _CHARS_LIST
    stopwatch = Stopwatch()
    stopwatch.start()
    for k in range(floor, ceiling):
        expected_total = get_cartesian_product_cardinality(len(n), k)
        chunk_size = _TARGET_CHUNK_SIZE if (expected_total / _CPU_COUNT) >= _TARGET_CHUNK_SIZE else 1
        passwords_generator = get_passwords_generator(n, k)
        results_iter = pool.imap_unordered(get_score, passwords_generator, chunksize=chunk_size)
        results_dict = {}
        buffer_size = 0

        print("pool size is: ", _CPU_COUNT)
        print("chunksize is: ", chunk_size)
        print("generating scored passwords...")
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
                    serialize_results_dict(results_dict, print_message=False)
                    results_dict = {}
                    buffer_size = 0

                buffer_size+= 1

        serialize_results_dict(results_dict)
    
    stopwatch.stop()
    print("done! elapsed time: ", stopwatch)


if __name__ == "__main__":
    description_text = "generates all possible combinations of printable characters, " \
        "rates them with zxcvbn, and serializes by length and rating."

    parser = argparse.ArgumentParser(description=description_text)
    parser.add_argument("floor", help="floor of password size to generate.", type=int)
    parser.add_argument("ceiling", help="non-inclusive ceiling of password size to generate", type=int)
    args = parser.parse_args()
    main(args)
