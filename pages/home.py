# pages/home.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from olist.seller_updated import Seller

dash.register_page(__name__, path="/", name="Finansal Özet")

# -----------------------------
# Styling (BI uyumlu)
# -----------------------------
CARD_STYLE = {"borderRadius": "16px", "border": "none"}
SECTION_CARD_CLASS = "shadow-sm mt-3"

# Net Kâr KPI kartını öne çıkarmak için (hafif primary vurgu + koyu border)
HIGHLIGHT_CARD_STYLE = {
    **CARD_STYLE,
    "border": "2px solid rgba(13, 110, 253, 0.55)",  # bootstrap primary
    "boxShadow": "0 0.5rem 1.25rem rgba(13, 110, 253, 0.12)",
}
HIGHLIGHT_BADGE_STYLE = {
    "background": "rgba(13, 110, 253, 0.10)",
    "color": "#0d6efd",
    "border": "1px solid rgba(13, 110, 253, 0.25)",
    "borderRadius": "999px",
    "padding": "2px 10px",
    "fontSize": "12px",
    "fontWeight": 700,
}

# Seller Impact ile aynı IT maliyeti modeli (senkron)
ALPHA, BETA = 3157.27, 978.23


def cost_of_it(n_sellers: int, quantity: float) -> float:
    return ALPHA * (n_sellers**0.5) + BETA * (quantity**0.5)


def load_sellers():
    return Seller().get_training_data()


def brl(value: float) -> str:
    return f"{value:,.0f} BRL"


def kpi_card(title, value, subtitle="", icon="", highlight: bool = False, badge_text: str | None = None):
    style = HIGHLIGHT_CARD_STYLE if highlight else CARD_STYLE

    header_row = html.Div(
        [
            html.Span(icon, style={"fontSize": "18px", "marginRight": "8px"}) if icon else None,
            html.Span(title, className="text-muted fw-semibold"),
            html.Span(badge_text, style=HIGHLIGHT_BADGE_STYLE, className="ms-auto") if badge_text else None,
        ],
        style={"display": "flex", "alignItems": "center"},
    )

    return dbc.Card(
        dbc.CardBody(
            [
                header_row,
                html.H3(brl(value), className="mt-2 mb-1 fw-bold"),
                html.Div(subtitle, className="text-muted"),
            ]
        ),
        className="shadow-sm h-100",
        style=style,
    )


def build_waterfall(k):
    # Renk Tanımlamaları (Standardize edildi)
    COLOR_REVENUE = "#28a745"  # Yeşil
    COLOR_COST = "#dc3545"     # Kırmızı
    COLOR_TOTAL = "#0d6efd"    # Mavi (Bootstrap Primary)

    fig = go.Figure(
        go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "total", "relative", "total", "relative", "total"],
            # X ekseni kısaltıldı (Madde 4)
            x=[
                "Abonelik",
                "Komisyon",
                "Toplam Gelir",
                "Review",
                "Brüt Kâr",
                "IT/Oper.",
                "Net Kâr",
            ],
            textposition="outside",
            # Değer etiketleri BRL formatlı (Madde 2)
            text=[
                f"+{k['gelir_abonelik']/1e6:.1f}M",
                f"+{k['gelir_satis_komisyonu']/1e6:.1f}M",
                f"{k['toplam_gelir']/1e6:.1f}M",
                f"-{k['maliyet_review']/1e6:.1f}M",
                f"{k['brut_kar']/1e6:.1f}M",
                f"-{k['it_maliyeti']/1e6:.1f}M",
                f"<b>{k['net_kar']/1e6:.1f}M</b>", # Net Kâr daha belirgin
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
            # Renkler standardize edildi (Madde 3)
            decreasing={"marker": {"color": COLOR_COST}},
            increasing={"marker": {"color": COLOR_REVENUE}},
            totals={"marker": {"color": COLOR_TOTAL}},
            connector={"line": {"width": 1, "color": "rgb(63, 63, 63)", "dash": "dot"}},
            # Tooltip zenginleştirildi (Madde 5)
            hovertemplate="<b>%{x}</b><br>Tutar: %{y:,.0f} BRL<extra></extra>"
        )
    )

    fig.update_layout(
        title="Gelir → Maliyet → Net Kâr Akışı",
        height=500,
        margin=dict(l=30, r=20, t=80, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=14, family="Inter, sans-serif"),
        title_font=dict(size=22),
        showlegend=False
    )

    # Grid ve 0 Çizgisi Ayarları (Madde 1)
    fig.update_xaxes(
        tickfont=dict(size=13, color="#495057"),
        showgrid=False
    )
    
    fig.update_yaxes(
        title="BRL",
        tickfont=dict(size=12, color="#6c757d"),
        showgrid=True,             # Yatay grid çizgileri açık
        gridcolor="rgba(0,0,0,0.05)", # Hafif belirgin grid
        zeroline=True,             # 0 çizgisi aktif
        zerolinewidth=2,           # 0 çizgisi kalınlaştırıldı
        zerolinecolor="black"      # 0 çizgisi netleştirildi
    )

    return fig


