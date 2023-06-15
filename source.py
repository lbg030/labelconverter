import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QComboBox, QFileDialog, QMessageBox, QFormLayout

from utils import labelme2yolo, labelme2hubble, yolo2labelme

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lbl_current_dir = QLabel('', self)
        self.lbl_format_type = QLabel('', self)
        self.lbl_status = QLabel('Not Executed', self)

        # Setup combo boxes
        self.format_combo = QComboBox(self)
        self.format_combo.addItem("-")
        self.format_combo.addItem("Object Detection/Labelme2YOLO")
        self.format_combo.addItem("Object Detection/Labelme2Hubble")
        self.format_combo.addItem("Object Detection/YOLO2Labelme")

        '''
        #TODO: Add this function
        self.format_combo.addItem("Segmentation/Labelme2Hubble")
        self.format_combo.addItem("Segmentation/Lens2Hubble")
        '''

        self.format_combo.currentIndexChanged.connect(self.set_format_type)

        # Setup buttons
        self.btn_dir = QPushButton('Select Directory', self)
        self.btn_dir.clicked.connect(self.select_directory)

        self.btn_format = QPushButton('Convert format', self)
        self.btn_format.clicked.connect(self.format_label)
        self.btn_format.setEnabled(False)

        # Organize layout
        form_layout = QFormLayout()
        form_layout.addRow("Directory: ", self.lbl_current_dir)
        form_layout.addRow("Format Type: ", self.lbl_format_type)
        
        vbox = QVBoxLayout()
        vbox.addLayout(form_layout)
        vbox.addWidget(self.format_combo)
        vbox.addWidget(self.lbl_status)
        vbox.addWidget(self.btn_dir)
        vbox.addWidget(self.btn_format)

        self.setLayout(vbox)

        self.setWindowTitle('Label Formatter')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def select_directory(self):
        self.directory = QFileDialog.getExistingDirectory(
            self, "Select Directory")
        if self.directory:
            self.btn_format.setEnabled(True)
            self.lbl_current_dir.setText(self.directory)
            self.class_list = [name for name in os.listdir(
                self.directory) if os.path.isdir(os.path.join(self.directory, name))]

    def set_format_type(self): 
        sender = self.sender()
        self.lbl_format_type.setText(sender.currentText().split('/')[1])
        self.lbl_status.setText('Not Executed')

    def format_label(self):
        format_type = self.lbl_format_type.text()

        if format_type:  # Check if format type is selected
            self.lbl_status.setText(f"Processing...")
            QApplication.processEvents()

            converted_files = {cls: 0 for cls in self.class_list}

            if format_type in ["Labelme2YOLO", "Labelme2Hubble"]:
                file_ext = '.json'
                conversion_funcs = {
                    "Labelme2YOLO": self.format_to_yolo,
                    "Labelme2Hubble": self.format_to_hubble
                }
            else:  # "YOLO2Labelme"
                file_ext = '.txt'
                conversion_funcs = {"YOLO2Labelme": self.format_to_labelme}

            self.process_files(file_ext, conversion_funcs[format_type], converted_files)
        else:
            QMessageBox.warning(self, "Warning", "Please select a format type.")

    def process_files(self, file_ext, conversion_func, converted_files):
        for dir_name in self.class_list:
            subdir_path = os.path.join(self.directory, dir_name)
            file_list = [f for f in os.listdir(
                subdir_path) if f.endswith(file_ext)]

            for file_name in file_list:
                file_path = os.path.join(subdir_path, file_name)
                with open(file_path, 'r') as file:
                    data = json.load(file)

                conversion_func(data, file_path, self.class_list)
                converted_files[dir_name] += 1

        self.lbl_status.setText(
            f"Conversion complete. Class-wise counts: {converted_files}")

    def format_to_yolo(self, data, file_path, class_list):
        labelme2yolo(data, file_path, class_list)

    def format_to_hubble(self, data, file_path, class_list=None):
        labelme2hubble(data, file_path, class_list)

    def format_to_labelme(self, data, class_list):
        yolo2labelme(data, class_list)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
