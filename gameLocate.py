import winreg as reg


def find_software_installation_path(folder_name):
    try:
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"SOFTWARE") as registry_key:
            for i in range(0, reg.QueryInfoKey(registry_key)[0]):
                sub_key_name = reg.EnumKey(registry_key, i)
                print(f"当前:{sub_key_name}")
                if folder_name.lower() == sub_key_name.lower():
                    print(f"找到了:{folder_name}")
                    sub_key = reg.OpenKey(registry_key, sub_key_name)

                    try:
                        install_path = reg.QueryValueEx(sub_key, "InstPath")[0]
                        return install_path
                    except FileNotFoundError:
                        pass
                    finally:
                        sub_key.Close()
            registry_key.Close()
    except Exception as e:
        print(e)
    return None

# folder_name = 'SeasunGame'  # 替换为你要查找的文件夹名称
# installation_path = find_software_installation_path(folder_name)
# if installation_path:
#     print(f"安装路径: {installation_path}")
# else:
#     print("没有找到软件的安装路径。")
