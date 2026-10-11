from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)

with app.app_context():
	db.create_all()

#Read + Create
@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		db.session.add(Product(name=request.form["name"]))
		db.session.commit()
		return redirect(url_for("index"))
	return render_template("index.html", products=Product.query.all())

#Update
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
	product = db.get_or_404(Product, id)
	product.name = request.form["name"]
	db.session.commit()
	return redirect(url_for("index"))

#Delete
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
	db.session.delete(db.get_or_404(Product, id))
	db.session.commit()
	return redirect(url_for("index"))

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
