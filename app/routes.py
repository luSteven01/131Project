from flask import Flask, render_template, flash, redirect
from app import obj
from app.forms import LoginForm, SearchForm

#these must be imported to manipulate the database

#different URL the app will implement
from app.models import User, Post
from app import db

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

        ############Add a row to database (user table)####################
        user = User(username=current_form.username.data, email = 'test@gmail.com')
        db.session.add(user)
        db.session.commit()

        ###############Get/search a row to the database (user table)################
        #look up all users
        #users = User.query.all()
        #for user in users:
            #shows on the terminal
            #print(user.id, user.username, user.email)

            #show on html
            #flash()

        ##############Look up users by ID#########################
        #print(User.query.get(2))

        ##############Look up users by attribute (returns a list)#############
        #search = User.query.filter_by(username='steven')
        #for s in search:
        #    print(s)

        ########delete a row in the database (user table)##############
        #user_to_delete = User.query.get(1)
        #db.session.delete(user_to_delete)
        #db.session.commit()

        ##########################################################################
        # Adding to User and Post
        #Step 1: create user
        #u = User(username=current_form.username.data, email='test@gmail.com')
        #db.session.add(u)
        #db.session.commit()

        #Step 2: create post
        #p = Post(body='hello this is a tweet', author=User.query.get(1))
        #db.session.add(p)
        #db.session.commit()

        #Step 3: search for post
        ##search for user
        #u = User.query.get(1)
        #print(u.posts)

        #return redirect('/')

    #flash('ERROR INVALID USERNAME OR PASSWORD')
    #print(f'This is the username {current_form.username.data}')
    #flash(f'{current_form.username.data} is an invalid username')
    return render_template("login.html", form=current_form)

@obj.route("/search", methods=["GET", "POST"])
#tells flask to execute login() when user goes to /login path of the webpage
def search():
    current_form = SearchForm()
    if current_form.validate_on_submit():
        flash(f'VALID FLIGHT NUMBER {current_form.fn.data}')

        ############Database Procedure here####################
    return render_template("search.html", form=current_form)


@obj.route("/guidelines")
def guidelines():
    return render_template('guidelines.html')
