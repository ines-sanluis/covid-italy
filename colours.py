import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

def populateColorColumn(df):
    df['color'] = 'none'

    # Government site where zone colours are updated
    urlRegionColours = "http://www.salute.gov.it/portale/nuovocoronavirus/dettaglioContenutiNuovoCoronavirus.jsp?area=nuovoCoronavirus&id=5351&lingua=italiano&menu=vuoto"
    r = requests.get(urlRegionColours)

    # Colours used in the gov site for zones
    redColour = "#dd222a"
    orangeColour = "#e78314"
    yellowColour = "#f8c300"
    whiteColour = "#f7f7f7"

    # Create soup
    soup = BeautifulSoup(r.text, 'lxml')

    # Zones are in divs with class col-md-3
    divs = soup.find_all("div", class_="col-md-3")
    for div in divs: #one div for each colour
        children = div.findChildren("div", recursive=False)
        style = children[0]["style"]
        regions = children[1].get_text("|")
        regions = regions.replace("PA", "P.A.").replace("Aosta", "d'Aosta").replace("a R", "a-R") #separated by |
        regions = regions.split("|")
        colour = re.search('background-color:#......;', style).group(0)
        if redColour in colour:
            colour = "Zona rossa"
        elif orangeColour in colour:
            colour = "Zona arancione"
        elif yellowColour in colour:
            colour = "Zona gialla"
        elif whiteColour in colour:
            colour = "Zona bianca"
        df.loc[df['denominazione_regione'].isin(regions), "color"] = colour

    return df

#urlData = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-latest.csv"
#df = pd.read_csv(urlData)
