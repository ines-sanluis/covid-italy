import pandas as pd

# They were both assigned code 4 but the other site uses 21 and 22
def fixTrentinoIstatCodes(df):
    df.at[df["nome_area"].str.contains("Bolzano"), "codice_regione_ISTAT"] = 21
    df.at[df["nome_area"].str.contains("Trento"), "codice_regione_ISTAT"] = 22
    return df

def getVaccinesData():
    urlVaccines = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.csv"
    dfVaccines = pd.read_csv(urlVaccines)
    dfVaccines = fixTrentinoIstatCodes(dfVaccines)
    wantedColumns = ["nome_area", "codice_regione_ISTAT", "dosi_somministrate", "dosi_consegnate", "percentuale_somministrazione"]
    dfVaccines = dfVaccines[wantedColumns]
    return dfVaccines

def addVaccinesData(dfRegional, dfNational):
    dfVaccines = getVaccinesData()
    # Populate regional
    dfRegional = dfRegional.merge(dfVaccines, how='left', left_on='codice_regione', right_on='codice_regione_ISTAT')
    dfRegional["dosi_disponibili"] = dfRegional["dosi_consegnate"] - dfRegional["dosi_somministrate"]
    # Populate national
    dfNational["dosi_somministrate"] = sum(dfRegional["dosi_somministrate"])
    dfNational["dosi_consegnate"] = sum(dfRegional["dosi_consegnate"])
    dfNational["percentuale_somministrazione"] = dfNational["dosi_somministrate"] / dfNational["dosi_consegnate"] * 100
    dfNational["dosi_disponibili"] = dfNational["dosi_consegnate"] - dfNational["dosi_somministrate"]
    return dfRegional, dfNational
