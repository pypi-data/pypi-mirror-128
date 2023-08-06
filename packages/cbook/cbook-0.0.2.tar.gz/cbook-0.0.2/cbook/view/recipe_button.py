from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QSizePolicy, QStyleOptionToolButton, QToolButton, QWidget



# class RecipeButton(QWidget):
#     def __init__(self, image_path, controller):
#         super(RecipeButton, self).__init__()
#         uic.loadUi("view/recipe_button.ui", self)
#         self.image_path = image_path
#         self.controller = controller
# 
# 
#     def set_name(self, name):
#         self.recipeLabel.setText(name)
# 
# 
#     def set_image(self, image_path):
#         self.imageLabel.setPixmap(QPixmap(image_path))

class RecipeButton(QToolButton):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)


    def set_name(self, name):
        self.setText("  " + name)


    def set_image(self, image_path):
        icon = QIcon(image_path)
        self.setIcon(icon)
        self.setIconSize(QSize(144,144))
        #self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)


    def add_cb(self, cb_function):
        self.cb_function = cb_function
        self.clicked.connect(self.onclick)


    def onclick(self):
        self.cb_function(self.recipe)
