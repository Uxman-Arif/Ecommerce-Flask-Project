from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
mig = Migrate(app, db)

app.config['UPLOAD_FOLDER'] = 'uploads/'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description =db.Column(db.String)
    price = db.Column(db.Float)
    image = db.Column(db.LargeBinary(100), nullable=True)

    # def __repr__():
    #     return self.name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def addproduct():
    # if request.method=='POST':
    print('yes here')
    prod = request.form.get('prod')
    description = request.form.get('description')
    price = request.form.get('price')
    file = request.files.get('Picture')
    print(prod, description, price, file)
    return render_template('addproduct.html')

admin = Admin(app, name='My Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Product, db.session))

if __name__ == '__main__':
    app.run(debug=True)