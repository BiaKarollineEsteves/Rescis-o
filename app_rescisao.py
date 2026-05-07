import streamlit as st
import pandas as pd
import numpy as np
import io
import base64
from datetime import datetime

st.set_page_config(
    page_title="Rescisão · Grupo LLE",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── LOGO BASE64 ──────────────────────────────────────────────────────────────
LOGO_B64 = "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"

# ── UFIR-RJ ──────────────────────────────────────────────────────────────────
UFIR_TABLE = {
    2010:2.0183,2011:2.1352,2012:2.2752,2013:2.4066,
    2014:2.5473,2015:2.7119,2016:3.0023,2017:3.1999,
    2018:3.2939,2019:3.4211,2020:3.5550,2021:3.7053,
    2022:4.0915,2023:4.3329,2024:4.5373,2025:4.7508,
    2026:4.9604,
}
MESES_PT = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
            7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}

# ── PALETA GRUPO LLE ─────────────────────────────────────────────────────────
AMARELO  = "#F5A800"
VERDE    = "#2B8C3C"
AZUL     = "#2B6FD4"
AZUL_ESC = "#1B2F6B"
CINZA_BG = "#F4F6FA"
BRANCO   = "#FFFFFF"

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap');

*, html, body, [class*="css"] {{
    font-family: 'Montserrat', sans-serif !important;
}}

/* Remove Streamlit default padding */
.block-container {{ padding-top: 0 !important; }}
header[data-testid="stHeader"] {{ background: {AZUL_ESC}; }}

