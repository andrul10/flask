from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.id} - {self.email}"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # print(f"Email: {email}, Password: {password}")
        
        emp = Employee(email=email, password=password)
        db.session.add(emp)
        db.session.commit()
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        emp = Employee.query.filter_by(id=id).first()
        emp.email = email
        emp.password = password
        db.session.commit()
        return redirect('/')
    emp = Employee.query.filter_by(id=id).first()   
    return render_template('edit.html', emp=emp)

@app.route('/delete/<int:id>')
def delete(id):
    emp = Employee.query.filter_by(id=id).first()
    db.session.delete(emp)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
