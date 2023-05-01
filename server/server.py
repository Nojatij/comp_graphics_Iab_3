import socket
import sys
import pickle
import os
import re
import numexpr as ne
import matplotlib.pyplot as plt
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QGridLayout,\
    QSlider, QPushButton, QLineEdit,QHBoxLayout, QRadioButton, QButtonGroup, QCheckBox, \
    QTableWidget,QTableWidgetItem,QHeaderView, QMessageBox
from PyQt6.QtCore import Qt
import datetime
from PIL import Image
from math import sin, cos, log, tan,\
                 sinh, cosh, tanh, asin, asinh,\
                 acos, acosh, atan, atanh
def calculus(s):
    def ctan(x):
        return 1/tan(x)

    def ctanh(x):
        return 1/tanh(x)

    s = s.replace('+\n', '')
    s = s.replace('-\n', '')
    s = s.replace('*\n', '')
    s = s.replace('/\n', '')
    s = s.replace('^\n', '')
    s = s.replace('^', '**')
    s = s.replace('tg', 'tan')
    s = s.replace('ln', 'log')
    return s

def polar_function(s):
    s = re.sub(r'(?<!\w)(\w+)(?=\()', r'np.\1', s)
    s = s.replace('x', 'theta')
    return s

def paint_plot(decode_data):
    func = calculus(decode_data[0])
    polar = decode_data[1]
    min = float(decode_data[2])
    max = float(decode_data[3])
    amount = int(decode_data[4])
    width = int(decode_data[5])
    style = decode_data[6]
    col = decode_data[7]
    mesh = decode_data[8]
    address = decode_data[9]
    error = False

    if polar:
        r = func.replace('x', 'theta')

        theta = np.linspace(min, max*np.pi, amount)
        try:
            fig = plt.figure()
            ax = plt.subplot(111,projection='polar')
            ax.set_rlim(0, max)
            ax.set_title('Polar coordinates')
            ax.grid(mesh)
            ax.plot(theta, ne.evaluate(r), color=col, linestyle=style, linewidth=width)
        except Exception:
            error = True
    else:
        plt.title('Function graph y = ' + func)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(mesh)
        x = np.linspace(min, max, amount)
        try:
            plt.plot(x, ne.evaluate(func), color=col, linestyle=style, linewidth=width)  
        except Exception:
            error = True
            
    if error == False:
        now = datetime.datetime.now()
        namenow = now.strftime("%Y-%m-%d_%H-%M-%S") + "_" + str(address) + "_grafic.jpg" 
        plt.savefig(namenow)
        img = Image.open(namenow)
        img.show()
        fig, ax = plt.subplots()  # Create a figure containing a single axes.
        fig.clear(True)
        print(namenow)
    else:
        msg = QMessageBox()
        msg.setText("ERROR!")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
        

def application():
    app = QApplication(sys.argv)
    widget = QWidget()
    ip_lbl = QLabel("IP")
    ip_le = QLineEdit("localhost")
    port_lbl = QLabel("Port")
    port_le = QLineEdit("2000")
    button_OK = QPushButton("OK")
    button_exit = QPushButton("Exit")
    layout = QGridLayout()

    widget.setLayout(layout)
    layout.addWidget(ip_lbl)
    layout.addWidget(ip_le)
    layout.addWidget(port_lbl)
    layout.addWidget(port_le)
    layout.addWidget(button_OK)
    layout.addWidget(button_exit)
        

    def start_server():
        ip = ip_le.text()
        port = int(port_le.text())
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip,port))
        sock.listen(10)
        while True:
            print("Waiting for the client...")
            client_socket, address = sock.accept()  # начинаем принимать соединения
            print('Сonnected:', address)  # выводим информацию о подключении
            data = client_socket.recv(1024)  # принимаем данные от клиента, по 1024 байт
            decode_data = pickle.loads(data)
            decode_data.append(address)
            print(decode_data)
            paint_plot(decode_data)
            print('Painting...')
            client_socket.close()

    def shut_server():
        sys.exit()

    button_OK.clicked.connect(start_server)
    button_exit.clicked.connect(shut_server)

    widget.show()
    sys.exit(app.exec())

    

if __name__ == "__main__":
    application()