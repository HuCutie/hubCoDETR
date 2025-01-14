# Copyright (c) OpenMMLab. All rights reserved.
import argparse

import cv2
import mmcv

from mmdet.apis import inference_detector, init_detector
from projects import *
from mmcv import Config
from mmdet.datasets import build_dataset


def parse_args():
    parser = argparse.ArgumentParser(description='MMDetection video demo')
    parser.add_argument('--video', default='/workspace/test2.mp4', help='Video file')
    parser.add_argument('--config', default='/workspace/projects/configs/co_deformable_detr/co_deformable_detr_r50_1x_coco.py', help='Config file')
    parser.add_argument('--checkpoint', default='/workspace/results/11373_2e-4/epoch_100.pth', help='Checkpoint file')
    parser.add_argument(
        '--device', default='cuda:4', help='Device used for inference')
    parser.add_argument(
        '--score-thr', type=float, default=0.3, help='Bbox score threshold')
    parser.add_argument('--out', type=str, default='A_lr2e-4.mp4', help='Output video file')
    parser.add_argument('--show', action='store_true', help='Show video')
    parser.add_argument(
        '--wait-time',
        type=float,
        default=1,
        help='The interval of show (s), 0 is block')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    assert args.out or args.show, \
        ('Please specify at least one operation (save/show the '
         'video) with the argument "--out" or "--show"')

    model = init_detector(args.config, args.checkpoint, device=args.device)

    video_reader = mmcv.VideoReader(args.video)
    video_writer = None
    if args.out:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(
            args.out, fourcc, video_reader.fps,
            (video_reader.width, video_reader.height))

    cfg = Config.fromfile(args.config)
    dataset = build_dataset(cfg.data.test)
    PALETTE = getattr(dataset, 'PALETTE', None)
    
    for frame in mmcv.track_iter_progress(video_reader):
        result = inference_detector(model, frame)
        frame = model.show_result(frame, result, score_thr=args.score_thr, bbox_color=PALETTE, text_color=PALETTE, mask_color=PALETTE,)
        if args.show:
            cv2.namedWindow('video', 0)
            mmcv.imshow(frame, 'video', args.wait_time)
        if args.out:
            video_writer.write(frame)

    if video_writer:
        video_writer.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