/* ── TOPBAR ── */
.lle-topbar {{
    background: {AZUL_ESC};
    padding: 0 36px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 72px;
    margin: -1rem -1rem 0 -1rem;
    box-shadow: 0 4px 20px rgba(27,47,107,0.3);
}}
.lle-topbar img {{ height: 44px; }}
.lle-topbar-title {{
    color: white;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    opacity: 0.95;
}}
.lle-badge {{
    background: {AMARELO};
    color: {AZUL_ESC};
    font-size: 0.65rem;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 20px;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

/* ── RC INFO BAR ── */
.rc-bar {{
    background: white;
    border-left: 5px solid {AMARELO};
    border-radius: 0 10px 10px 0;
    padding: 14px 24px;
    margin: 16px 0;
    display: flex;
    gap: 32px;
    align-items: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    flex-wrap: wrap;
}}
.rc-bar-item {{ display: flex; flex-direction: column; gap: 2px; }}
.rc-bar-label {{ font-size: 0.65rem; font-weight: 700; color: #888; text-transform: uppercase; letter-spacing: 0.8px; }}
.rc-bar-value {{ font-size: 0.92rem; font-weight: 700; color: {AZUL_ESC}; }}

/* ── METRIC CARDS ── */
.metric-row {{ display: flex; gap: 16px; margin: 16px 0; flex-wrap: wrap; }}
.metric-card {{
    flex: 1; min-width: 180px;
    background: white;
    border-radius: 12px;
    padding: 20px 22px;
    box-shadow: 0 2px 14px rgba(0,0,0,0.07);
    border-top: 4px solid {AZUL};
    position: relative;
    overflow: hidden;
}}
.metric-card::before {{
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 80px; height: 80px;
    background: {AZUL};
    opacity: 0.04;
    border-radius: 50%;
    transform: translate(20px, -20px);
}}
.metric-card.yellow {{ border-top-color: {AMARELO}; }}
.metric-card.yellow::before {{ background: {AMARELO}; }}
.metric-card.green  {{ border-top-color: {VERDE}; }}
.metric-card.green::before  {{ background: {VERDE}; }}
.metric-card.red    {{ border-top-color: #E53935; }}
.metric-card.red::before    {{ background: #E53935; }}

.metric-label {{ font-size: 0.68rem; font-weight: 700; color: #999; text-transform: uppercase; letter-spacing: 0.8px; }}
.metric-value {{ font-size: 1.6rem; font-weight: 800; color: {AZUL_ESC}; margin: 6px 0 2px; line-height: 1; }}
.metric-sub   {{ font-size: 0.72rem; color: #aaa; font-weight: 500; }}

/* ── SECTION TITLES ── */
.sec-title {{
    font-size: 0.72rem; font-weight: 800; color: {AZUL};
    letter-spacing: 2px; text-transform: uppercase;
    border-left: 4px solid {AMARELO};
    padding-left: 12px;
    margin: 28px 0 14px;
}}

/* ── CALCULO BOX ── */
.calc-box {{
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 14px rgba(0,0,0,0.07);
}}
.calc-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #f0f0f0;
    font-size: 0.88rem;
}}
.calc-row:last-child {{ border-bottom: none; }}
.calc-label {{ color: #555; font-weight: 500; }}
.calc-value {{ font-weight: 700; color: {AZUL_ESC}; }}
.calc-total {{
    background: {AZUL_ESC};
    color: white !important;
    border-radius: 8px;
    padding: 14px 20px;
    margin-top: 12px;
    display: flex;
    justify-content: space-between;
    font-weight: 800;
    font-size: 1rem;
}}
.calc-subtotal {{
    background: {AMARELO}22;
    border-left: 3px solid {AMARELO};
    border-radius: 0 6px 6px 0;
    padding: 10px 16px;
    margin: 4px 0;
    display: flex;
    justify-content: space-between;
    font-weight: 700;
    font-size: 0.9rem;
    color: {AZUL_ESC};
}}

/* ── FOOTER ASSINATURA ── */
.assinatura {{
    display: flex;
    gap: 40px;
    margin-top: 24px;
    padding-top: 20px;
    border-top: 2px solid {AZUL_ESC}22;
}}
.ass-item {{ flex: 1; }}
.ass-nome {{ font-weight: 700; color: {AZUL_ESC}; font-size: 0.88rem; }}
.ass-cargo {{ color: #888; font-size: 0.75rem; margin-top: 2px; }}
.ass-linha {{
    border-bottom: 1.5px solid {AZUL_ESC};
    margin-bottom: 6px;
    height: 28px;
}}

/* ── FOOTER ── */
.lle-footer {{
    background: {AZUL_ESC};
    color: rgba(255,255,255,0.5);
    font-size: 0.7rem;
    text-align: center;
    padding: 14px;
    margin: 32px -1rem -1rem -1rem;
    letter-spacing: 1px;
}}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {{
    background: {AZUL_ESC} !important;
}}
section[data-testid="stSidebar"] * {{
    color: white !important;
}}
section[data-testid="stSidebar"] .stFileUploader label,
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] .stNumberInput label {{
    color: rgba(255,255,255,0.85) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}
section[data-testid="stSidebar"] .stFileUploader {{
    background: rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 12px;
    border: 1px dashed rgba(255,255,255,0.25);
}}
section[data-testid="stSidebar"] hr {{
    border-color: rgba(255,255,255,0.15) !important;
}}
.sidebar-section-title {{
    color: {AMARELO} !important;
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}}

/* ── AUDIT ── */
.audit-ok   {{ color: {VERDE};   font-weight: 700; }}
.audit-warn {{ color: #F57C00;   font-weight: 700; }}
.audit-fail {{ color: #E53935;   font-weight: 700; }}

/* TAB styling */
.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    background: {AZUL_ESC}11;
    border-radius: 10px;
    padding: 4px;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px !important;
    font-weight: 600;
    font-size: 0.82rem;
    letter-spacing: 0.3px;
    color: {AZUL_ESC} !important;
}}
.stTabs [aria-selected="true"] {{
    background: {AZUL_ESC} !important;
    color: white !important;
}}
</style>
""", unsafe_allow_html=True)

# ── TOPBAR ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="lle-topbar">
  <img src="data:image/png;base64,{LOGO_B64}" alt="Grupo LLE">
  <span class="lle-topbar-title">Rescisão de Representante Comercial</span>
  <span class="lle-badge">Lei 4.886/65</span>
</div>
""", unsafe_allow_html=True)

# ── HELPERS ──────────────────────────────────────────────────────────────────
def fmt_brl(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",","X").replace(".",",").replace("X",".")
    except:
        return "R$ —"

def detect_header_row(df_raw):
    for i, row in df_raw.iterrows():
        vals = " ".join([str(v).strip() for v in row if pd.notna(v)])
        if "Vlr do Desdobramento" in vals or "Vlr Desdobramento" in vals:
            return i
    return 2

def load_file(file):
    ext = file.name.split(".")[-1].lower()
    engine = "xlrd" if ext == "xls" else "openpyxl"
    raw = pd.read_excel(file, sheet_name=0, header=None, engine=engine)
    hr  = detect_header_row(raw)
    df  = pd.read_excel(io.BytesIO(file.getvalue()), sheet_name=0, header=hr, engine=engine)
    df.columns = [str(c).strip() for c in df.columns]
    val_col     = next((c for c in df.columns if "Vlr" in c and "Desdobramento" in c), None) or \
                  next((c for c in df.columns if "Vlr" in c), None)
    nat_col     = next((c for c in df.columns if "Natureza" in c.lower()), None)
    baixa_col   = next((c for c in df.columns if "Data Baixa" in c or ("Baixa" in c and "Dt" in c)), None)
    neg_col     = next((c for c in df.columns if "Negoci" in c), None)
    parceiro_col= next((c for c in df.columns if c == "Parceiro"), None)
    nome_col    = next((c for c in df.columns if "Nome Parceiro" in c), None)
    return df, val_col, nat_col, baixa_col, neg_col, parceiro_col, nome_col

def filter_commissions(df, val_col, nat_col, date_col):
    if nat_col:
        mask = df[nat_col].astype(str).str.contains("Comissão s/ vendas|Comissao s/ vendas", case=False, na=False)
        df_f = df[mask].copy()
    else:
        df_f = df.copy()
    df_f = df_f.dropna(subset=[val_col])
    df_f[val_col] = pd.to_numeric(df_f[val_col], errors='coerce')
    df_f = df_f[df_f[val_col] > 0]
    if date_col:
        df_f[date_col] = pd.to_datetime(df_f[date_col], errors='coerce')
        df_f = df_f.dropna(subset=[date_col])
        df_f["Mês"] = df_f[date_col].dt.month
        df_f["Ano"] = df_f[date_col].dt.year
    return df_f

def build_monthly(df_f, val_col):
    g = df_f.groupby(["Ano","Mês"])[val_col].sum().reset_index()
    g.columns = ["Ano","Mês","Valor"]
    g = g.sort_values(["Ano","Mês"]).reset_index(drop=True)
    g["Mês/Ano"] = g.apply(lambda r: f"{MESES_PT[int(r['Mês'])]}/{int(r['Ano'])}", axis=1)
    return g

def build_annual(grp, ufir_ano):
    a = grp.groupby("Ano")["Valor"].sum().reset_index()
    a.columns = ["Ano","Comissão Bruta"]
    a["UFIR do Ano"] = a["Ano"].apply(lambda y: UFIR_TABLE.get(int(y), np.nan))
    a["Comissão Corrigida"] = a.apply(
        lambda r: ufir_ano * r["Comissão Bruta"] / r["UFIR do Ano"]
                  if pd.notna(r["UFIR do Ano"]) and r["UFIR do Ano"] > 0
                  else r["Comissão Bruta"], axis=1)
    return a

def calcular(ann, grp, irrf, ufir_ano):
    tb = ann["Comissão Bruta"].sum()
    tc = ann["Comissão Corrigida"].sum()
    ind112 = tc / 12
    u3  = grp.tail(3)
    bap = u3["Valor"].sum()
    avp = bap / 3
    bruta = ind112 + avp
    irrf_v = bruta * 0.15 if irrf == "Sim" else 0.0
    return dict(tb=tb, tc=tc, ind112=ind112, u3=u3, bap=bap, avp=avp,
                bruta=bruta, irrf=irrf_v, liq=bruta - irrf_v)

def audit(df_f, grp, ann, calc, val_col, nat_col, ufir_ano):
    checks = []
    def c(n, cat, desc, res, st, det=""):
        icon = {"ok":"✅","warn":"⚠️","fail":"❌"}[st]
        label= {"ok":"OK","warn":"ALERTA","fail":"FALHA"}[st]
        checks.append({"#":n,"Categoria":cat,"Verificação":desc,"Resultado":res,"Status":f"{icon} {label}","Detalhe":det})
    n = len(df_f)
    # integridade
    if nat_col:
        ok = df_f[nat_col].astype(str).str.contains("Comissão|Comissao",case=False).all()
        c(1,"Integridade","Filtro só contém comissões?",f"{n}/{n}","ok" if ok else "fail")
    else:
        c(1,"Integridade","Filtro só contém comissões?","N/A","warn","Coluna Natureza não encontrada")
    c(2,"Integridade","Registros têm Data Baixa?",f"{n}/{n}","ok")
    nz = (df_f[val_col] <= 0).sum()
    c(3,"Integridade","Valores negativos ou zero?",f"{nz}","ok" if nz==0 else "fail")
    c(4,"Integridade","Total de registros > 0?",f"{n}","ok" if n>0 else "fail")
    sem_ufir=[int(a) for a in ann["Ano"] if int(a) not in UFIR_TABLE]
    c(5,"Integridade","Anos têm UFIR cadastrado?",f"{len(ann)-len(sem_ufir)}/{len(ann)}","ok" if not sem_ufir else "warn",str(sem_ufir) if sem_ufir else "")
    # cruzamentos
    tf=df_f[val_col].sum(); tg=grp["Valor"].sum(); ta=ann["Comissão Bruta"].sum()
    c(6,"Cruzamento","Total filtrado = Base mensal?",f"{fmt_brl(tf)} vs {fmt_brl(tg)}","ok" if abs(tf-tg)<0.02 else "fail")
    c(7,"Cruzamento","Total filtrado = Total anual?",f"{fmt_brl(tf)} vs {fmt_brl(ta)}","ok" if abs(tf-ta)<0.02 else "fail")
    c(8,"Cruzamento","UFIR Ano Atual = Tabela?",f"{ufir_ano} vs {UFIR_TABLE.get(datetime.now().year,'—')}","ok")
    c(9,"Cruzamento","Base Aviso = 3 últ. meses?",f"{fmt_brl(calc['bap'])} vs {fmt_brl(calc['u3']['Valor'].sum())}","ok" if abs(calc['bap']-calc['u3']['Valor'].sum())<0.02 else "fail")
    # lógica
    c(10,"Lógica","Corrigida ≥ Bruta?",f"{fmt_brl(calc['tc'])} vs {fmt_brl(calc['tb'])}","ok" if calc['tc']>=calc['tb']-0.01 else "warn")
    c(11,"Lógica","Indenização = Corrigida/12?",f"{fmt_brl(calc['ind112'])} vs {fmt_brl(calc['tc']/12)}","ok" if abs(calc['ind112']-calc['tc']/12)<0.02 else "fail")
    c(12,"Lógica","Aviso Prévio = Base/3?",f"{fmt_brl(calc['avp'])} vs {fmt_brl(calc['bap']/3)}","ok" if abs(calc['avp']-calc['bap']/3)<0.02 else "fail")
    c(13,"Lógica","Bruta = 1/12 + Aviso?",f"{fmt_brl(calc['bruta'])} vs {fmt_brl(calc['ind112']+calc['avp'])}","ok" if abs(calc['bruta']-(calc['ind112']+calc['avp']))<0.02 else "fail")
    c(14,"Lógica","IRRF = 15% da Bruta?","N/A (não retido)" if calc['irrf']==0 else f"{fmt_brl(calc['irrf'])} vs {fmt_brl(calc['bruta']*0.15)}","ok")
    c(15,"Lógica","Líquido = Bruta - IRRF?",f"{fmt_brl(calc['liq'])}","ok" if abs(calc['liq']-(calc['bruta']-calc['irrf']))<0.02 else "fail")
    # riscos
    c(16,"Risco","IRRF não retido — intencional?","Não retido","warn" if calc['irrf']==0 else "ok","Confirmar se intencional" if calc['irrf']==0 else "IRRF retido")
    c(17,"Risco","Indenização > R$ 10.000?",fmt_brl(calc['bruta']),"warn" if calc['bruta']>10000 else "ok")
    pct=(calc['tc']/calc['tb']-1)*100 if calc['tb']>0 else 0
    c(18,"Risco","Correção monetária > 10%?",f"{pct:.1f}%","warn" if pct>10 else "ok")
    if len(grp)>0:
        mp=grp["Valor"].max()/grp["Valor"].sum()*100
        c(19,"Risco","Algum mês > 20% do total?",f"{mp:.0f}%","warn" if mp>20 else "ok")
    if len(grp)>1:
        cv=grp["Valor"].std()/grp["Valor"].mean()*100
        c(20,"Risco","Coeficiente variação > 50%?",f"{cv:.0f}%","warn" if cv>50 else "ok")
    return pd.DataFrame(checks)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f'<img src="data:image/png;base64,{LOGO_B64}" style="width:160px;margin-bottom:20px;">', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-section-title">📂 Arquivo</p>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Planilha do ERP", type=["xls","xlsx"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown('<p class="sidebar-section-title">📅 UFIR-RJ</p>', unsafe_allow_html=True)
    ano_atual = datetime.now().year

    # Inicializa tabela editável na session_state
    if "ufir_table" not in st.session_state:
        st.session_state.ufir_table = dict(UFIR_TABLE)

    # ── Editar UFIR do ano corrente ──
    anos_disponiveis = sorted(st.session_state.ufir_table.keys(), reverse=True)
    ano_sel = st.selectbox("Ano", options=anos_disponiveis,
                           index=anos_disponiveis.index(ano_atual) if ano_atual in anos_disponiveis else 0)
    ufir_ano = st.number_input(
        f"UFIR-RJ {ano_sel}",
        value=float(st.session_state.ufir_table.get(ano_sel, 4.9604)),
        min_value=0.0001, step=0.0001, format="%.4f",
        key=f"ufir_edit_{ano_sel}"
    )
    if st.button("💾 Salvar alteração", use_container_width=True):
        st.session_state.ufir_table[ano_sel] = ufir_ano
        st.success(f"UFIR {ano_sel} atualizado para {ufir_ano:.4f}")

    # ── Adicionar novo ano ──
    st.markdown('<p class="sidebar-section-title" style="margin-top:12px;">➕ Novo Ano</p>', unsafe_allow_html=True)
    col_a, col_v = st.columns([1,1])
    with col_a:
        novo_ano = st.number_input("Ano", value=ano_atual+1, min_value=2000, max_value=2100,
                                   step=1, format="%d", label_visibility="collapsed", key="novo_ano")
    with col_v:
        novo_ufir = st.number_input("UFIR", value=5.0000, min_value=0.0001, step=0.0001,
                                    format="%.4f", label_visibility="collapsed", key="novo_ufir")
    if st.button("➕ Adicionar", use_container_width=True):
        st.session_state.ufir_table[int(novo_ano)] = novo_ufir
        st.success(f"Ano {int(novo_ano)} adicionado com UFIR {novo_ufir:.4f}")

    # Sincroniza para uso no cálculo
    UFIR_TABLE.update(st.session_state.ufir_table)
    ufir_ano = float(st.session_state.ufir_table.get(ano_sel, ufir_ano))

    st.markdown("---")
    st.markdown('<p class="sidebar-section-title">💰 IRRF</p>', unsafe_allow_html=True)
    reter_irrf = st.radio("Reter IRRF (15%)?", ["Não","Sim"], index=0, label_visibility="collapsed")
    st.markdown("---")
    st.markdown('<p class="sidebar-section-title">📖 Tabela UFIR Completa</p>', unsafe_allow_html=True)
    df_ufir_show = pd.DataFrame(
        sorted(st.session_state.ufir_table.items()), columns=["Ano","UFIR-RJ"]
    )
    st.dataframe(df_ufir_show, hide_index=True, use_container_width=True, height=300)

# ── UPLOAD PROMPT ─────────────────────────────────────────────────────────────
if not uploaded:
    st.markdown(f"""
    <div style="text-align:center;padding:80px 20px;color:#aaa;">
      <div style="font-size:4rem;margin-bottom:16px;">📤</div>
      <h3 style="color:{AZUL_ESC};font-weight:800;margin-bottom:8px;">Carregue a planilha do ERP</h3>
      <p style="color:#999;max-width:400px;margin:0 auto;line-height:1.6;">
        Importe o arquivo <b>.xls</b> ou <b>.xlsx</b> exportado do sistema financeiro.<br>
        A planilha deve conter as colunas de comissão do representante.
      </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── PROCESSAR ────────────────────────────────────────────────────────────────
try:
    df, val_col, nat_col, baixa_col, neg_col, parceiro_col, nome_col = load_file(uploaded)
except Exception as e:
    st.error(f"Erro ao ler o arquivo: {e}")
    st.stop()

if val_col is None:
    st.error("Coluna de valor não encontrada. Verifique se o arquivo contém 'Vlr do Desdobramento'.")
    st.stop()

date_col = baixa_col or neg_col
df_f = filter_commissions(df, val_col, nat_col, date_col)
if len(df_f) == 0:
    st.warning("Nenhum registro de comissão encontrado.")
    st.stop()

grp  = build_monthly(df_f, val_col)
ufir_calculo = float(st.session_state.ufir_table.get(ano_atual, ufir_ano))
ann  = build_annual(grp, ufir_calculo)
calc = calcular(ann, grp, reter_irrf, ufir_calculo)

rc_code = str(df_f[parceiro_col].iloc[0]) if parceiro_col and parceiro_col in df_f.columns else "—"
rc_nome = str(df_f[nome_col].iloc[0]) if nome_col and nome_col in df_f.columns else "—"
p_ini   = f"{MESES_PT[int(grp['Mês'].iloc[0])]}/{int(grp['Ano'].iloc[0])}"
p_fim   = f"{MESES_PT[int(grp['Mês'].iloc[-1])]}/{int(grp['Ano'].iloc[-1])}"

# RC BAR
st.markdown(f"""
<div class="rc-bar">
  <div class="rc-bar-item">
    <span class="rc-bar-label">Representante</span>
    <span class="rc-bar-value">{rc_nome}</span>
  </div>
  <div class="rc-bar-item">
    <span class="rc-bar-label">Código</span>
    <span class="rc-bar-value">{rc_code}</span>
  </div>
  <div class="rc-bar-item">
    <span class="rc-bar-label">Período</span>
    <span class="rc-bar-value">{p_ini} → {p_fim}</span>
  </div>
  <div class="rc-bar-item">
    <span class="rc-bar-label">Registros</span>
    <span class="rc-bar-value">{len(df_f)}</span>
  </div>
  <div class="rc-bar-item">
    <span class="rc-bar-label">UFIR-RJ {ano_atual}</span>
    <span class="rc-bar-value">{ufir_calculo:.4f}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📅 Comissões por Mês", "📋 Dados Brutos", "🔎 Auditoria"])

# ══════════════ DASHBOARD ════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-title">Resumo Financeiro</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card">
        <div class="metric-label">Total Bruto</div>
        <div class="metric-value">{fmt_brl(calc['tb'])}</div>
        <div class="metric-sub">{len(grp)} meses de comissão</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Total Corrigido UFIR</div>
        <div class="metric-value">{fmt_brl(calc['tc'])}</div>
        <div class="metric-sub">UFIR {ano_atual} = {ufir_ano:.4f}</div>
      </div>
      <div class="metric-card yellow">
        <div class="metric-label">Indenização Bruta</div>
        <div class="metric-value">{fmt_brl(calc['bruta'])}</div>
        <div class="metric-sub">1/12 avos + Aviso Prévio 1/3</div>
      </div>
      <div class="metric-card {'green' if reter_irrf=='Não' else 'red'}">
        <div class="metric-label">Valor Líquido a Pagar</div>
        <div class="metric-value">{fmt_brl(calc['liq'])}</div>
        <div class="metric-sub">{'IRRF não retido' if reter_irrf=='Não' else f'IRRF retido: {fmt_brl(calc["irrf"])}'}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_t, col_g = st.columns([1,1])
    with col_t:
        st.markdown('<div class="sec-title">Comissões por Ano</div>', unsafe_allow_html=True)
        ann_d = ann.copy()
        ann_d["Ano"] = ann_d["Ano"].astype(int)
        ann_d["UFIR"] = ann_d["UFIR do Ano"].apply(lambda v: f"{v:.4f}")
        ann_d["Bruta"] = ann_d["Comissão Bruta"].apply(fmt_brl)
        ann_d["Corrigida"] = ann_d["Comissão Corrigida"].apply(fmt_brl)
        totrow = pd.DataFrame([{"Ano":"TOTAL","UFIR":"—","Bruta":fmt_brl(calc['tb']),"Corrigida":fmt_brl(calc['tc'])}])
        st.dataframe(pd.concat([ann_d[["Ano","UFIR","Bruta","Corrigida"]].astype(str), totrow],ignore_index=True),
                     hide_index=True, use_container_width=True)

    with col_g:
        st.markdown('<div class="sec-title">Evolução Anual</div>', unsafe_allow_html=True)
        chart_d = ann.set_index(ann["Ano"].astype(int))[["Comissão Bruta","Comissão Corrigida"]]
        st.bar_chart(chart_d, color=[AZUL, AMARELO])

    st.markdown('<div class="sec-title">Detalhamento do Cálculo</div>', unsafe_allow_html=True)
    u3_str = " · ".join(calc['u3']['Mês/Ano'].tolist())
    st.markdown(f"""
    <div class="calc-box">
      <div class="calc-row"><span class="calc-label">Base de Indenização (Total Corrigido)</span><span class="calc-value">{fmt_brl(calc['tc'])}</span></div>
      <div class="calc-row"><span class="calc-label">÷ 12 meses = Indenização 1/12 Avos</span><span class="calc-value">{fmt_brl(calc['ind112'])}</span></div>
      <div class="calc-row"><span class="calc-label">Últimos 3 meses: {u3_str}</span><span class="calc-value">&nbsp;</span></div>
      <div class="calc-row"><span class="calc-label">Base Aviso Prévio (soma 3 meses)</span><span class="calc-value">{fmt_brl(calc['bap'])}</span></div>
      <div class="calc-row"><span class="calc-label">÷ 3 = Aviso Prévio 1/3</span><span class="calc-value">{fmt_brl(calc['avp'])}</span></div>
      <div class="calc-subtotal"><span>Indenização 1/12 + Aviso Prévio = BRUTA</span><span>{fmt_brl(calc['bruta'])}</span></div>
      <div class="calc-row"><span class="calc-label">IRRF (15%) — {"Retido" if reter_irrf=="Sim" else "NÃO Retido"}</span><span class="calc-value">{fmt_brl(calc['irrf'])}</span></div>
      <div class="calc-total"><span>VALOR LÍQUIDO A PAGAR</span><span>{fmt_brl(calc['liq'])}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Aprovações</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="assinatura">
      <div class="ass-item">
        <div class="ass-linha"></div>
        <div class="ass-nome">Beatriz Esteves</div>
        <div class="ass-cargo">Gerente Financeira · Grupo LLE</div>
      </div>
      <div class="ass-item">
        <div class="ass-linha"></div>
        <div class="ass-nome">Controller</div>
        <div class="ass-cargo">Aprovação · Grupo LLE</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════ COMISSÕES MENSAIS ════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-title">Comissões por Mês/Ano</div>', unsafe_allow_html=True)
    grp_d = grp[["Mês/Ano","Valor"]].copy()
    grp_d["Valor (R$)"] = grp_d["Valor"].apply(fmt_brl)
    totrow_m = pd.DataFrame([{"Mês/Ano":"TOTAL GERAL","Valor":calc["tb"],"Valor (R$)":fmt_brl(calc["tb"])}])
    st.dataframe(pd.concat([grp_d, totrow_m],ignore_index=True)[["Mês/Ano","Valor (R$)"]],
                 hide_index=True, use_container_width=True)

    st.markdown('<div class="sec-title">Evolução Mensal</div>', unsafe_allow_html=True)
    st.line_chart(grp.set_index("Mês/Ano")["Valor"], color=AZUL)

    st.markdown('<div class="sec-title">Base Aviso Prévio — Últimos 3 Meses</div>', unsafe_allow_html=True)
    u3d = calc["u3"][["Mês/Ano","Valor"]].copy()
    u3d["Valor (R$)"] = u3d["Valor"].apply(fmt_brl)
    st.dataframe(u3d[["Mês/Ano","Valor (R$)"]], hide_index=True)
    st.markdown(f"**Base: {fmt_brl(calc['bap'])}  →  Aviso Prévio (÷ 3): {fmt_brl(calc['avp'])}**")

# ══════════════ DADOS BRUTOS ═════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-title">Registros Filtrados</div>', unsafe_allow_html=True)
    cols_show = [c for c in [parceiro_col,nome_col,date_col,nat_col,val_col,"Mês","Ano"] if c and c in df_f.columns]
    st.dataframe(df_f[cols_show].reset_index(drop=True), use_container_width=True)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df_f.to_excel(w, sheet_name="Filtrado", index=False)
        grp.to_excel(w, sheet_name="Mensal", index=False)
        ann.to_excel(w, sheet_name="Anual", index=False)
    st.download_button("⬇️ Exportar .xlsx", buf.getvalue(),
        file_name=f"rescisao_{rc_code}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ══════════════ AUDITORIA ════════════════════════════════════════════════════
with tab4:
    audit_df = audit(df_f, grp, ann, calc, val_col, nat_col, ufir_ano)
    n_ok   = (audit_df["Status"].str.startswith("✅")).sum()
    n_warn = (audit_df["Status"].str.startswith("⚠️")).sum()
    n_fail = (audit_df["Status"].str.startswith("❌")).sum()

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card"><div class="metric-label">Total Checks</div><div class="metric-value">{len(audit_df)}</div></div>
      <div class="metric-card green"><div class="metric-label">✅ OK</div><div class="metric-value">{n_ok}</div></div>
      <div class="metric-card yellow"><div class="metric-label">⚠️ Alerta</div><div class="metric-value">{n_warn}</div></div>
      <div class="metric-card red"><div class="metric-label">❌ Falha</div><div class="metric-value">{n_fail}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Resultado dos Checks</div>', unsafe_allow_html=True)
    def color_st(val):
        if "✅" in str(val): return "color:#2B8C3C;font-weight:700"
        if "⚠️" in str(val): return "color:#F57C00;font-weight:700"
        if "❌" in str(val): return "color:#E53935;font-weight:700"
        return ""
    st.dataframe(audit_df.style.applymap(color_st, subset=["Status"]),
                 hide_index=True, use_container_width=True, height=580)

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="lle-footer">
  GRUPO LLE · DEPARTAMENTO FINANCEIRO · RESCISÃO CONFORME LEI 4.886/65
</div>
""", unsafe_allow_html=True)
