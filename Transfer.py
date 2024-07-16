import os
import shutil


def Transfer(source_path, target_path):
    # 检查source_path和target_path是否存在
    if not os.path.exists(source_path) or not os.path.exists(target_path):
        return "无法找到角色信息"

    try:
        # 复制source_path中的所有文件到target_path
        for item in os.listdir(source_path):
            s = os.path.join(source_path, item)
            d = os.path.join(target_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)  # 递归复制文件夹，dirs_exist_ok确保目标文件夹已存在时也能复制
            else:
                shutil.copy2(s, d)  # 复制文件，并保留元数据
        return "同步成功！"
    except Exception as e:
        return "同步失败"


def Transfer_plug(source_path, target_path, name):
    # 检查source_path和target_path是否存在
    if not os.path.exists(source_path) or not os.path.exists(target_path):
        return "无法找到角色信息"

    try:
        # 复制source_path中的所有文件到target_path
        for item in os.listdir(source_path):
            s = os.path.join(source_path, item)
            d = os.path.join(target_path, item)

            # 跳过指定名称的文件夹
            if item == name and os.path.isdir(s):
                continue

            # 跳过info.jx3dat文件
            if item == "info.jx3dat" and os.path.isfile(s):
                continue

            # 跳过userdata文件夹下的gkp和chat_log文件夹
            if "userdata" in s:
                if "userdata/gkp" in s or "userdata/chat_log" in s:
                    continue

            if os.path.isdir(s):
                # 递归调用Transfer_plug来复制子目录
                if item != "gkp" and item != "chat_log":
                    Transfer_plug(s, d, name)
            else:
                shutil.copy2(s, d)  # 复制文件，并保留元数据
        return "同步成功！"
    except Exception as e:
        print(e)
        return "同步失败"


def Transfer_TemKey(source_path, target_path):
    if not os.path.exists(source_path):
        print(f"源路径不存在: {source_path}")
        return

    # 如果目标文件夹不存在，则创建它
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    try:
        # 复制source_path中的所有文件到target_path
        for item in os.listdir(source_path):
            s = os.path.join(source_path, item)
            d = os.path.join(target_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)  # 递归复制文件夹，dirs_exist_ok确保目标文件夹已存在时也能复制
            else:
                shutil.copy2(s, d)  # 复制文件，并保留元数据
        return "同步成功！"
    except Exception as e:
        return "同步失败"


def Transfer_TemPlug(source_path, target_path, name):
    # 检查source_path和target_path是否存在
    if not os.path.exists(source_path) :
        return 0
    # 如果目标文件夹不存在，则创建它
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    try:
        # 复制source_path中的所有文件到target_path
        for item in os.listdir(source_path):
            s = os.path.join(source_path, item)
            d = os.path.join(target_path, item)

            # 跳过指定名称的文件夹
            if item == name and os.path.isdir(s):
                continue

            # 跳过info.jx3dat文件
            if item == "info.jx3dat" and os.path.isfile(s):
                continue

            # 跳过userdata文件夹下的gkp和chat_log文件夹
            if "userdata" in s:
                if "userdata/gkp" in s or "userdata/chat_log" in s:
                    continue

            if os.path.isdir(s):
                # 递归调用Transfer_plug来复制子目录
                if item != "gkp" and item != "chat_log":
                    Transfer_TemPlug(s, d, name)
            else:
                shutil.copy2(s, d)  # 复制文件，并保留元数据
        return "同步成功！"
    except Exception as e:
        print(e)
        return "同步失败"