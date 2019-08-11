import json
import random as r
import pandas as pd
from flask import Flask, render_template, url_for, request, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, TextField, validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'bhuwanesh'
db = SQLAlchemy(app)

with open("stylight.json",'r') as file:
    categories = json.load(file)


def generate_uuid():
    random_string = ''
    random_str_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    uuid_format = [4, 4, 4]
    for n in range(len(uuid_format)):
        for i in range(0,uuid_format[n]):
            random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])
        if n != len(uuid_format)-1:
            random_string += '-'

    return random_string


def generate_discount_type(row):
    if row<3:
        value = "15% off"
    elif row<6:
        value = "15€ off"
    else:
        value = "Free Shipping"
    return value


dataframe = pd.DataFrame()
for row in range(len(categories["Categories"])):
    _id = categories["Categories"][row]['id']
    categoryn = categories["Categories"][row]['name'].split(" > ")[0].lower()
    sub_categoryn = categories["Categories"][row]['name'].split(" > ")[1].lower()
    productsn = categories["Categories"][row]['name'].split(" > ")[2].lower()
    discount_typen = generate_discount_type(row)
    temp = pd.DataFrame([{"id":_id, "category":categoryn, "sub_category":sub_categoryn,
                          "products":productsn, "discount_types":discount_typen}])
    dataframe = pd.concat([dataframe,temp])

dataframe = dataframe[['id','category','sub_category','products','discount_types']]


def choice_creation(choices_name):
    choices_list = []
    for cat in choices_name:
        choices_list.append(tuple([cat,cat]))
    return choices_list


class InfoForm(FlaskForm):
    subcategory = SelectField(u"Choose your Category:",
                            choices=choice_creation(dataframe.sub_category.unique()))
    product = SelectField(u"Choose your Product:",
                            choices=[])
    discount_type = SelectField(u"Choose your Discount Type:",
                            choices=choice_creation(dataframe.discount_types.unique()))
    minimum_price = TextField('Select the Minimum Price: ')
    submit = SubmitField('Generate Code and Save')


class Todo(db.Model):
    content = db.Column(db.String(200), nullable=False, primary_key=True)
    content1 = db.Column(db.String(200), nullable=False)
    content2 = db.Column(db.String(200), nullable=False)
    content3 = db.Column(db.String(200), nullable=False)
    discount_code = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, content, content1, content2, content3, discount_code):
        self.content = content
        self.content1 = content1
        self.content2 = content2
        self.content3 = content3
        self.discount_code = discount_code
    def __repr__(self):
        return '<Task %r>' % self.content


@app.route('/', methods=['POST', 'GET'])
def index():
    form = InfoForm()

    temp = dataframe.loc[dataframe['sub_category'] == 'clothing']
    form.product.choices = [tuple([temp['products'].iloc[row], temp['products'].iloc[row]]) for row in range(len(temp))]

    if request.method == 'POST' and form.validate_on_submit():
        task_subcat = form.subcategory.data
        task_content = form.product.data
        task_content2 = form.discount_type.data
        task_content3 = form.minimum_price.data
        codenew = generate_uuid()
        new_task = Todo(content=task_content, content1 = task_subcat, content2 = task_content2, discount_code=codenew, content3 = task_content3)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks, form = form)


@app.route('/delete/<string:content>')
def delete(content):
    task_to_delete = Todo.query.get_or_404(content)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/product/<subcategory>')
def prod(subcategory):
    products = dataframe.loc[dataframe['sub_category'] == subcategory]

    productArray = []

    for row in range(len(products)):
        prodobj = {}
        prodobj['id'] = products['products'].iloc[row]
        prodobj['name'] = products['products'].iloc[row]
        productArray.append(prodobj)
    return jsonify({'products': productArray})


if __name__ == "__main__":
    app.run(debug=True)