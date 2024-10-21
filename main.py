from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    choices_1 = [('☕', '☕'), ('☕☕', '☕☕'), ('☕☕☕', '☕☕☕'), ('☕☕☕☕', '☕☕☕☕'), ('☕☕☕☕☕', '☕☕☕☕☕')]
    choices_2 = [('✘', '✘'), ('💪🏾', '💪🏾'), ('💪🏾💪🏾', '💪🏾💪🏾'), ('💪🏾💪🏾💪🏾', '💪🏾💪🏾💪🏾'), ('💪🏾💪🏾💪🏾💪🏾', '💪🏾💪🏾💪🏾💪🏾'), ('💪🏾💪🏾💪🏾💪🏾💪🏾', '💪🏾💪🏾💪🏾💪🏾💪🏾')]
    choices_3 = [('✘', '✘'), ('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'), ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')]
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Map', validators=[DataRequired(), URL(require_tld=False, message="Invalid URL")])
    opening_time = StringField('Opening Time e.g. 6AM', validators=[DataRequired()])
    closing_time = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=choices_1, coerce=str, validators=[DataRequired()])
    wifi = SelectField('Wifi Strength Rating', choices=choices_2, coerce=str, validators=[DataRequired()])
    power = SelectField('Power Socket Availability', choices=choices_3, coerce=str,  validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", "a", encoding='utf-8') as f:
            f.write(f"\n{form.cafe.data},{form.location.data},{form.opening_time.data},{form.closing_time.data},{form.coffee_rating.data},{form.wifi.data},{form.power.data}")
        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
