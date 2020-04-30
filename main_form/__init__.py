import sys
import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from module.module import load_config, save_config, get_all_net_interface_status, net_interface_switch, set_wifi_data, wifi_on, wifi_off

# # determine if application is a script file or frozen exe
# if getattr(sys, 'frozen', False):
#     application_path = os.path.dirname(sys.executable)
#     CurrentPath = os.path.dirname(application_path)
#     print(CurrentPath)
# elif __file__:
#     application_path = os.path.dirname(__file__)
#     CurrentPath = os.path.dirname(application_path)
#     print(CurrentPath)

try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    CurrentPath = sys._MEIPASS
except Exception:
    CurrentPath = os.path.abspath(".")

print(CurrentPath)

qtCreatorFile = os.path.join(CurrentPath, 'ui/Main_Window.ui') # 設計好的ui檔案路徑
icon_path = os.path.join(CurrentPath, 'icon.ico')

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)   # 讀入用Qt Designer設計的GUI layout
CONFIG_FILE = os.path.join(CurrentPath, 'config.json')

class MainUi(QtWidgets.QMainWindow, Ui_MainWindow):  # Python的多重繼承 MainUi 繼承自兩個類別
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setWindowTitle('Network Interface Manager')
        self.setWindowIcon(QIcon(icon_path))

        self.setupUi(self)
        self.init_gui()
        self.bind_button()

    def init_gui(self):
        if os.path.exists(CONFIG_FILE):
            config = load_config(CONFIG_FILE)
        else:
            save_config(CONFIG_FILE)
            config = load_config(CONFIG_FILE)

        self.txb_ssid.setText(config['ap']['ssid'])
        self.txb_password.setText(config['ap']['pwd'])

        # Set Network Status
        self.btn_get_status_onClick()

    def bind_button(self):
        self.btn_save_wifi_setting.clicked.connect(self.btn_save_wifi_setting_onClick)
        self.btn_get_status.clicked.connect(self.btn_get_status_onClick)

        self.btn_wifi_on.clicked.connect(self.btn_wifi_on_onClick)
        self.btn_wifi_off.clicked.connect(self.btn_wifi_off_onClick)

    def btn_save_wifi_setting_onClick(self):
        self.btn_save_wifi_setting.setEnabled(False)
        ssid = self.txb_ssid.text()
        pwd = self.txb_password.text()
        save_config(CONFIG_FILE, ssid, pwd)
        result = set_wifi_data(CONFIG_FILE)
        self.show_information(result)
        self.btn_save_wifi_setting.setEnabled(True)

    def btn_get_status_onClick(self):
        net_interface = get_all_net_interface_status()
        self.set_cbx(self.cbx_interface_0, net_interface[self.cbx_interface_0.text()])
        self.set_cbx(self.cbx_interface_1, net_interface[self.cbx_interface_1.text()])
        self.set_cbx(self.cbx_interface_2, net_interface[self.cbx_interface_2.text()])
        self.set_cbx(self.cbx_interface_3, net_interface[self.cbx_interface_3.text()])

        self.set_cbx_function(self.cbx_interface_0)
        self.set_cbx_function(self.cbx_interface_1)
        self.set_cbx_function(self.cbx_interface_2)
        self.set_cbx_function(self.cbx_interface_3)
        self.show_information('NIC refreshed')

    def btn_wifi_on_onClick(self):
        self.btn_wifi_on.setEnabled(False)
        self.btn_wifi_off.setEnabled(True)
        result = wifi_on()
        self.show_information(result)

    def btn_wifi_off_onClick(self):
        self.btn_wifi_on.setEnabled(True)
        self.btn_wifi_off.setEnabled(False)
        result = wifi_off()
        self.show_information(result)

    def set_cbx(self, cbx, status):
        f = cbx.font()

        if status == None:
            f.setStrikeOut(True)
            cbx.setEnabled(False)
        elif status == False:
            f.setStrikeOut(False)
            cbx.setEnabled(True)
            cbx.setChecked(False)
        elif status == True:
            f.setStrikeOut(False)
            cbx.setEnabled(True)
            cbx.setChecked(True)

        cbx.setFont(f)

    def info(self, result):
        if result:
            self.show_information('SUCCESS!')
        else:
            self.show_information('FAIL!')

    def set_cbx_function(self, cbx):
        cbx.stateChanged.connect(self.cbx_stateChanged)

    def cbx_stateChanged(self):
        cbx = self.sender()
        net_interface_switch(cbx.text(), cbx.isChecked())

    def show_information(self, msg):
        QtWidgets.QMessageBox.information(self, 'Result', msg, QtWidgets.QMessageBox.Ok)
