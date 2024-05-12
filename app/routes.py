from flask import Flask, render_template
from app import obj

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

@obj.route("/login")
#tells flask to execute login() when user goes to /login path of the webpage
def login():
    return render_template("login.html")

@obj.route("/guidelines")
def guidelines():
    return render_template('guidelines.html')
