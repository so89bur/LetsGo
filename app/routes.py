import os
from flask import render_template, send_file, send_from_directory
from app import app

@app.route('/favicon.png')
def send_favicon():
  return send_file('../static/favicon.png')

@app.route('/img/<path:path>')
def send_img(path):
  return send_from_directory('../static/img', path)

@app.route('/css/<path:path>')
def send_css(path):
  return send_from_directory('../static/css', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
  return send_from_directory('../static/fonts', path)

@app.route('/js/<path:path>')
def send_js(path):
  return send_from_directory('../static/js', path)

@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def index(path):
  return render_template("index.html")
