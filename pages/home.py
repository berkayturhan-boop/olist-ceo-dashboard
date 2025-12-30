import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from olist.seller_updated import Seller

dash.register_page(__name__, path="/", name="Özet (CEO)")

def load_sellers():
    seller = Seller()
    return seller.get_training_data()

def build_kpis(sellers):
    gelir_satis_komisyonu = sellers.sales.sum() * 0.10
    gelir_abonelik = sellers.months_on_olist.sum() * 80
    toplam_gelir = sellers.revenues.sum()

    maliyet_review = sellers.cost_of_reviews.sum()
    it_maliyeti = 500_000  # eğitim varsayımı (notebook ile aynı)

    brut_kar = sellers.profits.sum()
    net_kar = brut_kar - it_maliyeti

    return {
        "gelir_satis_komisyonu": gelir_satis_komisyonu,
        "gelir_abonelik": gelir_abonelik,
        "toplam_gelir": toplam_gelir,
        "maliyet_review": maliyet_review,
        "it_maliyeti": it_maliyeti,
        "brut_kar": brut_kar,
        "net_kar": net_kar,
    }

def tl(value):
    return f"{value:,.0f} BRL"

def kpi_card(title, value, subtitle=""):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="text-muted"),
                html.H3(tl(value)),
                html.Div(subtitle, className="text-muted"),
            ]
        ),
        className="shadow-sm",
    )

def build_waterfall(k):
    fig = go.Figure(
        go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "total", "relative", "total", "relative", "total"],
            x=[
                "Aylık Abonelik",
                "Satış Komisyonu",
                "Toplam Gelir",
                "Review Maliyeti",
                "Brüt Kâr",
                "IT Maliyeti",
                "Net Kâr",
            ],
            y=[
                k["gelir_abonelik"],
                k["gelir_satis_komisyonu"],
                0,
                -k["maliyet_review"],
                0,
                -k["it_maliyeti"],
                0,
            ],
        )
    )
    fig.update_layout(
        title="Gelir–Maliyet Akışı (Waterfall)",
        margin=dict(l=30, r=30, t=60, b=30),
        height=450,
    )
    return fig

sellers_df = load_sellers()
k = build_kpis(sellers_df)
wf_fig = build_waterfall(k)

layout = dbc.Container(
    [
        html.H2("CEO Özeti", className="mt-4"),
        html.P(
            "Amaç: Kârlılığı artırmak için zarar eden satıcıların etkisini hızlıca göstermek.",
            className="text-muted",
        ),
        dbc.Row(
            [
                dbc.Col(kpi_card("Toplam Gelir", k["toplam_gelir"], "Abonelik + Komisyon"), md=3),
                dbc.Col(kpi_card("Review Maliyeti", k["maliyet_review"], "Operasyon maliyeti"), md=3),
                dbc.Col(kpi_card("IT Maliyeti (varsayım)", k["it_maliyeti"], "Eğitim senaryosu"), md=3),
                dbc.Col(kpi_card("Net Kâr", k["net_kar"], "Brüt Kâr - IT"), md=3),
            ],
            className="g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Gelir–Maliyet Özet Grafiği", className="mb-2"),
                                dcc.Graph(figure=wf_fig),
                            ]
                        ),
                        className="shadow-sm mt-3",
                    ),
                    md=12,
                )
            ]
        ),
        dbc.Alert(
            [
                html.B("Sunum mesajı: "),
                "Her satıcı değer yaratmıyor. Zarar eden satıcılar çıkarıldığında net kâr artabiliyor.",
            ],
            color="info",
            className="mt-3",
        ),
    ],
    fluid=True,
)
