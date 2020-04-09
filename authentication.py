from flask import Flask, request
from flask_api import status
import requests, lxml.html
from scrapy.http import TextResponse

app = Flask(__name__)
saved_session = None

@app.route('/login', methods=['POST'])
def hello_world():
    if not request.json or not 'email' in request.json or not 'password' in request.json:
        return "Back to the mines", status.HTTP_400_BAD_REQUEST
    session = requests.session()
    login = session.get('https://www.saltybet.com/authenticate?signin=1')
    login_html = lxml.html.fromstring(login.text)
    hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
    form['email'] = request.json['email']
    form['pword'] = request.json['password']
    response = session.post('https://www.saltybet.com/authenticate?signin=1', data=form)
    if response.url == 'https://www.saltybet.com/':
        global saved_session
        saved_session = session
        return "real", status.HTTP_201_CREATED
    else:
        return "fake", status.HTTP_403_FORBIDDEN

@app.route('/get_match', methods=['GET'])
def get_red_name():
    global saved_session
    response = saved_session.get('https://www.saltybet.com/')
    response = TextResponse(body=response.content, url='https://www.saltybet.com/')
    print(response.css('[id="sbettors1"]::text').extract())
    return"test"

def match_status():
    return "test"

if __name__ == '__main__':
    app.run()
