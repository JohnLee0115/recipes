from flask_app import app
from flask import render_template, request, redirect, session

from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

from flask_bcrypt import Bcrypt

from flask import flash

bcrypt = Bcrypt(app)

@app.route('/')
def login_registration_form():

    return render_template('login_register.html')

@app.route('/process', methods = ['POST'])
def submit_registration():
    if not User.validate_registration(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }

    user_id = User.register_user(data)

    session['user_id'] = user_id

    return redirect('/recipes')

@app.route('/login', methods=['POST'])
def login():
    data = {'email' : request.form['email']}
    email_in_db = User.get_by_email(data)

    if not email_in_db:
        flash('Invalid Email/Password')
        return redirect('/')
    if not bcrypt.check_password_hash(email_in_db.password, request.form['password']):
        flash('Invalid Email/Password')
        return redirect('/')
    
    session['user_id'] = email_in_db.id

    return redirect('/recipes')

@app.route('/recipes/')
def show_recipes():

    if 'user_id' not in session:
        return redirect ('/')

    one_user = User.get_user({'id' : session['user_id']})

    all_recipes = Recipe.get_all_recipes()

    return render_template('recipes.html', one_user = one_user, all_recipes = all_recipes)

@app.route('/logout')
def clear_session():

    session.clear()

    return redirect('/')
