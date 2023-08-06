from cbook.model import helper
from cbook.config import config
from cbook.controller.re_controller import ReController
from cbook.controller.rc_controller import RvController
from cbook.view import recipe_button as rb
from PyQt5 import QtCore
from PyQt5.QtWidgets import QCheckBox, QDialogButtonBox, QFileDialog, QMessageBox, QVBoxLayout
import os
from os.path import split



class MwController:
    tag_filter = []
    tags = []
    
    def __init__(self, model, window):
        self.model = model
        self.window = window
        self.rv_controller = RvController(model, window)
        self.re_controller = ReController(model, window)

        self.window.recipeList.layout().addStretch()

        self.window.backButton.clicked.connect(self.open_recipe_list)
        self.window.buttonCancel.clicked.connect(self.open_recipe_list)
        self.window.buttonNeuesRezept.clicked.connect(self.create_new_recipe)
        self.window.buttonSave.clicked.connect(self.save_recipe)
        self.window.editButton.clicked.connect(self.edit_recipe)
        self.window.toolButtonDelete.clicked.connect(self.open_confirmation_dialog)
        self.window.toolButtonFolder.clicked.connect(self.change_folder)

        self.check_recipe_path()

        self.load_recipes()


    def choose_recipe_folder(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setInformativeText("Bitte einen Rezeptordner wählen!")
        msg.setWindowTitle("Rezeptordner wählen")
        msg.setStandardButtons(QMessageBox.Open | QMessageBox.Cancel)

        ret = msg.exec_()
        if ret == QMessageBox.Cancel:
            exit()
        elif ret == QMessageBox.Open:
            # open file chooser
            fd = QFileDialog()
            options = QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
            text = "Wähle Rezeptordner"
            path = os.path.expanduser('~')
            dir = fd.getExistingDirectory(msg, text, path, options)
            if dir:
                config.set_recipe_path(dir)


    def check_recipe_path(self):
        recipes_path = config.get_recipe_path()
        while not config.get_recipe_path():
            self.choose_recipe_folder("Noch kein Rezeptordner ausgewählt.")
        if not os.path.exists(config.get_recipe_path()):
            self.choose_recipe_folder("Rezepteordner existierst nicht: " + config.get_recipe_path())


    def change_folder(self):
        fd = QFileDialog()
        options = QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        text = "Wähle Rezeptordner"
        path = os.path.expanduser('~')
        dir = fd.getExistingDirectory(self.window, text, path, options)
        if dir:
            config.set_recipe_path(dir)
        self.window.delete_recipe_buttons()
        self.load_recipes()


    def load_recipes(self):
        self.model.load_recipes()
        self.read_recipes()
        self.create_checkboxes()


    def create_recipe_button(self, recipe, recipe_dict):
        name = self.model.get_name(recipe_dict)
        image_path = self.get_image_path(recipe)
        recipe_button = rb.RecipeButton()
        recipe_button.set_name(name)
        recipe_button.set_image(image_path)
        recipe_button.recipe = recipe
        recipe_button.add_cb(self.open_recipe)
        return recipe_button


    def read_recipes(self):
        self.recipes = self.model.get_recipes()
        self.tags = []
        for r in self.recipes:
            rd = self.model.get_recipe_dict(r)
            self.tags = self.tags + self.model.get_tags(rd).split(',')
            self.window.add_recipe(self.create_recipe_button(r, rd))
        self.tags = sorted(set(self.tags))
        self.tag_filter = self.tags


    def show_button(self, recipe_dict):
        for t in self.model.get_tags(recipe_dict).split(','):
            if t in self.tag_filter:
                return True
        return False


    def filter_recipes(self):
        buttons = self.window.get_recipe_buttons()
        for b in buttons:
            rd = self.model.get_recipe_dict(b.recipe)
            b.setHidden(not self.show_button(rd))


    def filter_tag(self, state, tag):
        if QtCore.Qt.Checked == state:
            if tag not in self.tag_filter:
                self.tag_filter.append(tag)
        else:
            if tag in self.tag_filter:
                self.tag_filter.remove(tag)
        self.filter_recipes()


    def create_checkbox(self, tag):
        cb = QCheckBox(tag)
        cb.tag = tag
        if tag in self.tag_filter:
            cb.setChecked(True)
        cb.stateChanged.connect(lambda s, t=tag: self.filter_tag(s, t))
        return cb


    def clear_checkboxes(self):
        helper.clear_layout(self.window.tagsGroupBox.layout())


    def create_checkboxes(self):
        self.clear_checkboxes()
        for t in self.tags:
            self.window.tagsGroupBox.layout().addWidget(self.create_checkbox(t))


    def get_image_path(self, recipe_path):
        return os.path.dirname(recipe_path) + "/thumb.jpg"


    def open_recipe(self, recipe):
        self.recipe = recipe
        self.rv_controller.load_recipe(recipe)


    def open_confirmation_dialog(self):
        dlg = QMessageBox(self.window)
        dlg.setWindowTitle("Rezept löschen?")
        dlg.setText("Soll das Rezept wirklich gelöscht werden?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec_()

        if button == QMessageBox.Yes:
            self.delete_recipe()
        

    def delete_recipe(self):
        self.model.delete_recipe(self.recipe)
        self.window.delete_recipe_buttons()
        self.window.stackedWidget.setCurrentIndex(0)
        self.load_recipes()


    def edit_recipe(self):
        self.re_controller.prepare_edit(self.recipe, self.tags)
        self.window.stackedWidget.setCurrentIndex(2)


    def open_recipe_list(self):
        self.window.stackedWidget.setCurrentIndex(0)


    def create_new_recipe(self):
        self.re_controller.prepare_new(self.tags)
        self.window.stackedWidget.setCurrentIndex(2)


    def save_recipe(self):
        if self.re_controller.save_recipe():
            self.window.delete_recipe_buttons()
            self.window.stackedWidget.setCurrentIndex(0)
            self.load_recipes()
