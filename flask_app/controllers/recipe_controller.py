from flask_app import app
from flask import render_template, request, redirect, session

from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

from flask import flash

@app.route('/recipes/new')
def show_recipe_form():

    return render_template('new_recipe.html')

@app.route('/create_recipe', methods = ['POST'])
def submit_recipe_form():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    
    recipe_data = {
        **request.form,
        'user_id' : session['user_id']
    }

    Recipe.create_recipe(recipe_data)

    return redirect('/recipes')

@app.route('/recipes/<int:recipe_id>')
def show_recipe(recipe_id):
    
    if 'user_id' not in session:
        return redirect ('/')

    one_user = User.get_user({'id' : session['user_id']})

    one_recipe = Recipe.get_one_recipe({'recipe_id' : recipe_id})

    return render_template('recipe.html', one_recipe = one_recipe, one_user = one_user)

@app.route('/recipes/edit/<int:recipe_id>')
def show_edit_form(recipe_id):

    one_recipe = Recipe.get_one_recipe({'recipe_id' : recipe_id})



    return render_template('edit_recipe.html', one_recipe = one_recipe)

@app.route('/recipes/update/<int:recipe_id>', methods = ['POST'])
def submit_edit_form(recipe_id):

    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/edit/{recipe_id}')
    
    Recipe.update_recipe({
        **request.form,
        'recipe_id' : recipe_id
    })

    return redirect('/recipes')

@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):

    Recipe.recipe_delete({'recipe_id' : recipe_id})

    return redirect('/recipes')
