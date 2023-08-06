#!/usr/bin/env python3
from argparse import ArgumentParser
from json import load
from os import path, mkdir
import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QLabel

from radispawn.radial_widget import RadialMenu, Wedge

class MainWindow(QMainWindow):
    def __init__(self, geom, wedges):
        QMainWindow.__init__(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(geom)

        self.frame = QFrame()
        self.vbox = QVBoxLayout()

        self.menu = RadialMenu(wedges)

        self.vbox.addWidget(self.menu, Qt.AlignCenter, Qt.AlignCenter)
        self.frame.setLayout(self.vbox)
        self.setCentralWidget(self.frame)

        self.showMaximized()

def getWedges(data):
    if "wedges" not in data.keys() or len(data["wedges"]) == 0:
        raise KeyError("json file must contain at least one wedge.")
    wedges = []
    for wedge in data["wedges"]:
        wedges.append(Wedge(wedge["name"], wedge["call"], *wedge["color"]))
    wedges = [wedges[0], *reversed(wedges[1:])]
    return wedges

def start(data):
    wedges = getWedges(data)

    app = QApplication(sys.argv)
    window = MainWindow(app.primaryScreen().availableGeometry(), wedges)
    sys.exit(app.exec())


def main():
    # Create config folder if it doesn't exist
    if not path.exists(pth := path.expanduser("~/.config/radispawn")):
        mkdir(pth)

    # Parse args with argparse
    parser = ArgumentParser()
    parser.add_argument("file", help="JSON file to define the menu; relative paths search pwd and then ~/.config/radispawn/")
    args = parser.parse_args()

    # fa stands for file argument
    fa = args.file
    json_file = None
    if path.exists(fa):
        json_file = fa
    # cf stands for .config file
    elif path.exists(cf := path.expanduser(f"~/.config/radispawn/{fa}")) and fa[0] != "/":
        json_file = cf
    else:
        raise FileNotFoundError(f"json file {fa} not found")
    
    with open(json_file, "r") as f:
        data = load(f)
    print(data)
    start(data)

if __name__ == "__main__":
    main()
