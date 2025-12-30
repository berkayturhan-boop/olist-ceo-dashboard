import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/hakkinda", name="Hakkında")

layout = dbc.Container(
    [
        html.H2("Bu dashboard ne söylüyor?", className="mt-4"),
        html.Ul(
            [
                html.Li("Her satıcı platforma değer katmıyor; bazıları net kârı düşürüyor."),
                html.Li("En kötü satıcıları belirli bir noktaya kadar çıkarmak net kârı artırabiliyor."),
                html.Li("IT maliyeti dahil edildiğinde optimum satıcı sayısı değişebiliyor."),
            ]
        ),
        dbc.Alert(
            "Sunumda hedef: kod anlatmak değil, bu çıkarımlar üzerinden aksiyon önermek.",
            color="info",
        ),
    ],
    fluid=True,
)
