# pages/about.py
import dash
from dash import html
import dash_bootstrap_components as dbc

# Not: Navbar'da "Metodoloji" etiketi /hakkinda path'ine gidiyorsa burada path'i değiştirmiyoruz.
dash.register_page(__name__, path="/hakkinda", name="Metodoloji")

CARD_STYLE = {"borderRadius": "16px", "border": "none"}
SECTION_CARD_CLASS = "shadow-sm mt-3"


def pill(text: str, color: str = "light"):
    return dbc.Badge(
        text,
        color=color,
        pill=True,
        className="me-2",
        style={"fontWeight": 700, "padding": "8px 10px"},
    )


def mini_card(title: str, body: str):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="text-muted fw-bold"),
                html.Div(body, className="mt-2"),
            ]
        ),
        className="h-100 shadow-sm border-0",
        style=CARD_STYLE,
    )


layout = dbc.Container(
    [
        # Header
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("ℹ️ Metodoloji", className="mt-4 mb-1 fw-bold"),
                        html.P(
                            "Bu panel, Olist verisinden hareketle kârlılık ve memnuniyet dinamiklerini yönetim seviyesinde özetleyen "
                            "bir karar destek demosudur.",
                            className="text-muted mb-0",
                        ),
                        html.Div(
                            [
                                pill("BI / Yönetim Özeti", "dark"),
                                pill("Eğitim Senaryosu", "secondary"),
                                pill("Aksiyon Odaklı", "primary"),
                            ],
                            className="mt-3",
                        ),
                    ],
                    md=12,
                )
            ]
        ),

        # What it answers
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.Span("🎯", style={"fontSize": "20px", "marginRight": "10px"}),
                            html.H5("Bu panel hangi soruları cevaplıyor?", className="mb-0 fw-bold"),
                        ],
                        style={"display": "flex", "alignItems": "center"},
                        className="mb-3",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                mini_card(
                                    "💰 Finansal fotoğraf",
                                    "Mevcut durumda gelir–maliyet–net kâr dengemiz nasıl?",
                                ),
                                md=4,
                            ),
                            dbc.Col(
                                mini_card(
                                    "🧹 Portföy optimizasyonu",
                                    "Zarar eden satıcıları çıkarmak net kârı artırır mı? En iyi nokta neresi?",
                                ),
                                md=4,
                            ),
                            dbc.Col(
                                mini_card(
                                    "⭐ Memnuniyet sürücüleri",
                                    "Müşteri memnuniyetini en çok etkileyen operasyonel faktörler neler?",
                                ),
                                md=4,
                            ),
                        ],
                        className="g-3",
                    ),
                ]
            ),
            className=SECTION_CARD_CLASS,
            style=CARD_STYLE,
        ),

        # Assumptions
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.Span("🧾", style={"fontSize": "20px", "marginRight": "10px"}),
                            html.H5("Varsayımlar", className="mb-0 fw-bold"),
                        ],
                        style={"display": "flex", "alignItems": "center"},
                        className="mb-3",
                    ),
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItem(
                                [
                                    html.Span("📌 ", className="me-1"),
                                    html.B("Gelir: "),
                                    "Abonelik + satış komisyonu (satışların %10’u).",
                                ],
                                className="border-0",
                            ),
                            dbc.ListGroupItem(
                                [
                                    html.Span("📌 ", className="me-1"),
                                    html.B("Review maliyeti: "),
                                    "Düşük puanlı yorumların operasyonel maliyet yarattığı varsayımıyla hesaplanır.",
                                ],
                                className="border-0",
                            ),
                            dbc.ListGroupItem(
                                [
                                    html.Span("📌 ", className="me-1"),
                                    html.B("IT/Operasyon maliyeti: "),
                                    "Satıcı ve ürün hacmine göre ölçeklenen basit bir maliyet modeli (eğitim senaryosu).",
                                ],
                                className="border-0",
                            ),
                        ],
                        flush=True,
                    ),
                    dbc.Alert(
                        [
                            html.B("Not: "),
                            "Bu çalışma eğitim amaçlıdır. Maliyet kalemleri gerçek şirket verisi değildir; amaç karar destek yaklaşımını göstermektir.",
                        ],
                        color="primary",
                        className="mt-3 mb-0",
                        style={
                            "borderRadius": "14px",
                            "backgroundColor": "#2b8fd8",
                            "border": "none",
                            "color": "white",
                            "fontWeight": 600,
                        },
                    ),
                ]
            ),
            className=SECTION_CARD_CLASS,
            style=CARD_STYLE,
        ),

        # How to read pages
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.Span("🧭", style={"fontSize": "20px", "marginRight": "10px"}),
                            html.H5("Sayfalar nasıl okunur?", className="mb-0 fw-bold"),
                        ],
                        style={"display": "flex", "alignItems": "center"},
                        className="mb-3",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                mini_card(
                                    "📊 Finansal Özet",
                                    "Mevcut durumun gelir–maliyet–net kâr kırılımı.",
                                ),
                                md=4,
                            ),
                            dbc.Col(
                                mini_card(
                                    "📈 Portföy Optimizasyonu",
                                    "En düşük performanslı satıcılar çıkarıldığında net kârın senaryo bazlı değişimi.",
                                ),
                                md=4,
                            ),
                            dbc.Col(
                                mini_card(
                                    "⭐ Memnuniyet Sürücüleri",
                                    "Memnuniyeti/mutsuzluğu artıran ana operasyonel unsurlar ve önerilen aksiyonlar.",
                                ),
                                md=4,
                            ),
                        ],
                        className="g-3",
                    ),
                ]
            ),
            className=SECTION_CARD_CLASS,
            style=CARD_STYLE,
        ),

        # Executive focus (dark bar like other pages)
        dbc.Alert(
            [
                html.Span("🧠 ", className="me-1"),
                html.B("Sunum odağı: "),
                "Kod değil; içgörü ve aksiyon. Bu panel, yönetime “ne yapmalıyız?” sorusunun kısa cevabını vermeyi hedefler.",
            ],
            color="dark",
            className="mt-3",
            style={
                "borderRadius": "14px",
                "backgroundColor": "#263645",
                "border": "none",
                "color": "white",
                "fontWeight": 600,
            },
        ),
    ],
    fluid=True,
    className="pb-4",
)
