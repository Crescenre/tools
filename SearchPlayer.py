import os
import json
import re
import shutil


class CharacterKey:

    def __init__(self, account, server, character, subfolder, path):
        self.Account = account
        self.Server = server
        self.Character = character
        self.Subfolder = subfolder
        self.Path = path

    def to_json(self):
        return {
            '账号': self.Account,
            '大区': self.Server,
            '区服': self.Character,
            '角色': self.Subfolder,
            '键位路径': self.Path,

        }


# 将角色信息写入json
def scan_key(root_dir, output_file):
    user_dir = os.path.join(root_dir, 'userdata')
    folder_infos = []  # 用于收集所有的文件夹信息
    for subdir, dirs, files in os.walk(user_dir):
        # 检查当前目录是否是“双线区”或“电信区”
        if subdir.endswith(os.sep + "双线区") or subdir.endswith(os.sep + "电信区"):
            # 如果是，提取上一级目录名称作为账号名
            account = os.path.basename(os.path.dirname(subdir))
            # 确定大区名称
            server = "双线区" if subdir.endswith(os.sep + "双线区") else "电信区"
            # 遍历“双线区”或“电信区”下的所有直接子目录
            for dir_name in dirs:
                character_dir = os.path.join(subdir, dir_name)
                character = dir_name
                # 遍历这一层下的所有直接子目录
                for sub_dir_name in os.listdir(character_dir):
                    sub_dir_path = os.path.join(character_dir, sub_dir_name)
                    # 确保这是一个目录而不是文件
                    if os.path.isdir(sub_dir_path):
                        # 构造FolderInfo对象并添加到列表中
                        folder_info = CharacterKey(account, server, character, sub_dir_name, sub_dir_path)
                        folder_infos.append(folder_info.to_json())

                        # 在写入文件之前，按照账号名称对folder_infos进行排序
    sorted_folder_infos = sorted(folder_infos, key=lambda x: x['账号'])

    # 将所有的文件夹信息写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sorted_folder_infos, f, ensure_ascii=False, indent=4)

    # 配置和调用部分与之前相同


# 删除空角色文件
def clean_empty_file_directories(root_dir):
    user_dir = os.path.join(root_dir, 'userdata')

    # 遍历 userdata 目录下的直接子文件夹
    for subdir in os.listdir(user_dir):
        subdir_path = os.path.join(user_dir, subdir)
        if os.path.isdir(subdir_path):
            # 检查并删除每个子文件夹中只包含文件的子文件夹
            for subsubdir in os.listdir(subdir_path):
                subsubdir_path = os.path.join(subdir_path, subsubdir)
                if os.path.isdir(subsubdir_path):
                    if all(os.path.isfile(os.path.join(subsubdir_path, f)) for f in os.listdir(subsubdir_path)):
                        print(f"Deleting directory with only files: {subsubdir_path}")
                        shutil.rmtree(subsubdir_path)

            # 检查并删除每个子文件夹中的空的 电信区 或 双线区 文件夹
            for specific_folder in ['电信区', '双线区']:
                specific_folder_path = os.path.join(subdir_path, specific_folder)
                if os.path.exists(specific_folder_path) and os.path.isdir(specific_folder_path):
                    if not os.listdir(specific_folder_path):
                        print(f"Deleting empty directory: {specific_folder_path}")
                        shutil.rmtree(specific_folder_path)
                    else:
                        # 遍历非空的电信区或双线区目录下的直接子文件夹，删除其中的空文件夹
                        for sub_specific_folder in os.listdir(specific_folder_path):
                            sub_specific_folder_path = os.path.join(specific_folder_path, sub_specific_folder)
                            if os.path.isdir(sub_specific_folder_path):
                                if not os.listdir(sub_specific_folder_path):
                                    print(f"Deleting empty directory: {sub_specific_folder_path}")
                                    shutil.rmtree(sub_specific_folder_path)



def parse_jx3dat(content):
    # 去掉 return 并替换单引号为双引号
    content = content.replace('return ', '').replace("'", '"')

    # 使用正则表达式将属性名和值转换为带双引号的格式
    content = re.sub(r'(\w+)=', r'"\1":', content)

    # 修复重复的双引号问题
    content = re.sub(r'""([^""]*)""', r'"\1"', content)

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        print(f"处理后的内容: {content}")
        raise e

    return data

# 将角色信息写入json
def scan_plug(root_dir, output_file):
    user_dir = os.path.join(root_dir, 'interface\my#data')
    # 用于存储用户信息的列表
    user_data = []
    # 遍历 user_dir 目录下的所有子目录
    # 遍历 user_dir 目录下的所有子目录
    with os.scandir(user_dir) as it:
        for entry in it:
            if entry.is_dir():  # 只检查子目录
                info_file_path = os.path.join(entry.path, 'info.jx3dat')
                if os.path.isfile(info_file_path):  # 检查是否存在名为 info.jx3dat 的文件
                    try:
                        with open(info_file_path, 'r', encoding='ansi') as file:
                            content = file.read().strip()
                        data = parse_jx3dat(content)

                        user_info = {
                            "uid": data["uid"],
                            "大区": data["server_origin"],
                            "区服": data["region_origin"],
                            "角色": data["name"]
                        }

                        # 添加到用户数据列表
                        user_data.append(user_info)
                    except Exception as e:
                        print(f"解析 {info_file_path} 文件时出错: {e}")
                else:
                    print(f"{entry.name} 目录中不存在 info.jx3dat 文件")

    # 将所有用户信息写入 output_file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(user_data, outfile, ensure_ascii=False, indent=4)

    print(f"所有用户信息已保存到 {output_file}")

# root_dir = os.path.join('F:/SeasunGame', 'Game', 'JX3', 'bin', 'zhcn_hd')
# output_file = 'User_plug.json'
#
# scan_plug(root_dir, output_file)

# config_file = 'path_storage.json'
# script_dir = os.path.dirname(__file__)
# config_path = os.path.join(script_dir, config_file)
#
# with open(config_path, 'r', encoding='utf-8') as f:
#     config = json.load(f)
#
# root_dir = os.path.join(config.get('path', 'F:/JX3'), 'Game', 'JX3', 'bin', 'zhcn_hd', 'userdata')
# output_file = 'User_data.json'
#
# scan_folders(root_dir, output_file)
