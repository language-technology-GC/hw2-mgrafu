./format_for_preprocessing.py
fairseq-preprocess \
    --source-lang ice.g \
    --target-lang ice.p \
    --trainpref train \
    --validpref dev \
    --testpref test \
    --tokenizer space \
    --thresholdsrc 2 \
    --thresholdtgt 2 \
    > preprocessing_output.txt
rm dev.ice.g dev.ice.p test.ice.g test.ice.p train.ice.g train.ice.p