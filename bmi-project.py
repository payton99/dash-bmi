from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

app = Dash(__name__)

# Load file into pandas df
df = pd.read_csv("WHO_BMI_DATA.csv")

# Monaco, Sudan (former), Sudan, and South Sudan missing all
# data- no need to keep them
df = df.dropna()

# Convert column names to lowercase
df.columns = df.columns.str.lower()

df["agegroup"] = df["agegroup"].str.replace(" years", "")



#### Building plotly charts

df_regions = df.groupby(["region", "year"])["numeric"].mean().to_frame().reset_index()

region_line = px.line(
    df_regions,
    x = "year",
    y = "numeric",
    color = "region",
    title = "Average BMI by Region"
)

region_line.update_layout(
    plot_bgcolor = "#111111",
    paper_bgcolor = "#111111",
    font_color = '#7FDBFF',
    xaxis = {"showgrid": False}
    # yaxis = {"showgrid": False}
)



strictly_two_sex = df[df["sex"] != "Both sexes"]

sex_hist = px.histogram(
    strictly_two_sex,
    x = "numeric",
    color = "sex",
    barmode = "overlay",
    title = "BMI by Sex"
)

sex_hist.update_layout(
    plot_bgcolor = "#111111",
    paper_bgcolor = "#111111",
    font_color = '#7FDBFF'
)



app.layout = html.Div(style={"backgroundColor": "#111111"},
    children=[
        html.H1("Global BMI Rates 1975-2016", style = {"color": '#7FDBFF'}),

        dcc.Graph(
            figure=region_line            
        ),

        dcc.Graph(
            figure=sex_hist            
        ),
    ]
)

if __name__ == "__main__":
    # print(strictly_two_sex)
    app.run_server(debug = True)