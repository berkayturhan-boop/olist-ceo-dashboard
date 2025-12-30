# pages/seller_impact.py
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from olist.seller_updated import Seller

dash.register_page(__name__, path="/seller-impact", name="Satıcı Çıkarma Etkisi")

ALPHA, BETA = 3157.27, 978.23


def fmt_money(x: float) -> str:
    return f"{x:,.0f} BRL"


def cost_of_it(df_cum: pd.DataFrame, alpha: float = ALPHA, beta: float = BETA) -> pd.Series:
    """
    df_cum: cumsum sonrası kolonlar:
      - n_sellers (kümülatif satıcı sayısı)
      - quantity  (kümülatif ürün/adet)
    Pozitif IT maliyeti döndürür.
    """
    return alpha * (df_cum["n_sellers"] ** 0.5) + beta * (df_cum["quantity"] ** 0.5)


def prepare_metrics() -> pd.DataFrame:
    sellers = Seller().get_training_data()

    metrics = sellers[["seller_id", "revenues", "cost_of_reviews", "profits", "quantity"]].copy()

    # "En kötü satıcı"yı tanımlamak için IT dahil kâra göre sıralayacağız.
    # Bunun için satıcı bazında "yaklaşık" IT payı yerine kümülatif senaryo kullanacağız.
    # Sıralama burada profits (IT hariç) ile başlar: en düşük kâr = en kötü.
    metrics = metrics.sort_values("profits", ascending=False).reset_index(drop=True)
    return metrics


metrics_ordered = prepare_metrics()
MAX_REMOVE = len(metrics_ordered)


layout = dbc.Container(
    [
        html.H2("Satıcı Çıkarma Etkisi", className="mt-4"),
        html.P(
            "Slider ile en düşük performanslı satıcıları (zarar edenleri) çıkardığınızda toplam kârın nasıl değiştiğini görürsünüz.",
            className="text-muted",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Kaç satıcıyı çıkaralım? (En kötüden başlayarak)", className="mb-2"),
                    dcc.Slider(
                        id="remove_n",
                        min=0,
                        max=MAX_REMOVE,
                        step=1,
                        value=0,
                        tooltip={"placement": "bottom", "always_visible": False},
                    ),
                    html.Div(id="remove_summary", className="text-muted mt-2"),
                ]
            ),
            className="shadow-sm",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(id="profit_curve"),
                            ]
                        ),
                        className="shadow-sm mt-3",
                    ),
                    md=8,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(id="impact_barh"),
                            ]
                        ),
                        className="shadow-sm mt-3",
                    ),
                    md=4,
                ),
            ],
            className="g-3",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.B("Nasıl okunur? "),
                    "Solda tutulan satıcı sayısına göre kârın nasıl değiştiği, sağda seçilen senaryonun gelir–maliyet–net kâr özeti yer alır.",
                ]
            ),
            className="shadow-sm mt-3",
        ),
    ],
    fluid=True,
)


@dash.callback(
    Output("remove_summary", "children"),
    Output("profit_curve", "figure"),
    Output("impact_barh", "figure"),
    Input("remove_n", "value"),
)
def update_impact(remove_n: int):
    # Slider=0 -> tüm satıcılar kalır (Home ile aynı olmalı)
    kept = metrics_ordered.iloc[: len(metrics_ordered) - remove_n].copy()

    if len(kept) == 0:
        empty_fig = go.Figure()
        empty_fig.update_layout(height=450, margin=dict(l=20, r=20, t=60, b=30))
        return "Tüm satıcılar çıkarıldı.", empty_fig, empty_fig

    # Kümülatif hesap
    cum = kept[["revenues", "cost_of_reviews", "profits", "quantity"]].copy()
    cum["n_sellers"] = 1  # <-- kritik: kümülatifte 1,2,3... artsın
    cum = cum.cumsum()

    it_costs = cost_of_it(cum)
    cum["it_costs"] = -it_costs  # grafikte maliyet negatif dursun
    cum["profits_after_it"] = cum["profits"] + cum["it_costs"]

    profit_no_it = float(cum["profits"].iloc[-1])
    profit_after_it = float(cum["profits_after_it"].iloc[-1])

    summary = (
        f"Çıkarılan: {remove_n} | Kalan: {len(kept)} | "
        f"Kâr (IT hariç): {fmt_money(profit_no_it)} | "
        f"Kâr (IT dahil): {fmt_money(profit_after_it)}"
    )

    # --- Sol grafik: kâr eğrisi (IT hariç & IT dahil)
    fig_curve = go.Figure()
    fig_curve.add_trace(go.Scatter(x=cum["n_sellers"], y=cum["profits"], mode="lines", name="Kâr (IT hariç)"))
    fig_curve.add_trace(go.Scatter(x=cum["n_sellers"], y=cum["profits_after_it"], mode="lines", name="Kâr (IT dahil)"))
    fig_curve.update_layout(
        title="Toplam Kâr (Tutulan Satıcı Sayısına Göre)",
        xaxis_title="Tutulan satıcı sayısı (kümülatif)",
        yaxis_title="Kâr (BRL)",
        height=450,
        margin=dict(l=20, r=20, t=60, b=30),
    )

    # --- Sağ grafik: senaryo özeti
    revenues_total = float(cum["revenues"].iloc[-1])
    review_costs = float(cum["cost_of_reviews"].iloc[-1])
    it_costs_last = float(cum["it_costs"].iloc[-1])  # negatif
    impact = pd.DataFrame(
        {
            "Kalem": ["Gelir", "Review Maliyeti", "IT Maliyeti", "Net Kâr (IT dahil)"],
            "Tutar": [revenues_total, -review_costs, it_costs_last, profit_after_it],
        }
    )

    fig_barh = px.bar(
        impact,
        x="Tutar",
        y="Kalem",
        orientation="h",
        title="Senaryo Özeti (Gelir–Maliyet–Kâr)",
    )
    fig_barh.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=60, b=30),
        xaxis_title="BRL",
        yaxis_title="",
        showlegend=False,
    )

    return summary, fig_curve, fig_barh
