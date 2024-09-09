#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

from PIL import Image
import imagehash
import os
import sys
import time
import mss
import json

"""
哈希示例
"""

def is_image(filename):
    f = filename.lower()
    return f.endswith('.png') or f.endswith('.jpg') or \
           f.endswith('.jpeg') or f.endswith('.bmp') or \
           f.endswith('.gif') or '.jpg' in f or f.endswith('.svg')

def load_hashes_from_json(json_path):
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            return json.load(f)
    return []

def load_all_hashes(library_path):
    all_hashes = {}
    for filename in os.listdir(library_path):
        if filename.endswith('.json'):
            json_path = os.path.join(library_path, filename)
            episode = filename.split('.')[0]  # 提取集数
            hashes = load_hashes_from_json(json_path)
            all_hashes[episode] = hashes
    return all_hashes

def find_similar_images(input_image_path, hashfunc, all_hashes):
    if os.path.exists(input_image_path):
        input_hash = str(hashfunc(Image.open(input_image_path)))
        max_similarity = -1
        most_similar_episode = None
        most_similar_timestamp = None

        for episode, hashes in all_hashes.items():
            for i, hash_value in enumerate(hashes):
                similarity = 1 - (imagehash.hex_to_hash(input_hash) - imagehash.hex_to_hash(hash_value)) / len(input_hash) ** 2
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_episode = episode
                    most_similar_timestamp = i

        if most_similar_episode and most_similar_timestamp is not None:
            timestamp_seconds = most_similar_timestamp
            minutes = int(timestamp_seconds // 60)
            seconds = int(timestamp_seconds % 60)
            time_format = f"{minutes}:{seconds:02d}"
            if most_similar_episode == 'S0':
                episode_info = '序幕'
            else:
                episode_info = f'第{most_similar_episode[1:]}集'
            print(f"输入图像最相似于: 位于{episode_info}，{time_format}")
            print("相似度:", max_similarity)
        else:
            print("输入图像不相似于数据库中的任何图像。")

def capture_screen():
    with mss.mss() as sct:
        screenshot = sct.shot(output="screenshot.png")
    return "screenshot.png"

def schedule_screen_capture(hashfunc, library_path):
    all_hashes = load_all_hashes(library_path)
    while True:
        screenshot_path = capture_screen()
        find_similar_images(screenshot_path, hashfunc, all_hashes)
        time.sleep(6)

if __name__ == '__main__':  # noqa: C901
    def usage():
        sys.stderr.write("""用法: %s [ahash|phash|dhash|...]

识别目录中相似的图像。

方法:
  ahash:          平均哈希
  phash:          感知哈希
  dhash:          差异哈希
  whash-haar:     Haar小波哈希
  whash-db4:      Daubechies小波哈希
  colorhash:      HSV颜色哈希
  crop-resistant: 抗裁剪哈希

(C) Johannes Buchner, 2013-2017
""" % sys.argv[0])
        sys.exit(1)

    # 直接在代码中指定输入图像路径和比较库目录
    library_path = r"D:\imagehash-master\imagehash-master\hash_library"

    # 直接在代码中指定哈希函数
    hashfunc = imagehash.average_hash  # 默认使用平均哈希 (ahash)
    # hashfunc = imagehash.phash  # 切换到感知哈希 (phash)
    # hashfunc = imagehash.dhash  # 切换到差异哈希 (dhash)
    # hashfunc = imagehash.whash  # 切换到 Haar 小波哈希 (whash-haar)
    # def hashfunc(img):
    #     return imagehash.whash(img, mode='db4')  # 切换到 Daubechies 小波哈希 (whash-db4)
    # hashfunc = imagehash.colorhash  # 切换到 HSV 颜色哈希 (colorhash)
    # hashfunc = imagehash.crop_resistant_hash  # 切换到抗裁剪哈希 (crop-resistant)

    # 选择要执行的方法：实时屏幕监测或输入图片监测
    # 注释掉不需要的方法

    # 实时屏幕监测
    # schedule_screen_capture(hashfunc, library_path)

    # 输入图片监测
    input_image_path = r"D:\imagehash-master\imagehash-master\2.png"
    all_hashes = load_all_hashes(library_path)
    find_similar_images(input_image_path, hashfunc, all_hashes)