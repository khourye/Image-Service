from flask import Flask, render_template, request, flash
from flask_restful import Resource, Api, reqparse
from astro_sign import get_sign
from ImageService import getImages
import requests
import pyaztro
import datetime
import json
from time import sleep
from process_text import remove_citations


app = Flask(__name__)
api = Api(app)
app.secret_key = 'hifii32ri3nien3434n142n34nr'


# /users
class Users(Resource):

    def get(self):
        return {'message': 'Please submit a POST request to get your images.'}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('api_key', required=True)
        parser.add_argument('keyword', required=True)
        parser.add_argument('num_images', required=True)
        args = parser.parse_args()

        # validate api_key
        if args['api_key'] in ['greenhouse123', 'chickens456']:
            urls = getImages(args['keyword'], args['num_images'])
            return {'urls': urls}, 200
        else:
            return {'error': 'Invalid API key.'}, 400


api.add_resource(Users, '/users')


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/astrological-sign', methods=['GET', 'POST'])
def astrological_sign():
    sign_result = False
    if request.method == 'POST':

        month = request.form['month'].lower()
        day = int(request.form['day'])
        sign_result = get_sign(month, day)

        # invalid day
        if not sign_result[0]:
            flash('Please enter a valid day.')
        else:
            flash('Your astrological sign is ' + sign_result[1])

        return render_template('astro_sign.html')
    else:
        return render_template('astro_sign.html')


@app.route('/sign-info', methods=['GET', 'POST'])
def sign_info():

    sign_titles = {'Virgo': 'Origins',
                   'Leo': 'History',
                   'Aries': 'Background',
                   'Sagittarius': 'Astrology',
                   'Taurus': 'History',
                   'Gemini': 'Mythology',
                   'Cancer': 'Background',
                   'Libra': 'Astrological associations',
                   'Scorpio': 'Associations',
                   'Capricorn': 'Cultural significance',
                   'Aquarius': 'Myth',
                   'Pisces': 'Background'}

    if request.method == 'POST':
        sign = request.form['sign']
        url = "https://en.wikipedia.org/wiki/" + sign + "_(astrology)"

        # write to JSON file
        dict = {"url": url, "title": sign_titles[sign]}
        json_obj = json.dumps(dict)
        try:
            with open("wiki.json", "w") as openfile:
                openfile.write(json_obj)
        finally:
            openfile.close()
        sleep(1.0)

        # read from JSON file
        try:
            with open("wiki.json", "r") as openfile:
                wiki_info = json.load(openfile)
                data = remove_citations(wiki_info["text"])
        finally:
            openfile.close()

        flash(data)
        return render_template('sign_info.html', sign=sign)
    else:
        return render_template('sign_info.html')


@app.route('/daily-horoscope', methods=['GET', 'POST'])
def daily_horoscope():
    if request.method == 'POST':
        today = datetime.datetime.today()
        date = "Today is " + today.strftime("%B") + " " + today.strftime("%d") + ", " + today.strftime("%Y")

        # if user enters sign
        if 'sign' in request.form.keys():
            sign_result = request.form['sign']
            got_result = True

        # if user enters birthday
        if 'month' in request.form.keys() and 'day' in request.form.keys():
            month = request.form['month'].lower()
            day = int(request.form['day'])
            sign_result = get_sign(month, day)[1].lower()

        # collect horoscope information
        horoscope = pyaztro.Aztro(sign=sign_result, day='today')
        description = horoscope.description
        flash(description)
        return render_template('daily_horoscope.html', date=date)
    else:
        return render_template('daily_horoscope.html')


@app.route('/picture-of-the-day', methods=['GET', 'POST'])
def picture():
    response = requests.get("https://api.nasa.gov/planetary/apod?api_key=e6LagY694FsCgiDA4cCTV8eahoLkof5czr9seL8e")
    response_json = json.loads(response.content)
    url = response_json['url']
    title = response_json['title']
    explanation = response_json['explanation']
    return render_template('picture.html', url=url, title=title, explanation=explanation)


@app.route('/daily-horoscope-español', methods=['GET', 'POST'])
def translated():
    if request.method == 'POST':
        today = datetime.datetime.today()
        date = "Today is " + today.strftime("%B") + " " + today.strftime("%d") + ", " + today.strftime("%Y")

        # translate date
        data = {'lg-in': 'EN', 'lg-out': 'ES', 'phrase': date}
        response = requests.post('https://translate-api-cs361.herokuapp.com/translate', data=data)
        date = response.json()['translation']

        # if user enters sign
        if 'sign' in request.form.keys():
            sign_result = request.form['sign']
            got_result = True

        # if user enters birthday
        if 'month' in request.form.keys() and 'day' in request.form.keys():
            month = request.form['month'].lower()
            day = int(request.form['day'])
            sign_result = get_sign(month, day)[1].lower()

        # collect horoscope information
        horoscope = pyaztro.Aztro(sign=sign_result, day='today')
        description = horoscope.description

        # translate description
        data = {'lg-in': 'EN', 'lg-out': 'ES', 'phrase': description}
        response = requests.post('https://translate-api-cs361.herokuapp.com/translate', data=data)
        flash(response.json()['translation'])
        return render_template('daily_horoscope_spanish.html', date=date)
    else:
        return render_template('daily_horoscope_spanish.html')


