from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    interactions = db.relationship('Interaction', backref='contact', lazy=True)

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(200))
    email_content = db.Column(db.String(200))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))

@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    new_contact = Contact(name=name, email=email, phone=phone)
    db.session.add(new_contact)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit_contact/<int:id>', methods=['POST'])
def edit_contact(id):
    contact = Contact.query.get(id)
    contact.name = request.form.get('name')
    contact.email = request.form.get('email')
    contact.phone = request.form.get('phone')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_contact/<int:id>', methods=['POST'])
def delete_contact(id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_interaction/<int:contact_id>', methods=['POST'])
def add_interaction(contact_id):
    note = request.form.get('note')
    email_content = request.form.get('email_content')
    new_interaction = Interaction(note=note, email_content=email_content, contact_id=contact_id)
    db.session.add(new_interaction)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
