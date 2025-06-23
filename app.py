import sys

from PyQt6.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QSpacerItem, QSizePolicy, QScrollArea
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

import pdfhandler


class PDFViewer(QWidget):
    MAIN_COLOR = "#8D93AB"
    SECOND_COLOR = "#EAE2C6"
    THIRD_COLOR = "#BFBBA9"
    FOURTH_COLOR = "#ADA991"
    BLACK_COLOR = "#393E46"
    HOVER_COLOR = "#e0e0e0"

    def __init__(self):
        super().__init__()
        #Window spesifications
        self.setWindowTitle("PDF Merger")
        self.setFixedSize(1000, 600)
        self.setStyleSheet(f"background-color: {PDFViewer.MAIN_COLOR};")
        self.setWindowIcon(QIcon("Icons/icon.png"))

        #Window Layouts
        self.main_layout = QVBoxLayout(self)

        self.button_layout = QHBoxLayout(self)
        self.main_layout.addLayout(self.button_layout)

        self.content_container = QWidget()
        self.content_container.setStyleSheet(f"""
            background-color: {PDFViewer.SECOND_COLOR};
            border: 1px solid #888;
            border-radius: 12px;                                     
        """)
        
        self.content_layout = QHBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(10)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.content_container)
        self.scroll_area.setFixedHeight(530)
        self.scroll_area.setStyleSheet(f"""
            QScrollBar:horizontal {{
                background: transparent;
                height: 12px;
                margin: 0px 20px 0 20px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal {{
                background: {PDFViewer.THIRD_COLOR};
                border-radius: 6px;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                background: transparent;
            }}
        """)
        self.main_layout.addWidget(self.scroll_area)


        #Saves the current selected PDFs paths in this list
        self.selected_PDFs = []


        #Merge Button
        self.merge_button = QPushButton("Merge")
        self.merge_button.clicked.connect(self.merge_pdf)
        self.merge_button.setStyleSheet(f"""
            QPushButton {{
                color: {PDFViewer.BLACK_COLOR};
                font-weight: bold;
                background-color: {PDFViewer.THIRD_COLOR};
                border: 1px solid #888;
                border-radius: 12px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {PDFViewer.HOVER_COLOR};
            }}
        """)
        self.button_layout.addWidget(self.merge_button)

        #Reset Button
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset)
        self.reset_button.setStyleSheet(f"""
            QPushButton {{
                color: {PDFViewer.BLACK_COLOR};
                font-weight: bold;
                background-color: {PDFViewer.THIRD_COLOR};
                border: 1px solid #888;
                border-radius: 12px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {PDFViewer.HOVER_COLOR};
            }}
        """)
        self.button_layout.addWidget(self.reset_button)

        #Select PDF Button
        self.add_select_pdf_button()

    
    def add_select_pdf_button(self):
        self.select_button = QPushButton()
        self.select_button.clicked.connect(self.load_main_pdf)
        self.select_button.setFixedSize(300, 400)
        self.select_button.setIcon(QIcon("./Icons/plus.png"))
        self.select_button.setIconSize(QSize(64, 64))
        self.select_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {PDFViewer.THIRD_COLOR};
                border: 2px dashed #888;
                border-radius: 12px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {PDFViewer.HOVER_COLOR};
            }}
        """)
        self.content_layout.addWidget(self.select_button)


    def load_main_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if not path:
            return

        # Left button
        self.left_button = QPushButton()
        self.left_button.setFixedSize(100, 400)
        self.left_button.setIcon(QIcon("./Icons/plus.png"))
        self.left_button.setIconSize(QSize(64, 64))
        self.left_button.clicked.connect(lambda: self.add_pdf(side="left"))
        self.left_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {PDFViewer.THIRD_COLOR};
                border: 2px dashed #888;
                border-radius: 12px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {PDFViewer.HOVER_COLOR};
            }}
        """)
        self.content_layout.addWidget(self.left_button)

        # Left spacer
        self.content_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Central widget container
        self.pdf_widgets = QHBoxLayout()
        self.content_layout.addLayout(self.pdf_widgets)

        # Right spacer
        self.content_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Right button
        self.right_button = QPushButton()
        self.right_button.setFixedSize(100, 400)
        self.right_button.setIcon(QIcon("./Icons/plus.png"))
        self.right_button.setIconSize(QSize(64, 64))
        self.right_button.clicked.connect(lambda: self.add_pdf(side="right"))
        self.right_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {PDFViewer.THIRD_COLOR};
                border: 2px dashed #888;
                border-radius: 12px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {PDFViewer.HOVER_COLOR};
            }}
        """)
        self.content_layout.addWidget(self.right_button)

        # Add initial PDF
        self.add_pdf_widget(path)

        # Update UI
        self.content_layout.removeWidget(self.select_button)
        self.select_button.deleteLater()


    def add_pdf_widget(self, path, position='right'):
        pixmap = pdfhandler.render_pdf_page(path).scaled(300, 400)

        label = QLabel()
        label.setPixmap(pixmap)
        label.setFixedSize(300, 400)
        label.setStyleSheet(f"""
            border: None;
        """)

        if position == 'left':
            self.pdf_widgets.insertWidget(0, label)
            self.selected_PDFs = [path] + self.selected_PDFs
        elif position == 'right':
            self.pdf_widgets.addWidget(label)
            self.selected_PDFs.append(path)

        print("Successfully Added PDF")


    def add_pdf(self, side):
        path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if path:
            self.add_pdf_widget(path, position=side)
    

    def merge_pdf(self):
        pdfhandler.merge("merged", self.selected_PDFs)
        print("Successfully Merged!")


    def reset(self):
        self.selected_PDFs = []

        # Remove all widgets from main_layout
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

        # Recreate the initial Select PDF button
        self.add_select_pdf_button()

        print("reset")


    #Helperfunction for resetting the window
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())


#Running the app
app = QApplication(sys.argv)
viewer = PDFViewer()
viewer.show()
sys.exit(app.exec())