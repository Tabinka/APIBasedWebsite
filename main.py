import random
import requests as requests
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired

URL = "https://the-one-api.dev/v2"
TOKEN = "Bearer token"
HEADERS = {
    'Accept': 'application/json',
    "Authorization": TOKEN
}
SEARCH_BY = ["name", "height", "race", "gender", "chapterName"]
IN_BOOKS = ["chapter", "book"]

app = Flask(__name__)
app.config["SECRET_KEY"] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class SearchForm(FlaskForm):
    search = StringField("What do you want to search for?", validators=[DataRequired()],
                         render_kw={"placeholder": "What are you looking for?"})
    select = RadioField("Choose: ", choices=[("character", "Characters"), ("movie", "Movies"), ("book", "Books")],
                        default='character')


def find_random_quote():
    quote_api_request = requests.get(url=f"{URL}/quote", headers=HEADERS)
    quote_data = quote_api_request.json()['docs'][random.randint(0, len(quote_api_request.json()['docs']))]
    random_quote = quote_data["dialog"]
    character_api_request = requests.get(url=f"{URL}/character?_id={quote_data['character']}",
                                         headers=HEADERS)
    character_name = character_api_request.json()['docs'][0]['name']
    return random_quote, character_name


@app.route("/", methods=["POST", "GET"])
def home():
    global SEARCH_BY, IN_BOOKS
    searched_thing = None
    search_query = None
    form = SearchForm()
    random_quote, character_name = find_random_quote()
    if form.validate_on_submit():
        for search_by in SEARCH_BY:
            search_api_request = requests.get(url=f"{URL}/{form.select.data}?{search_by}=/{form.search.data}/i",
                                                  headers=HEADERS)
            searched_thing = search_api_request.json()['docs']
            if searched_thing:
                break
        search_query = form.search.data
    return render_template("index.html", quote=random_quote, name=character_name, form=form, thing=searched_thing,
                           query=search_query)


if __name__ == '__main__':
    app.run(debug=True)
