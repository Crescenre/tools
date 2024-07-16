import winreg as reg


def find_software_installation_location(folder_name):
    try:
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"SOFTWARE") as registry_key:
            for i in range(0, reg.QueryInfoKey(registry_key)[0]):
                sub_key_name = reg.EnumKey(registry_key, i)
                #print(f"当前:{sub_key_name}")
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

# def find_software_installation_location(software_name):
#     try:
#         with reg.OpenKey(reg.HKEY_LOCAL_MACHINE,
#                          r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as uninstall_key:
#             i = 0
#             while True:
#                 try:
#                     sub_key_name = reg.EnumKey(uninstall_key, i)
#                     with reg.OpenKey(uninstall_key, sub_key_name) as sub_key:
#                         try:
#                             display_name, _ = reg.QueryValueEx(sub_key, "DisplayName")
#                             if display_name == software_name:
#                                 install_location, _ = reg.QueryValueEx(sub_key, "DisplayIcon")
#                                 print(f"找到软件：{display_name}，安装位置：{install_location}")
#                                 return install_location
#                         except FileNotFoundError:
#                             i += 1
#                             continue
#                     i += 1
#                 except OSError:
#                     break
#         print(f"未找到名为 '{software_name}' 的软件")
#         return None
#     except PermissionError:
#         print("错误：权限被拒绝，无法访问注册表项。")
#     except Exception as e:
#         print(f"发生错误：{e}")
