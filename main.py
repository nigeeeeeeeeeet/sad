from ui import Ui_MainWindow

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import json

app = QApplication([])
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

notes = {}

def add_note():
    note_name, ok = QInputDialog.getText(MainWindow, "Додати замітку", "Назва замітки: ")
    if ok and note_name != "":
        notes[note_name] = {"text": "", "tags": []}
        ui.listWidget.addItem(note_name)
        ui.listWidget_2.clear()
        print(notes)
    else:
        print("Не вибрали замітку")

def show_note():
    if ui.listWidget.selectedItems():
        key = ui.listWidget.selectedItems()[0].text()
        ui.textEdit.setText(notes[key]["text"])
        ui.listWidget_2.clear()
        ui.listWidget_2.addItems(notes[key]["tags"])

def save_note():
    if ui.listWidget.selectedItems():
        key = ui.listWidget.selectedItems()[0].text()
        notes[key]["text"] = ui.textEdit.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
            print(notes)
    else:
        print("Не вибрана замітка для збереження")

def del_note():
    if ui.listWidget.selectedItems():
        key = ui.listWidget.selectedItems()[0].text()
        del notes[key]
        ui.listWidget.clear()
        ui.listWidget_2.clear()
        ui.textEdit.clear()
        ui.listWidget.addItems(notes.keys())
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Не вибрана замітка для видалення")

def add_tag():
    if ui.listWidget.selectedItems():
        key = ui.listWidget.selectedItems()[0].text()
        tag_name, ok = QInputDialog.getText(MainWindow, "Додати тег", "Назва тегу: ")
        if ok and tag_name != "":
            notes[key]["tags"].append(tag_name)
            ui.listWidget_2.clear()
            ui.listWidget_2.addItems(notes[key]["tags"])
            with open("notes_data.json", "w") as file:
                json.dump(notes, file, sort_keys=True, ensure_ascii=False)
            print(notes)

def del_tag():
    if ui.listWidget_2.selectedItems():
        key = ui.listWidget.selectedItems()[0].text()
        tag = ui.listWidget_2.selectedItems()[0].text()
        notes[key]["tags"].remove(tag)
        ui.listWidget_2.clear()
        ui.listWidget_2.addItems(notes[key]["tags"])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
            print(notes)
    else:
        print("Тег не вибрано для видалення")

def search_tag():
    tag = ui.lineEdit.text()
    if ui.pushButton_6.text() == "Шукати тег" and tag:
        notes_filtered = {note: notes[note] for note in notes if tag in notes[note]["tags"]}
        ui.pushButton_6.setText("Скинути пошук")
        ui.listWidget.clear()
        ui.listWidget_2.clear()
        ui.listWidget.addItems(notes_filtered.keys())
    else:
        ui.pushButton_6.setText("Шукати тег")
        ui.listWidget.clear()
        ui.listWidget_2.clear()
        ui.listWidget.addItems(notes.keys())

# Connect buttons
ui.pushButton.clicked.connect(add_note)
ui.listWidget.itemClicked.connect(show_note)
ui.pushButton_2.clicked.connect(del_note)
ui.pushButton_3.clicked.connect(save_note)
ui.pushButton_4.clicked.connect(add_tag)
ui.pushButton_5.clicked.connect(del_tag)
ui.pushButton_6.clicked.connect(search_tag)

# Load notes from file if available
try:
    with open('notes_data.json', "r") as file:
        notes = json.load(file)
        ui.listWidget.addItems(notes.keys())
except FileNotFoundError:
    notes = {}

MainWindow.show()
app.exec_()
