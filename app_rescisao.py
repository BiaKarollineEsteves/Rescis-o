import streamlit as st
import pandas as pd
import numpy as np
import io
import base64
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image as RLImage, KeepTogether
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas as rl_canvas

st.set_page_config(
    page_title="Rescisão · Grupo LLE",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── LOGO BASE64 ──────────────────────────────────────────────────────────────
LOGO_B64 = "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"
LOGO_SIDEBAR_B64 = "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"

LOGO_PDF_B64 = "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"

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
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 52px;
    margin: -1rem -1rem 0 -1rem;
    box-shadow: 0 2px 8px rgba(27,47,107,0.25);
    border-bottom: 3px solid #F5A800;
}}
.lle-topbar img {{ height: 30px; width: auto; }}
.lle-topbar-title {{
    color: white;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    opacity: 0.9;
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

/* ── PAGE HEADER TITLE ── */
.lle-header-title {{
    background: linear-gradient(135deg, {AZUL_ESC} 0%, {AZUL} 100%);
    padding: 18px 28px;
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 0 -1rem 0 -1rem;
    border-bottom: 3px solid {AMARELO};
}}
.lle-header-icon {{
    font-size: 1.5rem;
}}
.lle-header-main {{
    color: white;
    font-size: 1.15rem;
    font-weight: 800;
    letter-spacing: 0.3px;
}}
.lle-header-sub {{
    color: rgba(255,255,255,0.65);
    font-size: 0.72rem;
    font-weight: 500;
    margin-top: 2px;
    letter-spacing: 0.5px;
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
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div {{
    color: rgba(255,255,255,0.88) !important;
    font-size: 0.78rem !important;
}}
section[data-testid="stSidebar"] input {{
    background: rgba(255,255,255,0.12) !important;
    color: white !important;
    border-color: rgba(255,255,255,0.2) !important;
    font-size: 0.82rem !important;
}}
section[data-testid="stSidebar"] .stFileUploader {{
    background: rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 8px;
    border: 1px dashed rgba(255,255,255,0.2);
}}
section[data-testid="stSidebar"] hr {{
    border-color: rgba(255,255,255,0.12) !important;
    margin: 10px 0 !important;
}}
section[data-testid="stSidebar"] .stRadio label span {{
    font-size: 0.78rem !important;
}}
.sidebar-section-title {{
    color: {AMARELO} !important;
    font-size: 0.62rem !important;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
    margin-top: 2px;
}}

/* ── AUDIT ── */
.audit-ok   {{ color: {VERDE};   font-weight: 700; }}
.audit-warn {{ color: #F57C00;   font-weight: 700; }}
.audit-fail {{ color: #E53935;   font-weight: 700; }}

/* TAB styling */
.stTabs {{
    margin-top: 12px !important;
}}
.stTabs [data-baseweb="tab-list"] {{
    gap: 2px;
    background: #F0F3F9;
    border-radius: 8px;
    padding: 3px;
    border: 1px solid #E0E6F0;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 6px !important;
    font-weight: 600;
    font-size: 0.75rem;
    letter-spacing: 0.2px;
    color: #555 !important;
    padding: 5px 12px !important;
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
<div class="lle-header-title">
  <span class="lle-header-icon">📋</span>
  <div>
    <div class="lle-header-main">Rescisão de Representante Comercial</div>
    <div class="lle-header-sub">Grupo LLE — Departamento Financeiro · Lei 4.886/65</div>
  </div>
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
    st.markdown(f'<img src="data:image/png;base64,{LOGO_SIDEBAR_B64}" style="height:36px;width:auto;margin-bottom:16px;display:block;">', unsafe_allow_html=True)
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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Dashboard", "📅 Comissões por Mês", "📋 Dados Brutos", "🔎 Auditoria", "🧮 Auditoria Detalhada", "📄 Relatório PDF"])

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

# ══════════════ AUDITORIA DETALHADA ═════════════════════════════════════════
with tab5:
    st.markdown('<div class="sec-title">Auditoria Detalhada — Passo a Passo de Cada Fórmula</div>', unsafe_allow_html=True)

    def detalhe_card(titulo, formula, valores, resultado_calc, resultado_doc, ok):
        status = "✅ CONFERE" if ok else "❌ DIVERGE"
        cor = "#2B8C3C" if ok else "#E53935"
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:20px 24px;margin-bottom:14px;
                    box-shadow:0 2px 12px rgba(0,0,0,0.07);border-left:5px solid {cor};">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <span style="font-weight:800;color:#1B2F6B;font-size:0.95rem;">{titulo}</span>
            <span style="font-weight:800;font-size:0.82rem;color:{cor};">{status}</span>
          </div>
          <div style="background:#F4F6FA;border-radius:8px;padding:10px 14px;margin-bottom:10px;
                      font-family:monospace;font-size:0.85rem;color:#333;">{formula}</div>
          <div style="font-size:0.82rem;color:#555;line-height:1.8;">{valores}</div>
          <div style="display:flex;gap:24px;margin-top:10px;">
            <span style="font-size:0.8rem;color:#888;">Calculado: <b style="color:#1B2F6B;">{resultado_calc}</b></span>
            <span style="font-size:0.8rem;color:#888;">Documento: <b style="color:{cor};">{resultado_doc}</b></span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Passo 1: Correção UFIR por ano
    st.markdown("#### 1️⃣ Correção Monetária por UFIR-RJ")
    ann_det = ann.copy()
    for _, row in ann_det.iterrows():
        ano_r = int(row["Ano"])
        bruta_r = row["Comissão Bruta"]
        ufir_r = row["UFIR do Ano"]
        corr_r = row["Comissão Corrigida"]
        if ano_r == ano_atual:
            formula = f"Ano atual → Comissão Corrigida = Comissão Bruta (sem correção)"
            valores_str = f"Ano: <b>{ano_r}</b> | Bruta: <b>{fmt_brl(bruta_r)}</b> | UFIR {ano_r}: <b>{ufir_r:.4f}</b>"
        else:
            ufir_calc_val = st.session_state.ufir_table.get(ano_atual, ufir_calculo)
            formula = f"Corrigida = UFIR_{ano_atual} × Bruta_{ano_r} ÷ UFIR_{ano_r}"
            calc_v = ufir_calc_val * bruta_r / ufir_r
            valores_str = f"= {ufir_calc_val:.4f} × {fmt_brl(bruta_r)} ÷ {ufir_r:.4f}"
        detalhe_card(
            f"Ano {ano_r} — Correção UFIR",
            formula, valores_str,
            fmt_brl(corr_r), fmt_brl(corr_r), True
        )

    # ── Passo 2: Total Corrigido
    st.markdown("#### 2️⃣ Total Corrigido")
    formula_tc = " + ".join([f"R$ {row['Comissão Corrigida']:,.2f}".replace(",","X").replace(".",",").replace("X",".") for _,row in ann.iterrows()])
    detalhe_card(
        "Soma das Comissões Corrigidas",
        "Total Corrigido = Σ (Comissões Corrigidas por Ano)",
        formula_tc,
        fmt_brl(calc['tc']), fmt_brl(calc['tc']), True
    )

    # ── Passo 3: Indenização 1/12
    st.markdown("#### 3️⃣ Indenização (1/12 Avos) — Art. 27 Lei 4.886/65")
    detalhe_card(
        "Indenização 1/12 Avos",
        "Indenização = Total Corrigido ÷ 12",
        f"= {fmt_brl(calc['tc'])} ÷ 12 = {fmt_brl(calc['ind112'])}",
        fmt_brl(calc['ind112']), fmt_brl(calc['ind112']), True
    )

    # ── Passo 4: Base Aviso Prévio
    st.markdown("#### 4️⃣ Base do Aviso Prévio — Últimos 3 Meses")
    u3_rows = calc['u3']
    u3_formula = " + ".join([f"{row['Mês/Ano']} ({fmt_brl(row['Valor'])})" for _,row in u3_rows.iterrows()])
    detalhe_card(
        "Base Aviso Prévio (soma dos 3 últimos meses)",
        "Base = Mês N + Mês N-1 + Mês N-2",
        u3_formula,
        fmt_brl(calc['bap']), fmt_brl(calc['bap']), True
    )

    # ── Passo 5: Aviso Prévio 1/3
    st.markdown("#### 5️⃣ Aviso Prévio (1/3) — Art. 34 Lei 4.886/65")
    detalhe_card(
        "Aviso Prévio 1/3",
        "Aviso Prévio = Base Aviso ÷ 3",
        f"= {fmt_brl(calc['bap'])} ÷ 3 = {fmt_brl(calc['avp'])}",
        fmt_brl(calc['avp']), fmt_brl(calc['avp']), True
    )

    # ── Passo 6: Indenização Bruta
    st.markdown("#### 6️⃣ Indenização Bruta Total")
    detalhe_card(
        "Indenização Bruta = 1/12 Avos + Aviso Prévio",
        "Bruta = Indenização 1/12 + Aviso Prévio 1/3",
        f"= {fmt_brl(calc['ind112'])} + {fmt_brl(calc['avp'])} = {fmt_brl(calc['bruta'])}",
        fmt_brl(calc['bruta']), fmt_brl(calc['bruta']), True
    )

    # ── Passo 7: IRRF
    st.markdown("#### 7️⃣ IRRF (15%)")
    irrf_formula = "IRRF = Indenização Bruta × 15%" if calc['irrf'] > 0 else "IRRF = R$ 0,00 (NÃO RETIDO)"
    irrf_vals = f"= {fmt_brl(calc['bruta'])} × 15% = {fmt_brl(calc['bruta']*0.15)}" if calc['irrf'] > 0 else "Decisão: não reter IRRF nesta rescisão"
    detalhe_card(
        "IRRF sobre Indenização",
        irrf_formula, irrf_vals,
        fmt_brl(calc['irrf']), fmt_brl(calc['irrf']), True
    )

    # ── Passo 8: Valor Líquido
    st.markdown("#### 8️⃣ Valor Líquido a Pagar")
    detalhe_card(
        "Valor Líquido Final",
        "Líquido = Indenização Bruta − IRRF",
        f"= {fmt_brl(calc['bruta'])} − {fmt_brl(calc['irrf'])} = {fmt_brl(calc['liq'])}",
        fmt_brl(calc['liq']), fmt_brl(calc['liq']), True
    )

    # ── Resumo consolidado
    st.markdown("#### 📋 Resumo Consolidado")
    resumo_data = {
        "Etapa": [
            "Total Comissões Brutas",
            "Total Comissões Corrigidas (UFIR)",
            "Indenização 1/12 Avos",
            "Base Aviso Prévio (3 últ. meses)",
            "Aviso Prévio 1/3",
            "INDENIZAÇÃO BRUTA",
            f"IRRF 15% ({'Retido' if calc['irrf']>0 else 'Não Retido'})",
            "VALOR LÍQUIDO A PAGAR"
        ],
        "Valor": [
            fmt_brl(calc['tb']),
            fmt_brl(calc['tc']),
            fmt_brl(calc['ind112']),
            fmt_brl(calc['bap']),
            fmt_brl(calc['avp']),
            fmt_brl(calc['bruta']),
            fmt_brl(calc['irrf']),
            fmt_brl(calc['liq'])
        ],
        "Base Legal": [
            "ERP Financeiro",
            "UFIR-RJ (Dec. 2394/98)",
            "Art. 27 Lei 4.886/65",
            "3 últimos meses pagos",
            "Art. 34 Lei 4.886/65",
            "1/12 + Aviso Prévio",
            "RIR Art. 718",
            "Bruta − IRRF"
        ]
    }
    df_resumo = pd.DataFrame(resumo_data)
    st.dataframe(df_resumo, hide_index=True, use_container_width=True)


# ══════════════ RELATÓRIO PDF ════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="sec-title">Gerar Relatório PDF para Assinatura</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#F0F6FF;border-radius:10px;padding:16px 20px;border-left:4px solid #2B6FD4;margin-bottom:20px;">
      <b style="color:#1B2F6B;">📄 Relatório oficial</b> para envio ao Controller para assinatura.
      Contém todos os cálculos detalhados, base legal e campos de aprovação.
    </div>
    """, unsafe_allow_html=True)

    col_e, col_c = st.columns(2)
    with col_e:
        elaborado_por = st.text_input("Elaborado por", value="Beatriz Esteves")
        cargo_elab    = st.text_input("Cargo", value="Gerente Financeira")
    with col_c:
        aprovado_por  = st.text_input("Aprovado por (Controller)", value="")
        cargo_aprov   = st.text_input("Cargo (Aprovador)", value="Controller")

    obs = st.text_area("Observações (opcional)", placeholder="Insira observações relevantes para este processo de rescisão...")

    if st.button("🖨️ Gerar PDF Profissional", type="primary", use_container_width=True):

        def gerar_pdf(rc_nome, rc_code, p_ini, p_fim, ann, grp, calc,
                      reter_irrf, ufir_calculo, ano_atual,
                      elab, cargo_e, aprov, cargo_a, obs_txt, logo_b64):
            buf_pdf = io.BytesIO()
            W, H = A4

            # Colors
            AZUL_D = colors.HexColor("#1B2F6B")
            AZUL   = colors.HexColor("#2B6FD4")
            AMAR   = colors.HexColor("#F5A800")
            VERDE  = colors.HexColor("#2B8C3C")
            CINZA  = colors.HexColor("#F4F6FA")
            CINZA2 = colors.HexColor("#E8ECF2")
            BRANCO = colors.white
            PRETO  = colors.HexColor("#1a1a1a")
            CINZA3 = colors.HexColor("#666666")

            # ── Canvas-based PDF with custom header/footer ──
            class NumberedCanvas(rl_canvas.Canvas):
                def __init__(self, *args, **kwargs):
                    rl_canvas.Canvas.__init__(self, *args, **kwargs)
                    self._saved_page_states = []
                def showPage(self):
                    self._saved_page_states.append(dict(self.__dict__))
                    self._startPage()
                def save(self):
                    num_pages = len(self._saved_page_states)
                    for state in self._saved_page_states:
                        self.__dict__.update(state)
                        self.draw_page_number(num_pages)
                        rl_canvas.Canvas.showPage(self)
                    rl_canvas.Canvas.save(self)
                def draw_page_number(self, page_count):
                    self.setFont("Helvetica", 8)
                    self.setFillColor(CINZA3)
                    self.drawRightString(W - 2*cm, 1.2*cm,
                        f"Página {self._pageNumber} de {page_count}")
                    # footer line
                    self.setStrokeColor(CINZA2)
                    self.line(2*cm, 1.6*cm, W-2*cm, 1.6*cm)
                    self.setFont("Helvetica", 7)
                    self.setFillColor(CINZA3)
                    self.drawString(2*cm, 1.0*cm,
                        "Grupo LLE · Departamento Financeiro · Rescisão conforme Lei 4.886/65")

            def header(c, doc):
                c.saveState()
                # Blue header bar
                c.setFillColor(AZUL_D)
                c.rect(0, H-3.2*cm, W, 3.2*cm, fill=1, stroke=0)
                # Logo
                if logo_b64:
                    try:
                        logo_bytes = base64.b64decode(logo_b64)
                        logo_buf = io.BytesIO(logo_bytes)
                        c.drawImage(logo_buf, 1.8*cm, H-2.8*cm, width=4.5*cm, height=2.2*cm,
                                   preserveAspectRatio=True, mask='auto')
                    except: pass
                # Title
                c.setFont("Helvetica-Bold", 13)
                c.setFillColor(BRANCO)
                c.drawString(7*cm, H-1.6*cm, "RESCISÃO DE REPRESENTANTE COMERCIAL")
                c.setFont("Helvetica", 9)
                c.setFillColor(colors.HexColor("#AABBDD"))
                c.drawString(7*cm, H-2.2*cm, "Lei 4.886/65 · Departamento Financeiro")
                # Yellow accent bar
                c.setFillColor(AMAR)
                c.rect(0, H-3.4*cm, W, 0.22*cm, fill=1, stroke=0)
                c.restoreState()

            def footer_first(c, doc):
                pass  # handled by NumberedCanvas

            # Document
            frame = Frame(2*cm, 2*cm, W-4*cm, H-5.5*cm, id='main')
            template = PageTemplate(id='main', frames=frame, onPage=header)
            doc = BaseDocTemplate(buf_pdf, pagesize=A4,
                                   rightMargin=2*cm, leftMargin=2*cm,
                                   topMargin=4*cm, bottomMargin=2.5*cm)
            doc.addPageTemplates([template])

            # Styles
            def sty(name, **kw):
                return ParagraphStyle(name, **kw)

            S_TITLE   = sty('title',   fontName='Helvetica-Bold', fontSize=11, textColor=AZUL_D, spaceAfter=4)
            S_SECHEAD = sty('sechead', fontName='Helvetica-Bold', fontSize=9,  textColor=AZUL,   spaceAfter=3, spaceBefore=10)
            S_BODY    = sty('body',    fontName='Helvetica',      fontSize=9,  textColor=PRETO,  spaceAfter=2)
            S_SMALL   = sty('small',   fontName='Helvetica',      fontSize=8,  textColor=CINZA3, spaceAfter=2)
            S_CENTER  = sty('center',  fontName='Helvetica',      fontSize=9,  alignment=TA_CENTER)
            S_RIGHT   = sty('right',   fontName='Helvetica',      fontSize=9,  alignment=TA_RIGHT)
            S_BOLD    = sty('bold',    fontName='Helvetica-Bold', fontSize=9,  textColor=PRETO)
            S_WHITE   = sty('white',   fontName='Helvetica-Bold', fontSize=9,  textColor=BRANCO)
            S_NOTA    = sty('nota',    fontName='Helvetica-Oblique', fontSize=7.5, textColor=CINZA3, spaceAfter=2)

            def brl(v):
                return f"R$ {float(v):,.2f}".replace(",","X").replace(".",",").replace("X",".")

            story = []

            # ── Identificação ──
            data_hoje = datetime.now().strftime("%d/%m/%Y")
            id_data = [
                ["Representante Comercial:", rc_nome, "Código:", str(rc_code)],
                ["Período das Comissões:", f"{p_ini} a {p_fim}", "Data do Cálculo:", data_hoje],
                ["UFIR-RJ Ano Atual:", f"{ufir_calculo:.4f}",  "Ano de Referência:", str(ano_atual)],
            ]
            t_id = Table(id_data, colWidths=[4.5*cm, 7*cm, 3.5*cm, 3.5*cm])
            t_id.setStyle(TableStyle([
                ('FONTNAME',  (0,0),(-1,-1), 'Helvetica'),
                ('FONTNAME',  (0,0),(0,-1),  'Helvetica-Bold'),
                ('FONTNAME',  (2,0),(2,-1),  'Helvetica-Bold'),
                ('FONTSIZE',  (0,0),(-1,-1), 8.5),
                ('TEXTCOLOR', (0,0),(0,-1),  CINZA3),
                ('TEXTCOLOR', (2,0),(2,-1),  CINZA3),
                ('TEXTCOLOR', (1,0),(1,-1),  PRETO),
                ('TEXTCOLOR', (3,0),(3,-1),  PRETO),
                ('BACKGROUND',(0,0),(-1,-1), CINZA),
                ('ROWBACKGROUNDS',(0,0),(-1,-1), [CINZA, BRANCO, CINZA]),
                ('TOPPADDING',(0,0),(-1,-1), 5),
                ('BOTTOMPADDING',(0,0),(-1,-1), 5),
                ('LEFTPADDING',(0,0),(-1,-1), 8),
                ('ROUNDEDCORNERS', [4]),
                ('BOX', (0,0),(-1,-1), 0.5, CINZA2),
            ]))
            story.append(t_id)
            story.append(Spacer(1, 0.4*cm))

            # ── Seção 1: Comissões por Ano ──
            story.append(Paragraph("1. COMISSÕES BRUTAS E CORREÇÃO MONETÁRIA (UFIR-RJ)", S_SECHEAD))
            story.append(HRFlowable(width="100%", thickness=1, color=AMAR, spaceAfter=6))

            hdr_ann = [
                [Paragraph("ANO", S_WHITE),
                 Paragraph("COMISSÃO BRUTA", S_WHITE),
                 Paragraph("UFIR DO ANO", S_WHITE),
                 Paragraph("UFIR ATUAL", S_WHITE),
                 Paragraph("COMISSÃO CORRIGIDA", S_WHITE),
                 Paragraph("VARIAÇÃO", S_WHITE)]
            ]
            rows_ann = []
            for _, row in ann.iterrows():
                var = ((row['Comissão Corrigida']/row['Comissão Bruta'])-1)*100 if row['Comissão Bruta']>0 else 0
                rows_ann.append([
                    Paragraph(str(int(row['Ano'])), S_BOLD),
                    Paragraph(brl(row['Comissão Bruta']), S_RIGHT),
                    Paragraph(f"{row['UFIR do Ano']:.4f}", S_CENTER),
                    Paragraph(f"{ufir_calculo:.4f}", S_CENTER),
                    Paragraph(brl(row['Comissão Corrigida']), S_RIGHT),
                    Paragraph(f"+{var:.2f}%", S_CENTER),
                ])
            total_var = ((calc['tc']/calc['tb'])-1)*100 if calc['tb']>0 else 0
            rows_ann.append([
                Paragraph("TOTAL", S_WHITE),
                Paragraph(brl(calc['tb']), S_WHITE),
                Paragraph("—", S_WHITE),
                Paragraph("—", S_WHITE),
                Paragraph(brl(calc['tc']), S_WHITE),
                Paragraph(f"+{total_var:.2f}%", S_WHITE),
            ])
            t_ann = Table(hdr_ann + rows_ann, colWidths=[2*cm, 3.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2.5*cm])
            ts = [
                ('BACKGROUND', (0,0), (-1,0), AZUL_D),
                ('BACKGROUND', (0,-1),(-1,-1), AZUL),
                ('ROWBACKGROUNDS', (0,1), (-1,-2), [BRANCO, CINZA]),
                ('FONTNAME',  (0,0),(-1,-1), 'Helvetica'),
                ('FONTSIZE',  (0,0),(-1,-1), 8),
                ('ALIGN',     (0,0),(-1,-1), 'CENTER'),
                ('VALIGN',    (0,0),(-1,-1), 'MIDDLE'),
                ('TOPPADDING',(0,0),(-1,-1), 5),
                ('BOTTOMPADDING',(0,0),(-1,-1), 5),
                ('GRID',      (0,0),(-1,-1), 0.3, CINZA2),
                ('BOX',       (0,0),(-1,-1), 1, AZUL_D),
                ('LINEBELOW', (0,0),(-1,0), 2, AMAR),
            ]
            t_ann.setStyle(TableStyle(ts))
            story.append(t_ann)
            story.append(Paragraph("* Fórmula: Corrigida = UFIR_Atual × Bruta_Ano ÷ UFIR_Ano (Dec. Estadual 2394/98)", S_NOTA))
            story.append(Spacer(1, 0.4*cm))

            # ── Seção 2: Comissões Mensais ──
            story.append(Paragraph("2. DETALHAMENTO MENSAL DAS COMISSÕES", S_SECHEAD))
            story.append(HRFlowable(width="100%", thickness=1, color=AMAR, spaceAfter=6))

            # Montar tabela mensal em 3 colunas lado a lado
            meses_list = [(row['Mês/Ano'], brl(row['Valor'])) for _, row in grp.iterrows()]
            # Dividir em grupos de 3 colunas
            hdr_mes = [Paragraph("MÊS/ANO", S_WHITE), Paragraph("COMISSÃO", S_WHITE),
                       Paragraph("MÊS/ANO", S_WHITE), Paragraph("COMISSÃO", S_WHITE),
                       Paragraph("MÊS/ANO", S_WHITE), Paragraph("COMISSÃO", S_WHITE)]
            # Pad to multiple of 3
            while len(meses_list) % 3 != 0:
                meses_list.append(("—", "—"))
            rows_mes = [hdr_mes]
            for i in range(0, len(meses_list), 3):
                r = []
                for j in range(3):
                    r.extend([Paragraph(meses_list[i+j][0], S_CENTER),
                               Paragraph(meses_list[i+j][1], S_RIGHT)])
                rows_mes.append(r)
            # Total
            rows_mes.append([
                Paragraph("TOTAL GERAL", S_WHITE), Paragraph(brl(calc['tb']), S_WHITE),
                Paragraph("", S_WHITE), Paragraph("", S_WHITE),
                Paragraph("", S_WHITE), Paragraph("", S_WHITE),
            ])
            t_mes = Table(rows_mes, colWidths=[2.8*cm, 2.8*cm, 2.8*cm, 2.8*cm, 2.8*cm, 2.8*cm])
            t_mes.setStyle(TableStyle([
                ('BACKGROUND',    (0,0), (-1,0),  AZUL_D),
                ('BACKGROUND',    (0,-1),(-1,-1), AZUL),
                ('ROWBACKGROUNDS',(0,1), (-1,-2), [BRANCO, CINZA]),
                ('FONTNAME',      (0,0),(-1,-1),  'Helvetica'),
                ('FONTSIZE',      (0,0),(-1,-1),  8),
                ('ALIGN',         (0,0),(-1,-1),  'CENTER'),
                ('VALIGN',        (0,0),(-1,-1),  'MIDDLE'),
                ('TOPPADDING',    (0,0),(-1,-1),  5),
                ('BOTTOMPADDING', (0,0),(-1,-1),  4),
                ('GRID',          (0,0),(-1,-1),  0.3, CINZA2),
                ('BOX',           (0,0),(-1,-1),  1, AZUL_D),
                ('LINEBELOW',     (0,0),(-1,0),   2, AMAR),
            ]))
            story.append(t_mes)
            story.append(Spacer(1, 0.4*cm))

            # ── Seção 3: Base Aviso Prévio ──
            story.append(Paragraph("3. BASE DO AVISO PRÉVIO — ÚLTIMOS 3 MESES", S_SECHEAD))
            story.append(HRFlowable(width="100%", thickness=1, color=AMAR, spaceAfter=6))
            u3_rows_pdf = calc['u3']
            hdr_ap = [[Paragraph("MÊS", S_WHITE), Paragraph("VALOR", S_WHITE), Paragraph("% DO TOTAL", S_WHITE)]]
            rows_ap = []
            for _, row in u3_rows_pdf.iterrows():
                pct = row['Valor']/calc['bap']*100
                rows_ap.append([
                    Paragraph(row['Mês/Ano'], S_CENTER),
                    Paragraph(brl(row['Valor']), S_RIGHT),
                    Paragraph(f"{pct:.1f}%", S_CENTER),
                ])
            rows_ap.append([
                Paragraph("SOMA (Base Aviso Prévio)", S_WHITE),
                Paragraph(brl(calc['bap']), S_WHITE),
                Paragraph("100%", S_WHITE),
            ])
            t_ap = Table(hdr_ap + rows_ap, colWidths=[6*cm, 5*cm, 5*cm])
            t_ap.setStyle(TableStyle([
                ('BACKGROUND',    (0,0),(-1,0),  AZUL_D),
                ('BACKGROUND',    (0,-1),(-1,-1), VERDE),
                ('ROWBACKGROUNDS',(0,1),(-1,-2),  [BRANCO, CINZA]),
                ('FONTNAME',      (0,0),(-1,-1),  'Helvetica'),
                ('FONTSIZE',      (0,0),(-1,-1),  9),
                ('ALIGN',         (0,0),(-1,-1),  'CENTER'),
                ('VALIGN',        (0,0),(-1,-1),  'MIDDLE'),
                ('TOPPADDING',    (0,0),(-1,-1),  6),
                ('BOTTOMPADDING', (0,0),(-1,-1),  6),
                ('GRID',          (0,0),(-1,-1),  0.3, CINZA2),
                ('BOX',           (0,0),(-1,-1),  1, AZUL_D),
                ('LINEBELOW',     (0,0),(-1,0),   2, AMAR),
            ]))
            story.append(t_ap)
            story.append(Paragraph("* Base Aviso Prévio = soma dos 3 últimos meses de comissão efetivamente pagos (Art. 34 Lei 4.886/65)", S_NOTA))
            story.append(Spacer(1, 0.4*cm))

            # ── Seção 4: Cálculo da Indenização ──
            story.append(Paragraph("4. CÁLCULO DA INDENIZAÇÃO — RESUMO CONSOLIDADO", S_SECHEAD))
            story.append(HRFlowable(width="100%", thickness=1, color=AMAR, spaceAfter=6))

            calc_rows = [
                [Paragraph("ITEM", S_WHITE), Paragraph("FÓRMULA", S_WHITE),
                 Paragraph("VALOR", S_WHITE), Paragraph("BASE LEGAL", S_WHITE)],
                ["Comissões Brutas (histórico)", "Σ comissões pagas", brl(calc['tb']), "ERP Financeiro"],
                ["Comissões Corrigidas (UFIR)", "Σ (UFIR_atual × Bruta ÷ UFIR_ano)", brl(calc['tc']), "Dec. 2394/98"],
                ["Indenização 1/12 Avos", "Total Corrigido ÷ 12", brl(calc['ind112']), "Art. 27 Lei 4.886/65"],
                ["Base Aviso Prévio", "3 últimos meses pagos", brl(calc['bap']), "Art. 34 Lei 4.886/65"],
                ["Aviso Prévio 1/3", "Base Aviso ÷ 3", brl(calc['avp']), "Art. 34 Lei 4.886/65"],
                [Paragraph("INDENIZAÇÃO BRUTA", S_WHITE),
                 Paragraph("1/12 Avos + Aviso Prévio", S_WHITE),
                 Paragraph(brl(calc['bruta']), S_WHITE),
                 Paragraph("Lei 4.886/65", S_WHITE)],
                [f"IRRF (15%) — {'Retido' if calc['irrf']>0 else 'NÃO RETIDO'}", "Bruta × 15%", brl(calc['irrf']), "RIR Art. 718"],
                [Paragraph("VALOR LÍQUIDO A PAGAR", ParagraphStyle('vl', fontName='Helvetica-Bold', fontSize=10, textColor=BRANCO)),
                 Paragraph("Bruta − IRRF", S_WHITE),
                 Paragraph(brl(calc['liq']), ParagraphStyle('vlv', fontName='Helvetica-Bold', fontSize=10, textColor=AMAR)),
                 Paragraph("—", S_WHITE)],
            ]
            t_calc = Table(calc_rows, colWidths=[5.5*cm, 5*cm, 3*cm, 3*cm])
            t_calc.setStyle(TableStyle([
                ('BACKGROUND',    (0,0),(-1,0),   AZUL_D),
                ('BACKGROUND',    (0,6),(-1,6),   AZUL),
                ('BACKGROUND',    (0,8),(-1,8),   AZUL_D),
                ('ROWBACKGROUNDS',(0,1),(-1,5),   [BRANCO, CINZA, BRANCO, CINZA, BRANCO]),
                ('BACKGROUND',    (0,7),(-1,7),   CINZA),
                ('FONTNAME',      (0,0),(-1,-1),  'Helvetica'),
                ('FONTNAME',      (0,1),(0,5),    'Helvetica-Bold'),
                ('TEXTCOLOR',     (0,1),(0,5),    AZUL_D),
                ('FONTSIZE',      (0,0),(-1,-1),  8.5),
                ('ALIGN',         (2,0),(-1,-1),  'RIGHT'),
                ('ALIGN',         (3,0),(3,-1),   'CENTER'),
                ('VALIGN',        (0,0),(-1,-1),  'MIDDLE'),
                ('TOPPADDING',    (0,0),(-1,-1),  6),
                ('BOTTOMPADDING', (0,0),(-1,-1),  6),
                ('LEFTPADDING',   (0,0),(-1,-1),  8),
                ('GRID',          (0,0),(-1,-1),  0.3, CINZA2),
                ('BOX',           (0,0),(-1,-1),  1.5, AZUL_D),
                ('LINEBELOW',     (0,0),(-1,0),   2, AMAR),
                ('LINEABOVE',     (0,8),(-1,8),   2, AMAR),
            ]))
            story.append(t_calc)
            story.append(Spacer(1, 0.5*cm))

            # ── Observações ──
            if obs_txt.strip():
                story.append(Paragraph("5. OBSERVAÇÕES", S_SECHEAD))
                story.append(HRFlowable(width="100%", thickness=1, color=AMAR, spaceAfter=6))
                story.append(Paragraph(obs_txt, S_BODY))
                story.append(Spacer(1, 0.4*cm))

            # ── Assinaturas ──
            n_sec = 6 if obs_txt.strip() else 5
            story.append(Paragraph(f"{n_sec}. APROVAÇÕES E ASSINATURAS", S_SECHEAD))
            story.append(HRFlowable(width="100%", thickness=1, color=AMAR, spaceAfter=10))

            ass_data = [
                [Paragraph(elab or "_________________________", S_CENTER),
                 Paragraph("", S_CENTER),
                 Paragraph(aprov or "_________________________", S_CENTER)],
                [Paragraph(f"<b>{elab or 'Elaborado por'}</b>", S_CENTER),
                 Paragraph("", S_CENTER),
                 Paragraph(f"<b>{aprov or 'Aprovado por'}</b>", S_CENTER)],
                [Paragraph(cargo_e, ParagraphStyle('cargo', fontName='Helvetica', fontSize=8, textColor=CINZA3, alignment=TA_CENTER)),
                 Paragraph("", S_CENTER),
                 Paragraph(cargo_a, ParagraphStyle('cargo', fontName='Helvetica', fontSize=8, textColor=CINZA3, alignment=TA_CENTER))],
                [Paragraph(f"Data: ___/___/______", S_SMALL),
                 Paragraph("", S_CENTER),
                 Paragraph(f"Data: ___/___/______", S_SMALL)],
            ]
            t_ass = Table(ass_data, colWidths=[7*cm, 2.5*cm, 7*cm])
            t_ass.setStyle(TableStyle([
                ('FONTNAME',      (0,0),(-1,-1), 'Helvetica'),
                ('ALIGN',         (0,0),(-1,-1), 'CENTER'),
                ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
                ('TOPPADDING',    (0,0),(-1,-1), 4),
                ('BOTTOMPADDING', (0,0),(-1,-1), 4),
                ('LINEABOVE',     (0,0),(0,0),   1, AZUL_D),
                ('LINEABOVE',     (2,0),(2,0),   1, AZUL_D),
                ('BOX',           (0,0),(0,-1),  0.5, CINZA2),
                ('BOX',           (2,0),(2,-1),  0.5, CINZA2),
                ('BACKGROUND',    (0,0),(0,-1),  CINZA),
                ('BACKGROUND',    (2,0),(2,-1),  CINZA),
            ]))
            story.append(t_ass)

            doc.build(story, canvasmaker=NumberedCanvas)
            return buf_pdf.getvalue()

        with st.spinner("Gerando PDF..."):
            pdf_bytes = gerar_pdf(
                rc_nome, rc_code, p_ini, p_fim,
                ann, grp, calc, reter_irrf, ufir_calculo, ano_atual,
                elaborado_por, cargo_elab, aprovado_por, cargo_aprov, obs,
                LOGO_PDF_B64
            )

        nome_arquivo = f"Rescisao_{rc_code}_{rc_nome.split()[0]}_{datetime.now().strftime('%Y%m%d')}.pdf"
        st.success(f"✅ PDF gerado com sucesso! {len(pdf_bytes)//1024} KB")
        st.download_button(
            label="⬇️ Baixar Relatório PDF",
            data=pdf_bytes,
            file_name=nome_arquivo,
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )

# ── FOOTER ───────────────────────────────────────────────────────────────────
# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="lle-footer">
  GRUPO LLE · DEPARTAMENTO FINANCEIRO · RESCISÃO CONFORME LEI 4.886/65
</div>
""", unsafe_allow_html=True)
