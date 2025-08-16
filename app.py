from flask import Flask, render_template
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

@app.route('/')
def home():
    emp = Employee(email="andrul@gmail.com", password="123456")
    db.session.add(emp)
    db.session.commit()
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True)
