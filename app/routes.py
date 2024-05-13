from flask import Flask, render_template, flash, redirect
from app import obj
from app.forms import LoginForm

#different URL the app will implement
@obj.route("/")
@obj.route("/index.html")
#called view function
def hello():
    company_name_update = "Pet Jett"
    new_header = "Welcome to Pet Jett"
    team_names = ['Steven', 'Melanie', 'Jin', 'Ben']
    dictionary_of_pet_breeds = [
        {
            'breed': 'Cat Breeds',
            'body': ' Siamese, Russian Blue, American Short-hair'

        },
        {
            'breed': 'Dog Breeds',
            'body': ' German Shepherd, Bulldog, Labrador'
        }
    ]

    return render_template('home.html', company=company_name_update,
                           title=new_header, names=team_names, breeds=dictionary_of_pet_breeds)

@obj.route("/login", methods=["GET", "POST"])
#tells flask to execute login() when user goes to /login path of the webpage
def login():
    current_form = LoginForm()
    if current_form.validate_on_submit():
        flash(f'VALID USERNAME {current_form.username.data}')
        flash(f'VALID PASSWORD {current_form.password.data}')
        return redirect('/')

    flash('ERROR INVALID USERNAME OR PASSWORD')
    #print(f'This is the username {current_form.username.data}')
    #flash(f'{current_form.username.data} is an invalid username')
    return render_template("login.html", form=current_form)

@obj.route("/guidelines")
def guidelines():
    return render_template('guidelines.html')
