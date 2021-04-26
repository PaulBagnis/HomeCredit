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
import numpy as np
import json
import time
import math

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/predict', methods=['GET', 'POST'])
def predict():
    start_time = time.time()
    if request.method == 'POST':
        id = request.form['id']

    print("##########################   START   ##########################")
    print(time.time() - start_time, "seconds")

    df_train = pd.read_csv("C:\\Users\\Paul_\\Desktop\\Projet Machine Learning\\Données\\application_train.csv")
    df_test = pd.read_pickle("C:\\Users\\Paul_\\Desktop\\Projet Machine Learning\\Données\\my_test.pickle")
    print(df_test)
    # Récupération des predicts
    test_id =  df_test['ID'].tolist()
    test_target =  df_test['TARGET'].tolist()
    test_proba =  df_test['PROBA'].tolist()
    print(type(test_id[0]))
    print(type(id))
    list_test = []
    for idx in range(len(test_id)) :
        if test_id[idx] == int(id) :
            list_test.append(test_id[idx])
            list_test.append(test_target[idx])
            list_test.append(test_proba[idx])
    list_test[2][0] = list_test[2][0] * 100
    list_test[2][1] = list_test[2][1] * 100

    print("##########################   CSV OPENED   ##########################")
    print(time.time() - start_time, "seconds")

    # On récupère le row correspondant à l'ID
    prospect = df_train.loc[df_train['SK_ID_CURR'] == int(id)]
    
    # On récupère les valeurs nécessaires à la réalisation des différents graphiques en itérant sur le pickle
    chart1, chart2, chart3, chart4 = [], [], [], []

    col_target = df_train['TARGET'].tolist()
    col_contract = df_train['NAME_CONTRACT_TYPE'].tolist()
    col_ext2 = df_train['EXT_SOURCE_2'].tolist()
    col_ext3 = df_train['EXT_SOURCE_3'].tolist()
    col_db = df_train['DAYS_BIRTH'].tolist()
    col_amtCred = df_train['AMT_CREDIT'].tolist()

    for idx in range(len(col_target)) :
        chart1.append([col_target[idx], col_contract[idx]])
        chart2.append([col_ext2[idx], col_ext3[idx]])
        chart3.append([col_target[idx], abs(col_db[idx])])
        chart4.append([col_target[idx], col_amtCred[idx]])

    print("##########################   GET COLUMNS DONE   ##########################")
    print(time.time() - start_time, "seconds")

    # CHART SUR LES TYPES DE PRÊTS
    # On récupère le type de prêt que fait le prospect testé
    prospectLoan = list(prospect.to_dict()['NAME_CONTRACT_TYPE'].values())[0]

    # On récupère le nombre de prêts remboursés ou non en fonction du type de prêt
    cash_r_0, cash_c_0, cash_c_1, cash_r_1 = 0, 0, 0, 0
    for item in chart1:
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
    
    # On crée le json qui va être envoyé au javascript via Jinja
    mod_chart1 = json.dumps({ "array1" : [['Loan Type', 'Paid', 'Didn\'t pay'], ['Cash Loans', cash_c_0, cash_c_1], ['Revolving loans', cash_r_0, cash_r_1]] })
    
    # CHART SUR LES EXT_SOURCES
    # On récupère les valeurs du prospect
    prospectExt2 = list(prospect.to_dict()['EXT_SOURCE_2'].values())[0]
    prospectExt3 = list(prospect.to_dict()['EXT_SOURCE_3'].values())[0]

    # On calcule les valeurs moyennes pour EXT_SOURCE_2 et EXT_SOURCE_3
    meanExt2, meanExt3 = 0, 0
    chart2Ext2, chart3Ext3 = [], []
    for item in chart2:
        if item[0] :
            chart2Ext2.append(item[0])
        if item[1] :
            chart3Ext3.append(item[1])
    
    meanExt2 = np.nanmean(chart2Ext2)
    meanExt3 = np.nanmean(chart3Ext3)

    # On crée le json qui va être envoyé au javascript via Jinja en fonction des données que l'on as sur le prospect
    if not math.isnan(prospectExt2) and not math.isnan(prospectExt3) :
        mod_chart2 = json.dumps({ "array1" : [['Ext Source', 'Prospect Score', 'Average Score'], ['Ext Source 2', prospectExt2, meanExt2], ['Ext Source 3', prospectExt3, meanExt3]]})
    elif not math.isnan(prospectExt3) and math.isnan(prospectExt2) :
        mod_chart2 = json.dumps({ "array1" : [['Ext Source', 'Prospect Score', 'Average Score'], ['Ext Source 3', prospectExt3, meanExt3]]})
    else :
        mod_chart2 = json.dumps({ "array1" : [['Ext Source', 'Prospect Score', 'Average Score'], ['Ext Source 2', prospectExt2, meanExt2]]})
    
    # CHART SUR DAYS_BIRTH
    # On récupère le nombre de jours vécus du prospect
    prospectDB = abs(list(prospect.to_dict()['DAYS_BIRTH'].values())[0])
    
    # Moyennes des jours vécus des clients du csv
    ages0, ages1 = [], []
    for item in chart3:
        if item[0] == 0 :
            ages0.append(item[1])
        else :
            ages1.append(item[1])

    meanDb0 = np.nanmean(ages0)
    meanDb1 = np.nanmean(ages1)
    
    # On crée le json qui va être envoyé au javascript via Jinja
    mod_chart3 = json.dumps({ "array1" : [['Days Lived', 'Average of payeurs', 'Average of bad payeurs', 'Prospect'], [' ', meanDb0, meanDb1, prospectDB]]})

    # CHART ON AMT_CREDIT
    # On récupère le montant du prêt du prospect
    prospectCT = list(prospect.to_dict()['AMT_CREDIT'].values())[0]
    
    # On récupère la médiane des montants de prêts
    cT0, cT1 = [], []
    for item in chart4:
        if item[0] == 0 :
            cT0.append(item[1])
        else :
            cT1.append(item[1])

    meanCt0 = np.median(cT0)
    meanCt1 = np.median(cT1)

    # On crée le json qui va être envoyé au javascript via Jinja
    mod_chart4 = json.dumps({ "array1" : [['Credit Amount', 'Average of payeurs', 'Average of bad payeurs', 'Prospect'], [' ', meanCt0, meanCt1, prospectCT]]})

    print("##########################   ALL MOD CHARTS   ##########################")
    print(time.time() - start_time, "seconds")

    return render_template('predict.html', id=id, mod_chart1=mod_chart1, prospectLoan=prospectLoan, mod_chart2=mod_chart2, mod_chart3=mod_chart3, mod_chart4=mod_chart4, list_test=list_test)
