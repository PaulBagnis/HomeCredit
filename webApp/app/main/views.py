from flask import (
    render_template,
    session,
    redirect,
    url_for,
    abort,
    flash,
    request,
    current_app,
    make_response)
from app.main import main
import pandas as pd

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        id = request.form['id']

    df = pd.read_csv("C:\\Users\\Paul_\\Desktop\\Projet Machine Learning\\Données\\application_train.csv")
    chart1 = [['Loan Type', 'Yes or No']]
    for row in df[1:].iterrows():
        print(type(row[1]))
        print(row[1])
        #chart1.append([row['NAME_CONTRACT_TYPE'],row['TARGET']])
        
    return render_template('predict.html', id=id, chart1=chart1)

# Page d'accueil avec form avec id
# page avec predict et graphiques