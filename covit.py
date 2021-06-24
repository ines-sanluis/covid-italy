import pandas as pd
from datetime import date, timedelta, datetime
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def loadData():
    today = date.today().strftime("%Y%m%d")
    yesterday = (datetime.now() - timedelta(1)).strftime("%Y%m%d")
    print(today)
    url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-latest.csv"
    return pd.read_csv(url)

def main():
    # Load data
    df = loadData()
    print(df.columns)
    df = addCalculatedData(df)
    print(df["totale_tamponi"])

def addCalculatedData(df):
    df["totale_negativi_test_molecolare"] = df["tamponi_test_molecolare"] - df["totale_positivi_test_molecolare"]
    df["totale_negativi_test_antigenico"] = df["tamponi_test_antigenico_rapido"] - df["totale_positivi_test_antigenico_rapido"]
    df["totale_tamponi"] = df["tamponi_test_molecolare"] + df["tamponi_test_antigenico_rapido"]
    df["totale_positivi_test"] = df["totale_positivi_test_molecolare"] + df["totale_positivi_test_antigenico_rapido"]
    df["totale_negativi_test"] = df["totale_tamponi"] - df["totale_positivi_test"]
    df["perc_positivi_test"] = df["totale_positivi_test"]*100/df["totale_tamponi"]
    df["perc_negativi_test"] = df["totale_negativi_test"]*100/df["totale_tamponi"]
    return df
def showHospitalIncrement(df):
    fig, ax = plt.subplots()
    colormat = np.where(df['totale_ospedalizzati'] > 0, '#F97068','#28965A')
    ax.bar(df.index, df['totale_ospedalizzati'], color=colormat)
    ax.set_xticklabels(df.index, rotation=90)
    ax.set_ylabel("Incremento nel totale di ospedalizzati")
    plt.show()

def showIsolatingIncrement(df):
    fig, ax = plt.subplots()
    colormat = np.where(df['isolamento_domiciliare'] > 0, 'r','g')
    ax.bar(df.index, df['isolamento_domiciliare'], color=colormat)
    ax.set_xticklabels(df.index, rotation=90)
    ax.set_ylabel("Incremento nel totale in isolamento domiciliare")
    plt.show()

def showTotalPositiveIncrement(df):
    fig, ax = plt.subplots()
    colormat = np.where(df['totale_positivi'] > 0, 'r','g')
    ax.bar(df.index, df['totale_positivi'], color=colormat)
    ax.set_xticklabels(df.index, rotation=90)
    ax.set_ylabel("Incremento nel totale di positivi")
    plt.show()


main()
