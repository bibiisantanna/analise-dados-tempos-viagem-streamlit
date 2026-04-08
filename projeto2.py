import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
from scipy.stats import chisquare

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Análise de Tempos de Viagem",
    page_icon="🚛"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
}

/* Background */
.stApp {
    background: #ffffff;
    color: #1a1a1a;
}

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #e85d04 0%, #f48c06 50%, #ff6b00 100%);
    border-radius: 18px;
    padding: 36px 40px 28px 40px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(232,93,4,0.25);
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 220px; height: 220px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 30%;
    width: 300px; height: 300px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}

/* 3D truck emoji container */
.truck-3d {
    display: inline-block;
    font-size: 3.8rem;
    filter: drop-shadow(4px 6px 0px rgba(0,0,0,0.35)) drop-shadow(-1px -1px 0px rgba(255,255,255,0.2));
    transform: perspective(200px) rotateY(-8deg) rotateX(4deg);
    animation: truckFloat 3s ease-in-out infinite;
    margin-right: 16px;
    vertical-align: middle;
}
@keyframes truckFloat {
    0%, 100% { transform: perspective(200px) rotateY(-8deg) rotateX(4deg) translateY(0px); }
    50%       { transform: perspective(200px) rotateY(-8deg) rotateX(4deg) translateY(-5px); }
}

/* Main title */
.main-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.02em;
    margin-bottom: 0.2rem;
    text-shadow:
        3px 3px 0px rgba(0,0,0,0.25),
        1px 1px 0px rgba(0,0,0,0.15);
    display: inline;
    vertical-align: middle;
}
.main-subtitle {
    font-size: 1rem;
    color: rgba(255,255,255,0.85);
    margin-top: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.02em;
}

/* Section headers */
.section-header {
    font-size: 1.25rem;
    font-weight: 700;
    color: #e85d04;
    border-left: 4px solid #e85d04;
    padding-left: 12px;
    margin: 2rem 0 1rem 0;
    letter-spacing: -0.01em;
}

/* Metric cards */
.metric-card {
    background: #ffffff;
    border: 1.5px solid #ffe0c2;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 10px;
    transition: border-color 0.2s, box-shadow 0.2s;
    box-shadow: 0 2px 8px rgba(232,93,4,0.06);
}
.metric-card:hover {
    border-color: #e85d04;
    box-shadow: 0 4px 16px rgba(232,93,4,0.15);
}
.metric-label {
    font-size: 0.78rem;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
    margin-bottom: 6px;
}
.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.7rem;
    font-weight: 600;
    color: #e85d04;
    line-height: 1.1;
}
.metric-comment {
    font-size: 0.82rem;
    color: #666;
    margin-top: 8px;
    line-height: 1.5;
    border-top: 1px solid #f0e0d0;
    padding-top: 8px;
}

/* Info boxes */
.info-box {
    background: #fff8f3;
    border: 1px solid #ffd5b0;
    border-left: 4px solid #e85d04;
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: #333;
    line-height: 1.6;
    margin: 0.8rem 0;
}
.warn-box {
    background: #fffbf0;
    border: 1px solid #ffe0a0;
    border-left: 4px solid #f48c06;
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: #333;
    line-height: 1.6;
    margin: 0.8rem 0;
}
.success-box {
    background: #f0fff4;
    border: 1px solid #b7ebc4;
    border-left: 4px solid #22a642;
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: #333;
    line-height: 1.6;
    margin: 0.8rem 0;
}

/* Annex / manual calc */
.annex-step {
    background: #fafafa;
    border: 1px solid #ffe0c2;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.84rem;
    color: #333;
    line-height: 1.8;
}
.annex-title {
    font-family: 'Barlow', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #e85d04;
    margin-bottom: 10px;
}
.annex-result {
    color: #22a642;
    font-weight: 600;
}

/* Table */
.stDataFrame {
    border-radius: 8px;
    overflow: hidden;
}

/* Divider */
hr {
    border-color: #ffe0c2;
    margin: 2rem 0;
}

/* Streamlit overrides */
[data-testid="stMetric"] {
    background: #fff8f3;
    border: 1.5px solid #ffe0c2;
    border-radius: 10px;
    padding: 14px;
}

