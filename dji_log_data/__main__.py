from .languages import Python

import sys

import argparse
import os

def generate_files(language, frames_out, keys_out):
    l = language()
    l.generate_frames(frames_out)
    l.generate_keys(keys_out)


def main(args=None):
    if args == None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description="Generates files for loading DJI log data")
    supported_languages = {
        'python': Python
    }
    parser.add_argument('-l', '--language',     dest='language',    required=True, choices=supported_languages.keys(),  help='What language to generate code for')
    parser.add_argument('-f', '--frames-out',   dest='frames_out',  required=True, type=argparse.FileType('w'),         help='Where the output the frames file')
    parser.add_argument('-k', '--keys-out',     dest='keys_out',    required=True, type=argparse.FileType('w'),         help='Where the output the keys file')

    parsed_args = parser.parse_args(args)

    generate_files(supported_languages[parsed_args.language], parsed_args.frames_out, parsed_args.keys_out)



if __name__ == '__main__':
    main()