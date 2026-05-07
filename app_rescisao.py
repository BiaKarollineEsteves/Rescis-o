import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime

st.set_page_config(
    page_title="Rescisão de Representante Comercial — Grupo LLE",
    page_icon="📊",
    layout="wide"
)

# ─── UFIR-RJ TABLE ────────────────────────────────────────────────────────────
UFIR_TABLE = {
    2010: 2.0183, 2011: 2.1352, 2012: 2.2752, 2013: 2.4066,
    2014: 2.5473, 2015: 2.7119, 2016: 3.0023, 2017: 3.1999,
    2018: 3.2939, 2019: 3.4211, 2020: 3.5550, 2021: 3.7053,
    2022: 4.0915, 2023: 4.3329, 2024: 4.5373, 2025: 4.7508,
    2026: 4.9604,
}

MESES_PT = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
            7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}

# ─── STYLES ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }

.header-box {
    background: linear-gradient(135deg, #0071FE 0%, #0050BB 100%);
    color: white;
    padding: 28px 36px;
    border-radius: 14px;
    margin-bottom: 24px;
}
.header-box h1 { margin: 0; font-size: 1.8rem; font-weight: 800; }
.header-box p  { margin: 4px 0 0; font-size: 1rem; opacity: 0.9; }

.metric-card {
    background: white;
    border-radius: 12px;
    padding: 20px 24px;
    border-left: 5px solid #0071FE;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    margin-bottom: 12px;
}
.metric-card.yellow { border-left-color: #FAC318; }
.metric-card.green  { border-left-color: #0F8C3B; }
.metric-card.red    { border-left-color: #D32F2F; }

.metric-card .label { font-size: 0.78rem; color: #666; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.metric-card .value { font-size: 1.55rem; font-weight: 800; color: #1a1a1a; margin-top: 4px; }
.metric-card .sub   { font-size: 0.8rem; color: #888; margin-top: 2px; }

.section-title {
    font-size: 1rem; font-weight: 700; color: #0071FE;
    border-bottom: 2px solid #0071FE;
    padding-bottom: 6px; margin: 24px 0 14px;
    text-transform: uppercase; letter-spacing: 0.5px;
}

.audit-ok    { color: #0F8C3B; font-weight: 700; }
.audit-warn  { color: #E65100; font-weight: 700; }
.audit-fail  { color: #D32F2F; font-weight: 700; }

.rc-info {
    background: #F0F6FF; border-radius: 10px;
    padding: 16px 20px; margin-bottom: 20px;
    border: 1px solid #C5DAFF;
}
.rc-info b { color: #0071FE; }

.footer {
    text-align: center; color: #aaa; font-size: 0.75rem;
    margin-top: 40px; padding-top: 16px; border-top: 1px solid #eee;
}
</style>
""", unsafe_allow_html=True)

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
  <h1>📋 Rescisão de Representante Comercial</h1>
  <p>Grupo LLE — Departamento Financeiro · Lei 4.886/65</p>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configurações")

    uploaded = st.file_uploader(
        "📂 Carregar planilha do ERP",
        type=["xls", "xlsx"],
        help="Arquivo exportado do financeiro (mesmo formato do sistema)"
    )

    st.markdown("---")
    st.markdown("### 📅 UFIR-RJ")
    ano_atual = datetime.now().year
    ufir_default = UFIR_TABLE.get(ano_atual, 4.9604)
    ufir_atual = st.number_input(
        f"UFIR-RJ {ano_atual}",
        value=ufir_default, min_value=0.01, step=0.0001, format="%.4f"
    )
    UFIR_TABLE[ano_atual] = ufir_atual

    st.markdown("---")
    st.markdown("### 💰 IRRF")
    reter_irrf = st.radio("Reter IRRF (15%)?", ["Não", "Sim"], index=0)

    st.markdown("---")
    st.markdown("### 📖 Tabela UFIR-RJ")
    df_ufir_show = pd.DataFrame(list(UFIR_TABLE.items()), columns=["Ano","UFIR-RJ"])
    st.dataframe(df_ufir_show, hide_index=True, use_container_width=True, height=320)


# ─── HELPERS ─────────────────────────────────────────────────────────────────
def detect_header_row(df_raw):
    """Find row that contains 'Vlr do Desdobramento' or similar."""
    for i, row in df_raw.iterrows():
        vals = [str(v).strip() for v in row if pd.notna(v)]
        joined = " ".join(vals)
        if "Vlr do Desdobramento" in joined or "Vlr Desdobramento" in joined:
            return i
    return 2  # fallback

def load_and_filter(file):
    ext = file.name.split(".")[-1].lower()
    engine = "xlrd" if ext == "xls" else "openpyxl"
    df_raw = pd.read_excel(file, sheet_name=0, header=None, engine=engine)
    header_row = detect_header_row(df_raw)
    df = pd.read_excel(
        io.BytesIO(file.getvalue()), sheet_name=0,
        header=header_row, engine=engine
    )
    df.columns = [str(c).strip() for c in df.columns]

    # find value column
    val_col = next((c for c in df.columns if "Vlr" in c and "Desdobramento" in c), None)
    if val_col is None:
        val_col = next((c for c in df.columns if "Vlr" in c), None)

    # find natureza column
    nat_col = next((c for c in df.columns if "Natureza" in c or "natureza" in c.lower()), None)

    # find date columns
    baixa_col = next((c for c in df.columns if "Data Baixa" in c or "Data_Baixa" in c), None)
    if baixa_col is None:
        baixa_col = next((c for c in df.columns if "Baixa" in c and "Dt" in c), None)
    neg_col = next((c for c in df.columns if "Negociação" in c or "Negociacao" in c), None)

    # find partner columns
    parceiro_col = next((c for c in df.columns if c == "Parceiro"), None)
    nome_col = next((c for c in df.columns if "Nome Parceiro" in c), None)

    return df, val_col, nat_col, baixa_col, neg_col, parceiro_col, nome_col

def filter_commissions(df, val_col, nat_col, baixa_col):
    if nat_col:
        mask = df[nat_col].astype(str).str.contains("Comissão s/ vendas|Comissao s/ vendas", case=False, na=False)
        df_f = df[mask].copy()
    else:
        df_f = df.copy()

    # drop totals / NaN rows
    df_f = df_f.dropna(subset=[val_col])
    df_f = df_f[pd.to_numeric(df_f[val_col], errors='coerce').notna()]
    df_f[val_col] = pd.to_numeric(df_f[val_col], errors='coerce')
    df_f = df_f[df_f[val_col] > 0]

    if baixa_col:
        df_f[baixa_col] = pd.to_datetime(df_f[baixa_col], errors='coerce')
        df_f = df_f.dropna(subset=[baixa_col])
        df_f["Mês"]  = df_f[baixa_col].dt.month
        df_f["Ano"]  = df_f[baixa_col].dt.year
    else:
        # try Dt. Negociação
        for col in df_f.columns:
            if "Negoci" in col:
                df_f[col] = pd.to_datetime(df_f[col], errors='coerce')
                df_f["Mês"] = df_f[col].dt.month
                df_f["Ano"] = df_f[col].dt.year
                break

    return df_f

def build_monthly(df_f, val_col):
    grp = df_f.groupby(["Ano","Mês"])[val_col].sum().reset_index()
    grp.columns = ["Ano","Mês","Valor"]
    grp = grp.sort_values(["Ano","Mês"]).reset_index(drop=True)
    grp["Mês/Ano"] = grp.apply(lambda r: f"{MESES_PT[int(r['Mês'])]}/{int(r['Ano'])}", axis=1)
    return grp

def build_annual(grp):
    ann = grp.groupby("Ano")["Valor"].sum().reset_index()
    ann.columns = ["Ano","Comissão Bruta"]
    ann["UFIR do Ano"] = ann["Ano"].apply(lambda y: UFIR_TABLE.get(int(y), np.nan))
    ufir_atual_val = UFIR_TABLE.get(ano_atual, 4.9604)
    ann["Comissão Corrigida"] = ann.apply(
        lambda r: ufir_atual_val * r["Comissão Bruta"] / r["UFIR do Ano"]
                  if pd.notna(r["UFIR do Ano"]) and r["UFIR do Ano"] > 0 else r["Comissão Bruta"],
        axis=1
    )
    return ann

def calcular_indenizacao(ann, grp):
    total_bruto = ann["Comissão Bruta"].sum()
    total_corrigido = ann["Comissão Corrigida"].sum()
    indenizacao_112 = total_corrigido / 12

    # aviso prévio: últimos 3 meses
    ultimos3 = grp.tail(3)
    base_aviso = ultimos3["Valor"].sum()
    aviso_previo = base_aviso / 3

    bruta = indenizacao_112 + aviso_previo
    irrf = bruta * 0.15 if reter_irrf == "Sim" else 0.0
    liquido = bruta - irrf

    return {
        "total_bruto": total_bruto,
        "total_corrigido": total_corrigido,
        "indenizacao_112": indenizacao_112,
        "base_aviso": base_aviso,
        "ultimos3": ultimos3,
        "aviso_previo": aviso_previo,
        "bruta": bruta,
        "irrf": irrf,
        "liquido": liquido,
    }

def fmt_brl(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

def run_auditoria(df_f, grp, ann, calc, val_col, nat_col):
    checks = []

    def chk(num, cat, desc, resultado, status, detalhe=""):
        icon = {"ok":"✅","warn":"⚠️","fail":"❌"}[status]
        checks.append({"#":num,"Categoria":cat,"Verificação":desc,
                        "Resultado":resultado,"Status":icon+" "+({"ok":"OK","warn":"ALERTA","fail":"FALHA"}[status]),
                        "Detalhe":detalhe})

    n = len(df_f)
    # 1
    if nat_col:
        todos_com = df_f[nat_col].astype(str).str.contains("Comissão|Comissao", case=False).all()
        chk(1,"Integridade","Filtro só contém registros de comissão?",
            f"{n} de {n}", "ok" if todos_com else "fail",
            "Todos os registros são de comissão" if todos_com else "Verificar filtro")
    else:
        chk(1,"Integridade","Filtro só contém registros de comissão?","N/A (coluna Natureza não encontrada)","warn","Coluna de natureza não identificada")

    # 2
    chk(2,"Integridade","Todos os registros têm Data Baixa?",f"{n} de {n}","ok","Todas as datas preenchidas")

    # 3
    neg_zero = (df_f[val_col] <= 0).sum()
    chk(3,"Integridade","Algum valor negativo ou zero?",f"{neg_zero} registros",
        "ok" if neg_zero==0 else "fail",
        "Todos os valores são positivos" if neg_zero==0 else f"{neg_zero} valores ≤ 0")

    # 4
    chk(4,"Integridade","Quantidade de registros > 0?",f"{n} registros","ok" if n>0 else "fail","")

    # 5
    anos_sem_ufir = [int(a) for a in ann["Ano"] if int(a) not in UFIR_TABLE]
    chk(5,"Integridade","Todos os anos têm UFIR na tabela?",
        f"{len(ann)-len(anos_sem_ufir)} de {len(ann)}",
        "ok" if not anos_sem_ufir else "warn",
        "OK" if not anos_sem_ufir else f"Faltam: {anos_sem_ufir}")

    # 6
    t_f = df_f[val_col].sum()
    t_g = grp["Valor"].sum()
    chk(6,"Cruzamento","Total filtrado = Total base mensal?",
        f"{fmt_brl(t_f)} vs {fmt_brl(t_g)}",
        "ok" if abs(t_f-t_g)<0.02 else "fail","")

    # 7
    t_a = ann["Comissão Bruta"].sum()
    chk(7,"Cruzamento","Total filtrado = Total anual (Dashboard)?",
        f"{fmt_brl(t_f)} vs {fmt_brl(t_a)}",
        "ok" if abs(t_f-t_a)<0.02 else "fail","")

    # 8
    ufir_dash = UFIR_TABLE.get(ano_atual, None)
    ufir_tab  = UFIR_TABLE.get(ano_atual, None)
    chk(8,"Cruzamento","UFIR Ano Atual no Dashboard = tabela UFIR?",
        f"{ufir_dash} vs {ufir_tab}","ok","UFIR consistente")

    # 9
    base_aviso_r = calc["base_aviso"]
    aviso_calc   = calc["ultimos3"]["Valor"].sum()
    chk(9,"Cruzamento","Aviso Prévio base = 3 últimos meses?",
        f"{fmt_brl(base_aviso_r)} vs {fmt_brl(aviso_calc)}",
        "ok" if abs(base_aviso_r-aviso_calc)<0.02 else "fail","")

    # 10
    chk(10,"Lógica","Comissão Corrigida ≥ Comissão Bruta?",
        f"{fmt_brl(calc['total_corrigido'])} vs {fmt_brl(calc['total_bruto'])}",
        "ok" if calc["total_corrigido"] >= calc["total_bruto"]-0.01 else "warn",
        f"Correção: +{(calc['total_corrigido']/calc['total_bruto']-1)*100:.1f}%" if calc["total_bruto"]>0 else "")

    # 11
    ind_check = calc["total_corrigido"] / 12
    chk(11,"Lógica","Indenização = Corrigida/12?",
        f"{fmt_brl(calc['indenizacao_112'])} vs {fmt_brl(ind_check)}",
        "ok" if abs(calc["indenizacao_112"]-ind_check)<0.02 else "fail","")

    # 12
    aviso_check = calc["base_aviso"] / 3
    chk(12,"Lógica","Aviso Prévio = Base/3?",
        f"{fmt_brl(calc['aviso_previo'])} vs {fmt_brl(aviso_check)}",
        "ok" if abs(calc["aviso_previo"]-aviso_check)<0.02 else "fail","")

    # 13
    bruta_check = calc["indenizacao_112"] + calc["aviso_previo"]
    chk(13,"Lógica","Indenização Bruta = 1/12 + Aviso Prévio?",
        f"{fmt_brl(calc['bruta'])} vs {fmt_brl(bruta_check)}",
        "ok" if abs(calc["bruta"]-bruta_check)<0.02 else "fail","")

    # 14
    if reter_irrf == "Sim":
        irrf_check = calc["bruta"] * 0.15
        chk(14,"Lógica","IRRF = 15% da Bruta?",
            f"{fmt_brl(calc['irrf'])} vs {fmt_brl(irrf_check)}",
            "ok" if abs(calc["irrf"]-irrf_check)<0.02 else "fail","")
    else:
        chk(14,"Lógica","IRRF (se retido) = 15% da Bruta?","N/A (não retido)","ok","IRRF não retido")

    # 15
    liq_check = calc["bruta"] - calc["irrf"]
    chk(15,"Lógica","Valor Líquido = Bruta - IRRF?",
        f"{fmt_brl(calc['liquido'])} vs {fmt_brl(liq_check)}",
        "ok" if abs(calc["liquido"]-liq_check)<0.02 else "fail","")

    # 16 - IRRF alerta
    chk(16,"Risco","IRRF não retido — intencional?",
        "Não" if reter_irrf=="Não" else "Sim",
        "warn" if reter_irrf=="Não" else "ok",
        "IRRF não retido — confirmar decisão" if reter_irrf=="Não" else "IRRF retido conforme configurado")

    # 17 - indenização material
    chk(17,"Risco","Indenização material (> R$ 10.000)?",
        fmt_brl(calc["bruta"]),
        "warn" if calc["bruta"]>10000 else "ok",
        "Valor acima de R$ 10.000 — atenção" if calc["bruta"]>10000 else "Valor dentro do limite")

    # 18 - correção > 10%
    corr_pct = (calc["total_corrigido"]/calc["total_bruto"]-1)*100 if calc["total_bruto"]>0 else 0
    chk(18,"Risco","Correção monetária > 10%?",
        f"{corr_pct:.1f}%",
        "warn" if corr_pct>10 else "ok",
        "Correção significativa" if corr_pct>10 else "Correção dentro de 10%")

    # 19 - algum mês > 20% do total
    if len(grp)>0:
        max_mes_pct = grp["Valor"].max() / grp["Valor"].sum() * 100
        chk(19,"Risco","Algum mês > 20% do total?",
            f"{max_mes_pct:.0f}%",
            "warn" if max_mes_pct>20 else "ok",
            f"Mês com maior peso: {max_mes_pct:.0f}%")

    # 20 - CV
    if len(grp)>1:
        cv = grp["Valor"].std() / grp["Valor"].mean() * 100
        chk(20,"Risco","Coeficiente de variação > 50%?",
            f"{cv:.0f}%",
            "warn" if cv>50 else "ok",
            "Alta variabilidade" if cv>50 else "Variação aceitável")

    return pd.DataFrame(checks)


# ─── MAIN ─────────────────────────────────────────────────────────────────────
if not uploaded:
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px; color: #888;">
        <div style="font-size: 3rem;">📤</div>
        <h3 style="color:#555;">Carregue a planilha exportada do ERP</h3>
        <p>Formatos aceitos: <b>.xls</b> ou <b>.xlsx</b><br>
        A planilha deve conter as colunas de comissão do sistema financeiro.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── LOAD ──
try:
    df, val_col, nat_col, baixa_col, neg_col, parceiro_col, nome_col = load_and_filter(uploaded)
except Exception as e:
    st.error(f"Erro ao ler o arquivo: {e}")
    st.stop()

if val_col is None:
    st.error("Não foi possível identificar a coluna de valor (Vlr do Desdobramento). Verifique o arquivo.")
    st.stop()

df_f = filter_commissions(df, val_col, nat_col, baixa_col if baixa_col else neg_col)

if len(df_f) == 0:
    st.warning("Nenhum registro de comissão encontrado na planilha.")
    st.stop()

grp = build_monthly(df_f, val_col)
ann = build_annual(grp)
calc = calcular_indenizacao(ann, grp)

# ── RC INFO ──
rc_code = df_f[parceiro_col].iloc[0] if parceiro_col and parceiro_col in df_f.columns else "—"
rc_nome = df_f[nome_col].iloc[0] if nome_col and nome_col in df_f.columns else "—"
periodo_ini = f"{MESES_PT[int(grp['Mês'].iloc[0])]}/{int(grp['Ano'].iloc[0])}"
periodo_fim = f"{MESES_PT[int(grp['Mês'].iloc[-1])]}/{int(grp['Ano'].iloc[-1])}"

st.markdown(f"""
<div class="rc-info">
  <b>Representante:</b> {rc_nome} &nbsp;·&nbsp;
  <b>Código:</b> {rc_code} &nbsp;·&nbsp;
  <b>Período:</b> {periodo_ini} a {periodo_fim} &nbsp;·&nbsp;
  <b>Registros:</b> {len(df_f)}
</div>
""", unsafe_allow_html=True)

# ── TABS ──
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📅 Comissões Mensais", "📋 Dados Filtrados", "🔎 Auditoria"])

# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Total Comissões Brutas</div>
            <div class="value">{fmt_brl(calc['total_bruto'])}</div>
            <div class="sub">{len(grp)} meses</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Total Corrigido (UFIR)</div>
            <div class="value">{fmt_brl(calc['total_corrigido'])}</div>
            <div class="sub">UFIR {ano_atual} = {UFIR_TABLE[ano_atual]}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card yellow">
            <div class="label">Indenização Bruta</div>
            <div class="value">{fmt_brl(calc['bruta'])}</div>
            <div class="sub">1/12 avos + Aviso Prévio 1/3</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        card_class = "green" if reter_irrf == "Não" else "red"
        irrf_info = "IRRF não retido" if reter_irrf == "Não" else f"IRRF: {fmt_brl(calc['irrf'])}"
        st.markdown(f"""<div class="metric-card {card_class}">
            <div class="label">Valor Líquido a Pagar</div>
            <div class="value">{fmt_brl(calc['liquido'])}</div>
            <div class="sub">{irrf_info}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Comissões por Ano — Correção UFIR-RJ</div>', unsafe_allow_html=True)

    col_tabela, col_grafico = st.columns([1, 1])

    with col_tabela:
        ann_display = ann.copy()
        ann_display["Comissão Bruta"]    = ann_display["Comissão Bruta"].apply(fmt_brl)
        ann_display["Comissão Corrigida"] = ann_display["Comissão Corrigida"].apply(fmt_brl)
        ann_display["UFIR do Ano"]       = ann_display["UFIR do Ano"].apply(lambda v: f"{v:.4f}" if pd.notna(v) else "N/D")
        ann_display["Ano"] = ann_display["Ano"].astype(int)

        # total row
        total_row = pd.DataFrame([{
            "Ano": "TOTAL",
            "Comissão Bruta": fmt_brl(calc['total_bruto']),
            "UFIR do Ano": "—",
            "Comissão Corrigida": fmt_brl(calc['total_corrigido'])
        }])
        ann_display = pd.concat([ann_display.astype(str), total_row], ignore_index=True)
        st.dataframe(ann_display, hide_index=True, use_container_width=True)

    with col_grafico:
        chart_data = ann.set_index("Ano")[["Comissão Bruta","Comissão Corrigida"]]
        chart_data.index = chart_data.index.astype(int)
        st.bar_chart(chart_data, color=["#0071FE","#FAC318"])

    st.markdown('<div class="section-title">Detalhamento do Cálculo</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**🏦 Indenização (1/12 Avos)**")
        st.markdown(f"""
        | Item | Valor |
        |---|---|
        | Base de Indenização (Total Corrigido) | **{fmt_brl(calc['total_corrigido'])}** |
        | ÷ 12 = Indenização 1/12 Avos | **{fmt_brl(calc['indenizacao_112'])}** |
        """)

    with col_b:
        ultimos3_str = " · ".join(calc['ultimos3']['Mês/Ano'].tolist())
        st.markdown("**📅 Aviso Prévio (1/3)**")
        st.markdown(f"""
        | Item | Valor |
        |---|---|
        | Últimos 3 meses: {ultimos3_str} | — |
        | Base Aviso Prévio (soma) | **{fmt_brl(calc['base_aviso'])}** |
        | ÷ 3 = Aviso Prévio 1/3 | **{fmt_brl(calc['aviso_previo'])}** |
        """)

    st.markdown("---")
    col_x, col_y, col_z = st.columns(3)

    with col_x:
        st.markdown(f"""<div class="metric-card yellow">
            <div class="label">🟡 Indenização 1/12 + Aviso 1/3 = Bruta</div>
            <div class="value">{fmt_brl(calc['bruta'])}</div>
            <div class="sub">{fmt_brl(calc['indenizacao_112'])} + {fmt_brl(calc['aviso_previo'])}</div>
        </div>""", unsafe_allow_html=True)
    with col_y:
        st.markdown(f"""<div class="metric-card red">
            <div class="label">🔴 IRRF (15%) — {"Retido" if reter_irrf=="Sim" else "NÃO Retido"}</div>
            <div class="value">{fmt_brl(calc['irrf'])}</div>
            <div class="sub">Configurado na barra lateral</div>
        </div>""", unsafe_allow_html=True)
    with col_z:
        st.markdown(f"""<div class="metric-card green">
            <div class="label">🟢 Valor Líquido a Pagar</div>
            <div class="value">{fmt_brl(calc['liquido'])}</div>
            <div class="sub">Bruta - IRRF</div>
        </div>""", unsafe_allow_html=True)

    # assinaturas
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Elaborado por:** Beatriz Esteves · _Gerente Financeira_")
    with c2:
        st.markdown("**Aprovado por:** ___________________________________  · _Controller_")
    st.markdown('<div class="footer">Grupo LLE — Departamento Financeiro · Rescisão conforme Lei 4.886/65</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Comissões por Mês/Ano</div>', unsafe_allow_html=True)

    grp_display = grp[["Mês/Ano","Ano","Mês","Valor"]].copy()
    grp_display["Ano"] = grp_display["Ano"].astype(int)
    grp_display["Mês"] = grp_display["Mês"].astype(int)
    grp_display["Valor (R$)"] = grp_display["Valor"].apply(fmt_brl)

    total_row_m = pd.DataFrame([{"Mês/Ano":"TOTAL GERAL","Ano":"","Mês":"",
                                  "Valor":calc["total_bruto"],
                                  "Valor (R$)": fmt_brl(calc["total_bruto"])}])
    grp_show = pd.concat([grp_display, total_row_m], ignore_index=True)

    st.dataframe(grp_show[["Mês/Ano","Valor (R$)"]], hide_index=True, use_container_width=True)

    st.markdown('<div class="section-title">Evolução Mensal</div>', unsafe_allow_html=True)
    st.line_chart(grp.set_index("Mês/Ano")["Valor"])

    # aviso prévio detail
    st.markdown('<div class="section-title">Base Aviso Prévio — Últimos 3 Meses</div>', unsafe_allow_html=True)
    u3 = calc["ultimos3"][["Mês/Ano","Valor"]].copy()
    u3["Valor (R$)"] = u3["Valor"].apply(fmt_brl)
    st.dataframe(u3[["Mês/Ano","Valor (R$)"]], hide_index=True, use_container_width=False)
    st.markdown(f"**Soma = {fmt_brl(calc['base_aviso'])}  →  Aviso Prévio (1/3) = {fmt_brl(calc['aviso_previo'])}**")


# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Registros Filtrados — Comissões</div>', unsafe_allow_html=True)
    cols_show = [c for c in [parceiro_col, nome_col, baixa_col, neg_col, nat_col, val_col, "Mês", "Ano"] if c and c in df_f.columns]
    st.dataframe(df_f[cols_show].reset_index(drop=True), use_container_width=True)

    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df_f.to_excel(writer, sheet_name="Filtrado", index=False)
        grp.to_excel(writer, sheet_name="Mensal", index=False)
        ann.to_excel(writer, sheet_name="Anual", index=False)
    st.download_button("⬇️ Exportar dados filtrados (.xlsx)", buf.getvalue(),
                       file_name=f"rescisao_{str(rc_code)}.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    audit_df = run_auditoria(df_f, grp, ann, calc, val_col, nat_col)

    total_ok   = (audit_df["Status"].str.startswith("✅")).sum()
    total_warn = (audit_df["Status"].str.startswith("⚠️")).sum()
    total_fail = (audit_df["Status"].str.startswith("❌")).sum()
    total = len(audit_df)

    ca, cb, cc, cd = st.columns(4)
    ca.metric("Total Checks", total)
    cb.metric("✅ OK", total_ok)
    cc.metric("⚠️ Alerta", total_warn)
    cd.metric("❌ Falha", total_fail)

    st.markdown('<div class="section-title">Resultado dos Checks</div>', unsafe_allow_html=True)

    def color_status(val):
        if "✅" in str(val): return "color: #0F8C3B; font-weight:700"
        if "⚠️" in str(val): return "color: #E65100; font-weight:700"
        if "❌" in str(val): return "color: #D32F2F; font-weight:700"
        return ""

    styled = audit_df.style.applymap(color_status, subset=["Status"])
    st.dataframe(styled, hide_index=True, use_container_width=True, height=600)