# -----------------------------
# Compute KPIs (Mevcut durum)
# -----------------------------
sellers = load_sellers()

gelir_satis_komisyonu = sellers["sales"].sum() * 0.10
gelir_abonelik = sellers["months_on_olist"].sum() * 80
toplam_gelir = float(sellers["revenues"].sum())

maliyet_review = float(sellers["cost_of_reviews"].sum())

n_sellers = int(sellers["seller_id"].nunique())
quantity = float(sellers["quantity"].sum())
it_maliyeti = float(cost_of_it(n_sellers, quantity))

brut_kar = float(sellers["profits"].sum())
net_kar = brut_kar - it_maliyeti

k = {
    "gelir_satis_komisyonu": float(gelir_satis_komisyonu),
    "gelir_abonelik": float(gelir_abonelik),
    "toplam_gelir": toplam_gelir,
    "maliyet_review": maliyet_review,
    "it_maliyeti": it_maliyeti,
    "brut_kar": brut_kar,
    "net_kar": net_kar,
    "n_sellers": n_sellers,
    "quantity": quantity,
}

wf_fig = build_waterfall(k)

# -----------------------------
# Layout
# -----------------------------
layout = dbc.Container(
    [
        html.H2("Finansal Özet — Mevcut Durum", className="mt-4 mb-1 fw-bold"),
        html.P(
            "Hiç satıcı çıkarmadan, bugünkü tabloyu gelir–maliyet–net kâr kırılımıyla özetler.",
            className="text-muted mb-3",
        ),

        # KPI row
        dbc.Row(
            [
                dbc.Col(kpi_card("Toplam Gelir", k["toplam_gelir"], "Abonelik + Komisyon", "💰"), md=3),
                dbc.Col(kpi_card("Review Maliyeti", k["maliyet_review"], "Memnuniyetsizliğin maliyeti", "🧾"), md=3),
                dbc.Col(
                    kpi_card(
                        "IT / Operasyon",
                        k["it_maliyeti"],
                        f"{k['n_sellers']} satıcı • {int(k['quantity']):,} ürün (varsayım)",
                        "🖥️",
                    ),
                    md=3,
                ),
                # Net Kâr vurgulu
                dbc.Col(
                    kpi_card(
                        "Net Kâr",
                        k["net_kar"],
                        "Brüt kâr − IT/operasyon",
                        "📈",
                        highlight=True,
                        badge_text="PRIMARY KPI",
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
                        "Nasıl okunur? Yeşil bloklar gelir, kırmızı bloklar maliyet. En sağdaki Net Kâr, tüm gelirlerden tüm maliyetler çıktıktan sonra kalan tutardır.",
                        className="text-muted",
                    ),
                    dcc.Graph(figure=wf_fig, className="mt-2", config={"displayModeBar": False}),
                ]
            ),
            className=SECTION_CARD_CLASS,
            style=CARD_STYLE,
        ),

        # Insights section (BI-style)
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("📌 Yönetim için net çıkarımlar", className="mb-2 fw-bold"),
                    html.Ul(
                        [
                            html.Li("Gelirin ana kaynağı: abonelik ve satış komisyonu."),
                            html.Li("En büyük maliyet kalemi: review maliyeti (memnuniyetsizlik)."),
                            html.Li("Net kâr için iki kaldıraç: teslimat/gecikme performansını iyileştirmek + zarar eden satıcıları yönetmek."),
                        ],
                        className="mb-0",
                    ),
                ]
            ),
            className=SECTION_CARD_CLASS,
            style=CARD_STYLE,
        ),

        # Next step (bridge)
        dbc.Alert(
            [
                html.Span("➡️ ", className="me-1"),
                html.B("Sonraki adım: "),
                "“Satıcı Çıkarma Etkisi” sayfasında, en düşük performanslı satıcıları çıkardığımızda net kârın nasıl değiştiğini senaryo bazlı inceleyebilirsiniz.",
            ],
            color="primary",
            className="mt-3",
            style={"borderRadius": "14px"},
        ),
    ],
    fluid=True,
    className="pb-4",
)
