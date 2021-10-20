#!/usr/bin/env python

import argparse


def compute_wer(path):
    incorrect = 0
    total = 0
    with open(path, "r") as source:
        for line in source:
            line = line.rstrip()
            if line.startswith("T"):
                total += 1
                _, t = line.split("\t")
            if line.startswith("D"):
                _, _, d = line.split("\t")
                if t != d:
                    incorrect += 1
    return int(incorrect / total * 100)


def main(args):
    print("WER:", compute_wer(args.path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--path",
        type=str,
        default="predictions.txt",
        help="path to predictions text file",
    )

    main(parser.parse_args())
