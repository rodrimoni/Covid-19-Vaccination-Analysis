import dash_leaflet as dl
import dash_leaflet.express as dlx
import jsbeautifier
import json
from dash import Dash
from dash import html
from dash_extensions.javascript import arrow_function, assign
from dash.dependencies import Output, Input
from dataProcessor import getCityVaccineData

geojson = json.loads(getCityVaccineData())

# Create javascript function that filters out all cities but Aarhus.
# Create example app.
app = Dash()
app.layout = html.Div([
    dl.Map(children=[
        dl.TileLayer(),
        dl.GeoJSON(data=geojson, id="geojson")
    ], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, id="map"),
])

if __name__ == '__main__':
    app.run_server()