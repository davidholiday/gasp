# G.enerate A.nd S.core P.asswords

### what is it?
GASP is a password generator that sorts and serializes output by [zxcvn](https://github.com/dropbox/zxcvbn) score. 

### why do I care?
GASP, unlike rote brute-force generation methods, will score and order its results by both length of password and by zxcvn score. This is intended to augment the excellent [SecLists repository](https://github.com/danielmiessler/SecLists) of dictionary files. If you've tried everything there and haven't come up with a winning combination, this script will give you an organized set of options to play with. 

### how does it work? 
GASP is written in Python3. When invoked it will spin up *n* workers, where *n* is the number of cores on your machine. Those workers will 
* compute every possible permutation of printable characters between a floor and ceiling range you provide
* get the zxcvn score for each combination 
* serialize the results to disk under a sub-directory named `results_{EPOCH_TIME}`. Files are named `passwords_length_{LENGTH}_scored_{SCORE}`.
* GASP uses [tqdm](https://tqdm.github.io/) to print job progress to the terminal. 

### how do I use it? 
* make sure you have python >= 3.6 installed.
* it is recommended you use the `requirements.txt` file to create a `venv` to work in. See [this](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv) for instructions on how to do that. 
* syntax:
```bash
usage: gasp.py [-h] floor ceiling

generates all possible combinations of printable characters, rates them with
zxcvbn, and serializes by length and rating.

positional arguments:
  floor       floor of password size to generate.
  ceiling     non-inclusive ceiling of password size to generate

optional arguments:
  -h, --help  show this help message and exit
```


### other 
* *GASP is intended for educational and legal purposes only.*
* *TODO* add option to control the number of workers
* *TODO* add option to restore a halted run
* *TODO* add option to supply regex to provide generate passwords in accordance with a given password policy 
* *TODO* add option to automagically filter results based on presence in another password file / directory of password files
