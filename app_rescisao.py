import streamlit as st
import pandas as pd
import numpy as np
import io
import base64
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image as RLImage, KeepTogether
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

# ── PDF COLOR CONSTANTS (module level for NumberedCanvas scope) ──────────────
from reportlab.lib import colors as _rl_colors
PDF_AZUL_D = _rl_colors.HexColor("#1B2F6B")
PDF_AZUL   = _rl_colors.HexColor("#2B6FD4")
PDF_AMAR   = _rl_colors.HexColor("#F5A800")
PDF_VERDE  = _rl_colors.HexColor("#2B8C3C")
PDF_CINZA  = _rl_colors.HexColor("#F4F6FA")
PDF_CINZA2 = _rl_colors.HexColor("#E8ECF2")
PDF_CINZA3 = _rl_colors.HexColor("#666666")
PDF_BRANCO = _rl_colors.white
PDF_PRETO  = _rl_colors.HexColor("#1a1a1a")

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
.block-container {{ padding-top: 0 !important; padding-left: 1rem !important; padding-right: 1rem !important; max-width: 100% !important; }}
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
    margin: 20px 0 12px 0;
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
    background: {AZUL_ESC};
    padding: 16px 28px 16px 28px;
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 0 -1rem 0 -1rem;
    border-bottom: 4px solid {AMARELO};
}}
.lle-header-icon {{
    font-size: 1.4rem;
    flex-shrink: 0;
}}
.lle-header-main {{
    color: white;
    font-size: 1.1rem;
    font-weight: 800;
    letter-spacing: 0.3px;
    line-height: 1.2;
}}
.lle-header-sub {{
    color: rgba(255,255,255,0.6);
    font-size: 0.7rem;
    font-weight: 500;
    margin-top: 3px;
    letter-spacing: 0.4px;
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
    background: #041747 !important;
}}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div {{
    color: rgba(255,255,255,0.88) !important;
    font-size: 0.78rem !important;
}}
/* Sidebar inputs - dark bg, white text */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {{
    background: #041747 !important;
    color: #F5A800 !important;
    -webkit-text-fill-color: #F5A800 !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 6px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
}}
section[data-testid="stSidebar"] [data-baseweb="input"] {{
    background: #041747 !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 6px !important;
}}
section[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {{
    background: #041747 !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: {AMARELO} !important;
}}
section[data-testid="stSidebar"] [data-baseweb="select"] span {{
    color: {AMARELO} !important;
    -webkit-text-fill-color: {AMARELO} !important;
}}
section[data-testid="stSidebar"] [data-baseweb="popover"] {{
    background: #041747 !important;
}}
section[data-testid="stSidebar"] [role="option"] {{
    background: #041747 !important;
    color: white !important;
}}
section[data-testid="stSidebar"] [role="option"]:hover {{
    background: {AZUL} !important;
}}
section[data-testid="stSidebar"] .stNumberInput > div {{
    background: #041747 !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 6px !important;
}}
section[data-testid="stSidebar"] button[kind="stepperButton"],
section[data-testid="stSidebar"] button[data-testid="stNumberInputStepUp"],
section[data-testid="stSidebar"] button[data-testid="stNumberInputStepDown"] {{
    background: #2B6FD4 !important;
    color: white !important;
    border-color: rgba(255,255,255,0.3) !important;
}}
/* data_editor in sidebar */
section[data-testid="stSidebar"] .stDataFrame {{
    background: #041747 !important;
}}
section[data-testid="stSidebar"] .stDataFrame td,
section[data-testid="stSidebar"] .stDataFrame th {{
    color: white !important;
    background: #041747 !important;
    font-size: 0.75rem !important;
}}
section[data-testid="stSidebar"] .stFileUploader {{
    background: #041747;
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
</div>
<div class="lle-header-title">
  <span class="lle-header-icon">📋</span>
  <div>
    <div class="lle-header-main">Rescisão de Representante Comercial</div>
    <div class="lle-header-sub">Grupo LLE — Departamento Financeiro</div>
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
    val_col      = next((c for c in df.columns if "Vlr" in c and "Desdobramento" in c), None) or \
                   next((c for c in df.columns if "Vlr" in c), None)
    nat_col      = next((c for c in df.columns if "Natureza" in c), None) or \
                   next((c for c in df.columns if "natureza" in c.lower()), None)
    baixa_col    = next((c for c in df.columns if c == "Data Baixa"), None) or \
                   next((c for c in df.columns if "Baixa" in c and "Dt" in c), None)
    concil_col   = next((c for c in df.columns if "Concilia" in c), None)
    neg_col      = next((c for c in df.columns if "Negoci" in c), None)
    parceiro_col = next((c for c in df.columns if c == "Parceiro"), None)
    nome_col     = next((c for c in df.columns if "Nome Parceiro" in c), None)
    return df, val_col, nat_col, baixa_col, concil_col, neg_col, parceiro_col, nome_col

def filter_commissions(df, val_col, nat_col, baixa_col, concil_col):
    if nat_col:
        mask = df[nat_col].astype(str).str.contains("Comissão s/ vendas|Comissao s/ vendas", case=False, na=False)
        df_f = df[mask].copy()
    else:
        df_f = df.copy()
    df_f = df_f.dropna(subset=[val_col])
    df_f[val_col] = pd.to_numeric(df_f[val_col], errors='coerce')
    df_f = df_f[df_f[val_col] > 0]

    # ── DATA DE REFERÊNCIA: Dt. Conciliação com fallback para Data Baixa ──
    if concil_col and concil_col in df_f.columns:
        df_f[concil_col] = pd.to_datetime(df_f[concil_col], errors='coerce')
        if baixa_col and baixa_col in df_f.columns:
            df_f[baixa_col] = pd.to_datetime(df_f[baixa_col], errors='coerce')
            # Usa conciliação; onde for NaT, usa baixa
            df_f["_data_ref"] = df_f[concil_col].fillna(df_f[baixa_col])
        else:
            df_f["_data_ref"] = df_f[concil_col]
        date_ref = "_data_ref"
    elif baixa_col and baixa_col in df_f.columns:
        df_f[baixa_col] = pd.to_datetime(df_f[baixa_col], errors='coerce')
        date_ref = baixa_col
    else:
        date_ref = None

    if date_ref:
        df_f = df_f.dropna(subset=[date_ref])
        df_f["Mês"] = df_f[date_ref].dt.month
        df_f["Ano"] = df_f[date_ref].dt.year
        df_f["_data_ref_str"] = df_f[date_ref].dt.strftime("%d/%m/%Y")

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

    # Tabela UFIR editável com data_editor
    st.markdown('<p style="color:rgba(255,255,255,0.6);font-size:0.7rem;margin-bottom:4px;">Valores oficiais UFIR-RJ · Edite se necessário</p>', unsafe_allow_html=True)
    df_ufir_edit = pd.DataFrame(
        sorted(st.session_state.ufir_table.items()), columns=["Ano","UFIR-RJ"]
    )
    df_edited = st.data_editor(
        df_ufir_edit,
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Ano": st.column_config.NumberColumn("Ano", min_value=2000, max_value=2100, step=1, format="%d"),
            "UFIR-RJ": st.column_config.NumberColumn("UFIR-RJ", min_value=0.0001, format="%.4f"),
        },
        key="ufir_editor"
    )
    # Sync edits back
    if df_edited is not None and len(df_edited) > 0:
        st.session_state.ufir_table = dict(zip(df_edited["Ano"].astype(int), df_edited["UFIR-RJ"]))
        UFIR_TABLE.update(st.session_state.ufir_table)

    ufir_ano = float(st.session_state.ufir_table.get(ano_atual, list(st.session_state.ufir_table.values())[-1]))

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
    df, val_col, nat_col, baixa_col, concil_col, neg_col, parceiro_col, nome_col = load_file(uploaded)
except Exception as e:
    st.error(f"Erro ao ler o arquivo: {e}")
    st.stop()

if val_col is None:
    st.error("Coluna de valor não encontrada. Verifique se o arquivo contém 'Vlr do Desdobramento'.")
    st.stop()

df_f = filter_commissions(df, val_col, nat_col, baixa_col, concil_col)
# date_col kept for display in Dados Brutos
date_col = concil_col or baixa_col or neg_col
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
  <div class="rc-bar-item">
    <span class="rc-bar-label">Data de Referência</span>
    <span class="rc-bar-value" style="font-size:0.78rem;">{"Dt. Conciliação" if concil_col else "Data Baixa"}</span>
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
    st.dataframe(audit_df.style.map(color_st, subset=["Status"]),
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
    st.markdown("#### 3️⃣ Indenização (1/12 Avos) — Art. 27 ")
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
    st.markdown("#### 5️⃣ Aviso Prévio (1/3) — Art. 34 ")
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
            "Art. 27 ",
            "3 últimos meses pagos",
            "Art. 34 ",
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
            """PDF paisagem A4 — 1 página, formato igual ao modelo Excel."""
            from reportlab.lib.pagesizes import landscape, A4
            from reportlab.pdfgen import canvas as cv
            buf_pdf = io.BytesIO()

            W, H = landscape(A4)   # 841.89 x 595.28 pt
            M = 28.35              # 1 cm

            c = cv.Canvas(buf_pdf, pagesize=(W, H))

            AZUL  = PDF_AZUL_D
            AMAR  = PDF_AMAR
            BRC   = PDF_BRANCO
            CZ    = PDF_CINZA
            CZ2   = PDF_CINZA2
            CZ3   = PDF_CINZA3
            VERDE = PDF_VERDE

            def brl(v):
                try: return f"R$ {float(v):,.2f}".replace(",","X").replace(".",",").replace("X",".")
                except: return "—"

            # ── Margens ──────────────────────────────────────────────────────
            LM = 1.5*M   # left margin
            RM = W - 1.5*M
            CW = RM - LM  # content width

            # ════════════════════════════════════════════════════════════════
            # 1. CABEÇALHO
            # ════════════════════════════════════════════════════════════════
            # Barra azul
            c.setFillColor(AZUL)
            c.rect(0, H - 2.5*M, W, 2.5*M, fill=1, stroke=0)
            # Linha amarela
            c.setFillColor(AMAR)
            c.rect(0, H - 2.65*M, W, 0.18*M, fill=1, stroke=0)

            # Logo — write to tmp file (ReportLab needs path, not BytesIO)
            if logo_b64:
                try:
                    import tempfile, os
                    lb = base64.b64decode(logo_b64)
                    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                    tmp.write(lb); tmp.close()
                    c.drawImage(tmp.name, LM, H-2.35*M,
                                width=4.8*M, height=1.9*M,
                                preserveAspectRatio=True, mask='auto')
                    os.unlink(tmp.name)
                except: pass

            # Título centralizado
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(BRC)
            c.drawCentredString(W/2, H - 1.45*M, "RESCISÃO DE REPRESENTANTE COMERCIAL")
            c.setFont("Helvetica", 8)
            c.setFillColor(CZ3)
            c.drawCentredString(W/2, H - 2.05*M,
                "Grupo LLE  ·  Departamento Financeiro")

            # Data direita
            c.setFont("Helvetica", 8)
            c.setFillColor(BRC)
            c.drawRightString(RM, H - 1.45*M, datetime.now().strftime("%d/%m/%Y"))

            # ════════════════════════════════════════════════════════════════
            # 2. FAIXA IDENTIFICAÇÃO
            # ════════════════════════════════════════════════════════════════
            y = H - 3.3*M
            c.setFillColor(CZ)
            c.roundRect(LM, y - 1.0*M, CW, 1.0*M, 3, fill=1, stroke=0)
            c.setStrokeColor(CZ2)
            c.setLineWidth(0.5)
            c.roundRect(LM, y - 1.0*M, CW, 1.0*M, 3, fill=0, stroke=1)

            fields = [
                ("REPRESENTANTE", rc_nome[:50]),
                ("CÓDIGO", str(rc_code)),
                ("PERÍODO", f"{p_ini} a {p_fim}"),
                (f"UFIR-RJ {ano_atual}", f"{ufir_calculo:.4f}"),
            ]
            col_widths = [CW*0.45, CW*0.12, CW*0.28, CW*0.15]
            cx = LM + 0.4*M
            for lb, vl, fw in zip([f[0] for f in fields],
                                   [f[1] for f in fields], col_widths):
                c.setFont("Helvetica-Bold", 6.5)
                c.setFillColor(CZ3)
                c.drawString(cx, y - 0.32*M, lb)
                c.setFont("Helvetica-Bold", 9)
                c.setFillColor(AZUL)
                c.drawString(cx, y - 0.72*M, vl)
                cx += fw

            # ════════════════════════════════════════════════════════════════
            # 3. CONTEÚDO PRINCIPAL — 2 colunas
            # ════════════════════════════════════════════════════════════════
            y = H - 4.6*M
            col1_x = LM
            col2_x = LM + CW*0.52 + 0.3*M
            col1_w = CW*0.52
            col2_w = CW*0.48 - 0.3*M

            # ── helpers ──────────────────────────────────────────────────────
            def hdr(x, y, w, txt):
                c.setFillColor(AZUL)
                c.rect(x, y - 0.48*M, w, 0.48*M, fill=1, stroke=0)
                c.setFont("Helvetica-Bold", 8.5)
                c.setFillColor(BRC)
                c.drawString(x + 0.3*M, y - 0.32*M, txt)
                return y - 0.55*M

            def row(x, y, w, lbl, val, bold=False, bg=None, fg=None, fs=8):
                row_h = 0.42*M
                if bg:
                    c.setFillColor(bg)
                    c.rect(x, y - row_h, w, row_h, fill=1, stroke=0)
                fn = "Helvetica-Bold" if bold else "Helvetica"
                fc = fg if fg else AZUL
                c.setFont(fn, fs)
                c.setFillColor(fc)
                c.drawString(x + 0.3*M, y - row_h + 0.12*M, lbl)
                c.drawRightString(x + w - 0.3*M, y - row_h + 0.12*M, val)
                return y - row_h

            def tbl_hdr(x, y, w, cols, col_ws):
                c.setFillColor(CZ2)
                c.rect(x, y - 0.36*M, w, 0.36*M, fill=1, stroke=0)
                c.setFont("Helvetica-Bold", 7)
                c.setFillColor(AZUL)
                cx2 = x
                for col, cw in zip(cols, col_ws):
                    c.drawCentredString(cx2 + cw/2, y - 0.24*M, col)
                    cx2 += cw
                return y - 0.4*M

            # ════════════════════════════
            # COLUNA 1 — Tabela por ano
            # ════════════════════════════
            y1 = hdr(col1_x, y, col1_w, "COMISSÕES BRUTAS E CORREÇÃO UFIR-RJ")

            cws = [col1_w*0.18, col1_w*0.28, col1_w*0.18, col1_w*0.36]
            y1 = tbl_hdr(col1_x, y1, col1_w,
                         ["ANO","COMISSÃO BRUTA","UFIR","COMISSÃO CORRIGIDA"], cws)

            for idx, (_, r) in enumerate(ann.iterrows()):
                bg = CZ if idx%2==0 else BRC
                c.setFillColor(bg)
                c.rect(col1_x, y1-0.38*M, col1_w, 0.38*M, fill=1, stroke=0)
                c.setFont("Helvetica", 8)
                c.setFillColor(AZUL)
                vals2 = [str(int(r["Ano"])), brl(r["Comissão Bruta"]),
                         f"{r['UFIR do Ano']:.4f}" if pd.notna(r['UFIR do Ano']) else "—",
                         brl(r["Comissão Corrigida"])]
                cx2 = col1_x
                for v, cw in zip(vals2, cws):
                    c.drawCentredString(cx2+cw/2, y1-0.26*M, v)
                    cx2 += cw
                y1 -= 0.4*M

            # Total
            c.setFillColor(AZUL)
            c.rect(col1_x, y1-0.44*M, col1_w, 0.44*M, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 8.5)
            c.setFillColor(BRC)
            tot_vals = ["TOTAL", brl(calc['tb']), "—", brl(calc['tc'])]
            cx2 = col1_x
            for v, cw in zip(tot_vals, cws):
                c.drawCentredString(cx2+cw/2, y1-0.29*M, v)
                cx2 += cw
            y1 -= 0.55*M

            # Nota
            c.setFont("Helvetica-Oblique", 6.5)
            c.setFillColor(CZ3)
            c.drawString(col1_x, y1-0.22*M,
                f"* Corrigida = UFIR_{ano_atual} × Comissão ÷ UFIR_Ano   (Dec. Est. 2394/98)")
            y1 -= 0.55*M

            # ── Cálculo ──────────────────────────────────────────────────────
            y1 = hdr(col1_x, y1, col1_w, "CÁLCULO DA INDENIZAÇÃO")

            y1 = row(col1_x, y1, col1_w,
                     "Base de Indenização (Total Corrigido)", brl(calc['tc']))
            y1 = row(col1_x, y1, col1_w,
                     "Valor a Indenizar (1/12 Avos)", brl(calc['ind112']), bg=CZ)

            y1 -= 0.2*M  # espaço

            y1 = row(col1_x, y1, col1_w,
                     "Base Aviso Prévio", brl(calc['bap']))
            u3_str = "  → " + " · ".join(calc['u3']['Mês/Ano'].tolist())
            c.setFont("Helvetica-Oblique", 7.5)
            c.setFillColor(CZ3)
            c.drawString(col1_x+0.3*M, y1-0.22*M, u3_str)
            y1 -= 0.32*M
            y1 = row(col1_x, y1, col1_w,
                     "Valor Aviso Prévio (1/3)", brl(calc['avp']), bg=CZ)

            y1 -= 0.2*M  # espaço

            # Indenização Total a Receber (destaque)
            c.setFillColor(AZUL)
            c.rect(col1_x, y1-0.5*M, col1_w, 0.5*M, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 9.5)
            c.setFillColor(BRC)
            c.drawString(col1_x+0.3*M, y1-0.34*M, "Indenização Total a Receber")
            c.drawRightString(col1_x+col1_w-0.3*M, y1-0.34*M, brl(calc['bruta']))
            y1 -= 0.6*M

            y1 = row(col1_x, y1, col1_w,
                     f"IRRF (15%)", brl(calc['irrf']), bg=CZ)

            y1 -= 0.1*M
            # Valor Líquido — amarelo
            c.setFillColor(AMAR)
            c.rect(col1_x, y1-0.54*M, col1_w, 0.54*M, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(AZUL)
            c.drawString(col1_x+0.3*M, y1-0.37*M, "Indenização - Valor Líquido")
            c.drawRightString(col1_x+col1_w-0.3*M, y1-0.37*M, brl(calc['liq']))
            y1 -= 0.65*M

            # ════════════════════════════
            # COLUNA 2 — UFIR + Observações
            # ════════════════════════════
            y2 = hdr(col2_x, y, col2_w, "TABELA UFIR-RJ DE REFERÊNCIA")

            # UFIR table header
            ufir_cws = [col2_w*0.35, col2_w*0.35, col2_w*0.30]
            y2 = tbl_hdr(col2_x, y2, col2_w, ["ANO","UFIR-RJ","ANO"], ufir_cws)  # placeholder

            # Build UFIR table using only years present in the calculation
            years_used = sorted([int(a) for a in ann["Ano"]])
            # Get all years from UFIR_TABLE that are between min year and current year
            # We'll pass the ufir_table as a param - use calc years + context
            # For now use the ann data to get ufir values
            ufir_rows = [(int(r["Ano"]), r["UFIR do Ano"]) for _, r in ann.iterrows() if pd.notna(r["UFIR do Ano"])]
            # Also show current year if not in ann
            if ano_atual not in [r[0] for r in ufir_rows]:
                ufir_rows.append((ano_atual, ufir_calculo))
            ufir_rows.sort()

            # Split into 2 columns for the UFIR table
            half_u = (len(ufir_rows)+1)//2
            left_u  = ufir_rows[:half_u]
            right_u = ufir_rows[half_u:]
            sub_uw  = col2_w/2 - 0.1*M

            # Sub-headers
            for sx in [col2_x, col2_x + sub_uw + 0.2*M]:
                c.setFillColor(CZ2)
                c.rect(sx, y2-0.33*M, sub_uw, 0.33*M, fill=1, stroke=0)
                c.setFont("Helvetica-Bold", 7)
                c.setFillColor(AZUL)
                c.drawCentredString(sx + sub_uw*0.4, y2-0.22*M, "ANO")
                c.drawCentredString(sx + sub_uw*0.8, y2-0.22*M, "UFIR-RJ")
            y2 -= 0.37*M

            y2L, y2R = y2, y2
            for idx, (ano_u, ufir_u) in enumerate(left_u):
                bg = CZ if idx%2==0 else BRC
                c.setFillColor(bg)
                c.rect(col2_x, y2L-0.34*M, sub_uw, 0.34*M, fill=1, stroke=0)
                c.setFont("Helvetica", 7.5)
                c.setFillColor(AZUL)
                c.drawCentredString(col2_x+sub_uw*0.4, y2L-0.23*M, str(ano_u))
                c.drawCentredString(col2_x+sub_uw*0.8, y2L-0.23*M, f"{ufir_u:.4f}")
                y2L -= 0.35*M

            sx2 = col2_x + sub_uw + 0.2*M
            for idx, (ano_u, ufir_u) in enumerate(right_u):
                bg = CZ if idx%2==0 else BRC
                c.setFillColor(bg)
                c.rect(sx2, y2R-0.34*M, sub_uw, 0.34*M, fill=1, stroke=0)
                c.setFont("Helvetica", 7.5)
                c.setFillColor(AZUL)
                c.drawCentredString(sx2+sub_uw*0.4, y2R-0.23*M, str(ano_u))
                c.drawCentredString(sx2+sub_uw*0.8, y2R-0.23*M, f"{ufir_u:.4f}")
                y2R -= 0.35*M

            y2 = min(y2L, y2R) - 0.3*M

            # UFIR do ano atual em destaque
            c.setFillColor(AZUL)
            c.rect(col2_x, y2-0.44*M, col2_w, 0.44*M, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 8.5)
            c.setFillColor(AMAR)
            c.drawString(col2_x+0.3*M, y2-0.29*M, f"UFIR-RJ {ano_atual} (Ano de Referência)")
            c.drawRightString(col2_x+col2_w-0.3*M, y2-0.29*M, f"{ufir_calculo:.4f}")
            y2 -= 0.55*M

            # Observações
            if obs_txt and obs_txt.strip():
                y2 = hdr(col2_x, y2, col2_w, "OBSERVAÇÕES")
                c.setFont("Helvetica", 8)
                c.setFillColor(AZUL)
                # Simple word wrap
                words = obs_txt.split()
                line_txt = ""
                max_w = col2_w - 0.6*M
                for word in words:
                    test = (line_txt+" "+word).strip()
                    if c.stringWidth(test,"Helvetica",8) <= max_w:
                        line_txt = test
                    else:
                        c.drawString(col2_x+0.3*M, y2-0.28*M, line_txt)
                        y2 -= 0.36*M
                        line_txt = word
                if line_txt:
                    c.drawString(col2_x+0.3*M, y2-0.28*M, line_txt)
                    y2 -= 0.36*M

            # ════════════════════════════════════════════════════════════════
            # 4. ASSINATURAS — sempre fixas no rodapé
            # ════════════════════════════════════════════════════════════════
            y_ass = 3.5*M   # sempre 3.5 cm do fundo

            c.setFillColor(CZ)
            c.roundRect(LM, y_ass - 0.15*M, CW, 2.8*M, 3, fill=1, stroke=0)
            c.setStrokeColor(CZ2)
            c.setLineWidth(0.4)
            c.roundRect(LM, y_ass - 0.15*M, CW, 2.8*M, 3, fill=0, stroke=1)

            ass_section_w = CW/2 - 0.5*M
            for j, (nome, cargo) in enumerate([
                (elab or "________________________________", cargo_e),
                (aprov or "________________________________", cargo_a)
            ]):
                ax = LM + 0.8*M + j*(ass_section_w + 1.0*M)
                # Linha assinatura
                c.setStrokeColor(AZUL)
                c.setLineWidth(1)
                c.line(ax, y_ass + 1.8*M, ax + ass_section_w, y_ass + 1.8*M)
                # Nome
                c.setFont("Helvetica-Bold", 9)
                c.setFillColor(AZUL)
                c.drawCentredString(ax + ass_section_w/2, y_ass + 1.5*M, nome)
                # Cargo
                c.setFont("Helvetica", 8)
                c.setFillColor(CZ3)
                c.drawCentredString(ax + ass_section_w/2, y_ass + 1.15*M, cargo)
                # Data
                c.setFont("Helvetica", 8)
                c.setFillColor(AZUL)
                c.drawCentredString(ax + ass_section_w/2, y_ass + 0.6*M,
                                    "Data: _____ / _____ / ____________")

            # ════════════════════════════════════════════════════════════════
            # 5. RODAPÉ
            # ════════════════════════════════════════════════════════════════
            c.setFillColor(AZUL)
            c.rect(0, 0, W, 0.9*M, fill=1, stroke=0)
            c.setFillColor(AMAR)
            c.rect(0, 0.9*M, W, 0.12*M, fill=1, stroke=0)
            c.setFont("Helvetica", 7.5)
            c.setFillColor(BRC)
            c.drawCentredString(W/2, 0.32*M,
                "Grupo LLE  ·  Departamento Financeiro  ·  ")
            c.setFont("Helvetica-Bold", 7.5)
            c.setFillColor(AMAR)
            c.drawRightString(W-1.2*M, 0.32*M, "1 / 1")

            c.save()
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
  GRUPO LLE · DEPARTAMENTO FINANCEIRO · 
</div>
""", unsafe_allow_html=True)
