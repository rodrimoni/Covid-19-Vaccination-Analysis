import dash_html_components as html
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash
from dash_extensions.javascript import arrow_function, assign
from dash.dependencies import Output, Input

from ./dataProcessor/core.py import getCityVaccineData

################################################# Testar essa sugestão ##########################################################
import pandas as pd
import geojson

def data2geojson(df):
    features = []
    insert_features = lambda X: features.append(
            geojson.Feature(geometry=geojson.Point((X["long"],
                                                    X["lat"],
                                                    X["elev"])),
                            properties=dict(name=X["name"],
                                            description=X["description"])))
    df.apply(insert_features, axis=1)
    with open('map1.geojson', 'w', encoding='utf8') as fp:
        geojson.dump(geojson.FeatureCollection(features), fp, sort_keys=True, ensure_ascii=False)

col = ['lat','long','elev','name','description']
data = [[-29.9953,-70.5867,760,'A','Place ñ'],
        [-30.1217,-70.4933,1250,'B','Place b'],
        [-30.0953,-70.5008,1185,'C','Place c']]

df = pd.DataFrame(data, columns=col)

data2geojson(df)
################################################# Fim da sugestão ##############################################################


def get_info(feature=None):
    header = [html.H4("US Population Density")]
    if not feature:
        return header + [html.P("Hoover over a state")]
    return header + [html.B(feature["properties"]["name"]), html.Br(),
                     "{:.3f} people / mi".format(feature["properties"]["density"]), html.Sup("2")]


classes = [10, 30, 50, 70, 90]
colorscale = ['#ffffd4','#fed98e','#fe9929','#d95f0e','#993404']
style = dict(weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)
# Create colorbar.
ctg = ["{}+".format(cls, classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{}+".format(classes[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")
# Geojson rendering logic, must be JavaScript as it is executed in clientside.
style_handle = assign("""function(feature, context){
    const {classes, colorscale, style, colorProp} = context.props.hideout;  // get props from hideout
    const value = feature.properties[colorProp];  // get value the determines the color
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            style.fillColor = colorscale[i];  // set the fill color according to the class
        }
    }
    return style;
}""")
# Convert Pandas dataframe to geojson-like.
df =  getCityVaccineData()
dicts = df.to_dict('rows')

#for item in dicts:
#    item["tooltip"] = "{} ({:.1f})".format(item['city'], item[color_prop])  # bind tooltip

geojson = dlx.dicts_to_geojson(dicts, lon="lng")  # convert to geojson
geobuf = dlx.geojson_to_geobuf(geojson)  # convert to geobuf

geojson = dl.GeoJSON(data = geobuf, id="geojson", format = "geobuf",
                     options=dict(style=style_handle),  # how to style each polygon
                     zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                     zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                     hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')),  # style applied on hover
                     hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp="porcent_esquema_vacinal_completo"))
# Create info control.
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})
# Create app.
app = Dash(prevent_initial_callbacks=True)
app.layout = html.Div([dl.Map(children=[dl.TileLayer(), geojson, colorbar, info])],
                      style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, id="map")


@app.callback(Output("info", "children"), [Input("geojson", "hover_feature")])
def info_hover(feature):
    return get_info(feature)


if __name__ == '__main__':
    app.run_server()