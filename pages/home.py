# pages/home.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from olist.seller_updated import Seller

dash.register_page(__name__, path="/", name="Özet (CEO)")

# -----------------------------
# Data
# -----------------------------
def load_sellers():
    seller = Seller()
    return seller.get_training_data()

# -----------------------------
# Formatting
# -----------------------------
def brl(value: float) -> str:
    return f"{value:,.0f} BRL"

CARD_STYLE = {"borderRadius": "14px"}
SECTION_CARD_CLASS = "shadow-sm mt-3"

# -----------------------------
# IT cost (home & seller_impact aynı olmalı)
# -----------------------------
# Eğer seller_impact içinde farklı bir IT hesabı kullanıyorsanız,
# burayı onunla birebir aynı yapın.
IT_BASE = 200_000
IT_PER_SELLER = 50
IT_PER_ITEM = 1.35

def compute_it_cost(n_sellers: int, n_items: int) -> float:
    return IT_BASE + IT_PER_SELLER * n_sellers + IT_PER_ITEM * n_items

# -----------------------------
# KPI + Waterfall
# -----------------------------
def build_kpis(sellers_df):
    # Gelir kırılımı
    gelir_satis_komisyonu = sellers_df["sales"].sum() * 0.10
    gelir_abonelik = sellers_df["months_on_olist"].sum() * 80
    toplam_gelir = gelir_satis_komisyonu + gelir_abonelik

    # Maliyetler
    maliyet_review = sellers_df["cost_of_reviews"].sum()

    # IT maliyeti (dinamik/varsayım)
    n_sellers = sellers_df["seller_id"].nunique()
    n_items = int(sellers_df["quantity"].sum())
    it_maliyeti = compute_it_cost(n_sellers, n_items)

    # Kâr
    brut_kar = toplam_gelir - maliyet_review
    net_kar = brut_kar - it_maliyeti

    return {
        "gelir_satis_komisyonu": gelir_satis_komisyonu,
        "gelir_abonelik": gelir_abonelik,
        "toplam_gelir": toplam_gelir,
        "maliyet_review": maliyet_review,
        "it_maliyeti": it_maliyeti,
        "brut_kar": brut_kar,
        "net_kar": net_kar,
        "n_sellers": n_sellers,
        "n_items": n_items,
    }

def kpi_card(title: str, value: float, subtitle: str = "", icon: str = ""):
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
                html.H3(brl(value), className="mt-2 mb-1"),
                html.Div(subtitle, className="text-muted"),
            ]
        ),
        className="shadow-sm h-100",
        style=CARD_STYLE,
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
        title="Gelir–Maliyet Akışı",
        height=450,
        margin=dict(l=30, r=30, t=60, b=30),
        showlegend=False,
    )
    return fig

# -----------------------------
# Build page
# -----------------------------
sellers_df = load_sellers()
k = build_kpis(sellers_df)
wf_fig = build_waterfall(k)

layout = dbc.Container(
    [
        # Header
        html.H2("CEO Özeti", className="mt-4"),
        html.P(
            "Bu sayfa mevcut durumu (hiç satıcı çıkarmadan) gelir–maliyet–kâr kırılımıyla özetler.",
            className="text-muted",
        ),

        # KPI row (logit sayfasındaki gibi)
        dbc.Row(
            [
                dbc.Col(
                    kpi_card(
                        "Toplam Gelir",
                        k["toplam_gelir"],
                        "Abonelik + Komisyon",
                        icon="💰",
                    ),
                    md=3,
                ),
                dbc.Col(
                    kpi_card(
                        "Review Maliyeti",
                        k["maliyet_review"],
                        "Müşteri memnuniyetsizliği maliyeti",
                        icon="🧾",
                    ),
                    md=3,
                ),
                dbc.Col(
                    kpi_card(
                        "IT / Operasyon Maliyeti",
                        k["it_maliyeti"],
                        f"{k['n_sellers']} satıcı • {k['n_items']:,} ürün (varsayım)",
                        icon="🖥️",
                    ),
                    md=3,
                ),
                dbc.Col(
                    kpi_card(
                        "Net Kâr",
                        k["net_kar"],
                        "Brüt Kâr - IT",
                        icon="📈",
                    ),
                    md=3,
                ),
            ],
            className="g-3",
        ),

        # Main chart section
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        "Nasıl okunur? Yeşil bloklar geliri, kırmızı bloklar maliyetleri gösterir. "
                        "En sağdaki Net Kâr, tüm gelirlerden tüm maliyetler çıktıktan sonra kalan tutardır.",
                        className="text-muted",
                        style={"marginBottom": "10px"},
                    ),
                    dcc.Graph(figure=wf_fig, config={"displayModeBar": True}),
                ]
            ),
            className=SECTION_CARD_CLASS,
            style=CARD_STYLE,
        ),

        # Insights section (logit sayfasındaki “Özet çıkarımlar” gibi)
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Özet çıkarımlar", className="mb-2"),
                    html.Ul(
                        [
                            html.Li("Gelirin ana kaynağı: abonelik ve satış komisyonu."),
                            html.Li("En büyük maliyet kalemi: review maliyeti (memnuniyetsizlik)."),
                            html.Li("Net kârı artırmak için iki kaldıraç var: operasyonel gecikmeleri azaltmak ve zarar eden satıcıları yönetmek."),
                        ],
                        className="mb-0",
                    ),
                ]
            ),
            className=SECTION_CARD_CLASS,
            style=CARD_STYLE,
        ),

        # CTA / next step (seller_impact’e köprü kuran)
        dbc.Alert(
            [
                html.B("Sonraki adım: "),
                "“Satıcı Çıkarma Etkisi” sayfasında, en düşük performanslı satıcıları çıkardığımızda net kârın nasıl değiştiğini senaryo bazlı inceleyebilirsiniz.",
            ],
            color="primary",
            className="mt-3",
            style={"borderRadius": "12px"},
        ),
    ],
    fluid=True,
)
