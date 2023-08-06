#!/bin/env python3
from cbook.view.main_window import MainWindow
from cbook.model import cb_model
from cbook.controller import mw_controller as mwc

# Qt
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic

def main():
    app = QApplication(sys.argv)

    m_model = cb_model.CbModel()
    window = MainWindow()

    m_mwc = mwc.MwController(m_model, window)

    window.show()
    app.exec()


if __name__ == '__main__':
    sys.exit(main())
