#!python

"""
    Enable or Disable your touchpad on a Linux device
    if it bothers you when writing code!

    usage: Enable/Disable touchpad by using xinput functionality

    optional arguments:
      -h, --help  show this help message and exit
      -e          Enable protection from distrations
      -d          Disable protection from distrations
      Author: Stelios Tsagkarakis
"""

import os
import argparse
import itertools

s = 'touchpad'
s_perm = list(map(''.join, itertools.product(*zip(s.upper(), s.lower()))))

def parse_arguments():
    argparser = argparse.ArgumentParser(
        usage="python3 " + __file__,
        description="Enable/Disable the touchpad."
    )

    # pop this group to add required group first
    optional = argparser._action_groups.pop()
    required = argparser.add_argument_group("required arguments")
    argparser._action_groups.append(optional)

    required.add_argument('-e',
                          help="""Enable the touchpad.""",
                          action='store_true')

    required.add_argument('-d',
                          help="""Disable the touchpad.""",
                          action='store_true')

    args = argparser.parse_args()
    return args

def find_touchpad_device_ID():
    stream = os.popen('xinput list')
    output = stream.read()
    lines = output.split('\n')
    res_idx = -1
    for idx,item in enumerate(lines):
        tokens = item.split()
        # pprint(tokens)
        for i in s_perm:
            if i in tokens:
                res_idx = idx
                break
        if res_idx != -1:
            break

    try:
        assert res_idx != -1
    except AssertionError:
        print("Touchpad not found")
        exit(-1)
    
    # assured that res_idx != -1
    touchpadID = -1
    for idx,item in enumerate(tokens):
        f_res = item.find("id=")
        if f_res == 0:
            touchpadID = tokens[idx].split('=')[1]
            break

    return touchpadID


def enable_touchpad():
    os.system('xinput enable '+str(find_touchpad_device_ID()))
    print("Touchpad Enabled.")


def disable_touchpad():
    os.system('xinput disable '+str(find_touchpad_device_ID()))
    print("Touchpad Disabled.")    


if __name__ == "__main__":
    args = parse_arguments()
    assert (args.e ^ args.d)

    if args.e:
        enable_touchpad()
    
    if args.d:
        disable_touchpad()
