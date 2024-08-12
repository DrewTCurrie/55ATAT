from flask_bootstrap import Boostrap5
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os

from flask_cors import CORS, cross_origin

import random, secrets


app = Flask(__name__)
CORS(app)

app.secret_key = 'u*^,.-$S(Cc,`[i:r}3ILA^JgImqGY)BJFaDg{e^DAd!rinjjqlsI05YMGuO'
app.config['TEMPLATES_AUTO_RELOAD'] = True
foo = secrets.token_urlsafe(16)


bootstrap = Bootstrap5(app)


@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run()

