import os
import pickle
import re
import socket
import sys
import copy

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox,
                             QDialog, QDialogButtonBox, QGridLayout,
                             QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                             QMessageBox, QPushButton, QRadioButton, QSlider,
                             QVBoxLayout, QWidget)


class Plot:
    def __init__(self, ip, port, func, polar, min, max, amount, width, style, color, mesh):
        self.ip = ip
        self.port = port
        self.func = func
        self.polar = polar
        self.min = min
        self.max = max
        self.amount = amount
        self.width = width
        self.style = style
        self.color = color
        self.mesh = mesh
    
    def __add__(self, other):
        return Plot(self.ip, self.port, self.func + '+' + other.func, self.polar, min(self.min, other.min), max(self.max, other.max), max(self.amount, other.amount), self.width, self.style, self.color, self.mesh)
    
    def __sub__(self, other):
        return Plot(self.ip, self.port, self.func + '-' + other.func, self.polar, min(self.min, other.min), max(self.max, other.max), max(self.amount, other.amount), self.width, self.style, self.color, self.mesh)

class AdditionalFunction(QDialog):
    def __init__(self):
        super().__init__()
        self.func_lbl_add = QLabel("Function:")
        self.func_le_add = QLineEdit("sin(x)")
        self.polar_lbl_add = QLabel("Polar coordinates:")

        self.combo = QComboBox()
        self.combo.addItem("Add Function")
        self.combo.addItem("Subtract Function")

        self.polar_button_add = QCheckBox("Yes")
        self.polar = False

        def polar_button_clicked_add(checked):
            if checked == 2:
                self.polar = True
            else:
                self.polar = False

        self.polar_button_add.stateChanged.connect(polar_button_clicked_add)

        self.layout_add = QGridLayout()
        self.setLayout(self.layout_add)

        self.min_max_layout_add = QHBoxLayout()
        self.min_max_wdgt_add = QWidget()
        self.min_max_wdgt_add.setLayout(self.min_max_layout_add)
        self.min_max_lbl_add = QLabel("Minimum, maximum and amount of x:")
        self.min_le_add = QLineEdit('0')
        self.max_le_add = QLineEdit('2')
        self.amount_le_add = QLineEdit('100')
        self.min_max_layout_add.addWidget(self.min_le_add)
        self.min_max_layout_add.addWidget(self.max_le_add)
        self.min_max_layout_add.addWidget(self.amount_le_add)
        self.min_max_wdgt_add.setLayout(self.min_max_layout_add)


        self.layout_add.addWidget(self.func_lbl_add)
        self.layout_add.addWidget(self.func_le_add)
        self.layout_add.addWidget(self.polar_lbl_add) 
        self.layout_add.addWidget(self.polar_button_add)
        self.layout_add.addWidget(self.min_max_lbl_add)
        self.layout_add.addWidget(self.min_max_wdgt_add)
        self.layout_add.addWidget(self.combo)

        self.setWindowTitle("Additional function")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout_add.addWidget(self.buttonBox)

