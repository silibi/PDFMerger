import os

import fitz
from PyQt6.QtGui import QPixmap, QImage, QPainter, QPainterPath
from PyQt6.QtCore import Qt, QRectF


def merge(mergedName, filepaths):
    '''
    Merges a list of PDFs into a single PDF and writes it to the same folder
    as the first file in the list of PDFs
    '''
    merged = fitz.open()

    for filepath in filepaths:
        with fitz.open(filepath) as doc:
            merged.insert_pdf(doc)

    destination = os.path.dirname(filepaths[0])
    merged.save(os.path.join(destination, mergedName + ".pdf"))


def render_pdf_page(filepath, page_number=0, scale=0.3, radius=12):
    '''
    Renders the first page of a PDF file into a an image to display in the app
    Rounds the edges for a neater look
    '''
    doc = fitz.open(filepath)
    page = doc.load_page(page_number)
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
    
    pixmap = QPixmap.fromImage(QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)).scaled(300, 400)

    size = pixmap.size()
    rounded = QPixmap(size)
    rounded.fill(Qt.GlobalColor.transparent)

    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    path = QPainterPath()
    rect = QRectF(0, 0, size.width(), size.height())
    path.addRoundedRect(rect, radius, radius)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()

    return rounded


if __name__ == "__main__":
    merge("test", ["Testobjects/test1.pdf", "Testobjects/test2.pdf"])