# pages/logit_insights.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/logit-insights", name="Memnuniyet Sürücüleri")

# Notebook'tan alınan (standardize edilmiş) katsayılar
# Not: Bu sayfada "katsayı / logit / standardize" kelimelerini arayüzde göstermiyoruz.
COEFS_ONE_STAR = {
    "Teslimat süresi": 0.6907,                 # wait_time
    "Beklenenden geç gelme": 0.2626,           # delay_vs_expected
    "Siparişte satıcı sayısı": 0.2295,         # number_of_sellers
    "Satıcı–müşteri uzaklığı": -0.2193,        # distance_seller_customer
    "Kargo ücreti": 0.1090,                    # freight_value
    "Ürün fiyatı": 0.0407,                     # price
}

COEFS_FIVE_STAR = {
    "Teslimat süresi": -0.5140,                # wait_time
    "Beklenenden geç gelme": -0.4366,          # delay_vs_expected
    "Siparişte satıcı sayısı": -0.1716,        # number_of_sellers
    "Satıcı–müşteri uzaklığı": 0.1075,         # distance_seller_customer
    "Kargo ücreti": -0.0624,                   # freight_value
    "Ürün fiyatı": 0.0268,                     # price
}

# -------------------------
# Build tidy dataframe
# -------------------------
features = list(COEFS_ONE_STAR.keys())

df = pd.DataFrame(
    {
        "Faktör": features,
        "Mutsuzluk Riski (1★)": [COEFS_ONE_STAR[f] for f in features],
        "Memnuniyet (5★)": [COEFS_FIVE_STAR[f] for f in features],
    }
)

df_long = df.melt(id_vars="Faktör", var_name="Gösterge", value_name="Etki")
df_long["Mutlak Etki"] = df_long["Etki"].abs()

# Sıralama: en güçlü etki üstte görünsün
order = (
    df_long.groupby("Faktör")["Mutlak Etki"]
    .max()
    .sort_values(ascending=False)
    .index.tolist()
)

# -------------------------
# Figure
# -------------------------
fig = px.bar(
    df_long,
    x="Etki",
    y="Faktör",
    color="Gösterge",
    orientation="h",
    category_orders={"Faktör": order},
    title="Sipariş Deneyimini Etkileyen Unsurlar",
)

fig.update_layout(
    height=380,
    margin=dict(l=40, r=30, t=60, b=40),
    legend_title_text="",
)

# -------------------------
# Components
# -------------------------
def info_card(title: str, main: str, sub: str, icon: str = ""):
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
                html.H4(main, className="mt-2 mb-1"),
                html.Div(sub, className="text-muted"),
            ]
        ),
        className="shadow-sm h-100",
        style={"borderRadius": "14px"},
    )

layout = dbc.Container(
    [
        html.H2("Müşteri Memnuniyetini Etkileyen Faktörler", className="mt-4"),
        html.P(
            "Sipariş deneyiminde hangi unsurlar müşteriyi mutsuz ediyor, hangileri memnuniyeti artırıyor?",
            className="text-muted",
        ),

        dbc.Row(
            [
                dbc.Col(
                    info_card(
                        "Müşteriyi en çok mutsuz eden faktör",
                        "Teslimat Süresi",
                        "Teslimat süresi uzadıkça 1 yıldızlı yorum ihtimali belirgin şekilde artıyor.",
                        icon="⚠️",
                    ),
                    md=6,
                ),
                dbc.Col(
                    info_card(
                        "5 yıldızlı deneyimi en çok zayıflatan faktör",
                        "Gecikme ve beklentinin aşılması",
                        "Sipariş beklenenden geç geldikçe 5 yıldızlı yorum ihtimali düşüyor.",
                        icon="⭐",
                    ),
                    md=6,
                ),
            ],
            className="g-3",
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        "Nasıl okunur? Sağa uzayan çubuklar mutsuzluk riskini artıran, sola uzayanlar memnuniyeti destekleyen etkiyi gösterir.",
                        className="text-muted",
                        style={"marginBottom": "10px"},
                    ),
                    dcc.Graph(figure=fig, config={"displayModeBar": True}),
                ]
            ),
            className="shadow-sm mt-3",
            style={"borderRadius": "14px"},
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Özet çıkarımlar", className="mb-2"),
                    html.Ul(
                        [
                            html.Li("Teslimat süresi ve gecikme arttıkça memnuniyetsizlik yükseliyor."),
                            html.Li("Çok satıcılı siparişler daha fazla sorun yaratıyor."),
                            html.Li("Fiyatın etkisi, operasyonel faktörlere kıyasla daha sınırlı."),
                        ],
                        className="mb-0",
                    ),
                ]
            ),
            className="shadow-sm mt-3",
            style={"borderRadius": "14px"},
        ),

        dbc.Alert(
            [
                html.B("Önerilen Aksiyonlar (Yönetim Perspektifi) "),
                html.Ul(
                    [
                        html.Li("Teslimat süresi için net SLA’ler belirleyin ve takip edin."),
                        html.Li("Gecikme ihtimali yüksek siparişleri proaktif yönetin (erken uyarı)."),
                        html.Li("Çok satıcılı siparişleri sadeleştirin veya operasyonel olarak optimize edin."),
                    ],
                    className="mb-0",
                ),
            ],
            color="primary",
            className="mt-3",
            style={"borderRadius": "12px"},
        ),
    ],
    fluid=True,
)
