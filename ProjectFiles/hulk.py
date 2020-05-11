#!/usr/bin/env python3

import concurrent.futures
import hashlib
import os
import string
import sys

# Constants

ALPHABET = string.ascii_lowercase + string.digits

# Functions

def usage(exit_code=0):
    progname = os.path.basename(sys.argv[0])
    print(f'''Usage: {progname} [-a ALPHABET -c CORES -l LENGTH -p PATH -s HASHES]
    -a ALPHABET Alphabet to use in permutations
    -c CORES    CPU Cores to use
    -l LENGTH   Length of permutations
    -p PREFIX   Prefix for all permutations
    -s HASHES   Path of hashes file''')
    sys.exit(exit_code)

def md5sum(s):
    ''' Compute md5 digest for given string. '''
    # TODO: Use the hashlib library to produce the md5 hex digest of the given
    # string.
    s = s.encode()
    s = hashlib.md5(s)
    s = s.hexdigest()
    return s

def permutations(length, alphabet=ALPHABET):
    ''' Recursively yield all permutations of the given length using the
    provided alphabet. '''
    # TODO: Use yield to create a generator function that recursively produces
    # all the permutations of the given length using the provided alphabet.

    # base case (return nothing)
    if length == 0:
        yield ''

    # recursive call for each letter in alphabet
    else:
        for letter in alphabet:
            for p in permutations(length - 1, alphabet):
                yield letter + p

def flatten(sequence):
    ''' Flatten sequence of iterators. '''
    # TODO: Iterate through sequence and yield from each iterator in sequence.

    # use nested for loop to return 1 generator
    for seq in sequence:
        for it in seq:
            yield it

def crack(hashes, length, alphabet=ALPHABET, prefix=''):
    ''' Return all password permutations of specified length that are in hashes
    by sequentially trying all permutations. '''
    # TODO: Return list comprehension that iterates over a sequence of
    # candidate permutations and checks if the md5sum of each candidate is in
    # hashes.
    passwords = [prefix + pw for pw in permutations(length, alphabet) if md5sum(prefix+pw) in hashes]
    return passwords

def cracker(arguments):
    ''' Call the crack function with the specified arguments '''
    return crack(*arguments)

def smash(hashes, length, alphabet=ALPHABET, prefix='', cores=1):
    ''' Return all password permutations of specified length that are in hashes
    by concurrently subsets of permutations concurrently.
    '''
    # TODO: Create generator expression with arguments to pass to cracker and
    # then use ProcessPoolExecutor to apply cracker to all items in expression.

    # create a sequence of tuples to be passed into cracker
    arguments = ((hashes, length-1, alphabet, prefix + p) for p in alphabet)

    # use multiple cores to perform the cracking
    with concurrent.futures.ProcessPoolExecutor(cores) as executor:
            passwords = flatten(executor.map(cracker, arguments))

    return passwords

def main():
    arguments   = sys.argv[1:]
    alphabet    = ALPHABET
    cores       = 1
    hashes_path = 'hashes.txt'
    length      = 1
    prefix      = ''

    # TODO: Parse command line arguments
    while arguments:
        argument = arguments.pop(0)
        if argument == '-a':
            alphabet = arguments.pop(0)
        elif argument == '-c':
            cores = int(arguments.pop(0))
        elif argument == '-l':
            length = int(arguments.pop(0))
        elif argument == '-p':
            prefix = arguments.pop(0)
        elif argument == '-s':
            hashes_path = arguments.pop(0)
        else:
            usage(1)


    # TODO: Load hashes set
    hashes = set()
    for h in open(hashes_path):
        hashes.add(h.rstrip())


    # TODO: Execute crack or smash function
    passwords = smash(hashes, length, alphabet, prefix, cores)

    # TODO: Print all found passwords
    for password in passwords:
       print(password)


# Main Execution

if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
