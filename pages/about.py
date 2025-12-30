# pages/about.py
import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/hakkinda", name="Metadoloji")

CARD_STYLE = {"borderRadius": "16px", "border": "none"}
SECTION_CARD_CLASS = "shadow-sm mt-3"


def pill(text: str, color: str = "light"):
    return dbc.Badge(
        text,
        color=color,
        pill=True,
        className="me-2",
        style={"fontWeight": 600, "padding": "8px 10px"},
    )


layout = dbc.Container(
    [
        # Header
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("ℹ️ Metadoloji", className="mt-4 mb-1 fw-bold"),
                        html.P(
                            "Bu panel, Olist verisinden hareketle kârlılık ve memnuniyet dinamiklerini yönetim seviyesinde özetleyen "
                            "bir karar destek demosudur.",
                            className="text-muted mb-0",
                        ),
                        html.Div(
                            [
                                pill("BI / Yönetim Özeti", "primary"),
                                pill("Eğitim Senaryosu", "secondary"),
                                pill("Aksiyon Odaklı", "info"),
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
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div("💰 Kârlılık fotoğrafı", className="text-muted fw-bold"),
                                            html.Div(
                                                "Mevcut durumda gelir–maliyet–net kâr dengemiz nasıl?",
                                                className="mt-2",
                                            ),
                                        ]
                                    ),
                                    className="h-100 shadow-sm border-0",
                                    style=CARD_STYLE,
                                ),
                                md=4,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div("🧹 Portföy optimizasyonu", className="text-muted fw-bold"),
                                            html.Div(
                                                "Zarar eden satıcıları çıkarmak net kârı artırır mı? En iyi nokta neresi?",
                                                className="mt-2",
                                            ),
                                        ]
                                    ),
                                    className="h-100 shadow-sm border-0",
                                    style=CARD_STYLE,
                                ),
                                md=4,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div("⭐ Memnuniyet sürücüleri", className="text-muted fw-bold"),
                                            html.Div(
                                                "Müşteri memnuniyetini en çok etkileyen operasyonel faktörler neler?",
                                                className="mt-2",
                                            ),
                                        ]
                                    ),
                                    className="h-100 shadow-sm border-0",
                                    style=CARD_STYLE,
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
                            html.H5("Varsayımlar (basit ve şeffaf)", className="mb-0 fw-bold"),
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
                        color="info",
                        className="mt-3 mb-0",
                        style={"borderRadius": "14px"},
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
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div("📊 CEO Özeti", className="text-muted fw-bold"),
                                            html.Div(
                                                "Mevcut durumun gelir–maliyet–net kâr kırılımı.",
                                                className="mt-2",
                                            ),
                                        ]
                                    ),
                                    className="h-100 shadow-sm border-0",
                                    style=CARD_STYLE,
                                ),
                                md=4,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div("📈 Satıcı Çıkarma Etkisi", className="text-muted fw-bold"),
                                            html.Div(
                                                "En düşük performanslı satıcılar çıkarıldığında net kârın senaryo bazlı değişimi.",
                                                className="mt-2",
                                            ),
                                        ]
                                    ),
                                    className="h-100 shadow-sm border-0",
                                    style=CARD_STYLE,
                                ),
                                md=4,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div("⭐ Memnuniyet Sürücüleri", className="text-muted fw-bold"),
                                            html.Div(
                                                "Memnuniyeti/mutsuzluğu artıran ana operasyonel unsurlar ve önerilen aksiyonlar.",
                                                className="mt-2",
                                            ),
                                        ]
                                    ),
                                    className="h-100 shadow-sm border-0",
                                    style=CARD_STYLE,
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

        # Executive focus
        dbc.Alert(
            [
                html.Span("🧠 ", className="me-1"),
                html.B("Sunum odağı: "),
                "Kod değil; içgörü ve aksiyon. Bu panel, yönetime “ne yapmalıyız?” sorusunun kısa cevabını vermeyi hedefler.",
            ],
            color="primary",
            className="mt-3",
            style={"borderRadius": "14px"},
        ),
    ],
    fluid=True,
    className="pb-4",
)
