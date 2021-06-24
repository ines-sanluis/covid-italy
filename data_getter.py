import pandas as pd
from datetime import datetime, timedelta

def getNationalData(data):
    url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-";
    if data == "latest":  url += data;
    else: url += data.strftime("%Y%m%d")
    url += ".csv"
    df = pd.read_csv(url)
    df['data'] = pd.to_datetime(df["data"])
    return df

def addCalculatedData(df):
    df["totale_negativi_test_molecolare"] = df["tamponi_test_molecolare"] - df["totale_positivi_test_molecolare"]
    df["totale_negativi_test_antigenico"] = df["tamponi_test_antigenico_rapido"] - df["totale_positivi_test_antigenico_rapido"]
    df["totale_tamponi"] = df["tamponi_test_molecolare"] + df["tamponi_test_antigenico_rapido"]
    df["totale_positivi_test"] = df["totale_positivi_test_molecolare"] + df["totale_positivi_test_antigenico_rapido"]
    df["totale_negativi_test"] = df["totale_tamponi"] - df["totale_positivi_test"]
    df["perc_positivi_test"] = df["totale_positivi_test"]*100/df["totale_tamponi"]
    df["perc_negativi_test"] = df["totale_negativi_test"]*100/df["totale_tamponi"]
    return df

def getLast24hData(current, previous):
    cols = ["ricoverati_con_sintomi", "terapia_intensiva", "totale_ospedalizzati", "isolamento_domiciliare",
            "totale_positivi", "dimessi_guariti", "deceduti", "totale_casi", "tamponi", "casi_testati"]
    return current[cols] - previous[cols]

def getRegionalData(data):
    url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-";
    if data == "latest":  url += data;
    else: url += data.strftime("%Y%m%d")
    url += ".csv"
    df = pd.read_csv(url)
    df['data'] = pd.to_datetime(df["data"])
    return df

def getPreviousDay(day):
    return day - timedelta(days = 1)
