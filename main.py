import json
import os
import shutil
import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QMessageBox, QFileDialog, QInputDialog

import SearchGame
import SearchPlayer
import Transfer  # 引入Transfer模块
import app2

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))


# 从文件中读取JSON数据
def load_data(filename):
    with open(os.path.join(current_dir, filename), 'r', encoding='utf-8') as file:
        return json.load(file)


# 判定是否找到安装目录
Not_found = 0

root_dir = ""

data_key = ''

data_plug = ''

reWrite = 0

Tem = ''

cur_page = 0


# 手动选择剑网3目录
def select_directory():
    # app1 = QApplication(sys.argv)
    dialog = QFileDialog()
    dialog.setWindowTitle('请选择剑网3目录')
    dialog.setFileMode(QFileDialog.Directory)
    if dialog.exec_() == QFileDialog.Accepted:
        directory = dialog.selectedFiles()[0]
    else:
        directory = None
    return directory


# 寻找剑三目录，目录正确 Not_found = 0
def Check_Jx3(installation_location):
    global Not_found
    if installation_location:
        try:
            while True:
                # 检查是否已经是根目录
                if installation_location == os.path.dirname(installation_location):
                    Not_found = 1
                    return None
                # 获取当前目录的最后一个部分
                # parent_dir = os.path.basename(installation_location)

                if os.path.exists(os.path.join(installation_location, 'Game')):
                    file_path = installation_location
                    Not_found = 0
                    return file_path
                    # 获取上一级目录
                installation_location = os.path.dirname(installation_location)
        except Exception:
            Not_found = 1
            return None
    else:
        Not_found = 1
        return None


