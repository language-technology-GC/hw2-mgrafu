fairseq-generate \
    data-bin \
    --source-lang ice.g \
    --target-lang ice.p \
    --path checkpoints/checkpoint_best.pt \
    --gen-subset test \
    --beam 8 \
    > predictions.txt
