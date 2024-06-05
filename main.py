from datetime import datetime
from flask import Flask, render_template
from flask import redirect
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipe.db"

db = SQLAlchemy(app)


all_recipes = [
    {"title": "Recipe 1", "description": "Some Ingredients for Recipe 1", "Author": "Kes"},
    {"title": "Recipe 2", "description": "Some Ingredients for Recipe 2"}
]


class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Recipe" + str(self.id)


@app.route("/recipes/")
def recipes():
    all_recipes = Recipe.query.all()
    return render_template("recipes.html", recipes=all_recipes)


@app.route("/recipes/delete/<int:id>/")
def delete(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect("/recipes")


@app.route("/recipes/edit/<int:id>/", methods=["GET", "POST"])
def edit(id):
    recipe = Recipe.query.get_or_404(id)
    if request.method == "POST":
        recipe_title = request.form['title']
        recipe_description = request.form['description']
        db.session.commit()
        return redirect("/recipes")
    else:
        return render_template("edit.html", recipe=recipe)


@app.route("/recipes/new/", methods=['GET', 'POST'])
def new_recipe():
    if request.method == "POST":
        recipe_title = reqest.form["title"]
        recipe_description = request.form["description"]
        recipe = Recipe(title=recipe_title, description=recipe_description, author="Kes")
        db.session.add(recipe)
        db.session.commit()
        return redirect("/recipes")
    else:
        return render_template("new_recipes.html")


@app.route("/home/")
def home():
    num_recipes = Recipe.query.count()
    return render_template("index.html", num_recipes=num_recipes)


@app.route("/hello/<string:name>")
def hello(name):
    return f"Hello, {name}!"


if __name__ == "__main__":
    app.run(debug=True)
