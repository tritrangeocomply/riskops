import plotly.express as px
import plotly
import os
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.flowables import Flowable
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, cm
from pdfrw import PdfReader, PdfDict
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER,TA_RIGHT
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly_plots as pp
import PyPDF2
from reportlab.pdfgen import canvas


# # Standard Letter dimensions
# W: 612
# H: 792
# Actual dimesion being used is landscape:
# pW: 871 pH: 612
pW, pH = letter
pW, pH = pH * 1.1, pW


class PdfImage(Flowable):
    def __init__(self, filename_or_object, width=None, height=None, kind='direct'):
        # If using StringIO buffer, set pointer to begining
        if hasattr(filename_or_object, 'read'):
            filename_or_object.seek(0)
        self.page = PdfReader(filename_or_object, decompress=True).pages[0]
        self.xobj = pagexobj(self.page)

        self.imageWidth = width
        self.imageHeight = height
        x1, y1, x2, y2 = self.xobj.BBox

        self._w, self._h = x2 - x1, y2 - y1
        if not self.imageWidth:
            self.imageWidth = self._w
        if not self.imageHeight:
            self.imageHeight = self._h
        self.__ratio = float(self.imageWidth)/self.imageHeight
        if kind in ['direct', 'absolute'] or width==None or height==None:
            self.drawWidth = width or self.imageWidth
            self.drawHeight = height or self.imageHeight
        elif kind in ['bound', 'proportional']:
            factor = min(float(width)/self._w, float(height)/self._h)
            self.drawWidth = self._w*factor
            self.drawHeight = self._h*factor

    def wrap(self, availableWidth, availableHeight):
        return self.drawWidth, self.drawHeight

    def drawOn(self, canv, x, y, _sW=0):
        if _sW > 0 and hasattr(self, 'hAlign'):
            a = self.hAlign
            if a in ('CENTER', 'CENTRE', TA_CENTER):
                x += 0.5*_sW
            elif a in ('RIGHT', TA_RIGHT):
                x += _sW
            elif a not in ('LEFT', TA_LEFT):
                raise ValueError("Bad hAlign value " + str(a))

        #xobj_name = makerl(canv._doc, self.xobj)
        xobj_name = makerl(canv, self.xobj)

        xscale = self.drawWidth/self._w
        yscale = self.drawHeight/self._h

        x -= self.xobj.BBox[0] * xscale
        y -= self.xobj.BBox[1] * yscale

        canv.saveState()
        canv.translate(x, y)
        canv.scale(xscale, yscale)
        canv.doForm(xobj_name)
        canv.restoreState()


def merge_pdf():
    files_dir = os.path.join(os.getcwd(), 'plotly_out')

    # pdf_files = ['plotly_rl8.pdf', 'plotly_rl5.pdf']
    pdf_files = []
    merger = PyPDF2.PdfMerger()

    for filename in pdf_files:
        merger.append(PyPDF2.PdfReader(os.path.join(files_dir, filename), "rb"))

    merger.write(os.path.join(files_dir, "merged_full.pdf"))
    merger.close()


def page_4f(canvas, fig1, fig2, fig3, fig4):
    img1 = BytesIO()
    img2 = BytesIO()
    img3 = BytesIO()
    img4 = BytesIO()
    fig1.write_image(img1, format='pdf', scale=1)
    fig2.write_image(img2, format='pdf', scale=1)
    fig3.write_image(img3, format='pdf', scale=1)
    fig4.write_image(img4, format='pdf', scale=1)

    img1_flowable = PdfImage(img1, width=430, height=300)
    img2_flowable = PdfImage(img2, width=430, height=300)
    img3_flowable = PdfImage(img3, width=430, height=300)
    img4_flowable = PdfImage(img4, width=430, height=300)

    top_left_x, top_left_y = 0, 0
    img1_flowable.drawOn(canvas, top_left_x, top_left_y)
    img2_flowable.drawOn(canvas, top_left_x + pW/2, top_left_y)
    img3_flowable.drawOn(canvas, top_left_x, top_left_y + pH/2)
    img4_flowable.drawOn(canvas, top_left_x + pW/2, top_left_y + pH/2)

    return canvas


def draw_paragraph(canvas, msg, x, y, max_width, max_height):
    message_style = ParagraphStyle('Normal')
    message = msg.replace('\n', '<br />')
    message = Paragraph(message, style=message_style)
    w, h = message.wrap(max_width, max_height)
    message.drawOn(canvas, x, y - h)
    return canvas

def page_3f_1p(canvas, msg, fig1, fig2, fig3):
    img1 = BytesIO()
    img2 = BytesIO()
    img3 = BytesIO()
    fig1.write_image(img1, format='pdf', scale=1)
    fig2.write_image(img2, format='pdf', scale=1)
    fig3.write_image(img3, format='pdf', scale=1)

    img1_flowable = PdfImage(img1, width=430, height=300)
    img2_flowable = PdfImage(img2, width=430, height=300)
    img3_flowable = PdfImage(img3, width=430, height=300)

    # top_left_x, top_left_y = 0.02, 0.42
    top_left_x, top_left_y = 0, 0
    img1_flowable.drawOn(canvas, top_left_x, top_left_y)
    img2_flowable.drawOn(canvas, top_left_x + pW / 2, top_left_y)
    img3_flowable.drawOn(canvas, top_left_x, top_left_y + pH / 2)

    draw_paragraph(canvas, msg,
                   top_left_x + pW / 2, pH,
                   pW/2, pH/2)

    return canvas


def plot_canvas(file_name, path_to_storage,  c=None, ):
    if c is None:
        c = canvas.Canvas(os.path.join(os.getcwd(), path_to_storage, file_name))
    c.setPageSize((pW, pH))
    c.saveState()
    c.setFont('Times-Bold', 20)
    fig1 = pp.plot_surface()
    fig2 = pp.plot_scatter()
    fig3 = pp.plot_curve()
    fig4 = pp.plot_heatmap()

    c = page_4f(c, fig1, fig2, fig3, fig4)

    c.showPage()

    # c = page_4f(c, fig2, fig4, fig1, fig4)

    msg = """<para leftIndent=60 >&bull;Lorem ipsum dolor sit amet, consectetur adipiscing elit, <br/></para>"""
    c = page_3f_1p(c, msg, fig1, fig2, fig3)
    # c.restoreState()
    c.save()


if __name__ == "__main__":

    path_to_storage = os.path.join(os.getcwd(),
                                   # 'plotly_out'
                                   )
    file_name = 'canvas1.pdf'
    plot_canvas(file_name, path_to_storage)
    print(file_name)

