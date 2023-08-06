from cbook.config import config
from cbook.model import recipe_parser as rp


class CbModel:
    recipes = []


    def load_recipes(self):
        self.recipes = rp.get_recipes(config.get_recipe_path())


    def get_recipes(self):
        return self.recipes


    def get_recipe_dict(self, recipe):
        return rp.read_recipe(recipe)


    def get_name(self, recipe):
        return rp.get_name(recipe)


    def get_instructions(self, recipe):
        return rp.get_instructions(recipe)
    

    def get_servings(self, recipe):
        return rp.get_servings(recipe)


    def get_tags(self, recipe):
        return rp.get_keywords(recipe)


    def get_ingredients(self, recipe):
        return rp.get_ingredients(recipe)


    def get_description(self, recipe):
        return rp.get_description(recipe)


    def check_name(self, name):
        for r in self.get_recipes():
            rd = self.get_recipe_dict(r)
            if name == rp.get_name(rd):
                return False
        return True


    def save_recipe(self, name, image, ingredients, servings, description,
            instructions, tags):
        rd = rp.create_recipe_dict(name, ingredients, servings, description,
                instructions, tags)
        rp.write_recipe(config.get_recipe_path(), rd, image)


    def delete_recipe(self, recipe):
        rp.delete_recipe(recipe)
