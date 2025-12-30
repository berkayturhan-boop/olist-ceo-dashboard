# pages/logit_insights.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np

dash.register_page(__name__, path="/logit-insights", name="Logit İçgörüleri")

# Notebook'tan alınan katsayılar (standardize edilmiş feature'lar için)
COEFS_ONE = {
    "wait_time": 0.6907,
    "delay_vs_expected": 0.2626,
    "number_of_sellers": 0.2295,
    "distance_seller_customer": -0.2193,
    "price": 0.0407,
    "freight_value": 0.1090,
}
COEFS_FIVE = {
    "wait_time": -0.5140,
    "delay_vs_expected": -0.4366,
    "number_of_sellers": -0.1716,
    "distance_seller_customer": 0.1075,
    "price": 0.0268,
    "freight_value": -0.0624,
}

df = pd.DataFrame({
    "feature": list(COEFS_ONE.keys()),
    "1★ katsayı": [COEFS_ONE[k] for k in COEFS_ONE],
    "5★ katsayı": [COEFS_FIVE[k] for k in COEFS_ONE],
})
df_m = df.melt(id_vars="feature", var_name="model", value_name="coef")
df_m["abs_coef"] = df_m["coef"].abs()

fig = px.bar(
    df_m.sort_values("abs_coef", ascending=True),
    x="coef",
    y="feature",
    color="model",
    orientation="h",
    title="Memnuniyet Sürücüleri (Logit Katsayıları, standardize)",
)

layout = dbc.Container(
    [
        html.H2("Logit İçgörüleri (Sipariş Memnuniyeti)", className="mt-4"),
        html.P(
            "1★ ve 5★ ihtimalini etkileyen faktörleri, model katsayıları üzerinden özetler.",
            className="text-muted",
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.Div("En güçlü negatif etki (5★)", className="text-muted"),
                    html.H4("wait_time / delay_vs_expected"),
                    html.Div("Bekleme ve gecikme uzadıkça 5★ olasılığı düşer.", className="text-muted"),
                ]), className="shadow-sm"), md=6),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.Div("En güçlü risk (1★)", className="text-muted"),
                    html.H4("wait_time"),
                    html.Div("Bekleme uzadıkça 1★ olasılığı artar.", className="text-muted"),
                ]), className="shadow-sm"), md=6),
            ],
            className="g-3",
        ),
        dbc.Card(dbc.CardBody([dcc.Graph(figure=fig)]), className="shadow-sm mt-3"),
        dbc.Alert(
            [
                html.B("Önerilen aksiyonlar: "),
                "Teslimat süresini düşürmek (SLA), gecikmeyi azaltmak (operasyon), çok satıcılı siparişleri optimize etmek.",
            ],
            color="info",
            className="mt-3",
        ),
    ],
    fluid=True,
)
