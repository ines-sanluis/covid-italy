# Import libraries and read data
from urllib.request import urlopen
import pandas as pd
import plotly.express as px
import json
from colours import *

# Drop useless colums
def getMapFigure():
    urlRegions = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"
    with urlopen(urlRegions) as response:
        regions = json.load(response)

    # Read Data
    urlData = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-latest.csv"
    df = pd.read_csv(urlData)
    df = populateColorColumn(df)

    wantedColumns = ['codice_regione', 'totale_casi', 'color']
    df = df[wantedColumns]
    # Columns manipulation
    df = df.rename(columns={'codice_regione': 'Region'})
    df = df.rename(columns={'totale_casi': 'Totale Casi'})
    df = df.rename(columns={'color': 'Colore zona'})
    # Create figure
    color_discrete_map = {'Zona rossa':'red', 'Zona arancione':'orange','Zona gialla':'yellow', 'Zona bianca':'white'}
    fig = px.choropleth(
        df,
        geojson=urlRegions,
        locations='Region',
        color="Colore zona",
        color_discrete_map=color_discrete_map,
        featureidkey='properties.reg_istat_code_num',
        hover_data={"Region":False, "Colore zona":False, "Totale Casi":True}
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor= 'rgba(0,0,0,0)', projection_scale=0.5),
        dragmode=False
    )
    fig.update_traces(showlegend=False)
    fig.update_geos(fitbounds="locations", visible=False)
    return fig
