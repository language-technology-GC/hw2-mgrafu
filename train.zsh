fairseq-train \
    data-bin \
    --source-lang ice.g \
    --target-lang ice.p \
    --seed 42 \
    --arch lstm \
    --encoder-bidirectional \
    --dropout .2 \
    --encoder-embed-dim 128 \
    --decoder-embed-dim	128 \
    --decoder-out-embed-dim	128 \
    --criterion label_smoothed_cross_entropy \
    --label-smoothing .1 \
    --optimizer adam \
    --lr .001 \
    --clip-norm 1 \
    --batch-size 50 \
    --max-update 800 \
    --no-epoch-checkpoints
