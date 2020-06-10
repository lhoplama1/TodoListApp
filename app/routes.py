from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, enterItemForm, removeItemForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Item
from werkzeug.urls import url_parse
# , db 
# from app.forms import LoginForm, RegistrationForm
# from flask import render_template, flash, redirect, url_for, request
# from flask_login import current_user, login_user, logout_user, login_required
# from app.models import User

# from datetime import datetime
# from app.forms import EditProfileForm



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():    
    form = enterItemForm()
    # user = User.query.filter_by(username=form.username.data).first()
    items = Item.query.filter_by(userId=current_user.id).order_by("priority")

    # print("outside")
    print(form.errors)
    if form.validate():
        print("valid")
    #click submit button
    if form.validate_on_submit():
        # print("hi")
        #turn form.date.data into a datetime object
        item = Item(item=form.item.data, priority=form.priority.data, date=form.date.data, userId=current_user.id, inProgress=False)
        db.session.add(item)
        db.session.commit()
        flash('Congratulations, you added something to your list!')
        # items = Item.query.filter_by(userId=current_user.id)
        return redirect(url_for('index'))


    remove = removeItemForm()
    # print(remove.errors)
    if remove.validate():
        print("Valid")

    if remove.validate_on_submit():
        print("hi")
        checkList = request.form.getlist("myCheckBox")
        # print(checkList)
        inProgressList = request.form.getlist("inProgress")

        for value in inProgressList:
            item = Item.query.filter_by(id=int(value)).first()
            item.inProgress=True
            db.session.commit()

        for idNumber in checkList:
            item = Item.query.filter_by(id=int(idNumber)).first()
            db.session.delete(item)
            db.session.commit()

        return redirect(url_for('index'))    


    return render_template("index.html", title='Home Page', form=form, items=items, remove=remove)

#Rewrite the code for the index/finish the code above fixing the database filtering
#


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

