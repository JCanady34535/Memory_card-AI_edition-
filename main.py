import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QListWidget, QLineEdit, QInputDialog

app = QApplication([])

window = QWidget()
window.setWindowTitle('Smart Notes (made with AI)')
window.move(100, 100)
window.resize(400, 400)

notes_data = {}

try:
    with open('notes_data.json', 'r') as file:
        notes_data = json.load(file)
except FileNotFoundError:
    pass

def show_note():
    selected_items = ZList2.selectedItems()
    if selected_items:
        name = selected_items[0].text()
        text1.setText(notes_data[name]['text'])
        TList2.clear()
        TList2.addItems(notes_data[name]['tags'])

def add_note():
    note_name, ok = QInputDialog.getText(window, 'Add a Note', 'Note Title:')
    if ok and note_name:
        notes_data[note_name] = {'tags': [], 'text': ''}
        ZList2.addItem(note_name)
        TList2.clear()
        save_notes_to_json()

def del_note():
    selected_items = ZList2.selectedItems()
    if selected_items:
        ZName = selected_items[0].text()
        del notes_data[ZName]
        ZList2.clear()
        TList2.clear()
        text1.clear()
        save_notes_to_json()

def save_note():
    selected_items = ZList2.selectedItems()
    if selected_items:
        ZName = selected_items[0].text()
        notes_data[ZName]['text'] = text1.toPlainText()
        save_notes_to_json()

def add_tag():
    selected_items = ZList2.selectedItems()
    if selected_items:
        ZName = selected_items[0].text()
        tag = Tag.text()
        if tag:
            notes_data[ZName]['tags'].append(tag)
            TList2.addItem(tag)
            Tag.clear()
            save_notes_to_json()

def search_tag():
    tag = Tag.text()
    if tag:
        notes_filtered = {z: data for z, data in notes_data.items() if tag in data['tags']}
        ZList2.clear()
        ZList2.addItems(notes_filtered.keys())
    else:
        ZList2.clear()
        ZList2.addItems(notes_data.keys())
    save_notes_to_json()

def del_tag():
    selected_items = ZList2.selectedItems()
    if selected_items:
        ZName = selected_items[0].text()
        TName = TList2.selectedItems()
        if TName:
            TName = TName[0].text()
            notes_data[ZName]['tags'].remove(TName)
            TList2.clear()
            TList2.addItems(notes_data[ZName]['tags'])
            save_notes_to_json()

def save_notes_to_json():
    with open('notes_data.json', 'w') as file:
        json.dump(notes_data, file)

# Create layouts and widgets
text1 = QTextEdit()
ZList = QLabel('Notes List')
TList = QLabel('Tags List')
addd = QPushButton('Add Tag')
find = QPushButton('Search by Tag')
unpin = QPushButton('Remove Tag')
create = QPushButton('Create Note')
delete = QPushButton('Delete Note')
safe = QPushButton('Save Note')
ZList2 = QListWidget()
TList2 = QListWidget()
Tag = QLineEdit('Enter Tag...')

ZList2.addItems(notes_data.keys())

# Create layouts and set up the window
v_line = QVBoxLayout()
h_line = QVBoxLayout()
line = QHBoxLayout()
line.addLayout(h_line)
line.addLayout(v_line)
h_line.addWidget(text1)
v_line.addWidget(ZList)
v_line.addWidget(ZList2)
v_line.addWidget(addd)
v_line.addWidget(find)
v_line.addWidget(unpin)
v_line.addWidget(TList)
v_line.addWidget(TList2)
v_line.addWidget(create)
v_line.addWidget(delete)
v_line.addWidget(safe)
v_line.addWidget(Tag)
window.setLayout(line)

# Connect signals to slots
ZList2.itemClicked.connect(show_note)
create.clicked.connect(add_note)
delete.clicked.connect(del_note)
safe.clicked.connect(save_note)
addd.clicked.connect(add_tag)
unpin.clicked.connect(del_tag)
find.clicked.connect(search_tag)

# Show the window and start the application
window.show()
app.exec_()
