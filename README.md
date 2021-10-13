# HW 2: Grapheme-to-phoneme conversion

In this assignment you will use [FairSeq](https://github.com/pytorch/fairseq), a
neural network sequence-to-sequence learning tool, to build an [encoder-decoder
LSTM](https://fairseq.readthedocs.io/en/latest/models.html#module-fairseq.models.lstm)
grapheme-to-phoneme engine for Icelandic.

Icelandic is written in a Roman script but the mapping from spelling to
pronunciation regular but rather complex.

This repository contains three data files:

-   training data: [`ice_train.tsv`](ice_train.tsv) is a two-column TSV file in
    which the first column is a Icelandic word in UTF-8, and the second column
    gives that word's space-delimited IPA transcription in UTF-8. There are 800
    training examples in all. For instance, the row

        auga ø yː ɣ a

    indicates that *auga* 'eye' is pronounced \[øyːɣa\].

-   development data: [`ice_dev.tsv`](ice_dev.tsv) is a two-column, 100-row TSV
    file in the same format as the previous file.

-   test data: [`ice_test.tsv`](ice_test.tsv) is a two-column, 100-row TSV file
    in the same format as the previous two files.

## Part 1: environment preparation

First, set up your environment.

### What to do

Install FairSeq:

    pip install fairseq==0.10.2

### What to turn in

Nothing for this part of the assignment.

### Hints

If the above command fails with an error message reading:

    Sorry, Python >= 3.6 is required for fairseq.

Then you are using an (ancient) system Python instead of Conda. Please just use
Conda instead.

## Part 2: preprocessing

FairSeq requires you to "preprocess" the data into binary files that it can read
into memory rapidly during training, development, and testing. Preprocessing is
performed by the
[`fairseq-preprocess`](https://fairseq.readthedocs.io/en/latest/command_line_tools.html#fairseq-preprocess)
command-line tool. This tool takes a series of arguments specifying the location
of the data and how it to be "tokenized" into graphemes and phones. Because this
tool makes certain assumptions about the format of your data, you will have to
first convert the aforementioned TSV and text files as follows:

1.  Write the first column of [`ice_train.tsv`](ice_train.tsv) to a file called
    `train.ice.g`. You must also place a space between each UTF-8 character.
    Thus, the row

        auga ø yː ɣ a

    would appear in `train.ice.g` as

        a u g a

2.  Write the second column of [`ice_train.tsv`](ice_train.tsv) to a file called
    `train.ice.p`. The data has already been segmented with spaces *so do not
    add additional spaces*. Thus the aforementioned row would appear in
    `train.ice.p` as

        ø yː ɣ a

3.  Write the first column of [`ice_dev.tsv`](ice_dev.tsv) to a file called
    `dev.ice.g` using the same style as you did in step 1.

4.  Write the second column of [`ice_dev.tsv`](ice_dev.tsv) to a file called
    `dev.ice.p` using the same style as you did in step 2.

5.  Write the first column of [`ice_test.tsv`](ice_test.tsv) to a file called
    `test.ice.g` using the same style as you did in steps 1 and 3.

6.  Write the second column of [`ice_test.tsv`](ice_test.tsv) to a file called
    `test.ice.p` using the same style as you did in steps 2 and 4.

Then, call `fairseq-preprocess` as follows:

    fairseq-preprocess \
        --source-lang ice.g \
        --target-lang ice.p \
        --trainpref train \
        --validpref dev \
        --testpref test \
        --tokenizer space \
        --thresholdsrc 2 \
        --thresholdtgt 2

### What to turn in

1.  All Python code you used to prepare the data.
2.  The logging output from `fairseq-preprocess`.

### Hints

-   The `\` character used at the end of a lines above is a "continuation": it
    indicates that the current command continues on the next line. You yourself
    do not need to type it in at the command line.
-   You need to name the files exactly what I say: `fairseq-preprocess` is
    finicky like that.
-   Visually inspect all six `.g` and `.p` files before attempting to call
    `fairseq-preprocess`; confirm there are no blank lines and that there are
    spaces between grapheme and phone symbols.
-   Read the [the
    docs](https://fairseq.readthedocs.io/en/latest/command_line_tools.html#fairseq-preprocess)
    for `fairseq-preprocess`.
-   If you call `fairseq-preprocess` multiple times it may crash with a
    `FileExistsError`. If you see this error, simply remove the `data-bin`
    directory and try again.

## Part 3: training

Model training is performed by the
[`fairseq-train`](https://fairseq.readthedocs.io/en/latest/command_line_tools.html#fairseq-train)
command-line tool.

#### What to do

Using `fairseq-train`, train the model. You should use the following parameters:

-   random seed: pick some random number
-   architecture: LSTM
-   bidirectional encoder
-   dropout probability .2
-   encoder embedding dimensionality: 128
-   decoder embedding dimensionality: 128
-   decoder output embedding dimensionality: 128
-   encoder hidden layer size: 512
-   decoder hidden layer size: 512
-   criterion: label-smoothed cross-entropy
-   label smoothing coefficient: .1
-   optimizer: Adam
-   learning rate: .001
-   norm clipping coefficient: 1
-   batch size: 50
-   maximum number of updates: 800
-   don't store epoch checkpoints

If successful, this will produce two large model files in a `checkpoints`
directory.

### What to turn in

The `fairseq-train` command you ran.

#### Hints

-   You do not need to write any Python for this step; your goal here is to read
    the documentation carefully and figure out how to get `fairseq-train` to do
    what you want.

-   The command will begin as follows:

        fairseq-train \
            data-bin \
            --source-lang ice.g \
            --target-lang ice.p \
            ...

    but many more flags are required (roughly, one for each bullet point).

-   Read [the
    docs](https://fairseq.readthedocs.io/en/latest/command_line_tools.html#fairseq-train)
    for `fairseq-train`.

### Part 4: evaluation

Grapheme-to-phoneme conversion engines are traditionally evaluated using word
error rate (WER), which is simply the percentage of incorrectly predicted word
pronuniciations in the test set. Unfortunately, FairSeq does not provide any
tool to compute word error rate. Instead, the
[`fairseq-generate`](https://fairseq.readthedocs.io/en/latest/command_line_tools.html#fairseq-generate)
command-line tool is used for inference/prediction, and this program's output
can then be processed to compute WER.

#### What to do

Run the following command to write the one-best prediction for each test example
to a file called `predictions.txt`.

    fairseq-generate \
        data-bin \
        --source-lang ice.g \
        --target-lang ice.p \
        --path checkpoints/checkpoint_best.pt \
        --gen-subset test \
        --beam 8 \
        > predictions.txt

Then, automatically process `predictions.txt`, a verbose (but human-readable)
text file, to compute test set WER.

#### What to turn in

1.  A Python script for computing WER from the `predictions.txt` file.
2.  Your word error rate, rounded to an appropriate number of digits given the
    number of test examples.

#### Hints

-   I obtained a WER of 23, but your mileage may vary somewhat.
-   Since there are only 100 examples, multiply WER by 100 and round to the
    nearest integer. Thus WER should be some number between 0 and 100, the
    smaller the better.
-   In this file, the gold ("target") pronunciation is indicated by line-initial
    `T-` and the predicted ("hypothesis") pronunciation is indicated by
    line-initial `H-`.
-   Don't forget to turn in your WER.
-   Read [the
    docs](https://fairseq.readthedocs.io/en/latest/command_line_tools.html#fairseq-generate)
    for `fairseq-generate`.

## Part 5: reflection

Please provide a brief (roughly one page) reflection on this assignment.

### What to turn in

A brief description of the challenges and problems you ran into during this
assignment.

## Stretch goals

-   Run the above experiment on a GPU, such as available in the computational
    linguistics lab (7400.13). Using `time` to keep track of "wall clock" time
    (i.e., human time), report the runtime of the CPU and GPU versions.
-   Tune at least two of the hyperparameters to minimize word error rate on the
    development set.
-   Perform an error analysis along the lines proposed in section 8 of [Ashby et
    al. 2021](https://aclanthology.org/2021.sigmorphon-1.13/).
-   Try an alternative sequence-to-sequence model supported by FairSeq, such as
    the
    [transformer](https://fairseq.readthedocs.io/en/latest/models.html#module-fairseq.models.transformer),
    using hyperparameters such as those proposed by [Wu et
    al. 2021](https://aclanthology.org/2021.eacl-main.163/).
