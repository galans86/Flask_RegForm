from flask import Flask, request, render_template, redirect, url_for
from models import db, User

from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = '5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'
csrf = CSRFProtect(app)
db.init_app(app)


@app.route('/')
def index():
    db.create_all()
    return redirect(url_for('regform'))

@app.route("/regform/")
@csrf.exempt
def regform():
    form = RegisterForm()
    return render_template('regform.html', form=form)


@app.route('/save_data/', methods=['GET', 'POST'])
def save_data():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        user = User(
            username=form.username.data,
            surname=form.surname.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        context = {"user":user}
        return render_template('main.html',**context)
    return render_template('regform.html', form=form)


@app.post('/exit/')
@csrf.exempt
def exit():
    return redirect(url_for('regform'))
