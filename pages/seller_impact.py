import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from olist.seller_updated import Seller

dash.register_page(__name__, path="/satici-etkisi", name="Satıcı Çıkarma Etkisi")

# Eğitimde kullanılan parametreler
alpha, beta = 3157.27, 978.23

def cost_of_it(df, alpha, beta):
    return alpha * (df["n_sellers"] ** 0.5) + beta * (df["quantity"] ** 0.5)

def prepare_metrics():
    sellers = Seller().get_training_data()

    metrics_ordered = (
        sellers[["revenues", "cost_of_reviews", "profits", "quantity"]]
        .sort_values(by="profits", ascending=False)
        .reset_index(drop=True)
    )
    # maliyetleri negatif göstermek için
    metrics_ordered["cost_of_reviews"] *= -1
    metrics_ordered["n_sellers"] = 1

    metrics_cum = metrics_ordered.cumsum()

    metrics_cum_it = metrics_ordered.cumsum()
    metrics_cum_it["it_costs"] = -cost_of_it(metrics_cum_it, alpha, beta)
    metrics_cum_it["profits_after_it"] = metrics_cum_it["profits"] + metrics_cum_it["it_costs"]

    opt_without_it = int(metrics_cum["profits"].idxmax())
    opt_with_it = int(metrics_cum_it["profits_after_it"].idxmax())

    return metrics_ordered, metrics_cum, metrics_cum_it, opt_without_it, opt_with_it

metrics_ordered, metrics_cum, metrics_cum_it, opt_wo, opt_w = prepare_metrics()
max_remove = len(metrics_ordered) - 1

def cumulative_profit_figure(metrics_cum, metrics_cum_it, opt_wo, opt_w):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=metrics_cum.index,
            y=metrics_cum["profits"],
            name="Kâr (IT hariç)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=metrics_cum_it.index,
            y=metrics_cum_it["profits_after_it"],
            name="Kâr (IT dahil)",
        )
    )

    fig.add_vline(
        x=opt_wo,
        line_dash="dash",
        annotation_text="En iyi (IT hariç)",
        annotation_position="top left",
    )
    fig.add_vline(
        x=opt_w,
        line_dash="dash",
        annotation_text="En iyi (IT dahil)",
        annotation_position="top right",
    )

    fig.update_layout(
        title="Toplam Kâr (Tutulan Satıcı Sayısına Göre)",
        xaxis_title="Tutulan satıcı sayısı (kümülatif)",
        yaxis_title="Kâr (BRL)",
        height=450,
        margin=dict(l=30, r=30, t=60, b=30),
        legend_title_text="",
    )
    return fig

base_line_fig = cumulative_profit_figure(metrics_cum, metrics_cum_it, opt_wo, opt_w)

def fmt_money(x):
    return f"{x:,.0f}"

layout = dbc.Container(
    [
        html.H2("Satıcı Çıkarma Etkisi", className="mt-4"),
        html.P(
            "Slider ile en kötü performanslı satıcıları (zarar edenleri) çıkardığımızda toplam kârın nasıl değiştiğini görürsünüz.",
            className="text-muted",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div("Kaç satıcıyı çıkaralım? (En kötüden başlayarak)"),
                    dcc.Slider(
                        id="remove_n",
                        min=0,
                        max=max_remove,
                        step=1,
                        value=min(200, max_remove),
                        tooltip={"placement": "bottom", "always_visible": False},
                    ),
                    html.Div(id="remove_summary", className="mt-2 text-muted"),
                ]
            ),
            className="shadow-sm",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([dcc.Graph(id="cum_profit_graph", figure=base_line_fig)]),
                        className="shadow-sm mt-3",
                    ),
                    md=8,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([dcc.Graph(id="impact_barh")]),
                        className="shadow-sm mt-3",
                    ),
                    md=4,
                ),
            ],
            className="g-3",
        ),
        dbc.Alert(
            [
                html.B("Nasıl okunur? "),
                "Solda kârın trendi, sağda seçilen senaryonun gelir–maliyet–net kâr özeti var.",
            ],
            color="secondary",
            className="mt-3",
        ),
    ],
    fluid=True,
)

@dash.callback(
    Output("remove_summary", "children"),
    Output("impact_barh", "figure"),
    Input("remove_n", "value"),
)
def update_impact(remove_n):
    # remove_n: en kötüden kaç satıcı çıkarılıyor?
    kept = metrics_ordered.iloc[: max_remove - remove_n]

    cum = kept[["revenues", "cost_of_reviews", "profits", "quantity"]].copy()
    cum["n_sellers"] = 1
    cum = cum.cumsum()
    cum["it_costs"] = -cost_of_it(cum, alpha, beta)
    cum["profits_after_it"] = cum["profits"] + cum["it_costs"]

    profit_no_it = float(cum["profits"].iloc[-1]) if len(cum) else 0.0
    profit_after_it = float(cum["profits_after_it"].iloc[-1]) if len(cum) else 0.0

    summary = (
        f"Çıkarılan: {remove_n} | Kalan: {len(kept)} | "
        f"Kâr (IT hariç): {fmt_money(profit_no_it)} | "
        f"Kâr (IT dahil): {fmt_money(profit_after_it)}"
    )

    revenues_total = float(cum["revenues"].iloc[-1]) if len(cum) else 0.0
    review_costs = float(cum["cost_of_reviews"].iloc[-1]) if len(cum) else 0.0
    it_costs = float(cum["it_costs"].iloc[-1]) if len(cum) else 0.0

    impact = pd.DataFrame(
        {
            "Kalem": ["Gelir", "Review Maliyeti", "IT Maliyeti", "Net Kâr (IT dahil)"],
            "Tutar": [revenues_total, review_costs, it_costs, profit_after_it],
        }
    )

    fig = px.bar(
        impact,
        x="Tutar",
        y="Kalem",
        orientation="h",
        title="Senaryo Özeti (Gelir–Maliyet–Kâr)",
    )
    fig.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=60, b=30),
        xaxis_title="BRL",
        yaxis_title="",
        showlegend=False,
    )

    return summary, fig