def application():
    plot = Plot
    app = QApplication(sys.argv)
    widget = QWidget()
    ip_lbl = QLabel("IP:")
    ip_le = QLineEdit("localhost")
    port_lbl = QLabel("Port:")
    port_le = QLineEdit("2000")
    OK_button = QPushButton("OK")
    func_lbl = QLabel("Function:")
    func_le = QLineEdit("tg(x)")
    polar_lbl = QLabel("Polar coordinates:")
    
    polar_button = QCheckBox("Yes")
    plot.polar = False
    
    def polar_button_clicked(checked):
        if checked == 2:
            plot.polar = True
        else:
            plot.polar = False

    polar_button.stateChanged.connect(polar_button_clicked)
    
    layout = QGridLayout()
    widget.setLayout(layout)
    
    min_max_layout = QHBoxLayout()
    min_max_wdgt = QWidget()
    min_max_wdgt.setLayout(min_max_layout)
    min_max_lbl = QLabel("Minimum, maximum and amount of x:")
    min_le = QLineEdit('0')
    max_le = QLineEdit('2')
    amount_le = QLineEdit('100')
    min_max_layout.addWidget(min_le)
    min_max_layout.addWidget(max_le)
    min_max_layout.addWidget(amount_le)
    min_max_wdgt.setLayout(min_max_layout)
    
    width_lbl = QLabel("Line width:")
    plot.width = 2
    width_slider = QSlider(Qt.Orientation.Horizontal)
    width_slider.setMinimum(1)
    width_slider.setMaximum(10)
    def widthChange(width_slider):
        plot.width = width_slider
        
    width_slider.valueChanged[int].connect(widthChange)
    
    style_lbl = QLabel('Style line:')
    style_rb1 = QRadioButton('-.')
    style_rb1.setChecked(True)
    style_rb2 = QRadioButton('--')
    style_rb3 = QRadioButton(':')
    style_button_group = QButtonGroup()
    style_button_group.addButton(style_rb1)
    style_button_group.addButton(style_rb2)
    style_button_group.addButton(style_rb3)
    plot.style = style_rb1.text()
    
    def style_rb_clicked(button):
        plot.style = button.text()
        
    style_button_group.buttonClicked.connect(style_rb_clicked)
    style_layout = QHBoxLayout()
    style_wdgt = QWidget()
    style_wdgt.setLayout(style_layout)
    style_layout.addWidget(style_rb1)
    style_layout.addWidget(style_rb2)
    style_layout.addWidget(style_rb3)
    
    color_lbl = QLabel("Color:")
    plot.color = 'r'
    color_red_rb = QRadioButton('Red')
    color_red_rb.setChecked(True)
    color_blue_rb = QRadioButton('Blue')
    color_green_rb = QRadioButton('Green')
    color_red_rb.setStyleSheet("* { color: red }")
    color_blue_rb.setStyleSheet("* { color: blue }")
    color_green_rb.setStyleSheet("* { color: green }")
    color_button_group = QButtonGroup()
    color_button_group.addButton(color_red_rb)
    color_button_group.addButton(color_blue_rb)
    color_button_group.addButton(color_green_rb)

    def color_rb_clicked(button):
        if button.text() == 'Red':
            plot.color = 'r'
        elif button.text() == 'Blue':
            plot.color = 'b'
        elif button.text() == 'Green':
            plot.color = 'g'
        

    color_button_group.buttonClicked.connect(color_rb_clicked)
    color_layout = QHBoxLayout()
    color_wdgt = QWidget()
    color_wdgt.setLayout(color_layout)
    color_layout.addWidget(color_red_rb)
    color_layout.addWidget(color_blue_rb)
    color_layout.addWidget(color_green_rb)

    
    mesh_lbl = QLabel("Grid:")
    mesh_button = QCheckBox("Yes:")
    plot.mesh = False
    
    def mesh_button_clicked(checked):
        if checked == 2:
            plot.mesh = True
        else:
            plot.mesh = False

    mesh_button.stateChanged.connect(mesh_button_clicked)
    
    layout.addWidget(ip_lbl)
    layout.addWidget(ip_le)
    layout.addWidget(port_lbl)
    layout.addWidget(port_le)
    layout.addWidget(func_lbl)
    layout.addWidget(func_le)
    layout.addWidget(polar_lbl) 
    layout.addWidget(polar_button)
    layout.addWidget(min_max_lbl)
    layout.addWidget(min_max_wdgt)
    layout.addWidget(width_lbl)
    layout.addWidget(width_slider)
    layout.addWidget(style_lbl)
    layout.addWidget(style_wdgt)
    layout.addWidget(color_lbl)
    layout.addWidget(color_wdgt)
    layout.addWidget(mesh_lbl)
    layout.addWidget(mesh_button)
    layout.addWidget(OK_button)

    def send():
        plot.ip = ip_le.text()
        plot.port = int(port_le.text())
        plot.func = func_le.text()
        plot.min = min_le.text()
        plot.max = max_le.text()
        plot.amount = amount_le.text()

        message = QMessageBox()
        message.setText("Add function?")
        message.setStandardButtons(QMessageBox.StandardButton.Ok| QMessageBox.StandardButton.Cancel)
        message.setWindowTitle("I have a question!")
        message.setIcon(QMessageBox.Icon.Question)
        data = []
        if message.exec() == QMessageBox.StandardButton.Ok:
            dlg = AdditionalFunction()
            if dlg.exec():
                add_plot = Plot(plot.ip, plot.port, dlg.func_le_add.text(), dlg.polar, dlg.min_le_add.text(), dlg.max_le_add.text(),\
                                 dlg.amount_le_add.text(), plot.width, plot.style, plot.color, plot.mesh)
                plot1 = Plot(plot.ip, plot.port, plot.func, plot.polar, plot.min, plot.max, plot.amount, plot.width, plot.style, \
                             plot.color, plot.mesh)
                if plot1.polar != add_plot.polar:
                    warn_message = QMessageBox()
                    warn_message.setText("Coordinate systems do not match. Should we restore the default coordinate system or apply a new one?")
                    warn_message.setStandardButtons(QMessageBox.StandardButton.RestoreDefaults | QMessageBox.StandardButton.Apply)
                    warn_message.setWindowTitle("I have a question!")
                    warn_message.setIcon(QMessageBox.Icon.Question)
                    button1 = warn_message.exec()
                    if button1 == QMessageBox.StandardButton.Apply:
                        add_plot.polar = plot1.polar
                    else:
                        plot1.polar = add_plot.polar

                if dlg.combo.currentIndex() == 0:
                    answer_plot = plot1 + add_plot 
                else:
                    answer_plot = plot1 - add_plot      
                data = [answer_plot.func, answer_plot.polar, answer_plot.min, answer_plot.max, answer_plot.amount, \
                        answer_plot.width, answer_plot.style, answer_plot.color, answer_plot.mesh]     
            else:
                data = [plot.func, plot.polar, plot.min, plot.max, plot.amount, plot.width, plot.style, plot.color, plot.mesh]
                print("Cancel!")
        else:
            data = [plot.func, plot.polar, plot.min, plot.max, plot.amount, plot.width, plot.style, plot.color, plot.mesh]
        print(data)

        with socket.create_connection((plot.ip, plot.port)) as conn:
            print("Connecting to the server...")
            print("Data transmission...")
            conn.send(pickle.dumps(data))
            print("Sent!")
        print("The connection is closed!")
    OK_button.clicked.connect(send)
    widget.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    application()