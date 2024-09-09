import subprocess
import os
import json
from PIL import Image
import imagehash

def extract_frames(video_path, output_folder, episode):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 使用FFmpeg命令提取帧并重命名
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', 'fps=1',   # 每秒截一帧
        os.path.join(output_folder, f'{episode}_%08d.png')
    ]

    subprocess.run(command, check=True)

def calculate_hashes(output_folder, episode):
    hash_list = []
    for filename in sorted(os.listdir(output_folder)):
        if filename.endswith('.png') and filename.startswith(episode):
            image_path = os.path.join(output_folder, filename)
            try:
                hash = imagehash.average_hash(Image.open(image_path))
                hash_list.append(str(hash))
            except Exception as e:
                print(f"Error calculating hash for {filename}: {e}")
    return hash_list

def save_hashes_to_json(hash_list, output_folder):
    json_path = os.path.join(output_folder, 'S7.json')
    with open(json_path, 'w') as json_file:
        json.dump(hash_list, json_file, indent=4)

if __name__ == '__main__':
    video_path = r"D:\imagehash-master\imagehash-master\video\S7.mp4" # 输入视频文件路径
    output_folder = r"D:\imagehash-master\imagehash-master\library\S7" # 输出帧文件夹路径
    episode = 'S7' # 集数

    # 提取帧并重命名,保存图片部分，不用可注释
    extract_frames(video_path, output_folder, episode)
    print("Frames extracted and renamed successfully.")

    # 计算哈希值并保存到JSON,保存图片哈希值部分，不用可注释
    hash_list = calculate_hashes(output_folder, episode)
    save_hashes_to_json(hash_list, output_folder)
    print("Hashes calculated and saved to JSON successfully.")