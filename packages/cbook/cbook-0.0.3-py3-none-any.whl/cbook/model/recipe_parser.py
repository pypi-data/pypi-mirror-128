from os import listdir
import os, shutil
from os.path import isdir, lexists
import json
from PIL import Image

THUMB_SIZE = 96


def get_recipes(recipepath):
    files = listdir(recipepath)
    recipes = []

    for file in files:
        fullpath = os.path.join(recipepath, file)
        if isdir(fullpath):
            if lexists(os.path.join(fullpath, "recipe.json")):
                recipes.append(os.path.join(fullpath, "recipe.json"))
    return recipes


def read_recipe(recipe_path):
    f = open(recipe_path, "r")
    lines = f.readlines()
    recipe_dict = json.loads(lines[0])
    return recipe_dict


def get_name(recipe):
    return recipe['name']


def get_servings(recipe):
    return recipe['recipeYield']


def get_ingredients(recipe):
    return recipe['recipeIngredient']


def get_description(recipe):
    return recipe['description']


def get_instructions(recipe):
    return recipe['recipeInstructions']


def get_keywords(recipe):
    return recipe['keywords']


def create_recipe_dict(name, ingredients, servings, description, instructions,
        tags):
    rd = {
        "name":name,
        "description":description,
        "recipeIngredient":ingredients,
        "recipeInstructions":instructions.split('\n\n'),
        "recipeYield":servings,
        "keywords":tags,
            }
    return rd

def save_image(image, target_folder):
    img = Image.open(image)
    rgb_image = img.convert('RGB')
    rgb_image.save(os.path.join(target_folder, "full.jpg"))
    thumb = rgb_image.resize((THUMB_SIZE, THUMB_SIZE))
    thumb.save(os.path.join(target_folder, "thumb.jpg"), quality=90)


def write_recipe(recipe_path, recipe_dict, image):
    data = json.dumps(recipe_dict)
    folder = os.path.join(recipe_path, get_name(recipe_dict))
    os.makedirs(folder, exist_ok=True)
    filepath = folder + "/recipe.json"
    f = open(filepath, "w")
    f.write(data)
    if image:
        save_image(image, folder)


def delete_recipe(recipe):
    shutil.rmtree(os.path.dirname(recipe))
