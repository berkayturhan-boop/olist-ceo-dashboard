# pages/logit_insights.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/memnuniyet", name="Memnuniyet Sürücüleri")

# -----------------------------
# Modern Stil ve Renk Paleti
# -----------------------------
COLOR_RISK = "#E74C3C"          # 1★ Riski için uyarıcı kırmızı
COLOR_SATISFACTION = "#2E86C1"  # 5★ Kaybı için kurumsal mavi
CARD_STYLE = {"borderRadius": "20px", "border": "none", "backgroundColor": "#ffffff"}

def load_effects() -> pd.DataFrame:
    """
    Notebook analizindeki katsayılar (coef) baz alınmıştır.
    wait_time: 0.69 (1*) / -0.51 (5*)
    delay_vs_expected: 0.26 (1*) / -0.44 (5*)
    number_of_sellers: 0.23 (1*) / -0.17 (5*)
    """
    data = [
        ("Teslimat Süresi", 0.69, 0.51),
        ("Gecikme (Beklenti vs Gerçek)", 0.26, 0.44),
        ("Siparişteki Satıcı Sayısı", 0.23, 0.17),
        ("Müşteri-Satıcı Uzaklığı", 0.10, 0.06), # Mutlak değerler kullanılmıştır
        ("Kargo Ücreti", 0.11, 0.06),
        ("Ürün Fiyatı", 0.04, 0.03),
    ]
    return pd.DataFrame(data, columns=["Faktör", "Risk", "Memnuniyet_Kaybi"])

def build_modern_bar(df: pd.DataFrame, col: str, title: str, color: str, max_val: float):
    # En yüksek etkiyi en başa almak için azalan sıralama (Descending)
    d = df.sort_values(col, ascending=True).copy() 

    fig = px.bar(
        d, x=col, y="Faktör", orientation="h",
        text=col,
        title=f"<b>{title}</b>"
    )

    fig.update_traces(
        marker_color=color,
        texttemplate="<b>%{text:.2f}</b>", # Katsayıları vurgula
        textposition="outside",
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Göreceli Etki Gücü: %{x}<extra></extra>"
    )

    fig.update_layout(
        height=400,
        margin=dict(l=10, r=50, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=True, zerolinecolor="#d1d1d1", range=[0, max_val * 1.2], visible=False),
        yaxis=dict(tickfont=dict(size=13, color="#2c3e50"), showline=False, title=""),
        font=dict(family="Inter, Segoe UI, sans-serif"),
        title_font=dict(size=18, color="#2c3e50")
    )
    return fig

# Veri Hazırlığı
df = load_effects()
# İki grafik arası kıyaslanabilirlik için ortak üst sınır
max_range = max(df["Risk"].max(), df["Memnuniyet_Kaybi"].max())

fig_risk = build_modern_bar(df, "Risk", "▼ 1★ Riskini Tetikleyenler", COLOR_RISK, max_range)
fig_sat = build_modern_bar(df, "Memnuniyet_Kaybi", "✦ 5★ Kaybına Neden Olanlar", COLOR_SATISFACTION, max_range)

# Layout
layout = dbc.Container([
    # Başlık
    html.Div([
        html.H2("Operasyonel Memnuniyet Analizi", className="mt-4 fw-bold", style={"color": "#2c3e50"}),
        html.P("Lojistik regresyon katsayılarına göre operasyonel faktörlerin puanlar üzerindeki etkisi.", className="text-muted mb-4"),
    ]),

    # Üst KPI Kartları
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.Small("🚨 EN BÜYÜK RİSK", className="text-danger fw-bold"),
            html.H3("Teslimat Süresi", className="fw-bold mt-1"),
            html.P("Hız, müşteri memnuniyetsizliğinin birincil matematiksel sürücüsü.", className="text-muted small mb-0")
        ]), style=CARD_STYLE, className="shadow-sm"), md=6),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.Small("✨ SADAKAT KRİTERİ", className="text-primary fw-bold"),
            html.H3("Zamanında Teslim", className="fw-bold mt-1"),
            html.P("Gecikme, müşteriyi 5★ kategorisinden hızla uzaklaştırıyor.", className="text-muted small mb-0")
        ]), style=CARD_STYLE, className="shadow-sm"), md=6),
    ], className="g-4 mb-4"),

    # Grafikler
    dbc.Card(dbc.CardBody([
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_risk, config={"displayModeBar": False}), md=6),
            dbc.Col(dcc.Graph(figure=fig_sat, config={"displayModeBar": False}), md=6),
        ])
    ]), style=CARD_STYLE, className="shadow-sm mb-4"),

    # Çıkarımlar ve Aksiyonlar
    dbc.Row([
        dbc.Col(html.Div([
            html.H5("📌 Analizden Çıkarımlar", className="fw-bold"),
            html.Ul([
                html.Li("Lojistik performans (hız ve gecikme), fiyat etkisinden 15 kat daha baskındır."),
                html.Li("Gecikme (Delay), 5★ kaybetme olasılığını, 1★ alma olasılığından daha fazla etkiliyor."),
                html.Li("Müşteri-Satıcı mesafesi kontrol edildiğinde, uzak mesafelerde tolerans bir miktar artıyor."),
            ], className="mt-3")
        ]), md=7),
        dbc.Col(dbc.Alert([
            html.H5("🚀 Stratejik Öneriler", className="fw-bold"),
            html.Hr(),
            html.Ul([
                html.Li("Fiyat indiriminden ziyade teslimat hızını optimize etmeye odaklan."),
                html.Li("5★ sadakati için gecikme riskini proaktif olarak yönet."),
            ], className="ps-3")
        ], color="info", style={"borderRadius": "15px"}), md=5),
    ]),
], fluid=True, className="px-4 pb-5", style={"backgroundColor": "#f8f9fa", "minHeight": "100vh"})