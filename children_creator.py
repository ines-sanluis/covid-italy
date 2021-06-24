import pandas as pd
import dash_html_components as html

def getNumberToPrint(number):
    return '{:,}'.format(round(number))

def getNationalValue(df, colname):
    return df.iloc[0, df.columns.get_loc(colname)]

def getRegionalValue(df, colname, region):
    return df.loc[df["codice_regione"] == region, colname].item()

def getValueToPrint(df, colname, region=""):
    if region == "":
        value = getNationalValue(df, colname)
    else:
        value = getRegionalValue(df, colname, region)
    return getNumberToPrint(value)

def getPositiveChildren(df, region=""):
    positivi = getValueToPrint(df, "totale_positivi", region)
    terapia = getValueToPrint(df, "terapia_intensiva", region)
    sintomi = getValueToPrint(df, "ricoverati_con_sintomi", region)
    isolamento = getValueToPrint(df, "isolamento_domiciliare", region)
    return html.H1(positivi+' positivi'), html.Div(
        className = "row",
        children = [
            html.Div( className = "col-sm-4 rounded", children = [ html.H4(terapia+' terapia intensiva'), ] ),
            html.Div( className = "col-sm-4 rounded", children = [ html.H4(sintomi+' ricoverati con sintomi') ] ),
            html.Div( className = "col-sm-4 rounded", children = [ html.H4(isolamento+' isolamento') ] )
        ]
    )
def getTotalChildren(df, region=""):
    casi = getValueToPrint(df, "totale_casi", region)
    positivi = getValueToPrint(df, "totale_positivi", region)
    guariti = getValueToPrint(df, "dimessi_guariti", region)
    deceduti = getValueToPrint(df, "deceduti", region)
    return html.H1(casi+' casi' ), html.Div(
        className = "row",
        children = [
            html.Div( className = "col-sm-4 rounded", children = [ html.H4(positivi+' positivi'), ] ),
            html.Div( className = "col-sm-4 rounded", children = [ html.H4(guariti+' guariti') ] ),
            html.Div( className = "col-sm-4 rounded", children = [ html.H4(deceduti+' deceduti') ] )
        ]
    )
def getVaccinesChildren(df, region=""):
    somministrate = getValueToPrint(df, "dosi_somministrate", region)
    consegnate = getValueToPrint(df, "dosi_consegnate", region)
    percentuale = getValueToPrint(df, "percentuale_somministrazione", region)
    disponibili = getValueToPrint(df, "dosi_disponibili", region)
    return html.H1(somministrate+' vaccini' ), html.Div(
        className = "row",
        children = [
            html.Div( className = "col-sm-4 rounded", children = [ html.H4(consegnate+' consegnate') ] ),
            html.Div( className = "col-sm-4 rounded", children = [ html.H4(somministrate+' somministrate'), ] ),
            html.Div( className = "col-sm-4 rounded", children = [ html.H4(disponibili+' disponibili') ] )
        ]
    )
