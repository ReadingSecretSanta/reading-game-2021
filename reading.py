#!/usr/bin/python3
"""
Module documentation is for squares.
"""

import hashlib
import os
import subprocess
import sys
import time

def sha256str(x):
    """
    Convenience function to compute the SHA256 hash of the string
    representation of an object. Returns the hash as a hexadecimal string.

    :rtype: str
    """
    return hashlib.sha256(str(x).encode('utf-8')).hexdigest()


_ANSWER_HASHES = {
    "module1" : '63479ad69a090b258277ec8fba6f99419a2ffb248981510657c944ccd1148e97',
    "module2" : '7f1064d5b57feeff68efa92e54885c65984d389d4128f92549b86b481806a288',
    "module3" : '139f7142f4b7efda09983101409cd9c8ec34bdf0dc411caa762b9cfbf088e807',
    "module4" : 'fd74f24b7141d07a06044c06c9df4a75dd35577142802ec71e9c8ec5102430c1',
    "module5" : 'ea3a38c1c7d110bd293de20057ec66203413b447780d4c4a4d9f8c0c8ac2f9c8',
}

def clean(s):
    """
    Returns a version of the given string that removes silly formatting.
    """
    r = ""
    for c in s:
        if c.isalpha() or c.isdigit():
            r += c.lower()

    return r


def verify(inputs):
    """
    Verifies that the answer is correct for the answers in the given questions

    :type  inputs: dict[str,str]
    """
    if not isinstance(inputs, dict):
        raise TypeError("inputs must be a dict, got %s instead" % type(inputs))

    for inpt, value in sorted(inputs.items()):
        print("Parsing input '%s' '%s'" % (inpt, value))
        norm_inpt  = str(inpt).lower()
        norm_value = str(value).upper()
        norm_inpt  = clean(str(inpt))
        norm_value = clean(str(value))

        good_hash = _ANSWER_HASHES.get(norm_inpt)
        if good_hash is None:
            raise ValueError("Input '%s' is not needed." % (inpt,))

        value_hash = sha256str(norm_value)

        if value_hash != good_hash:
            raise ValueError("Input '%s' has invalid value, '%s'." % (inpt, value))

        module_fn = "%s.py.enc" % norm_inpt
        if not os.path.exists(module_fn):
            raise IOError("Missing critical file '%s'!" % module_fn)

        # Kinda hacky, but should work on most Mac & Linux systems without
        # installing any additional libraries.
        code = subprocess.check_output(["openssl",
                                        "enc",
                                        "-aes256",
                                        "-pbkdf2",
                                        "-d",
                                        "-in", "%s.py.enc" % norm_inpt,
                                        "-k", norm_value])
        exec(code)

        result = locals()['read'](x=value, y=inpt, z=len(inputs))

        if result != 7:
            raise ValueError("What is this return value!? It clearly should be "
                             "7...")


def main():
    args = sys.argv
    if len(args) == 1 or args[0].split(".")[0] != args[1]:
        print("Something is missing...\n")
        sys.exit(3)

    else:
        print("Greetings, Dr. Wu.\n")

        print("First question to help verify your identity:\n"
              "What is a cryptographer's favorite spice?\n")

    # Check if inputs were given from the commandline.
    if len(args) > 2 and len(args) % 2 == 0:
        inputs = dict(zip(args[2::2], args[3::2]))

    else:
        print("Hmm, some arguments seem to be missing...")
        sys.exit(4)

    verify(inputs)


if __name__ == "__main__":
    main()
