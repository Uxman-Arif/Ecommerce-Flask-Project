from flask import Flask, render_template, request, Response, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_url, login_required, current_user, LoginManager, UserMixin

app = Flask(__name__)

app.secret_key = 'Nosecretbasheergoialafromthenakyalhatli'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
mig = Migrate(app, db)

app.config['UPLOAD_FOLDER'] = 'uploads/'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(400), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description =db.Column(db.String)
    price = db.Column(db.Float)
    image = db.Column(db.LargeBinary(100), nullable=True)

    # def __repr__():
    #     return self.name

# def load_user(user_id):
#     return User.query.get(int(user_id))

@app.route('/image/<int:product_id>')
def serve_image(product_id):
    product = Product.query.get_or_404(product_id)  # Fetch product by ID
    if product.image:  # Check if the image exists
        return Response(product.image, mimetype='image/png')  # Return image with the correct MIME type
    else:
        return "No image found", 404

@app.route('/signup', methods=['GET', 'POST'])
def signupfnc():
    if request.method=='POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password)
        print(username, email, password, hashed_password)
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signinfnc():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            print('exist')
            if check_password_hash(user.password, password):
                flash('Login Successfully!', 'success')
                print('login')
                login_user(user)
                print(current_user.username)
            else:
                print('wrong password')
                flash('Password Dosnot match!', 'error')
        else:
            print('user not exist!')

    return render_template('signin.html')

@app.route('/')
def index():
    prods = Product.query.all()
    
    return render_template('index.html', products=prods)

@app.route('/add', methods=['GET', 'POST'])
def addproduct():
    # if request.method=='POST':
    print('yes here')
    prod = request.form.get('prod')
    description = request.form.get('description')
    price = request.form.get('price')
    file = request.files.get('Picture')
    image = file.read()
    
    newprod = Product(name=prod, description=description, price=price, image=image)
    db.session.add(newprod)
    db.session.commit()
    return render_template('addproduct.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def updateprod(id):
    prod = Product.query.get(id)
    if request.method=='POST':
        product = request.form.get('prod')
        description = request.form.get('description')
        price = request.form.get('price')
        prod.name = product
        prod.description = description
        prod.price = price
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('updateprod.html', prod=prod)

admin = Admin(app, name='My Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(User, db.session))

if __name__ == '__main__':
    app.run(debug=True)