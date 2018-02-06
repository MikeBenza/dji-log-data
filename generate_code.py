from languages import Python

import argparse
import os

def generate_files(language, frames_out, keys_out):
    l = language(os.path.join('data', 'frames.json'), os.path.join('data', 'keys.json'), 'templates')
    l.generate_frames(frames_out)
    l.generate_keys(keys_out)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generates files for loading DJI log data")
    supported_languages = {
        'python': Python
    }
    parser.add_argument('-l', '--language',     dest='language',    required=True, choices=supported_languages.keys(),  help='What language to generate code for')
    parser.add_argument('-f', '--frames-out',   dest='frames_out',  required=True, type=argparse.FileType('w'),         help='Where the output the frames file')
    parser.add_argument('-k', '--keys-out',     dest='keys_out',    required=True, type=argparse.FileType('w'),         help='Where the output the keys file')

    args = parser.parse_args()

    generate_files(supported_languages[args.language], args.frames_out, args.keys_out)

