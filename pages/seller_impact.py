# pages/seller_impact.py
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from olist.seller_updated import Seller

dash.register_page(__name__, path="/seller-impact", name="Satıcı Çıkarma Etkisi")

# -----------------------------
# Styling helpers (home + logit ile uyumlu)
# -----------------------------
CARD_STYLE = {"borderRadius": "14px"}
SECTION_CARD_CLASS = "shadow-sm mt-3"

def brl(x: float) -> str:
    return f"{x:,.0f} BRL"

def kpi_card(title: str, value: str, subtitle: str = "", icon: str = ""):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Span(icon, style={"fontSize": "18px", "marginRight": "8px"}) if icon else None,
                        html.Span(title, className="text-muted"),
                    ],
                    style={"display": "flex", "alignItems": "center"},
                ),
                html.H3(value, className="mt-2 mb-1"),
                html.Div(subtitle, className="text-muted"),
            ]
        ),
        className="shadow-sm h-100",
        style=CARD_STYLE,
    )

# -----------------------------
# Data load
# -----------------------------
def load_sellers_df() -> pd.DataFrame:
    seller = Seller()
    return seller.get_training_data()

SELLERS_DF = load_sellers_df().copy()

# Bu sayfada "kâr" dediğimiz şey, training_data içindeki revenue/cost üzerinden:
# gross_profit (IT hariç) = revenues - cost_of_reviews
SELLERS_DF["gross_profit"] = SELLERS_DF["revenues"] - SELLERS_DF["cost_of_reviews"]

# "En kötüden başla" = gross_profit en düşük olanlar önce çıkarılacak
SELLERS_ASC = SELLERS_DF.sort_values("gross_profit", ascending=True).reset_index(drop=True)

# "Kümülatif eğri"yi anlatmak için: en iyi satıcıları tutarak kârın nasıl değiştiği
SELLERS_DESC = SELLERS_DF.sort_values("gross_profit", ascending=False).reset_index(drop=True)

TOTAL_SELLERS = SELLERS_DF["seller_id"].nunique()
TOTAL_ITEMS = int(SELLERS_DF["quantity"].sum())

# -----------------------------
# IT cost (home ile aynı mantıkta olmalı)
# -----------------------------
IT_BASE = 200_000
IT_PER_SELLER = 50
IT_PER_ITEM = 1.35

def compute_it_cost(n_sellers: int, n_items: int) -> float:
    return IT_BASE + IT_PER_SELLER * n_sellers + IT_PER_ITEM * n_items

def scenario_totals(df: pd.DataFrame) -> dict:
    n_sellers = df["seller_id"].nunique()
    n_items = int(df["quantity"].sum())

    revenue = float(df["revenues"].sum())
    review_cost = float(df["cost_of_reviews"].sum())
    gross_profit = float(df["gross_profit"].sum())

    it_cost = float(compute_it_cost(n_sellers, n_items))
    net_profit = gross_profit - it_cost

    return {
        "n_sellers": n_sellers,
        "n_items": n_items,
        "revenue": revenue,
        "review_cost": review_cost,
        "gross_profit": gross_profit,
        "it_cost": it_cost,
        "net_profit": net_profit,
    }

BASE = scenario_totals(SELLERS_DF)

# -----------------------------
# Figures
# -----------------------------
def build_profit_curve_fig(kept_count: int):
    """
    Soldaki çizgi grafik:
    - X: tutulan satıcı sayısı (en iyi satıcılardan başlayarak)
    - Y: kümülatif kâr
    İki çizgi:
      - IT hariç (gross)
      - IT dahil (net)
    """
    # En iyi satıcıları sırayla ekleyerek kümülatif topla
    tmp = SELLERS_DESC.copy()
    tmp["cum_sellers"] = range(1, len(tmp) + 1)
    tmp["cum_items"] = tmp["quantity"].cumsum()
    tmp["cum_revenue"] = tmp["revenues"].cumsum()
    tmp["cum_review_cost"] = tmp["cost_of_reviews"].cumsum()
    tmp["cum_gross_profit"] = tmp["cum_revenue"] - tmp["cum_review_cost"]

    # kümülatif IT maliyeti (aynı formül)
    tmp["cum_it_cost"] = tmp.apply(
        lambda r: compute_it_cost(int(r["cum_sellers"]), int(r["cum_items"])),
        axis=1,
    )
    tmp["cum_net_profit"] = tmp["cum_gross_profit"] - tmp["cum_it_cost"]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=tmp["cum_sellers"],
            y=tmp["cum_gross_profit"],
            mode="lines",
            name="Kâr (IT hariç)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=tmp["cum_sellers"],
            y=tmp["cum_net_profit"],
            mode="lines",
            name="Kâr (IT dahil)",
        )
    )

    # Seçili senaryo için dikey çizgi
    fig.add_vline(
        x=kept_count,
        line_width=2,
        line_dash="dash",
        annotation_text="Seçili senaryo",
        annotation_position="top",
    )

    fig.update_layout(
        title="Kârın Satıcı Sayısına Göre Değişimi (en iyi satıcılardan başlayarak)",
        height=420,
        margin=dict(l=40, r=30, t=60, b=40),
        legend_title_text="",
        xaxis_title="Tutulan satıcı sayısı",
        yaxis_title="Kâr (BRL)",
    )
    return fig