def check():
    global Not_found
    global root_dir
    global reWrite
    file_path = ''
    Not_found = 0

    root_dir = ""

    reWrite = 0
    # 执行SearchGame.py
    config_path = os.path.join(current_dir, 'path_storage.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                if f.read(1):  # 检查文件是否为空
                    f.seek(0)  # 重置文件指针位置
                    config = json.load(f)
                    # 判定是否存在游戏路径
                    if not os.path.exists(
                            os.path.join(config.get('path', 'D:/SeasunGame'), 'Game', 'JX3', 'bin', 'zhcn_hd')):
                        Not_found = 1
                        f.close()
                        os.remove(config_path)  # 文件为空时删除文件
                else:
                    Not_found = 1
                    f.close()
                    os.remove(config_path)  # 文件为空时删除文件
        except json.JSONDecodeError:
            Not_found = 1
            f.close()
            os.remove(config_path)
    else:
        Not_found = 1
    # 没有发现安装路径，启动SearchGame寻找安装路径
    if Not_found:
        software_name = "SeasunGame"
        installation_location = SearchGame.find_software_installation_location(software_name)
        print(installation_location)
        file_path = Check_Jx3(installation_location)
        reWrite = 1
    # 如果SearchGame没有找到正确的地址，手动选择地址
    while Not_found:
        confirm = QMessageBox.question(None, "错误", "没有找到剑网3安装位置\n请手动选择剑网3根目录")
        if confirm == QMessageBox.Yes:
            installation_location = select_directory()
            file_path = Check_Jx3(installation_location)
            reWrite = 1
        else:
            break

    # 写入path_storage.json
    if reWrite:
        data1 = {"path": file_path}
        filename = 'path_storage.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data1, f, ensure_ascii=False, indent=4)
        print(f"路径已保存到 {filename}")
        print(f"安装位置: {file_path}")

    # 确保path_storage.json生成
    if not os.path.exists(os.path.join(current_dir, 'path_storage.json')):
        QMessageBox.critical(None, "错误", "剑网3安装路径生成失败")
        return

    # 执行SearchPlayer.py
    config_file = 'path_storage.json'
    config_path = os.path.join(current_dir, config_file)
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 找到玩家信息所在位置
    if not os.path.exists(os.path.join(config.get('path', 'C:'), 'Game', 'JX3', 'bin', 'zhcn_hd')):
        QMessageBox.critical(None, "错误", "剑网3角色信息获取失败")
    root_dir = os.path.join(config.get('path', ''), 'Game', 'JX3', 'bin', 'zhcn_hd')

    SearchPlayer.scan_key(root_dir, 'User_data.json')
    SearchPlayer.scan_plug(root_dir, 'User_plug.json')
    # 确保User_data.json生成
    if not os.path.exists(os.path.join(current_dir, 'User_data.json')):
        QMessageBox.critical(None, "错误", "User_data.json生成失败")
        return
    if not os.path.exists(os.path.join(current_dir, 'User_plug.json')):
        QMessageBox.critical(None, "错误", "User_plug.json生成失败")
        return
    # 重新加载User_data.json
    print(f"角色键位信息已保存到 {'User_data.json'}")
    print(f"角色插件信息已保存到 {'User_plug.json'}")
    global data_key
    global data_plug
    global Tem
    data_key = load_data('User_data.json')
    data_plug = load_data('User_plug.json')
    if os.path.exists(os.path.join(current_dir, 'template.json')):
        Tem = load_data('template.json')





class App(app2.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('剑网3同步工具')
        self.setWindowIcon(QIcon(os.path.join(current_dir, 'jx3Sync.ico')))

        # 背景序号
        self.backgrounds = ["bg1.jpg", "bg2.jpg", "bg3.jpg", "bg4.jpg", "bg5.jpg", "bg6.jpg", "bg7.jpg"
            , "bg8.jpg", "bg9.jpg", "bg10.jpg", "bg11.jpg", "bg12.jpg", "bg13.jpg", "bg14.jpg", "bg15.jpg"]
        self.current_bg_index = 0

        check()
        global data_key, data_plug, Tem
        self.data_key = data_key
        self.data_plug = data_plug
        self.Tem = Tem
        self.font_size = 10;

        self.accounts = sorted(set(item["账号"] for item in self.data_key))

        # 加载背景图片
        bg_path = os.path.join(current_dir, 'images', self.backgrounds[self.current_bg_index])
        pixmap = QPixmap(bg_path)

        # 创建 QLabel 作为背景
        self.bg_label = QLabel(self.centralwidget)
        self.bg_label.setPixmap(pixmap)
        self.bg_label.setScaledContents(True)  # 自动缩放以铺满整个 QLabel 区域

        # 设置 QLabel 大小和位置以铺满整个窗口
        self.bg_label.setGeometry(0, 0, self.width(), self.height())

        # 将背景置于底层
        self.bg_label.lower()

        # 监听窗口大小变化事件
        # self.resizeEvent = self.on_resize

        # 换肤按钮功能
        self.huanfu_2.clicked.connect(self.change_skin)

        # 切换选项卡功能
        self.cur_Page = 0
        self.all_roles_button.clicked.connect(lambda: self.onTabClicked(self.all_roles_button, 0))
        self.template_button.clicked.connect(lambda: self.onTabClicked(self.template_button, 1))

        # 创建下拉框内容
        self.source_comboboxes = (
            self.findChild(QComboBox, 'source_account_combobox'),
            self.findChild(QComboBox, 'source_server_combobox'),
            self.findChild(QComboBox, 'source_server_list_combobox'),
            self.findChild(QComboBox, 'source_character_combobox')
        )

        self.target_comboboxes = (
            self.findChild(QComboBox, 'target_account_combobox'),
            self.findChild(QComboBox, 'target_server_combobox'),
            self.findChild(QComboBox, 'target_server_list_combobox'),
            self.findChild(QComboBox, 'target_character_combobox')
        )

        self.setup_comboboxes(self.source_comboboxes, "roles", left=True)
        self.setup_comboboxes(self.target_comboboxes, "roles", left=False)
        self.setup_comboboxes(self.template_comboboxes, "template", left=False)


        # 按钮功能
        self.sync_button_ui.clicked.connect(self.sync)
        self.sync_button_plug.clicked.connect(self.sync_plug)
        self.sync_button_tem.clicked.connect(self.set_template)


        self.del_button.clicked.connect(self.del_characters)
        self.clean_button.clicked.connect(self.clean_empty)
        self.refresh_button.clicked.connect(self.refresh_characters)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        # 当窗口大小变化时调用
        new_width = event.size().width()
        new_height = event.size().height()

        # 调整 Label 的字体大小，示例中每100像素减小一次字体大小
        self.font_size = max(10, int(new_width / 75))  # 通过计算设置字体大小
        font_size = self.font_size

        style_15_4 = (f"""
                QPushButton {{
                    font-size: {font_size*1.5}pt;
                    border-radius: 4px;
                    background-color: white;  /* 设置背景颜色 */
                    border: 1px solid #808080;  /* 设置边框颜色，防止按钮变透明 */
                }}
                QPushButton:hover {{
                    background-color: #C6E2FF;  /* 手动设置悬停时的背景颜色 */
                }}
                QPushButton:pressed {{
                    background-color: #C0C0C0;
                    border: 1px solid #808080;
                }}
            """)

        style_9_3 = (f"""
                QPushButton {{
                    font-size: {font_size*0.9}pt;
                    border-radius: 3px;
                    background-color: white;  /* 设置背景颜色 */
                    border: 1px solid #808080;  /* 设置边框颜色，防止按钮变透明 */
                }}
                QPushButton:hover {{
                    background-color: #C6E2FF;  /* 手动设置悬停时的背景颜色 */
                }}
                QPushButton:pressed {{
                    background-color: #C0C0C0;
                    border: 1px solid #808080;
                }}
            """)

        style_11_4_D = (f"""
                QPushButton {{
                    font-size: {font_size*1.1}pt;
                    border-radius: 4px;
                    background-color: #DDDDDD;  /* 设置背景颜色 */
                    border: 1px solid #808080;  /* 设置边框颜色，防止按钮变透明 */
                }}
                QPushButton:hover {{
                    background-color: #C6E2FF;  /* 手动设置悬停时的背景颜色 */
                }}
                QPushButton:pressed {{
                    background-color: #C0C0C0;
                    border: 1px solid #808080;
                }}
            """)
        style_11_4_W = (f"""
                QPushButton {{
                    font-size: {font_size*1.1}pt;
                    border-radius: 4px;
                    background-color: white;  /* 设置背景颜色 */
                    border: 1px solid #808080;  /* 设置边框颜色，防止按钮变透明 */
                }}
                QPushButton:hover {{
                    background-color: #C6E2FF;  /* 手动设置悬停时的背景颜色 */
                }}
                QPushButton:pressed {{
                    background-color: #C0C0C0;
                    border: 1px solid #808080;
                }}
            """)
        self.huanfu_2.setStyleSheet(f"""
                QPushButton {{
                    font-size: {font_size*0.9}pt;
                    border-radius: 3px;
                    background-color: white;  /* 设置背景颜色 */
                    border: 1px solid #808080;  /* 设置边框颜色，防止按钮变透明 */
                }}
                QPushButton:hover {{
                    background-color: #C6E2FF;  /* 手动设置悬停时的背景颜色 */
                }}
                QPushButton:pressed {{
                    background-color: #C0C0C0;
                    border: 1px solid #808080;
                }}
            """)


        self.target_lebal.setStyleSheet(f"font-size: {font_size*1.7}pt;color: white")
        self.roles_account_label.setStyleSheet(f"font-size: {font_size*1.5}pt;color: white")
        self.roles_server_label.setStyleSheet(f"font-size: {font_size * 1.5}pt;color: white")
        self.roles_serverlist_label.setStyleSheet(f"font-size: {font_size * 1.5}pt;color: white")
        self.roles_character_label.setStyleSheet(f"font-size: {font_size * 1.5}pt;color: white")

        self.tar_account_label.setStyleSheet(f"font-size: {font_size*1.5}pt;color: white")
        self.tar_server_label.setStyleSheet(f"font-size: {font_size * 1.5}pt;color: white")
        self.tar_server_list_label.setStyleSheet(f"font-size: {font_size * 1.5}pt;color: white")
        self.tar_character_label.setStyleSheet(f"font-size: {font_size * 1.5}pt;color: white")

        self.template_character.setStyleSheet(f"font-size: {font_size * 1.5}pt;color: white")

        self.all_roles_button.setStyleSheet(style_11_4_D)
        self.template_button.setStyleSheet(style_11_4_W)

        self.sync_button_ui.setStyleSheet(style_15_4)

        self.sync_button_plug.setStyleSheet(style_15_4)
        self.sync_button_tem.setStyleSheet(style_15_4)

        self.del_button.setStyleSheet(style_9_3)
        self.clean_button.setStyleSheet(style_9_3)
        self.refresh_button.setStyleSheet(style_9_3)

        self.source_comboboxes[0].setStyleSheet(f"font-size: {font_size * 1.5}pt;")
        self.source_comboboxes[1].setStyleSheet(f"font-size: {font_size * 1.4}pt;")
        self.source_comboboxes[2].setStyleSheet(f"font-size: {font_size * 1.4}pt;")
        self.source_comboboxes[3].setStyleSheet(f"font-size: {font_size * 1.4}pt;")


        self.target_comboboxes[0].setStyleSheet(f"font-size: {font_size * 1.5}pt;")
        self.target_comboboxes[1].setStyleSheet(f"font-size: {font_size * 1.4}pt;")
        self.target_comboboxes[2].setStyleSheet(f"font-size: {font_size * 1.4}pt;")
        self.target_comboboxes[3].setStyleSheet(f"font-size: {font_size * 1.4}pt;")

        self.template_comboboxes.setStyleSheet(f"font-size: {font_size * 1.5}pt;")


        #print(font_size)
        #print(1)




    #def on_resize(self, event):
        # 窗口大小变化时，重新调整背景图片大小


    def setup_comboboxes(self, comboboxes, combobox_type, left):

        if combobox_type == "roles":


            comboboxes[0].addItems(sorted(set(item["账号"] for item in self.data_key)))
            comboboxes[0].setCurrentIndex(-1)
            comboboxes[0].currentIndexChanged.connect(lambda index: self.update_servers(left))
            comboboxes[0].setMaxVisibleItems(15)  # 设置下拉选项框显示的最大行数为15行

            #comboboxes[1].setFont(QFont(*font_style))
            comboboxes[1].setCurrentIndex(-1)
            comboboxes[1].currentIndexChanged.connect(lambda index: self.update_server_lists(left))

            #comboboxes[2].setFont(QFont(*font_style))
            comboboxes[2].setCurrentIndex(-1)
            comboboxes[2].currentIndexChanged.connect(lambda index: self.update_characters(left))

            #comboboxes[3].setFont(QFont(*font_style))
            comboboxes[3].setCurrentIndex(-1)




        elif combobox_type == "template":
            #comboboxes.setFont(QFont(*font_style))
            comboboxes.addItems(sorted(set(item["name"] for item in self.Tem)))
            comboboxes.setCurrentIndex(-1)


    # 设置账号
    def update_combobox(self, combobox, items):
        combobox.clear()
        # combobox.addItem("")  # 添加一个空选项
        combobox.addItems(items)
        combobox.setCurrentIndex(-1)  # 设置为未选择状态

    # 设置大区
    def update_servers(self, left):
        comboboxes = self.source_comboboxes if left else self.target_comboboxes
        selected_account = comboboxes[0].currentText()
        if selected_account:
            servers = sorted(set(item["大区"] for item in self.data_key if item["账号"] == selected_account))
            self.update_combobox(comboboxes[1], servers)
        else:
            self.update_combobox(comboboxes[1], [])

    # 区服
    def update_server_lists(self, left):
        comboboxes = self.source_comboboxes if left else self.target_comboboxes
        selected_account = comboboxes[0].currentText()
        selected_server = comboboxes[1].currentText()
        if selected_account and selected_server:
            server_lists = sorted(set(item["区服"] for item in self.data_key if
                                      item["账号"] == selected_account and item["大区"] == selected_server))
            self.update_combobox(comboboxes[2], server_lists)
        else:
            self.update_combobox(comboboxes[2], [])

    # 角色
    def update_characters(self, left):
        comboboxes = self.source_comboboxes if left else self.target_comboboxes
        selected_account = comboboxes[0].currentText()
        selected_server = comboboxes[1].currentText()
        selected_server_list = comboboxes[2].currentText()
        if selected_account and selected_server and selected_server_list:
            characters = sorted(set(item["角色"] for item in self.data_key if
                                    item["账号"] == selected_account and item["大区"] == selected_server and item[
                                        "区服"] == selected_server_list))
            self.update_combobox(comboboxes[3], characters)
        else:
            self.update_combobox(comboboxes[3], [])

    def onTabClicked(self, button, index):
        # 重置所有按钮的样式
        self.reset_button_styles()
        # 切换选项卡
        self.stackedWidget.setCurrentIndex(index)
        # 设置点击按钮的样式
        self.cur_Page = index
        button.setStyleSheet(f"""
                QPushButton {{
                    font-size: {self.font_size*1.1}pt;
                    border-radius: 4px;
                    background-color: #DDDDDD;  /* 设置背景颜色 */
                    border: 1px solid #808080;  /* 设置边框颜色，防止按钮变透明 */
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #C6E2FF;  /* 手动设置悬停时的背景颜色 */
                }}
                QPushButton:pressed {{
                    background-color: #C0C0C0;
                    border: 1px solid #808080;
                }}
            """)

    # 重置所有按钮的样式
    def reset_button_styles(self):
        self.all_roles_button.setStyleSheet(f"""
                QPushButton {{
                    font-size: {self.font_size*1.1}pt;
                    border-radius: 4px;
                    background-color: white;  /* 设置背景颜色 */
                    border: 1px solid #808080;  /* 设置边框颜色，防止按钮变透明 */
                    font-weight: normal;
                }}
                QPushButton:hover {{
                    background-color: #C6E2FF;  /* 手动设置悬停时的背景颜色 */
                }}
                QPushButton:pressed {{
                    background-color: #C0C0C0;
                    border: 1px solid #808080;
                }}
            """)
        self.template_button.setStyleSheet(f"""
                QPushButton {{
                    font-size: {self.font_size*1.1}pt;
                    border-radius: 4px;
                    background-color: white;  /* 设置背景颜色 */
                    border: 1px solid #808080;  /* 设置边框颜色，防止按钮变透明 */
                    font-weight: normal;
                }}
                QPushButton:hover {{
                    background-color: #C6E2FF;  /* 手动设置悬停时的背景颜色 */
                }}
                QPushButton:pressed {{
                    background-color: #C0C0C0;
                    border: 1px solid #808080;
                }}
            """)

    def sync(self):
        print(self.cur_Page)
        if self.cur_Page:
            source_template = self.template_comboboxes.currentText()
            if source_template:
                source_path = os.path.join(current_dir, 'templates', source_template + '_Key')
            else:
                QMessageBox.critical(self, "错误", "无模板角色信息")
                return


        else:
            source_account = self.source_comboboxes[0].currentText()
            source_server = self.source_comboboxes[1].currentText()
            source_server_list = self.source_comboboxes[2].currentText()
            source_character = self.source_comboboxes[3].currentText()

            source_path = next((item["键位路径"] for item in self.data_key if
                                item["账号"] == source_account and
                                item["大区"] == source_server and
                                item["区服"] == source_server_list and
                                item["角色"] == source_character), None)

        target_account = self.target_comboboxes[0].currentText()
        target_server = self.target_comboboxes[1].currentText()
        target_server_list = self.target_comboboxes[2].currentText()
        target_character = self.target_comboboxes[3].currentText()

        target_path = next((item["键位路径"] for item in self.data_key if
                            item["账号"] == target_account and
                            item["大区"] == target_server and
                            item["区服"] == target_server_list and
                            item["角色"] == target_character), None)

        if not source_path or not target_path:
            QMessageBox.critical(self, "错误", "不存在角色信息")
            return

        result = Transfer.Transfer(source_path, target_path)
        if result:
            QMessageBox.information(self, "同步成功", "角色同步成功")
        else:
            QMessageBox.critical(self, "同步失败", "角色同步失败")

    def sync_plug(self):
        print(self.cur_Page)
        if self.cur_Page:
            source_template = self.template_comboboxes.currentText()
            if source_template:
                source_path = os.path.join(current_dir, 'templates', source_template + '_Plug')
            else:
                QMessageBox.critical(self, "错误", "无模板角色信息")
                return

        else:
            source_path = next((item["uid"] for item in self.data_plug if
                                item["大区"] == self.source_comboboxes[1].currentText() and
                                item["区服"] == self.source_comboboxes[2].currentText() and
                                item["角色"] == self.source_comboboxes[3].currentText()), None)
            if not source_path:
                QMessageBox.critical(self, "错误", "不存在角色信息")
                return
            source_path = os.path.join(root_dir, 'interface', 'my#data', source_path + '@zhcn_hd')

        target_path = next((item["uid"] for item in self.data_plug if
                            item["大区"] == self.target_comboboxes[1].currentText() and
                            item["区服"] == self.target_comboboxes[2].currentText() and
                            item["角色"] == self.target_comboboxes[3].currentText()), None)

        if not source_path or not target_path:
            QMessageBox.critical(self, "错误", "不存在角色信息")
            return

        target_path = os.path.join(root_dir, 'interface', 'my#data', target_path + '@zhcn_hd')
        name = self.source_comboboxes[3].currentText()

        result = Transfer.Transfer_plug(source_path, target_path, name)
        if result:
            QMessageBox.information(self, "同步成功", "角色插件同步成功")
        else:
            QMessageBox.critical(self, "同步失败", "角色插件同步失败")

    # 刷新模板
    def refresh_template(self):
        if os.path.exists(os.path.join(current_dir, 'template.json')):
            Tem = load_data('template.json')
            self.Tem = Tem
            self.template_comboboxes.clear()
            self.template_comboboxes.addItems(sorted(set(item["name"] for item in self.Tem)))
            self.template_comboboxes.setCurrentIndex(-1)

    def refresh_characters(self):
        if os.path.exists(os.path.join(current_dir, 'User_data.json')):
            os.remove(os.path.join(current_dir, 'User_data.json'))
        check()
        QMessageBox.information(self, "刷新成功", "角色信息已刷新")
        # 重新加载数据
        self.data_key = data_key
        self.data_plug = data_plug
        self.Tem = Tem
        self.accounts = sorted(set(item["账号"] for item in self.data_key))

        self.template_comboboxes.clear()
        self.template_comboboxes.addItems(sorted(set(item["name"] for item in self.Tem)))
        self.template_comboboxes.setCurrentIndex(-1)

        # 更新源角色和目标角色的账号下拉框选项
        self.source_comboboxes[0].clear()
        self.source_comboboxes[0].addItems(self.accounts)
        self.target_comboboxes[0].clear()
        self.target_comboboxes[0].addItems(self.accounts)

        # 不自动选择任何项
        self.source_comboboxes[0].setCurrentIndex(-1)
        self.target_comboboxes[0].setCurrentIndex(-1)

    def refresh_characters_only(self, side, account, server, server_list):
        characters = [item["角色"] for item in self.data_key if
                      item["账号"] == account and item["大区"] == server and item["区服"] == server_list]
        if side == 'left':
            self.source_comboboxes[3].clear()  # 清空原有的选项
            self.source_comboboxes[3].addItems(characters)  # 添加新的角色选项
            self.source_comboboxes[3].setCurrentIndex(-1)  # 设置下拉框不自动选择
        else:
            self.target_comboboxes[3].clear()  # 清空原有的选项
            self.target_comboboxes[3].addItems(characters)  # 添加新的角色选项
            self.target_comboboxes[3].setCurrentIndex(-1)  # 设置下拉框不自动选择

    def del_characters(self):
        confirm = QMessageBox.question(self, "确认删除", "您确定要删除吗？\n此操作不可逆！",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            if self.cur_Page:
                source_template = self.template_comboboxes.currentText()
                if source_template:
                    source_path_key = os.path.join(current_dir, 'templates', source_template + '_key')
                    source_path_plug = os.path.join(current_dir, 'templates', source_template + '_Plug')
                else:
                    QMessageBox.critical(self, "错误", "无模板角色信息")
                    return
            else:
                source_account = self.source_comboboxes[0].currentText()
                source_server = self.source_comboboxes[1].currentText()
                source_server_list = self.source_comboboxes[2].currentText()
                source_character = self.source_comboboxes[3].currentText()

                # 查找要删除的角色对应的路径
                source_path_key = next((item["键位路径"] for item in self.data_key if
                                        item["账号"] == source_account and
                                        item["大区"] == source_server and
                                        item["区服"] == source_server_list and
                                        item["角色"] == source_character), None)

                source_path_plug = next((item["uid"] for item in self.data_plug if
                                         item["大区"] == self.source_comboboxes[1].currentText() and
                                         item["区服"] == self.source_comboboxes[2].currentText() and
                                         item["角色"] == self.source_comboboxes[3].currentText()), None)
                if not source_path_key:
                    QMessageBox.critical(self, "错误", "不存在角色信息")
                    return
                if source_path_plug:
                    source_path_plug = os.path.join(root_dir, 'interface', 'my#data', source_path_plug + '@zhcn_hd')

            try:
                # 删除角色路径
                shutil.rmtree(source_path_key)
                # 更新 data_key，移除对应项
                if self.cur_Page:
                    self.Tem = [item for item in self.Tem if not (
                            item["name"] == source_template
                    )]
                    # 保存新的 User_data.json
                    with open(os.path.join(current_dir, 'template.json'), 'w', encoding='utf-8') as file:
                        json.dump(self.Tem, file, ensure_ascii=False, indent=4)
                    QMessageBox.information(self, "删除成功", "角色删除成功")
                    self.refresh_template()

                else:
                    self.data_key = [item for item in self.data_key if not (
                            item["账号"] == source_account and
                            item["大区"] == source_server and
                            item["区服"] == source_server_list and
                            item["角色"] == source_character
                    )]
                    # 保存新的 User_data.json
                    with open(os.path.join(current_dir, 'User_data.json'), 'w', encoding='utf-8') as file:
                        json.dump(self.data_key, file, ensure_ascii=False, indent=4)

                    # 刷新角色下拉框
                    self.refresh_characters_only('left', source_account, source_server, source_server_list)
                    QMessageBox.information(self, "删除成功", "角色删除成功")

            except Exception as e:
                QMessageBox.critical(self, "删除失败", f"删除角色失败：{str(e)}")
            if source_path_plug and os.path.exists(source_path_plug):
                shutil.rmtree(source_path_plug)
            else:
                return

    # 清除空角色
    def clean_empty(self):
        confirm = QMessageBox.question(self, "清理空文件", "您要删除所有空文件信息吗？\n此操作不会删除正常角色信息！")
        if confirm == QMessageBox.Yes:
            SearchPlayer.clean_empty_file_directories(root_dir)
            QMessageBox.information(self, "清除成功", "空角色已被清除")

    def change_skin(self):
        # 切换到下一个背景图片
        self.current_bg_index = (self.current_bg_index + 1) % len(self.backgrounds)
        bg_path = os.path.join(current_dir, 'images', self.backgrounds[self.current_bg_index])
        self.bg_label.setPixmap(QPixmap(bg_path))

    def set_template(self):
        source_account = self.source_comboboxes[0].currentText()
        source_server = self.source_comboboxes[1].currentText()
        source_server_list = self.source_comboboxes[2].currentText()
        source_character = self.source_comboboxes[3].currentText()

        if not source_character:
            QMessageBox.critical(self, "错误", "无角色信息")
            return

        source_Key_path = next((item["键位路径"] for item in self.data_key if
                                item["账号"] == source_account and
                                item["大区"] == source_server and
                                item["区服"] == source_server_list and
                                item["角色"] == source_character), None)

        source_Plug_path = next((item["uid"] for item in self.data_plug if
                                 item["大区"] == self.source_comboboxes[1].currentText() and
                                 item["区服"] == self.source_comboboxes[2].currentText() and
                                 item["角色"] == self.source_comboboxes[3].currentText()), None)

        if not source_Plug_path:
            QMessageBox.critical(self, "错误", "角色茗伊插件路径不存在, 仅设置键位")
            source_Plug_path = ' '
        else:
            source_Plug_path = os.path.join(root_dir, 'interface', 'my#data', source_Plug_path + '@zhcn_hd')

        while True:
            text, ok = QInputDialog.getText(self, '输入模板名称', '请输入模板名称:')
            if not ok:
                return  # 用户点击取消，返回函数

            if text:
                new_entry = {'name': text}
                try:
                    if os.path.exists('template.json'):
                        with open('template.json', 'r', encoding='utf-8') as file:
                            data = json.load(file)
                    else:
                        data = []
                except Exception as e:
                    QMessageBox.critical(self, '错误', f'读取JSON文件时发生错误: {e}')
                    return

                if any(entry['name'] == text for entry in data):
                    reply = QMessageBox.question(self, '名称重复', '输入的名称已存在，是否重新输入？',
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.No:
                        return  # 用户选择不重新输入，返回函数
                else:
                    data.append(new_entry)
                    try:
                        with open('template.json', 'w', encoding='utf-8') as file:
                            json.dump(data, file, ensure_ascii=False, indent=4)
                        # QMessageBox.information(self, '成功', '模板已成功添加!')
                        break
                    except Exception as e:
                        QMessageBox.critical(self, '错误', f'写入JSON文件时发生错误: {e}')
                        return
            else:
                QMessageBox.warning(self, '警告', '模板名称不能为空，请重新输入。')

        result1 = Transfer.Transfer_TemKey(source_Key_path, os.path.join(current_dir, 'templates', text + '_Key'))

        if result1:
            QMessageBox.information(self, "设置成功", "模板键位设置成功")
        else:
            QMessageBox.critical(self, "设置失败", "模板键位设置失败")
        result2 = Transfer.Transfer_TemPlug(source_Plug_path, os.path.join(current_dir, 'templates', text + '_Plug'),
                                            source_character)
        if result2:
            QMessageBox.information(self, "设置成功", "模板插件设置成功")
        else:
            QMessageBox.critical(self, "设置失败", "模板茗伊插件设置失败")
        self.refresh_template()


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    # 启动执行一次加载程序
    ex = App()
    ex.show()
    sys.exit(app.exec_())
