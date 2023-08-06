from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from cbook.model import helper
import os


class RvController:
    

    def __init__(self, model, window):
        self.model = model
        self.window = window


    def get_fullimage_path(self, recipe_path):
        return os.path.dirname(recipe_path) + "/full.jpg"


    def load_recipe(self, recipe):
        # fill recipe data
        self.recipe = recipe
        recipe_dict = self.model.get_recipe_dict(recipe)
        self.window.nameLabel.setText(self.model.get_name(recipe_dict))
        self.window.set_image(self.get_fullimage_path(recipe))

        instructions = self.model.get_instructions(recipe_dict)
        self.window.anleitungLabel.setText(self.get_instructions_string(instructions))
        self.window.beschreibungLabel.setText(self.model.get_description(recipe_dict))
        self.window.portionenSpinBox.setValue(self.model.get_servings(recipe_dict))

        # tags
        t = self.model.get_tags(recipe_dict)
        self.window.tagsLabel.setText(t)

        self.set_ingredients(self.model.get_ingredients(recipe_dict))

        self.window.portionenSpinBox.valueChanged.connect(lambda: self.change_servings(recipe_dict))

        # open recipe view
        self.window.stackedWidget.setCurrentIndex(1)


    def get_instructions_string(self, instructions):
        instruction_text = ""
        for i in instructions:
            instruction_text = instruction_text + i + "\n\n\n"
        return instruction_text


    def clear_ingredients(self):
        grid = self.window.zutatenGrid
        for i in range(1, grid.rowCount()):
            item = grid.itemAtPosition(i, 0)
            if item:
                item.widget().deleteLater()
            item = grid.itemAtPosition(i, 1)
            if item:
                item.widget().deleteLater()
            item = grid.itemAtPosition(i, 2)
            if item:
                item.widget().deleteLater()


    def set_ingredients(self, ingredients):
        self.clear_ingredients()
        grid = self.window.zutatenGrid
        for x, i in enumerate(ingredients):
            if len(i.split(' ')) >= 3:
                label = QLabel(i.split(' ')[0].replace(",", "."))
                label.setAlignment(Qt.AlignRight)
                grid.addWidget(label, x + 1, 0)
                grid.addWidget(QLabel(i.split(' ')[1]), x + 1, 1)
                ing = ""
                for e in i.split(' ')[2:]:
                    ing = ing + e + " "
                grid.addWidget(QLabel(ing[:-1]), x + 1, 2)


    def get_amounts(self, ingredients):
        amounts = []
        for x, i in enumerate(ingredients):
            if len(i.split(' ')) >= 3:
                amounts.append(i.split(' ')[0].replace(",", "."))
        return amounts


    def change_servings(self, recipe_dict):
        default_servings = self.model.get_servings(recipe_dict)
        new_servings = self.window.portionenSpinBox.value()
        grid = self.window.zutatenGrid
        amounts = self.get_amounts(self.model.get_ingredients(recipe_dict))
        for i in range(1, len(amounts)):
            item = grid.itemAtPosition(i, 0)
            if item:
                a = amounts[i - 1]
                if a != '':
                    convert = "%g" % (float(a) * new_servings / default_servings)
                    item.widget().setText(convert)