def build_pl_snapshot_fig(totals: dict):
    """
    Sağdaki özet bar: Gelir / Review / IT / Net kâr
    """
    dfp = pd.DataFrame(
        {
            "Kalem": ["Gelir", "Review Maliyeti", "IT / Operasyon", "Net Kâr"],
            "Tutar": [
                totals["revenue"],
                -totals["review_cost"],
                -totals["it_cost"],
                totals["net_profit"],
            ],
        }
    )

    fig = px.bar(
        dfp,
        x="Tutar",
        y="Kalem",
        orientation="h",
        title="Senaryo Özeti (Gelir–Maliyet–Net Kâr)",
    )
    fig.update_layout(
        height=420,
        margin=dict(l=40, r=20, t=60, b=40),
        xaxis_title="BRL",
        yaxis_title="",
        showlegend=False,
    )
    return fig

# -----------------------------
# Layout
# -----------------------------
layout = dbc.Container(
    [
        html.H2("Satıcı Çıkarma Etkisi", className="mt-4"),
        html.P(
            "Bu sayfa, en düşük performanslı satıcıları çıkardığımızda toplam kârın nasıl değiştiğini senaryo bazlı gösterir.",
            className="text-muted",
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        "Senaryo: “En kötü satıcılardan” başlayarak kaç satıcı çıkaralım?",
                        className="text-muted",
                        style={"marginBottom": "8px"},
                    ),
                    dcc.Slider(
                        id="remove_sellers",
                        min=0,
                        max=TOTAL_SELLERS,
                        step=1,
                        value=0,
                        tooltip={"placement": "bottom", "always_visible": False},
                    ),
                    html.Div(id="scenario_line", className="text-muted", style={"marginTop": "10px"}),
                ]
            ),
            className="shadow-sm",
            style=CARD_STYLE,
        ),

        dbc.Row(
            [
                dbc.Col(kpi_card("Çıkarılan satıcı", "0", "En kötüden başlayarak", icon="🧹"), md=3),
                dbc.Col(kpi_card("Kalan satıcı", f"{TOTAL_SELLERS}", "Mevcut durum", icon="🏪"), md=3),
                dbc.Col(kpi_card("Net Kâr", brl(BASE["net_profit"]), "IT dahil", icon="📈"), md=3),
                dbc.Col(kpi_card("Değişim", brl(0), "Mevcut duruma göre", icon="🧭"), md=3),
            ],
            id="kpi_row",
            className="g-3 mt-0",
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        "Nasıl okunur? Solda satıcı sayısı arttıkça kârın nasıl değiştiğini görürsünüz. "
                        "Sağda ise seçili senaryonun gelir–maliyet–net kâr özeti vardır.",
                        className="text-muted",
                        style={"marginBottom": "10px"},
                    ),
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(id="profit_curve"), md=8),
                            dbc.Col(dcc.Graph(id="pl_snapshot"), md=4),
                        ],
                        className="g-3",
                    ),
                ]
            ),
            className=SECTION_CARD_CLASS,
            style=CARD_STYLE,
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Özet çıkarımlar", className="mb-2"),
                    html.Ul(
                        [
                            html.Li("Bazı satıcılar toplam kârı aşağı çekebilir; yönetim için aksiyon alanı oluşturur."),
                            html.Li("Kârın tepe yaptığı noktada ‘gereksiz zarar’ minimize edilir."),
                            html.Li("Karar önerisi: Zarar eden satıcıları iyileştirme planı + gerekiyorsa portföyden çıkarma."),
                        ],
                        className="mb-0",
                    ),
                ]
            ),
            className=SECTION_CARD_CLASS,
            style=CARD_STYLE,
        ),

        dbc.Alert(
            [
                html.B("Sunum mesajı: "),
                "Hedef ‘satıcı sayısını azaltmak’ değil; toplam kârı düşüren satıcıları tespit edip aksiyon almak "
                "(iyileştirmek, şartları güncellemek veya portföyden çıkarmak).",
            ],
            color="primary",
            className="mt-3",
            style={"borderRadius": "12px"},
        ),
    ],
    fluid=True,
)

# -----------------------------
# Callback
# -----------------------------
@dash.callback(
    Output("profit_curve", "figure"),
    Output("pl_snapshot", "figure"),
    Output("scenario_line", "children"),
    Output("kpi_row", "children"),
    Input("remove_sellers", "value"),
)
def update_scenario(remove_n: int):
    remove_n = int(remove_n or 0)

    # Senaryo: en kötüden remove_n satıcıyı çıkar
    kept_df = SELLERS_ASC.iloc[remove_n:].copy()
    totals = scenario_totals(kept_df)

    kept_count = totals["n_sellers"]
    removed_count = TOTAL_SELLERS - kept_count

    # Grafikler
    fig_left = build_profit_curve_fig(kept_count=kept_count)
    fig_right = build_pl_snapshot_fig(totals)

    # Üst bilgi satırı
    delta = totals["net_profit"] - BASE["net_profit"]
    delta_txt = f"{'+' if delta >= 0 else ''}{brl(delta)}"

    scenario_text = (
        f"Çıkarılan: {removed_count} | Kalan: {kept_count} | "
        f"Net Kâr (IT dahil): {brl(totals['net_profit'])} | Değişim: {delta_txt}"
    )

    # KPI row (güncel)
    kpis = [
        dbc.Col(kpi_card("Çıkarılan satıcı", f"{removed_count}", "En kötüden başlayarak", icon="🧹"), md=3),
        dbc.Col(kpi_card("Kalan satıcı", f"{kept_count}", "Seçili senaryo", icon="🏪"), md=3),
        dbc.Col(kpi_card("Net Kâr", brl(totals["net_profit"]), "IT dahil", icon="📈"), md=3),
        dbc.Col(kpi_card("Değişim", delta_txt, "Mevcut duruma göre", icon="🧭"), md=3),
    ]

    return fig_left, fig_right, scenario_text, kpis
