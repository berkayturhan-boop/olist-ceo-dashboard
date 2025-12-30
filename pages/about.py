# pages/about.py
import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/about", name="Hakkında")

layout = dbc.Container(
    [
        html.H2("Hakkında", className="mt-4"),
        html.P(
            "Bu dashboard, Olist verisi üzerinde satıcı bazlı kârlılığı analiz ederek "
            "zarar eden satıcıların çıkarılması durumunda kârın nasıl değiştiğini göstermeyi amaçlar.",
            className="text-muted",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Varsayımlar"),
                    html.Ul(
                        [
                            html.Li("Gelir = %10 satış komisyonu + 80 BRL/ay abonelik."),
                            html.Li("Review maliyeti: 1★=100, 2★=50, 3★=40, 4★/5★=0."),
                            html.Li("IT maliyeti: dinamik (alpha*sqrt(satıcı) + beta*sqrt(adet))."),
                        ]
                    ),
                ]
            ),
            className="shadow-sm",
        ),
    ],
    fluid=True,
)
