from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, DateField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "include_a_strong_secret_key"
app.config["MONGO_URI"] = "mongodb+srv://amaga016:LAkoSCU5JW6RdYcp@cluster0.h4apwqt.mongodb.net/db?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)


class Expenses(FlaskForm):
    description = StringField("Description", validators=[DataRequired()])
    category = SelectField("Category", choices=[("electricity", "Electricity"), ("gas", "Gas"), ("water", "Water"),
                                                ("internet", "Internet"), ("insurance", "Insurance"),
                                                ("restaurant", "Restaurant"), ("groceries", "groceries"),
                                                ("college", "College"), ("party", "Party"), ("other", "Other")])
    cost = DecimalField("Cost", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])


def get_total_expenses(category):
    category_expense = mongo.db.expenses.find({"category": category})
    total_category_expense = 0

    # Iterate over each document in the category
    for expense in category_expense:
        # Check if the 'cost' key exists in the expense document
        if 'cost' in expense:
            # Convert the cost to float and add it to total_category_expense
            total_category_expense += float(expense["cost"])

    return total_category_expense


@app.route('/')
def index():

    my_expenses = mongo.db.expenses.find()  # since there's no  query(filter)
                                            # it's going to find(or get) all of the database
    total_cost = 0
    for i in my_expenses:
        total_cost += float(i["cost"])
    expensesByCategory = [
        ("electricity", get_total_expenses("electricity")),
        ("gas", get_total_expenses("gas")),
        ("water", get_total_expenses("water")),
        ("internet", get_total_expenses("internet")),
        ("insurance", get_total_expenses("insurance")),
        ("restaurant", get_total_expenses("restaurant")),
        ("groceries", get_total_expenses("groceries")),
        ("college", get_total_expenses("college")),
        ("party", get_total_expenses("party")),
        ("other", get_total_expenses("other"))
    ]
    return render_template("index.html", expenses=total_cost, expensesByCategory=expensesByCategory)


@app.route('/addExpenses', methods=["GET", "POST"])
def addExpenses():
    expensesForm = Expenses(request.form)
    if request.method == "POST":
        # Encapsulating all of the user input into the variables
        description_selected = expensesForm.description.data
        category_selected = expensesForm.category.data
        cost_selected = float(expensesForm.cost.data)
        date_selected = expensesForm.date.data.strftime("%Y-%m-%d")
        # inserting the data into the mongodb application
        mongo.db.expenses.insert_one({
            "description": description_selected,
            "category": category_selected,
            "cost": cost_selected,
            "date": date_selected
        })
        return render_template('expensesAdded.html', description_selected=description_selected,
                               category_selected=category_selected, cost_selected=cost_selected,
                               date_selected=date_selected)
    return render_template("addExpenses.html", form=expensesForm)


if __name__ == '__main__':
    app.run(port=5050, debug=True)
