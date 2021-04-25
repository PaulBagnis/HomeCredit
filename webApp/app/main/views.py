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
import json

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        id = request.form['id']

    df = pd.read_csv("C:\\Users\\Paul_\\Desktop\\Projet Machine Learning\\Données\\application_train.csv")
    
    user = df.loc[df['SK_ID_CURR'] == int(id)]
    userLoan = user.to_dict()['NAME_CONTRACT_TYPE'][2]

    chart1 = [['Loan Type', 'Paid', 'Didn\'t pay']]
    for row in df[1:].iterrows():
        #print(type(row[1].to_dict()))
        #print(row[1].to_dict())
        tempDict = row[1].to_dict()
        chart1.append([tempDict['TARGET'], tempDict['NAME_CONTRACT_TYPE']])

    # For Chart1    
    cash_r_0, cash_c_0, cash_c_1, cash_r_1 = 0, 0, 0, 0
    for item in chart1[1:]:
        if item[1] == "Cash loans" : 
            if item[0] == 0 :
                cash_c_0 += 1
            else :
                cash_c_1 += 1
        elif item[1] == "Revolving loans" :
            if item[0] == 0 :
                cash_r_0 += 1
            else :
                cash_r_1 += 1
    
    mod_chart = json.dumps({ "array1" : [['Loan Type', 'Yes', 'No'], ['Cash Loans', cash_c_0, cash_c_1], ['Revolving loans', cash_r_0, cash_r_1]] })
    #print(chart1)
    
        
    return render_template('predict.html', id=id, mod_chart=mod_chart, userLoan=userLoan)

# Page d'accueil avec form avec id
# page avec predict et graphiques