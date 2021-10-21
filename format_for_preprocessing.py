#!/usr/bin/env python
import os.path

from typing import List


def output_formatted_files(path: str) -> None:
    _, file = os.path.split(path)
    name, _ = os.path.splitext(file)
    lang, sample = name.split("_")
    g_sink_path = sample + "." + lang + ".g"
    p_sink_path = sample + "." + lang + ".p"
    with open(path, "r") as source, open(g_sink_path, "w") as g_sink, open(
        p_sink_path, "w"
    ) as p_sink:
        for line in source:
            grapheme, phoneme = line.rstrip().split("\t")
            grapheme = " ".join([char for char in grapheme])
            print(grapheme, file=g_sink)
            print(phoneme, file=p_sink)


def main() -> None:
    file_paths: List[str] = ["ice_dev.tsv", "ice_test.tsv", "ice_train.tsv"]
    for path in file_paths:
        output_formatted_files(path)


if __name__ == "__main__":
    main()