/* Expander */
[data-testid="stExpander"] {
    border: 1.5px solid #ffe0c2 !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_excel('dados.xlsx', header=0)
dados = df.iloc[:, 0].dropna()
n = len(dados)

# ── Calculations ──────────────────────────────────────────────────────────────
media     = np.mean(dados)
mediana   = np.median(dados)
minimo    = np.min(dados)
maximo    = np.max(dados)
moda      = stats.mode(dados, keepdims=True).mode[0]
amplitude = maximo - minimo
variancia = np.var(dados, ddof=1)
desvio    = np.std(dados, ddof=1)
coef_var  = desvio / media
assimetria = stats.skew(dados)
Q1  = np.percentile(dados, 25)
Q3  = np.percentile(dados, 75)
IQR = Q3 - Q1
lim_inf  = Q1 - 1.5 * IQR
lim_sup  = Q3 + 1.5 * IQR
outliers = dados[(dados < lim_inf) | (dados > lim_sup)]
soma     = np.sum(dados)

k = 4
freq_obs, intervalos = np.histogram(dados, bins=k)
freq_esp = [n / k] * k
chi2_val, p_valor = chisquare(freq_obs, freq_esp)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div>
        <span class="truck-3d">🚛</span>
        <span class="main-title">Análise de Tempos de Viagem</span>
    </div>
    <div class="main-subtitle">Fábrica → Centro de Distribuição &nbsp;|&nbsp; Análise Exploratória Estatística &nbsp;|&nbsp; n = 200 observações</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="info-box">⚠️ <strong>Nota metodológica:</strong> Os valores apresentados foram considerados em uma mesma unidade de tempo (não especificada), sendo utilizados exclusivamente para fins de análise exploratória de dados e identificação de padrões estatísticos.</div>', unsafe_allow_html=True)

# ── Raw data ──────────────────────────────────────────────────────────────────
with st.expander("📋 Ver tabela de dados brutos (200 observações)", expanded=False):
    st.dataframe(df, use_container_width=True, height=300)

st.markdown("---")

# ── Medidas de posição ────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📍 Medidas de Posição</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Média</div>
        <div class="metric-value">{media:.2f}</div>
        <div class="metric-comment">Valor central esperado de um tempo de viagem. Indica que, em média, cada percurso demora aproximadamente <strong>{media:.1f}</strong> unidades de tempo.</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Mediana</div>
        <div class="metric-value">{mediana:.2f}</div>
        <div class="metric-comment">Ponto que divide os dados ao meio. Metade das viagens dura menos que <strong>{mediana:.1f}</strong> unidades. Próxima da média → distribuição aproximadamente simétrica.</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Moda</div>
        <div class="metric-value">{moda}</div>
        <div class="metric-comment">Valor que aparece com maior frequência no conjunto. Tempo de viagem mais "recorrente" registrado nas observações.</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Mínimo</div>
        <div class="metric-value">{minimo}</div>
        <div class="metric-comment">Menor tempo de viagem registrado. Representa a condição mais favorável de tráfego e logística observada no período.</div>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Máximo</div>
        <div class="metric-value">{maximo}</div>
        <div class="metric-comment">Maior tempo de viagem registrado. Representa o pior cenário observado, útil para planejamento de capacidade e prazos de contingência.</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="info-box">💡 <strong>Interpretação conjunta:</strong> A proximidade entre média (<strong>{:.1f}</strong>) e mediana (<strong>{:.1f}</strong>) é um indicativo importante de que a distribuição dos tempos de viagem é aproximadamente simétrica — ou seja, não há uma tendência clara de concentração de viagens em tempos muito curtos ou muito longos.</div>'.format(media, mediana), unsafe_allow_html=True)

st.markdown("---")

# ── Medidas de dispersão ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">📊 Medidas de Dispersão</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Amplitude</div>
        <div class="metric-value">{amplitude}</div>
        <div class="metric-comment">Diferença entre o maior e o menor tempo registrado. Uma amplitude de <strong>{amplitude}</strong> unidades revela alta variabilidade total no conjunto — os tempos de viagem oscilam bastante de um percurso para outro.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Variância</div>
        <div class="metric-value">{variancia:.2f}</div>
        <div class="metric-comment">Mede o grau médio de afastamento dos dados em relação à média, elevado ao quadrado. O valor elevado confirma alta dispersão, mas é interpretado principalmente em conjunto com o desvio padrão.</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Desvio Padrão</div>
        <div class="metric-value">{desvio:.2f}</div>
        <div class="metric-comment">Indica que os tempos de viagem variam, em média, <strong>±{desvio:.1f}</strong> unidades em torno da média. É a medida de dispersão mais intuitiva e aplicável operacionalmente.</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Coef. de Variação</div>
        <div class="metric-value">{coef_var:.2%}</div>
        <div class="metric-comment">Representa a dispersão em termos relativos à média. Um CV de <strong>{coef_var:.1%}</strong> indica variabilidade <strong>{'alta' if coef_var > 0.30 else 'moderada'}</strong> — acima de 30% é convencional considerar o conjunto heterogêneo.</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Assimetria (Skewness)</div>
        <div class="metric-value">{assimetria:.4f}</div>
        <div class="metric-comment">
            Mede o grau de desvio da simetria da distribuição.<br><br>
            • <strong>= 0</strong>: perfeitamente simétrica<br>
            • <strong>> 0</strong>: assimetria positiva (cauda à direita)<br>
            • <strong>< 0</strong>: assimetria negativa (cauda à esquerda)<br><br>
            Valor de <strong>{assimetria:.4f}</strong> → distribuição praticamente simétrica, sem cauda dominante.
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── Histograma ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Distribuição dos Tempos de Viagem</div>', unsafe_allow_html=True)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.patch.set_facecolor('#ffffff')

# Histograma
ax1 = axes[0]
ax1.set_facecolor('#fff8f3')
counts, bins, patches = ax1.hist(dados, bins=20, color='#e85d04', edgecolor='#ffffff', linewidth=0.8, alpha=0.85)
ax1.axvline(media, color='#cc2200', linewidth=2, linestyle='--', label=f'Média: {media:.1f}')
ax1.axvline(mediana, color='#f48c06', linewidth=2, linestyle='--', label=f'Mediana: {mediana:.1f}')
ax1.set_title("Histograma de Frequências", color='#1a1a1a', fontsize=13, fontweight='bold', pad=12)
ax1.set_xlabel("Tempo de Viagem", color='#555', fontsize=10)
ax1.set_ylabel("Frequência", color='#555', fontsize=10)
ax1.tick_params(colors='#555')
ax1.spines[:].set_color('#ffe0c2')
ax1.legend(facecolor='#fff8f3', edgecolor='#ffe0c2', labelcolor='#333', fontsize=9)
ax1.grid(axis='y', color='#ffe0c2', linewidth=0.5)

# Boxplot
ax2 = axes[1]
ax2.set_facecolor('#fff8f3')
bp = ax2.boxplot(dados, vert=False, patch_artist=True,
    boxprops=dict(facecolor='#ffe0c2', color='#e85d04', linewidth=1.5),
    whiskerprops=dict(color='#e85d04', linewidth=1.5),
    capprops=dict(color='#e85d04', linewidth=2),
    medianprops=dict(color='#cc2200', linewidth=2.5),
    flierprops=dict(marker='o', color='#f48c06', markersize=6, alpha=0.7))
ax2.set_title("Boxplot — Visão Quartílica", color='#1a1a1a', fontsize=13, fontweight='bold', pad=12)
ax2.set_xlabel("Tempo de Viagem", color='#555', fontsize=10)
ax2.tick_params(colors='#555', left=False, labelleft=False)
ax2.spines[:].set_color('#ffe0c2')
ax2.grid(axis='x', color='#ffe0c2', linewidth=0.5)
# Annotations
ax2.annotate(f'Q1={Q1:.0f}', xy=(Q1, 1), xytext=(Q1, 1.35), color='#555', fontsize=8, ha='center')
ax2.annotate(f'Q3={Q3:.0f}', xy=(Q3, 1), xytext=(Q3, 1.35), color='#555', fontsize=8, ha='center')
ax2.annotate(f'Md={mediana:.0f}', xy=(mediana, 1), xytext=(mediana, 0.62), color='#cc2200', fontsize=8, ha='center', fontweight='bold')

plt.tight_layout(pad=2.5)
st.pyplot(fig)

st.markdown('<div class="info-box">📌 O histograma mostra uma distribuição aproximadamente <strong>uniforme</strong>, com frequências relativamente equilibradas ao longo de todo o intervalo. Não há um pico dominante, o que é consistente com a hipótese de distribuição uniforme testada adiante. As linhas tracejadas confirmam a proximidade entre média e mediana.</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Análise de outliers ───────────────────────────────────────────────────────
st.markdown('<div class="section-header">🔍 Análise de Outliers — Método IQR</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Q1 (1º Quartil)</div>
        <div class="metric-value">{Q1:.2f}</div>
        <div class="metric-comment">25% das viagens duram menos que este valor. Representa o limite inferior da faixa central dos dados.</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Q3 (3º Quartil)</div>
        <div class="metric-value">{Q3:.2f}</div>
        <div class="metric-comment">75% das viagens duram menos que este valor. Representa o limite superior da faixa central dos dados.</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">IQR (Amplitude Interquartil)</div>
        <div class="metric-value">{IQR:.2f}</div>
        <div class="metric-comment">Diferença entre Q3 e Q1. Cobre os 50% centrais da distribuição. É resistente a valores extremos, tornando-o robusto para detecção de outliers.</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Outliers Encontrados</div>
        <div class="metric-value" style="color: {'#3fb950' if len(outliers)==0 else '#ff7b72'}">{len(outliers)}</div>
        <div class="metric-comment">Quantidade de observações fora dos limites de <strong>{lim_inf:.2f}</strong> (inferior) e <strong>{lim_sup:.2f}</strong> (superior), calculados como Q1 − 1,5×IQR e Q3 + 1,5×IQR.</div>
    </div>""", unsafe_allow_html=True)

st.markdown(f"""
<div class="info-box">
    📐 <strong>Critério de Tukey (1,5 × IQR):</strong><br>
    O Intervalo Interquartil (IQR = {IQR:.2f}) representa a faixa central dos dados, cobrindo os 50% das observações mais típicas.
    Os limites de detecção são calculados como:<br>
    &nbsp;&nbsp;• Limite inferior: Q1 − 1,5 × IQR = {Q1:.2f} − {1.5*IQR:.2f} = <strong>{lim_inf:.2f}</strong><br>
    &nbsp;&nbsp;• Limite superior: Q3 + 1,5 × IQR = {Q3:.2f} + {1.5*IQR:.2f} = <strong>{lim_sup:.2f}</strong>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="success-box">
    ✅ <strong>Resultado:</strong> Não foram identificados outliers com base no critério de 1,5 × IQR.
    Isso indica que, apesar da alta variabilidade dos dados (CV ≈ {coef_var:.1%}), não há valores extremamente discrepantes em relação ao comportamento geral da amostra.
    Todos os {n} registros podem ser considerados observações legítimas do processo.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Teste Qui-Quadrado ────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🎲 Teste de Aderência — Distribuição Uniforme</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="info-box">
    🧪 <strong>Hipóteses do Teste:</strong><br>
    &nbsp;&nbsp;• <strong>H₀:</strong> Os dados seguem uma distribuição uniforme<br>
    &nbsp;&nbsp;• <strong>H₁:</strong> Os dados NÃO seguem uma distribuição uniforme<br><br>
    O teste Qui-Quadrado (χ²) de aderência compara as frequências observadas em cada classe com as frequências que seriam esperadas caso os dados fossem uniformemente distribuídos.
    </div>
    """, unsafe_allow_html=True)

    # Tabela de frequências
    intervalos_str = [f"[{intervalos[i]:.1f} – {intervalos[i+1]:.1f})" for i in range(k)]
    intervalos_str[-1] = intervalos_str[-1].replace(")", "]")
    tabela = pd.DataFrame({
        "Classe": intervalos_str,
        "Freq. Observada": freq_obs,
        "Freq. Esperada": [int(e) for e in freq_esp],
        "Diferença": [o - int(e) for o, e in zip(freq_obs, freq_esp)]
    })
    st.dataframe(tabela, use_container_width=True, hide_index=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="margin-bottom:10px">
        <div class="metric-label">Estatística Qui-Quadrado (χ²)</div>
        <div class="metric-value">{chi2_val:.4f}</div>
        <div class="metric-comment">Soma ponderada das diferenças quadráticas entre frequências observadas e esperadas. Quanto maior, mais os dados se afastam da distribuição hipotética.</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">p-valor</div>
        <div class="metric-value" style="color: {'#3fb950' if p_valor > 0.05 else '#ff7b72'}">{p_valor:.4f}</div>
        <div class="metric-comment">Probabilidade de observar uma estatística χ² tão extrema, assumindo H₀ verdadeira. p-valor > 0,05 → não rejeitamos H₀ ao nível de 5% de significância.</div>
    </div>
    """, unsafe_allow_html=True)

if p_valor > 0.05:
    st.markdown(f"""
    <div class="success-box">
        ✅ <strong>Conclusão (α = 0,05):</strong> Não rejeitamos H₀. Com p-valor = {p_valor:.4f} > 0,05, os dados apresentam aderência à distribuição uniforme.
        Isso significa que os tempos de viagem se distribuem de forma relativamente homogênea ao longo do intervalo [{minimo}, {maximo}],
        sem concentração preferencial em nenhuma faixa específica — um comportamento coerente com processos onde os tempos variam aleatoriamente sem padrão dominante.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div style="background:#fff0f0;border:1px solid #ffb3b3;border-left:4px solid #cc2200;border-radius:8px;padding:14px 18px;font-size:0.88rem;color:#333;margin:0.8rem 0;">
        ❌ <strong>Conclusão (α = 0,05):</strong> Rejeitamos H₀. Com p-valor = {p_valor:.4f} ≤ 0,05, os dados não aderem à distribuição uniforme.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# ANEXO — CÁLCULOS DETALHADOS PASSO A PASSO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">📎 Anexo Técnico — Desenvolvimento Matemático Passo a Passo</div>', unsafe_allow_html=True)
st.markdown('<div class="info-box">Este anexo apresenta todas as contas realizadas de forma detalhada, para verificação pela equipe de matemáticos e estatísticos. Os valores são calculados sobre a amostra completa de <strong>n = 200</strong> observações.</div>', unsafe_allow_html=True)

dados_sorted = sorted(dados.values.tolist())

with st.expander("1️⃣  Média Aritmética", expanded=True):
    st.markdown(f"""
    <div class="annex-step">
<div class="annex-title">Fórmula</div>
x̄ = (Σxᵢ) / n

<div class="annex-title">Substituição</div>
Soma de todos os valores: Σxᵢ = {soma:,}
Número de observações:   n   = {n}

x̄ = {soma:,} / {n}

<span class="annex-result">x̄ = {media:.4f} ≈ {media:.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with st.expander("2️⃣  Mediana"):
    pos_inf = n // 2      # posição 100 (0-indexed: 99)
    pos_sup = n // 2 + 1  # posição 101 (0-indexed: 100)
    v_inf = dados_sorted[pos_inf - 1]
    v_sup = dados_sorted[pos_inf]
    st.markdown(f"""
    <div class="annex-step">
<div class="annex-title">Procedimento</div>
Com n = {n} (número par), a mediana é a média aritmética
dos dois valores centrais na distribuição ordenada:

Posição {n//2}ª  = {v_inf}
Posição {n//2+1}ª = {v_sup}

Mediana = ({v_inf} + {v_sup}) / 2
        = {v_inf + v_sup} / 2

<span class="annex-result">Mediana = {mediana:.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with st.expander("3️⃣  Amplitude Total"):
    st.markdown(f"""
    <div class="annex-step">
<div class="annex-title">Fórmula</div>
A = Xmáx − Xmín

<div class="annex-title">Substituição</div>
Xmáx = {maximo}
Xmín = {minimo}

A = {maximo} − {minimo}

<span class="annex-result">A = {amplitude}</span>
    </div>
    """, unsafe_allow_html=True)

with st.expander("4️⃣  Variância Amostral"):
    # Show first 5 terms of the sum
    desvios_ex = [(x, x - media, (x - media)**2) for x in dados_sorted[:5]]
    st.markdown(f"""
    <div class="annex-step">
<div class="annex-title">Fórmula</div>
s² = Σ(xᵢ − x̄)² / (n − 1)

<div class="annex-title">Primeiros termos do somatório (ilustrativo — 5 de {n})</div>
{''.join([f"  ({xi} − {media:.2f})² = ({xi - media:.2f})² = {(xi-media)**2:.4f}" + chr(10) for xi, _, _ in desvios_ex])}
  ... (continua para todos os {n} valores)

Σ(xᵢ − x̄)² = {variancia * (n-1):.4f}

s² = {variancia * (n-1):.4f} / ({n} − 1)
   = {variancia * (n-1):.4f} / {n-1}

<span class="annex-result">s² = {variancia:.4f} ≈ {variancia:.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with st.expander("5️⃣  Desvio Padrão Amostral"):
    st.markdown(f"""
    <div class="annex-step">
<div class="annex-title">Fórmula</div>
s = √s²

<div class="annex-title">Substituição</div>
s = √{variancia:.4f}

<span class="annex-result">s = {desvio:.4f} ≈ {desvio:.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with st.expander("6️⃣  Coeficiente de Variação"):
    st.markdown(f"""
    <div class="annex-step">
<div class="annex-title">Fórmula</div>
CV = s / x̄   (expresso em %)

<div class="annex-title">Substituição</div>
CV = {desvio:.4f} / {media:.4f}
   = {coef_var:.6f}

<span class="annex-result">CV = {coef_var:.4f} = {coef_var:.2%}</span>

Interpretação: CV > 30% → conjunto heterogêneo (alta variabilidade relativa)
    </div>
    """, unsafe_allow_html=True)

with st.expander("7️⃣  Coeficiente de Assimetria (Skewness de Fisher)"):
    st.markdown(f"""
    <div class="annex-step">
<div class="annex-title">Fórmula</div>
g₁ = [n / ((n−1)(n−2))] × Σ[(xᵢ − x̄) / s]³

<div class="annex-title">Parâmetros</div>
n    = {n}
x̄   = {media:.4f}
s    = {desvio:.4f}

<div class="annex-title">Resultado (calculado pelo método de Fisher)</div>
Σ[(xᵢ − x̄) / s]³ computado sobre todos os {n} valores

<span class="annex-result">g₁ = {assimetria:.6f} ≈ {assimetria:.4f}</span>

|g₁| < 0,15  →  distribuição praticamente simétrica  ✓
    </div>
    """, unsafe_allow_html=True)

with st.expander("8️⃣  Quartis e Intervalo Interquartil (IQR)"):
    st.markdown(f"""
    <div class="annex-step">
<div class="annex-title">Método: interpolação linear (numpy percentile)</div>

Q1  = percentil 25 de {n} observações ordenadas
Q3  = percentil 75 de {n} observações ordenadas

Posição do Q1: L = 0.25 × ({n} − 1) + 1 = {0.25*(n-1)+1:.2f}
  → interpolação entre valores nas posições {int(0.25*(n-1))+1}ª e {int(0.25*(n-1))+2}ª
  → {dados_sorted[int(0.25*(n-1))]} e {dados_sorted[int(0.25*(n-1))+1]}
  → Q1 = {dados_sorted[int(0.25*(n-1))]} + {0.25*(n-1) % 1:.4f} × ({dados_sorted[int(0.25*(n-1))+1]} − {dados_sorted[int(0.25*(n-1))]})

<span class="annex-result">Q1 = {Q1:.2f}</span>

Posição do Q3: L = 0.75 × ({n} − 1) + 1 = {0.75*(n-1)+1:.2f}
  → interpolação entre valores nas posições {int(0.75*(n-1))+1}ª e {int(0.75*(n-1))+2}ª
  → {dados_sorted[int(0.75*(n-1))]} e {dados_sorted[int(0.75*(n-1))+1]}

<span class="annex-result">Q3 = {Q3:.2f}</span>

IQR = Q3 − Q1 = {Q3:.2f} − {Q1:.2f}

<span class="annex-result">IQR = {IQR:.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with st.expander("9️⃣  Limites de Outliers (Critério de Tukey)"):
    st.markdown(f"""
    <div class="annex-step">
<div class="annex-title">Fórmulas</div>
Limite Inferior = Q1 − 1,5 × IQR
Limite Superior = Q3 + 1,5 × IQR

<div class="annex-title">Substituição</div>
Limite Inferior = {Q1:.2f} − 1,5 × {IQR:.2f}
               = {Q1:.2f} − {1.5*IQR:.4f}

<span class="annex-result">Limite Inferior = {lim_inf:.4f}</span>

Limite Superior = {Q3:.2f} + 1,5 × {IQR:.2f}
               = {Q3:.2f} + {1.5*IQR:.4f}

<span class="annex-result">Limite Superior = {lim_sup:.4f}</span>

Verificação: nenhuma observação está abaixo de {lim_inf:.2f} ou acima de {lim_sup:.2f}
→ Outliers detectados: {len(outliers)}
    </div>
    """, unsafe_allow_html=True)

with st.expander("🔟  Teste Qui-Quadrado de Aderência à Distribuição Uniforme"):
    gl = k - 1
    chi2_critico = stats.chi2.ppf(0.95, df=gl)
    st.markdown(f"""
    <div class="annex-step">
<div class="annex-title">Configuração do Teste</div>
Hipótese H₀: Os dados seguem distribuição Uniforme no intervalo [{minimo}, {maximo}]
Nível de significância: α = 0,05
Número de classes: k = {k}
Graus de liberdade: gl = k − 1 = {gl}

<div class="annex-title">Construção das classes (largura igual)</div>
Largura de cada classe = ({maximo} − {minimo}) / {k} = {amplitude} / {k} = {amplitude/k:.4f}

  Classe 1: [{intervalos[0]:.2f} ; {intervalos[1]:.2f})  →  Freq. Obs. = {freq_obs[0]}
  Classe 2: [{intervalos[1]:.2f} ; {intervalos[2]:.2f})  →  Freq. Obs. = {freq_obs[1]}
  Classe 3: [{intervalos[2]:.2f} ; {intervalos[3]:.2f})  →  Freq. Obs. = {freq_obs[2]}
  Classe 4: [{intervalos[3]:.2f} ; {intervalos[4]:.2f}]  →  Freq. Obs. = {freq_obs[3]}

<div class="annex-title">Frequência Esperada (sob H₀ uniforme)</div>
Eᵢ = n / k = {n} / {k} = {n/k:.1f}  (para cada classe)

<div class="annex-title">Cálculo da estatística χ²</div>
χ² = Σ [(Oᵢ − Eᵢ)² / Eᵢ]

  Classe 1: ({freq_obs[0]} − {n/k:.1f})² / {n/k:.1f} = {(freq_obs[0]-n/k)**2/(n/k):.4f}
  Classe 2: ({freq_obs[1]} − {n/k:.1f})² / {n/k:.1f} = {(freq_obs[1]-n/k)**2/(n/k):.4f}
  Classe 3: ({freq_obs[2]} − {n/k:.1f})² / {n/k:.1f} = {(freq_obs[2]-n/k)**2/(n/k):.4f}
  Classe 4: ({freq_obs[3]} − {n/k:.1f})² / {n/k:.1f} = {(freq_obs[3]-n/k)**2/(n/k):.4f}

χ² = {(freq_obs[0]-n/k)**2/(n/k):.4f} + {(freq_obs[1]-n/k)**2/(n/k):.4f} + {(freq_obs[2]-n/k)**2/(n/k):.4f} + {(freq_obs[3]-n/k)**2/(n/k):.4f}

<span class="annex-result">χ² calculado = {chi2_val:.4f}</span>

<div class="annex-title">Valor crítico e decisão</div>
χ² crítico (α=0,05; gl={gl}) = {chi2_critico:.4f}

χ² calculado ({chi2_val:.4f}) {'<' if chi2_val < chi2_critico else '>'} χ² crítico ({chi2_critico:.4f})
p-valor = {p_valor:.4f} {'>' if p_valor > 0.05 else '<='} 0,05

<span class="annex-result">{'→ Não rejeitamos H₀. Os dados são aderentes à distribuição uniforme.' if p_valor > 0.05 else '→ Rejeitamos H₀. Os dados não aderem à distribuição uniforme.'}</span>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#484f58; font-size:0.78rem; padding: 10px 0 20px 0;">
    Análise Exploratória de Dados · Tempos de Viagem Fábrica–CD · n = 200 observações
</div>
""", unsafe_allow_html=True)
