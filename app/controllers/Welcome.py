"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Welcome(Controller):
    def __init__(self, action):
        super(Welcome, self).__init__(action)
        self.load_model('WelcomeModel')
        self.db = self._app.db
   
    def index(self):
   
        return self.load_view('index.html')

    def create(self):
        user_info = {
            "fname" : request.form['fname'],
            "lname" : request.form['lname'],
            "email" : request.form['email'],
            "password" : request.form['pwd'],
            "pw_confirmation" : request.form['cpwd']
        }
        create_status = self.models['WelcomeModel'].create_user(user_info)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id'] 
            session['name'] = create_status['user']['first_name']
            flash("Successfully registered")
            # we can redirect to the users profile page here
            return redirect('/success')
        else:
            # set flashed error messages here from the error messages we returned from the Model
            for message in create_status['errors']:
                flash(message)
            # redirect to the method that renders the form
            return redirect('/')
    def success(self):
        return self.load_view('success.html', name=session['name'], id= session['id'] )
    
    def login(self):
        user_info ={
        "email" : request.form['email'],
        "password" : request.form['password']
            }
        login_status = self.models['WelcomeModel'].login_user(user_info)
        if login_status['status'] == True:
            session['id'] = login_status['user']['id'] 
            session['name'] = login_status['user']['first_name']
            flash("Successfully logged in")
            # we can redirect to the users profile page here
            return redirect('/success')
        else:
            flash("invalid login")
            return redirect('/')
        
