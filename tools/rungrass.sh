CONFIG=$1
GPUS=$2
WORKDIR=$3

PORT=${PORT:-29500}
PYTHONPATH="$(dirname $0)/..":$PYTHONPATH
echo $PYTHONPATH
python -m torch.distributed.launch --nproc_per_node=$GPUS --master_port=$PORT \
    $(dirname "$0")/train.py $CONFIG --launcher pytorch ${@:4} --work-dir $WORKDIR --cfg-options \
    data.train.ann_file='data/coco/annotations/train_grass.json' \
    data.train.img_prefix='data/coco/train_grass/' \
    data.val.ann_file='data/coco/annotations/val_grass.json' \
    data.val.img_prefix='data/coco/val_grass/' \

# CUDA_VISIBLE_DEVICES=4,5,6,7 bash tools/dist_train.sh projects/configs/co_deformable_detr/co_deformable_detr_r50_1x_coco.py 7 /workspace/results/test data.train.ann_file='data/coco/annotations/train_grass.json' data.train.img_prefix='data/coco/train_grass/' 
    # data.val.ann_file='data/coco/annotations/val_grass.json' \
    # data.val.img_prefix='data/coco/val_grass/' \