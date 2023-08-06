from cbook.model import helper
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QMainWindow, QStyle, QToolButton
import os, sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)



class MainWindow(QMainWindow):
    recipe_buttons = []


    def __init__(self):
        super(MainWindow, self).__init__()
        ui_file = resource_path("main_window.ui")
        uic.loadUi(ui_file, self)
        self.set_icons()


    def set_icons(self):
        self.toolButtonDelete.setIcon(self.get_icon('edit-delete', QStyle.SP_TrashIcon))
        self.editButton.setIcon(self.get_icon('edit', QStyle.SP_ArrowForward))
        self.backButton.setIcon(self.get_icon('go-previous', QStyle.SP_ArrowBack))
        self.buttonSave.setIcon(self.get_icon('document-save', QStyle.SP_DialogSaveButton))
        self.buttonReload.setIcon(self.get_icon('edit-clear', QStyle.SP_BrowserReload))
        self.buttonCancel.setIcon(self.get_icon('edit-clear-all', QStyle.SP_DialogCancelButton))
        self.deleteImageButton.setIcon(self.get_icon('edit-delete', QStyle.SP_DialogDiscardButton))
        self.buttonClearTags.setIcon(self.get_icon('edit-delete', QStyle.SP_DialogDiscardButton))
        self.loadImageButton.setIcon(self.get_icon('document-open', QStyle.SP_FileDialogStart))
        self.toolButtonFolder.setIcon(self.get_icon('folder', QStyle.SP_DirIcon))
        self.buttonNeuesRezept.setIcon(self.get_icon('document-new', QStyle.SP_FileIcon))
        self.buttonAddIngredient.setIcon(self.get_icon('list-add', QStyle.SP_ArrowDown))
        self.buttonDeleteIngredient.setIcon(self.get_icon('list-remove', QStyle.SP_ArrowUp))


    def add_recipe(self, recipe_button):
        self.recipe_buttons.append(recipe_button)
        layout = self.recipeList.layout()
        layout.insertWidget(layout.count()-1,recipe_button)


    def get_recipe_buttons(self):
        return self.recipe_buttons


    def delete_recipe_buttons(self):
        layout = self.recipeList.layout()
        helper.clear_layout(layout)
        self.recipe_buttons.clear()


    def set_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.imageLabel.setPixmap(pixmap)

        self.imageLabel.resize(pixmap.width(),pixmap.height())


    def get_icon(self, theme_icon, fallback_icon):
        if QIcon.hasThemeIcon(theme_icon):
            return QIcon.fromTheme(theme_icon)
        else:
            # return default qt icon (fallback_icon)
            return self.style().standardIcon(fallback_icon)


    def get_default_meal_image_path(self):
        return resource_path("meal_icon.svg")
