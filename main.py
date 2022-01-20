from flask import Flask, render_template, redirect, request, Response, url_for
app = Flask('app')


import pandas as pd, requests
import json
from openpyxl import load_workbook

@app.route('/')
def index():
  weather_data = weatherobject()
  xlsxd = load_data_file()
  lblchart = load_xlsx['Nombres']
  dchart = load_xlsx['Calificacion']
  context = {
    'weather_data' : weather_data,
    'data' : xlsxd,
    'labelschart': lblchart,
    'datachart': dchart,
  }
  #templates = ['base.html','index.html','data.html']
  return render_template(['index.html','data.html'], **context)

def weatherobject():
  city = 'Hermosillo'
  apikey = '2a3fb1b2218fbfd52ce8ac946fea8c25'
  url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={apikey}'
  response = requests.get(url).json()
  data = []
  weather = {
    'temperature' : convert2celsius(response['main']['temp']),
    'description' : response['weather'][0]['description'],
    'icon' : response['weather'][0]['icon'],
  }
  data.append(weather)
  return data

def convert2celsius(temp):
  res = round(temp - 273.15, 2)
  return res

@app.route("/data", methods=['GET','POST'])
def load_data_file():
  df = load_xlsx()
  data = df.to_html()
  return render_template("data.html",data=data)

def load_xlsx():
  wb = load_workbook(filename="calificaciones.xlsx")
  sh = wb.active
  v = sh.values
  pdf = pd.DataFrame(v)
  return pdf

app.run(host='0.0.0.0', port=8080)