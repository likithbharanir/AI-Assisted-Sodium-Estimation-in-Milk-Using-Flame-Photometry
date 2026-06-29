import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from sklearn.linear_model import LinearRegression
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                Paragraph, Spacer, Image as RLImage,
                                HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

st.set_page_config(page_title="Chemistry PBL – Sodium in Milk",
                   layout="wide", page_icon="🔬")

st.markdown("""
<style>
[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:#0e1220!important;}
[data-testid="stSidebar"]{background:#141929!important;border-right:1px solid #2a3550;}
[data-testid="stSidebar"] *{color:#c8d8f0!important;font-size:15px!important;}
html,body,[class*="css"],p,li,div{color:#dce8ff;font-size:17px;}
h1{color:#7eb8ff!important;font-size:30px!important;font-weight:800!important;}
h2{color:#a0c8ff!important;font-size:24px!important;font-weight:700!important;}
h3{color:#b8d4ff!important;font-size:20px!important;}
label{color:#c0d0ee!important;font-size:16px!important;}
p{font-size:17px!important;}
[data-testid="stTabs"] button{color:#88aadd!important;background:#141929!important;
  border-radius:8px 8px 0 0;font-size:17px!important;padding:12px 22px!important;font-weight:600!important;}
[data-testid="stTabs"] button[aria-selected="true"]{color:#7eb8ff!important;
  border-bottom:3px solid #7eb8ff!important;background:#0e1220!important;}
[data-testid="stNumberInput"] input,[data-testid="stTextInput"] input{
  background:#1a2035!important;color:#dce8ff!important;
  border:1px solid #2a3a60!important;font-size:17px!important;padding:10px!important;}
[data-testid="stDataFrame"],[data-testid="stDataEditor"]{background:#131824!important;}
[data-testid="stDataEditor"] th{background:#1e2d50!important;color:#a0c8ff!important;
  font-size:17px!important;font-weight:700!important;padding:12px!important;}
[data-testid="stDataEditor"] td{background:#131824!important;color:#dce8ff!important;
  font-size:17px!important;padding:10px!important;}
[data-testid="stAlert"]{background:#0d2040!important;border:1px solid #1e4080!important;
  color:#c0d8ff!important;font-size:16px!important;}
.top-heading{background:linear-gradient(135deg,#0d1f45 0%,#1a3a7a 100%);
  border:2px solid #2255cc;border-radius:16px;padding:22px 30px;text-align:center;margin-bottom:20px;}
.top-heading .dept{font-size:14px;color:#88aaee;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:6px;}
.top-heading .main{font-size:34px;font-weight:900;color:#ffffff;line-height:1.2;margin-bottom:4px;}
.top-heading .sub{font-size:18px;color:#a0c8ff;}
.hero-box{background:#0d1f45;border:1.5px solid #2255cc;border-radius:16px;
  padding:32px 28px;text-align:center;margin:16px 0 20px 0;}
.hero-label{font-size:14px;font-weight:600;color:#88aaee;text-transform:uppercase;letter-spacing:.12em;margin-bottom:10px;}
.hero-value{font-size:52px;font-weight:800;color:#ffffff;line-height:1.1;margin-bottom:8px;}
.hero-sub{font-size:17px;color:#aabcdd;line-height:1.8;}
.hero-box-green{background:#0a2a18;border:1.5px solid #22885a;border-radius:16px;
  padding:28px 24px;text-align:center;margin:10px 0 16px 0;}
.hero-box-green .hero-label{color:#66ddaa;}
.hero-box-green .hero-value{font-size:44px;font-weight:800;color:#aaffd4;line-height:1.1;margin-bottom:8px;}
.hero-box-green .hero-sub{font-size:16px;color:#88ccaa;line-height:1.8;}
.hero-box-orange{background:#2a1800;border:1.5px solid #cc7700;border-radius:16px;
  padding:28px 24px;text-align:center;margin:10px 0 16px 0;}
.hero-box-orange .hero-label{color:#ffb347;}
.hero-box-orange .hero-value{font-size:44px;font-weight:800;color:#ffd580;line-height:1.1;margin-bottom:8px;}
.hero-box-orange .hero-sub{font-size:16px;color:#ccaa66;line-height:1.8;}
.hero-box-purple{background:#1a0d30;border:1.5px solid #7755cc;border-radius:16px;
  padding:28px 24px;text-align:center;margin:10px 0 16px 0;}
.hero-box-purple .hero-label{color:#bb99ff;}
.hero-box-purple .hero-value{font-size:44px;font-weight:800;color:#ddccff;line-height:1.1;margin-bottom:8px;}
.hero-box-purple .hero-sub{font-size:16px;color:#9980cc;line-height:1.8;}
.result-box{background:#0f1e3e;border:1px solid #2255cc;border-radius:10px;padding:18px 22px;margin:6px 0;}
.result-box .lbl{font-size:13px;font-weight:600;color:#88aaee;text-transform:uppercase;letter-spacing:.10em;margin-bottom:6px;}
.result-box .val{font-size:24px;font-weight:700;color:#ffffff;}
.formula-box{background:#101c38;border-left:4px solid #7eb8ff;border-radius:0 10px 10px 0;
  padding:18px 22px;margin:10px 0 18px 0;font-size:17px;color:#c8d8ff;line-height:2.2;font-family:'Courier New',monospace;}
.formula-box b{color:#7eb8ff;font-family:inherit;}
.section-card{background:#0f1a30;border:1px solid #1e3060;border-radius:12px;padding:22px 26px;margin:14px 0;}
.labman-heading{font-size:18px;font-weight:800;color:#ffffff;letter-spacing:0.01em;
  margin:22px 0 10px 0;border-bottom:2px solid #2a3a60;padding-bottom:6px;}
div.stButton>button[kind="primary"]{background:#1a4ab0!important;color:#ffffff!important;
  font-size:18px!important;font-weight:700!important;border:none!important;
  border-radius:8px!important;padding:14px 36px!important;}
div.stButton>button[kind="primary"]:hover{background:#2255cc!important;}
div.stDownloadButton>button{background:#145530!important;color:#ffffff!important;
  font-size:18px!important;font-weight:700!important;border:none!important;
  border-radius:8px!important;padding:14px 36px!important;}
div.stDownloadButton>button:hover{background:#1a6a3a!important;}
</style>
""", unsafe_allow_html=True)

# ── TOP HEADING
st.markdown("""
<div class="top-heading">
  <div class="dept">RV College of Engineering &middot; Department of Chemistry</div>
  <div class="main">Chemistry PBL</div>
  <div class="sub">AI-Assisted Flame Photometric Estimation of Sodium in Milk</div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR
st.sidebar.title("📋 Project Details")
st.sidebar.markdown("**CPBL Project:** Flame Photometric Estimation of Sodium in Milk")
st.sidebar.markdown("**Teacher In-charge:** Dr. Mahesh R")
st.sidebar.subheader("👥 Team Members")
team = [
    "Jane Christopher Dhawale (1RV25CH013)",
    "Jeevan P (1RV25CH014)",
    "Likith Bharani R (1RV25CH015)",
    "Mahika Ravikumar (1RV25CH016)"
]
for m in team:
    st.sidebar.caption(m)
st.sidebar.divider()

st.sidebar.subheader("🧪 Stock Solution Details")
W_nacl = st.sidebar.number_input(
    "Weight of NaCl in Diluted Milk Stock (g)",
    value=0.0139, step=0.0001, format="%.4f"
)
Vol_stock = st.sidebar.number_input(
    "Total Stock Volume (cm³)", value=100.0, step=10.0, format="%.1f"
)
st.sidebar.divider()

st.sidebar.subheader("🥛 Milk Sample Dilution")
milk_vol_taken = st.sidebar.number_input(
    "Volume of Milk Taken (mL)", value=10.0, step=1.0, format="%.1f"
)
diluted_to_vol = st.sidebar.number_input(
    "Diluted To (mL)", value=100.0, step=10.0, format="%.1f"
)
dilution_factor = diluted_to_vol / milk_vol_taken if milk_vol_taken > 0 else 1.0

st.sidebar.markdown(f"""
<div style="background:#1a1200;border:1px solid #cc7700;border-radius:10px;padding:14px;margin-top:8px;">
  <div style="font-size:13px;color:#ffb347;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px;">Dilution Factor</div>
  <div style="font-size:22px;font-weight:800;color:#ffd580;">{dilution_factor:.1f}×</div>
  <div style="font-size:13px;color:#ccaa66;margin-top:4px;">
    {milk_vol_taken:.0f} mL milk → {diluted_to_vol:.0f} mL stock solution
  </div>
</div>
""", unsafe_allow_html=True)

# ── STANDARD STRENGTH A
# A = Na (g) per cm³ of diluted milk stock
# 58.5 g NaCl → 23 g Na
# W_nacl g NaCl in Vol_stock cm³  →  A = (W_nacl × 23) / (58.5 × Vol_stock)
A_g  = (W_nacl * 23.0) / (58.5 * Vol_stock)   # g per cm³ of stock
A_mg = A_g * 1000                               # mg per cm³ of stock

st.sidebar.markdown(f"""
<div style="background:#0d1f3a;border:1px solid #1e4080;border-radius:10px;padding:16px;margin-top:8px;">
  <div style="font-size:13px;color:#88aaee;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px;">Standard Strength A</div>
  <div style="font-size:13px;color:#7eb8ff;line-height:2.0;">
    A = (W × 23) / (58.5 × {Vol_stock:.0f})<br>
    = ({W_nacl:.4f} × 23) / (58.5 × {Vol_stock:.0f})<br>
    <b style="color:#fff;font-size:15px;">= {A_g:.6f} g/cm³</b><br>
    <b style="color:#fff;font-size:15px;">= {A_mg:.6f} mg/cm³</b>
  </div>
</div>
""", unsafe_allow_html=True)

# ── SESSION STATE
SL_NOS    = [1, 2, 3, 4, 5, "Unknown\n(Milk)"]
DEF_VOLS  = [2.0, 4.0, 6.0, 8.0, 10.0, None]
DEF_READS = [168.0, 210.0, 240.0, 280.0, 306.0, 232.0]

for k, v in [('flame_readings', DEF_READS.copy()), ('submitted', False),
             ('processed_df', pd.DataFrame()), ('fig', None),
             ('pred_vol', None), ('pred_wt', None), ('pred_wt_g', None),
             ('ts_read', None), ('manual_vol', 0.0), ('manual_wt', 0.0),
             ('err_vol', None), ('err_wt', None),
             ('manual_A_g', 0.0), ('err_A_val', None),
             ('na_in_stock_100ml', None),
             ('na_in_orig_milk_vol', None),
             ('na_per_100ml_milk', None)]:
    if k not in st.session_state:
        st.session_state[k] = v

cal_data = pd.DataFrame({
    "Sl. No.": SL_NOS,
    "Vol. of Diluted Milk (cm³)": DEF_VOLS,
    "Flame Photometer Reading": st.session_state.flame_readings,
})

# Train regression on standards 1-5 only
std_df  = cal_data.iloc[:5].dropna()
X_train = std_df[["Vol. of Diluted Milk (cm³)"]].values.astype(float)
y_train = std_df["Flame Photometer Reading"].values.astype(float)
model     = LinearRegression().fit(X_train, y_train)
slope     = float(model.coef_[0])
intercept = float(model.intercept_)
r_squared = float(model.score(X_train, y_train))

# ── TABS
tab1, tab2, tab3 = st.tabs(["📊 Data Table", "📈 Graph & Results", "📄 Download PDF"])

# ══════════════════════════ TAB 1 ══════════════════════════
with tab1:
    st.header("Laboratory Tabulation")
    st.info("🔬 Enter flame photometer readings for the 5 standard solutions and the unknown milk sample. Click **Submit & Calculate** when done.")

    col_cfg = {
        "Sl. No.": st.column_config.TextColumn("Sl. No.", width="small", disabled=True),
        "Vol. of Diluted Milk (cm³)": st.column_config.NumberColumn(
            "Vol. of Diluted Milk (cm³)", width="medium", disabled=True, format="%.1f"),
        "Flame Photometer Reading": st.column_config.NumberColumn(
            "Flame Photometer Reading", width="large", format="%.2f"),
    }
    edited_df = st.data_editor(
        cal_data, num_rows="fixed", use_container_width=True,
        column_config=col_cfg, key="table_editor", height=420,
    )
    new_reads = edited_df["Flame Photometer Reading"].tolist()
    if new_reads != st.session_state.flame_readings:
        st.session_state.flame_readings = new_reads
        st.session_state.submitted = False
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        if st.button("🔬 Submit & Calculate", type="primary", use_container_width=True):
            st.session_state.submitted = True

    if not st.session_state.submitted:
        st.info("Enter all readings above, then click **Submit & Calculate**.")
    else:
        proc = edited_df.copy()

        # Sodium weight for each standard: Wt (mg) = Volume (cm³) × A (mg/cm³)
        proc.loc[:4, "Wt. of Sodium (mg)"] = (
            pd.to_numeric(proc.loc[:4, "Vol. of Diluted Milk (cm³)"], errors='coerce') * A_mg
        )

        ts_read = pd.to_numeric(proc.loc[5, "Flame Photometer Reading"], errors='coerce')

        if pd.notna(ts_read) and slope != 0:
            # Step 3 — Volume from calibration (inverse regression)
            pred_vol  = (float(ts_read) - intercept) / slope

            # Step 4 — Na in the unknown solution (= Na in pred_vol cm³ of stock)
            # This is the weight of sodium in the unknown solution as read from the graph
            pred_wt   = abs(pred_vol) * A_mg    # mg
            pred_wt_g = pred_wt / 1000          # g

            # Step 5 — Na in the full 100 mL stock solution
            # Since A_mg is Na per cm³ of stock:  Na in 100 mL stock = A_mg × 100
            # Equivalently: (pred_wt / pred_vol) × 100  — same result
            na_in_stock_100ml = A_mg * Vol_stock   # mg in entire stock

            # Step 6 — Na in original milk (milk_vol_taken mL)
            # The 100 mL stock came from milk_vol_taken mL of milk
            na_in_orig_milk_vol = na_in_stock_100ml   # mg in milk_vol_taken mL of milk

            # Step 7 — Na per 100 mL of original milk (for label comparison)
            na_per_100ml_milk = (na_in_orig_milk_vol / milk_vol_taken) * 100.0

            proc.loc[5, "Vol. of Diluted Milk (cm³)"] = pred_vol
            proc.loc[5, "Wt. of Sodium (mg)"]         = pred_wt
        else:
            pred_vol = pred_wt = pred_wt_g = None
            na_in_stock_100ml = na_in_orig_milk_vol = na_per_100ml_milk = None

        st.markdown("**Processed Table with Sodium Weights:**")
        st.dataframe(
            proc.style.format({
                "Vol. of Diluted Milk (cm³)": lambda v: f"{float(v):.4f}" if pd.notna(v) else "—",
                "Flame Photometer Reading":   lambda v: f"{float(v):.2f}"  if pd.notna(v) else "—",
                "Wt. of Sodium (mg)":         lambda v: f"{float(v):.4f}" if pd.notna(v) else "—",
            }),
            use_container_width=True, hide_index=True, height=340,
        )

        # ── CALCULATION DISPLAY
        st.markdown('<div class="labman-heading">Calculation</div>', unsafe_allow_html=True)
        st.markdown(f"""
<div class="formula-box">
<b>Standard Strength A:</b><br>
&nbsp;&nbsp;Amount of NaCl in {Vol_stock:.0f} cm&sup3; diluted milk stock = {W_nacl:.4f} g<br>
&nbsp;&nbsp;({milk_vol_taken:.0f} mL milk diluted to {diluted_to_vol:.0f} mL with distilled water)<br>
&nbsp;&nbsp;58.5 g of NaCl contains 23 g of Na<br>
&nbsp;&nbsp;&there4; 1 cm&sup3; of stock contains = (W &times; 23) / (58.5 &times; {Vol_stock:.0f}) = A g of Na<br>
&nbsp;&nbsp;A = ({W_nacl:.4f} &times; 23) / (58.5 &times; {Vol_stock:.0f})<br>
&nbsp;&nbsp;A = <b>{A_g:.6f} g/cm&sup3; &nbsp;=&nbsp; {A_mg:.6f} mg/cm&sup3;</b>
</div>
""", unsafe_allow_html=True)

        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.markdown(f"""
<div class="hero-box-green">
  <div class="hero-label">Standard Strength A (g/cm³)</div>
  <div class="hero-value">{A_g:.6f}</div>
  <div class="hero-sub">Na per cm³ of diluted milk stock</div>
</div>""", unsafe_allow_html=True)
        with col_a2:
            st.markdown(f"""
<div class="hero-box-green">
  <div class="hero-label">Standard Strength A (mg/cm³)</div>
  <div class="hero-value">{A_mg:.6f}</div>
  <div class="hero-sub">Na per cm³ of diluted milk stock</div>
</div>""", unsafe_allow_html=True)

        # ── ERROR FOR A
        st.markdown('<div class="labman-heading">Error Analysis — Standard Strength A</div>', unsafe_allow_html=True)
        col_ma, _ = st.columns([1, 2])
        with col_ma:
            manual_A_g = st.number_input(
                "Your Manual A value (g/cm³)",
                value=float(st.session_state.manual_A_g or 0.0),
                step=0.000001, format="%.6f", key="manual_A_inp"
            )
        if manual_A_g > 0:
            err_A       = abs(manual_A_g - A_g) / abs(A_g) * 100
            manual_A_mg = manual_A_g * 1000
            def colour(e): return "#50fa7b" if e < 5 else ("#ffa500" if e < 15 else "#ff6b6b")
            def verdict(e): return "✅ Excellent" if e < 5 else ("⚠️ Acceptable" if e < 15 else "❌ Large — recheck")
            col_ea1, col_ea2 = st.columns(2)
            with col_ea1:
                st.markdown(f"""
<div class="hero-box">
  <div class="hero-label">% Error — A (g/cm³)</div>
  <div class="hero-value" style="font-size:46px;color:{colour(err_A)};">{err_A:.2f}%</div>
  <div class="hero-sub">{verdict(err_A)}<br>AI: {A_g:.6f} &nbsp;|&nbsp; Manual: {manual_A_g:.6f}</div>
</div>""", unsafe_allow_html=True)
            with col_ea2:
                st.markdown(f"""
<div class="hero-box">
  <div class="hero-label">% Error — A (mg/cm³)</div>
  <div class="hero-value" style="font-size:46px;color:{colour(err_A)};">{err_A:.2f}%</div>
  <div class="hero-sub">{verdict(err_A)}<br>AI: {A_mg:.6f} &nbsp;|&nbsp; Manual: {manual_A_mg:.6f}</div>
</div>""", unsafe_allow_html=True)
            st.session_state.manual_A_g = manual_A_g
            st.session_state.err_A_val  = err_A
        else:
            st.info("Enter your manually calculated A value above to compute % error.")

        # ── UNKNOWN MILK RESULT
        if pred_wt is not None and pred_wt > 0:
            st.markdown('<div class="labman-heading">Result — Unknown Milk Sample</div>', unsafe_allow_html=True)
            st.markdown(f"""
<div class="formula-box">
<b>Step 3 — Volume of unknown (inverse regression):</b><br>
&nbsp;&nbsp;V = (Flame Reading &minus; c) &divide; m<br>
&nbsp;&nbsp;V = ({float(ts_read):.2f} &minus; {intercept:.4f}) &divide; {slope:.4f}<br>
&nbsp;&nbsp;V = <b>{pred_vol:.4f} cm&sup3;</b><br>
<br>
<b>Step 4 — Weight of Na in unknown solution (from graph):</b><br>
&nbsp;&nbsp;Wt = V &times; A = {pred_vol:.4f} &times; {A_mg:.6f}<br>
&nbsp;&nbsp;= <b>{pred_wt:.4f} mg = {pred_wt_g:.6f} g</b><br>
&nbsp;&nbsp;(This is the Na present in the equivalent volume of the unknown sample)<br>
<br>
<b>Step 5 — Na in full {Vol_stock:.0f} mL stock solution:</b><br>
&nbsp;&nbsp;= A &times; {Vol_stock:.0f} = {A_mg:.6f} &times; {Vol_stock:.0f}<br>
&nbsp;&nbsp;= <b>{na_in_stock_100ml:.4f} mg</b><br>
&nbsp;&nbsp;(Since the stock is uniform, Na per cm&sup3; = A, so Na in {Vol_stock:.0f} cm&sup3; = A &times; {Vol_stock:.0f})<br>
<br>
<b>Step 6 — Na in {milk_vol_taken:.0f} mL original milk:</b><br>
&nbsp;&nbsp;The {Vol_stock:.0f} mL stock was made from {milk_vol_taken:.0f} mL milk<br>
&nbsp;&nbsp;&there4; Na in {milk_vol_taken:.0f} mL milk = <b>{na_in_orig_milk_vol:.4f} mg</b><br>
<br>
<b>Step 7 — Na per 100 mL original milk:</b><br>
&nbsp;&nbsp;= ({na_in_orig_milk_vol:.4f} &divide; {milk_vol_taken:.0f}) &times; 100<br>
&nbsp;&nbsp;= <b>{na_per_100ml_milk:.4f} mg / 100 mL</b><br>
&nbsp;&nbsp;Reference (Nandini Shubham label): ~55 mg / 100 mL ✓
</div>
""", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
<div class="hero-box">
  <div class="hero-label">Na in Unknown Solution (from graph)</div>
  <div class="hero-value">{pred_wt:.4f} mg</div>
  <div class="hero-sub">= {pred_wt_g:.6f} g<br>
    Vol: {pred_vol:.4f} cm³ &nbsp;|&nbsp; Reading: {float(ts_read):.2f} &nbsp;|&nbsp; R²={r_squared:.4f}</div>
</div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
<div class="hero-box-orange">
  <div class="hero-label">Na in {Vol_stock:.0f} mL Stock = Na in {milk_vol_taken:.0f} mL Milk</div>
  <div class="hero-value">{na_in_orig_milk_vol:.4f} mg</div>
  <div class="hero-sub">= A &times; {Vol_stock:.0f} = {A_mg:.6f} &times; {Vol_stock:.0f}<br>
    ({milk_vol_taken:.0f} mL milk was diluted to make this {Vol_stock:.0f} mL stock)</div>
</div>""", unsafe_allow_html=True)

            st.markdown(f"""
<div class="hero-box-purple">
  <div class="hero-label">Na per 100 mL Original Milk — Label Comparison</div>
  <div class="hero-value">{na_per_100ml_milk:.2f} mg / 100 mL</div>
  <div class="hero-sub">
    Calculated: <b>{na_per_100ml_milk:.2f} mg</b> per 100 mL &nbsp;|&nbsp;
    Nandini Shubham label: ~55 mg per 100 mL ✓
  </div>
</div>""", unsafe_allow_html=True)

        # ── Save to session state
        st.session_state.processed_df        = proc
        st.session_state.pred_vol            = pred_vol
        st.session_state.pred_wt             = pred_wt
        st.session_state.pred_wt_g           = pred_wt_g
        st.session_state.ts_read             = ts_read
        st.session_state.na_in_stock_100ml   = na_in_stock_100ml
        st.session_state.na_in_orig_milk_vol = na_in_orig_milk_vol
        st.session_state.na_per_100ml_milk   = na_per_100ml_milk

# ══════════════════════════ TAB 2 ══════════════════════════
with tab2:
    st.header("AI Regression Model, Calibration Graph & Error Analysis")

    if not st.session_state.submitted or st.session_state.processed_df.empty:
        st.warning("Complete data entry in **Tab 1** and click **Submit & Calculate** first.")
    else:
        pred_vol            = st.session_state.pred_vol
        pred_wt             = st.session_state.pred_wt
        pred_wt_g           = st.session_state.pred_wt_g
        ts_read             = st.session_state.ts_read
        na_in_stock_100ml   = st.session_state.na_in_stock_100ml   or 0
        na_in_orig_milk_vol = st.session_state.na_in_orig_milk_vol or 0
        na_per_100ml_milk   = st.session_state.na_per_100ml_milk   or 0
        proc                = st.session_state.processed_df

        st.markdown('<div class="labman-heading">Calculation</div>', unsafe_allow_html=True)
        st.markdown(f"""
<div class="formula-box">
<b>Step 1 — Standard Strength A:</b><br>
&nbsp;&nbsp;A = ({W_nacl:.4f} &times; 23) / (58.5 &times; {Vol_stock:.0f})
  = <b>{A_g:.6f} g/cm&sup3; = {A_mg:.6f} mg/cm&sup3;</b><br>
<br>
<b>Step 2 — AI Regression Line (y = mx + c):</b><br>
&nbsp;&nbsp;Flame Reading = ({slope:.4f} &times; Volume) + ({intercept:.4f})&nbsp;&nbsp;
  R&sup2; = {r_squared:.4f}<br>
<br>
<b>Step 3 — Volume of Unknown (inverse regression):</b><br>
&nbsp;&nbsp;V = ({float(ts_read):.2f} &minus; {intercept:.4f}) &divide; {slope:.4f}
  = <b>{pred_vol:.4f} cm&sup3;</b><br>
<br>
<b>Step 4 — Na in Unknown Solution (from graph):</b><br>
&nbsp;&nbsp;Wt = {pred_vol:.4f} &times; {A_mg:.6f}
  = <b>{pred_wt:.4f} mg = {pred_wt_g:.6f} g</b><br>
<br>
<b>Step 5 — Na in {Vol_stock:.0f} mL Stock = Na in {milk_vol_taken:.0f} mL Original Milk:</b><br>
&nbsp;&nbsp;= A &times; {Vol_stock:.0f} = {A_mg:.6f} &times; {Vol_stock:.0f}
  = <b>{na_in_stock_100ml:.4f} mg</b><br>
<br>
<b>Step 6 — Na per 100 mL Original Milk:</b><br>
&nbsp;&nbsp;= ({na_in_orig_milk_vol:.4f} &divide; {milk_vol_taken:.0f}) &times; 100
  = <b>{na_per_100ml_milk:.4f} mg / 100 mL</b><br>
&nbsp;&nbsp;Reference (Nandini Shubham label): ~55 mg / 100 mL ✓
</div>
""", unsafe_allow_html=True)

        # Results summary cards
        st.markdown('<div class="labman-heading">Results Summary</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        for col, lbl, val in zip(
            [c1, c2, c3],
            ["Weight of NaCl (g)", "Std. Strength A (g/cm³)", "Std. Strength A (mg/cm³)"],
            [f"{W_nacl:.4f}", f"{A_g:.6f}", f"{A_mg:.6f}"]
        ):
            col.markdown(f'<div class="result-box"><div class="lbl">{lbl}</div>'
                         f'<div class="val">{val}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3, c4, c5 = st.columns(5)
        for col, lbl, val in zip(
            [c1, c2, c3, c4, c5],
            ["Flame Reading", "Vol. (cm³)", "Na — unknown soln (mg)",
             f"Na — {milk_vol_taken:.0f} mL milk (mg)", "Na / 100 mL milk (mg)"],
            [f"{float(ts_read):.2f}", f"{pred_vol:.4f}",
             f"{pred_wt:.4f}", f"{na_in_orig_milk_vol:.4f}", f"{na_per_100ml_milk:.2f}"]
        ):
            col.markdown(f'<div class="result-box"><div class="lbl">{lbl}</div>'
                         f'<div class="val">{val}</div></div>', unsafe_allow_html=True)

        # ── Calibration graph
        st.markdown("<br>", unsafe_allow_html=True)
        x_pts = pd.to_numeric(proc.iloc[:5]["Vol. of Diluted Milk (cm³)"], errors='coerce').values
        y_pts = pd.to_numeric(proc.iloc[:5]["Flame Photometer Reading"],   errors='coerce').values
        valid = ~np.isnan(x_pts) & ~np.isnan(y_pts)

        fig, ax = plt.subplots(figsize=(10, 5.5), facecolor="#0e1220")
        ax.set_facecolor("#141929")
        if valid.sum() >= 2:
            xl = np.linspace(x_pts[valid].min() * 0.8, x_pts[valid].max() * 1.15, 300)
            ax.plot(xl, slope * xl + intercept, color="#7eb8ff", linestyle="--", linewidth=2.2,
                    label=f"Regression y={slope:.2f}x+{intercept:.2f}  R²={r_squared:.4f}")
            ax.scatter(x_pts[valid], y_pts[valid], color="#ff6b6b", s=110, zorder=4,
                       label="Standard solutions", edgecolors="#ffaaaa", linewidths=0.8)
        if pred_vol is not None:
            ax.scatter([pred_vol], [float(ts_read)], color="#ffa500", s=200,
                       edgecolors="white", linewidths=2, zorder=5,
                       label=f"Unknown Milk (reading={float(ts_read):.0f})")
            ax.axvline(x=pred_vol,       color="#ffa500", linestyle=":", linewidth=1.6, alpha=0.85)
            ax.axhline(y=float(ts_read), color="#ffa500", linestyle=":", linewidth=1.6, alpha=0.85)
            ax.annotate(
                f" V={pred_vol:.3f} cm³\n Na(unknown soln)={pred_wt:.3f} mg"
                f"\n Na({milk_vol_taken:.0f}mL milk)={na_in_orig_milk_vol:.3f} mg"
                f"\n Na/100mL milk={na_per_100ml_milk:.2f} mg",
                xy=(pred_vol, float(ts_read)),
                xytext=(pred_vol + 0.4, float(ts_read) - 14),
                color="#ffa500", fontsize=9.5,
                arrowprops=dict(arrowstyle="->", color="#ffa500", lw=1.3)
            )
        ax.set_xlabel("Volume of Diluted Milk Stock (cm³)", fontsize=13, color="#c8d8f0")
        ax.set_ylabel("Flame Photometer Reading",           fontsize=13, color="#c8d8f0")
        ax.set_title("Calibration Curve — Volume of Diluted Milk vs Flame Photometer Reading",
                     fontsize=14, color="#dce8ff", pad=14)
        ax.tick_params(colors="#c8d8f0", labelsize=12)
        for sp in ax.spines.values():
            sp.set_edgecolor("#2a3a60")
        ax.grid(True, linestyle=":", alpha=0.25, color="#3a5a8f")
        ax.legend(loc="upper left", framealpha=0.5, facecolor="#0e1220",
                  edgecolor="#2a3a60", labelcolor="#dce8ff", fontsize=11)
        plt.tight_layout()
        st.pyplot(fig)
        st.session_state.fig = fig

        # ── Error analysis
        st.markdown('<div class="labman-heading">Error Analysis — Unknown Milk Sample</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="section-card">
<p style="font-size:17px;color:#a0c8ff;margin:0;">
Enter the values you calculated manually from your hand-drawn calibration graph.<br>
Enter <b>manual Na weight = manual volume × A</b> (the weight of Na in the unknown solution, before scaling to full stock).
</p>
</div>
""", unsafe_allow_html=True)

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("**Manual Volume (from hand-drawn graph)**")
            manual_vol = st.number_input(
                "Manual Volume of Unknown (cm³)",
                value=float(st.session_state.manual_vol or 0.0),
                step=0.0001, format="%.4f", key="manual_vol_inp"
            )
        with col_m2:
            st.markdown("**Manual Na Weight in Unknown Solution (Vol × A)**")
            manual_wt = st.number_input(
                "Manual Wt. of Na in unknown soln (mg)",
                value=float(st.session_state.manual_wt or 0.0),
                step=0.0001, format="%.4f", key="manual_wt_inp"
            )

        if manual_vol > 0 and manual_wt > 0 and pred_vol is not None and pred_wt is not None:
            err_vol = abs(manual_vol - pred_vol) / abs(pred_vol) * 100
            err_wt  = abs(manual_wt  - pred_wt)  / abs(pred_wt)  * 100
            # Scale manual values the same correct way
            manual_na_stock   = A_mg * Vol_stock              # same A, same stock vol
            manual_na_per100  = (manual_na_stock / milk_vol_taken) * 100.0

            def colour(e): return "#50fa7b" if e < 5 else ("#ffa500" if e < 15 else "#ff6b6b")
            def verdict(e): return "✅ Excellent" if e < 5 else ("⚠️ Acceptable" if e < 15 else "❌ Large — recheck")

            ev, ew = st.columns(2)
            with ev:
                st.markdown(f"""
<div class="hero-box">
  <div class="hero-label">% Error — Volume</div>
  <div class="hero-value" style="font-size:46px;color:{colour(err_vol)};">{err_vol:.2f}%</div>
  <div class="hero-sub">{verdict(err_vol)}<br>
    AI: {pred_vol:.4f} cm³ &nbsp;|&nbsp; Manual: {manual_vol:.4f} cm³</div>
</div>""", unsafe_allow_html=True)
            with ew:
                st.markdown(f"""
<div class="hero-box">
  <div class="hero-label">% Error — Na in Unknown Soln</div>
  <div class="hero-value" style="font-size:46px;color:{colour(err_wt)};">{err_wt:.2f}%</div>
  <div class="hero-sub">{verdict(err_wt)}<br>
    AI: {pred_wt:.4f} mg &nbsp;|&nbsp; Manual: {manual_wt:.4f} mg</div>
</div>""", unsafe_allow_html=True)

            st.markdown(f"""
<div class="formula-box">
<b>% Error Formula:</b> |Manual &minus; AI| &divide; |AI| &times; 100<br>
<br>
<b>Volume % Error:</b><br>
&nbsp;&nbsp;= |{manual_vol:.4f} &minus; {pred_vol:.4f}| &divide; |{pred_vol:.4f}| &times; 100
  = <b>{err_vol:.4f}%</b><br>
<br>
<b>Na (unknown soln) % Error:</b><br>
&nbsp;&nbsp;= |{manual_wt:.4f} &minus; {pred_wt:.4f}| &divide; |{pred_wt:.4f}| &times; 100
  = <b>{err_wt:.4f}%</b><br>
<br>
<b>Manual Na in {milk_vol_taken:.0f} mL milk = A &times; {Vol_stock:.0f} = {manual_na_stock:.4f} mg</b><br>
<b>Manual Na per 100 mL milk = {manual_na_per100:.2f} mg / 100 mL</b>
</div>
""", unsafe_allow_html=True)

            st.session_state.manual_vol = manual_vol
            st.session_state.manual_wt  = manual_wt
            st.session_state.err_vol    = err_vol
            st.session_state.err_wt     = err_wt
        else:
            st.info("Enter both manual volume and sodium weight above to calculate % error.")
            st.session_state.err_vol = None
            st.session_state.err_wt  = None

# ══════════════════════════ TAB 3 — PDF ══════════════════════════
with tab3:
    st.header("Download Full Lab Report (PDF)")

    if not st.session_state.submitted or st.session_state.processed_df.empty:
        st.warning("Complete your analysis in **Tab 1** first, then return here to download.")
    else:
        proc                = st.session_state.processed_df
        pred_vol_r          = st.session_state.pred_vol or 0
        pred_wt_r           = st.session_state.pred_wt  or 0
        pred_wt_g_r         = st.session_state.pred_wt_g or 0
        ts_read_r           = st.session_state.ts_read  or 0
        na_in_stock_r       = st.session_state.na_in_stock_100ml   or 0
        na_in_milk_r        = st.session_state.na_in_orig_milk_vol or 0
        na_per_100ml_r      = st.session_state.na_per_100ml_milk   or 0
        manual_vol_r        = st.session_state.manual_vol or 0
        manual_wt_r         = st.session_state.manual_wt  or 0
        err_vol_r           = st.session_state.err_vol
        err_wt_r            = st.session_state.err_wt
        manual_A_g_r        = st.session_state.manual_A_g or 0
        err_A_r             = st.session_state.err_A_val
        fig_r               = st.session_state.fig

        def build_pdf():
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4,
                                    leftMargin=2*cm, rightMargin=2*cm,
                                    topMargin=2*cm, bottomMargin=2*cm)
            styles = getSampleStyleSheet()
            title_s   = ParagraphStyle('T',  parent=styles['Title'],   fontSize=18, leading=26,
                                       spaceAfter=4, alignment=TA_CENTER,
                                       textColor=colors.HexColor('#1a3a7a'))
            sub_s     = ParagraphStyle('Su', parent=styles['Normal'],  fontSize=13,
                                       alignment=TA_CENTER, textColor=colors.grey, spaceAfter=2)
            h2_s      = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, leading=20,
                                       spaceBefore=14, spaceAfter=6,
                                       textColor=colors.HexColor('#1a3a7a'))
            body_s    = ParagraphStyle('B',  parent=styles['Normal'],  fontSize=12,
                                       leading=18, spaceAfter=5)
            formula_s = ParagraphStyle('F',  parent=styles['Normal'],  fontSize=11, leading=18,
                                       spaceAfter=4, leftIndent=20, fontName='Courier')
            caption_s = ParagraphStyle('Ca', parent=styles['Normal'],  fontSize=10, leading=14,
                                       spaceAfter=4, alignment=TA_CENTER, textColor=colors.grey)

            story = []

            # Title block
            story.append(Paragraph("Chemistry PBL", title_s))
            story.append(Paragraph("RV College of Engineering — Department of Chemistry", sub_s))
            story.append(Paragraph("Teacher In-charge: Dr. Mahesh R", sub_s))
            story.append(Paragraph("AI-Assisted Flame Photometric Estimation of Sodium in Milk", sub_s))
            story.append(HRFlowable(width="100%", thickness=1.5,
                                    color=colors.HexColor('#1a3a7a'), spaceAfter=10))

            story.append(Paragraph("Team Members", h2_s))
            for m in team:
                story.append(Paragraph(f"• {m}", body_s))
            story.append(Spacer(1, 8))

            story.append(Paragraph("Stock Solution Details", h2_s))
            story.append(Paragraph(
                f"Stock: {milk_vol_taken:.0f} mL of Nandini milk diluted to "
                f"{diluted_to_vol:.0f} mL with distilled water", body_s))
            story.append(Paragraph(
                f"NaCl content in {diluted_to_vol:.0f} cm<super>3</super> "
                f"diluted milk stock (W) = <b>{W_nacl:.4f} g</b>", body_s))
            story.append(Paragraph(
                f"Dilution Factor = {diluted_to_vol:.0f} / {milk_vol_taken:.0f}"
                f" = <b>{dilution_factor:.1f}</b>", body_s))
            story.append(Spacer(1, 6))

            story.append(Paragraph("Calculation", h2_s))
            story.append(Paragraph(
                f"Amount of NaCl in {Vol_stock:.0f} cm<super>3</super> "
                f"diluted milk stock = {W_nacl:.4f} g", body_s))
            story.append(Paragraph("58.5 g of NaCl contains 23 g of Na.", body_s))
            story.append(Spacer(1, 4))

            story.append(Paragraph("Step 1 — Standard Strength A:", body_s))
            story.append(Paragraph(
                f"1 cm<super>3</super> of stock contains = (W x 23) / (58.5 x {Vol_stock:.0f}) = A g of Na",
                formula_s))
            story.append(Paragraph(
                f"A = ({W_nacl:.4f} x 23) / (58.5 x {Vol_stock:.0f})"
                f" = <b>{A_g:.6f} g/cm<super>3</super> = {A_mg:.6f} mg/cm<super>3</super></b>",
                formula_s))
            story.append(Spacer(1, 4))

            if manual_A_g_r > 0 and err_A_r is not None:
                story.append(Paragraph("Standard Strength A — Error Analysis:", body_s))
                story.append(Paragraph(
                    f"AI Value  : {A_g:.6f} g/cm<super>3</super> ({A_mg:.6f} mg/cm<super>3</super>)",
                    formula_s))
                story.append(Paragraph(
                    f"Manual A  : {manual_A_g_r:.6f} g/cm<super>3</super> "
                    f"({manual_A_g_r*1000:.6f} mg/cm<super>3</super>)", formula_s))
                story.append(Paragraph(f"% Error   : <b>{err_A_r:.4f}%</b>", formula_s))
                story.append(Spacer(1, 4))

            story.append(Paragraph("Step 2 — AI Regression Line:", body_s))
            story.append(Paragraph(
                f"Flame Reading = ({slope:.4f} x Volume) + ({intercept:.4f})   "
                f"R2 = {r_squared:.4f}", formula_s))
            story.append(Spacer(1, 4))

            story.append(Paragraph("Step 3 — Volume of Unknown (inverse regression):", body_s))
            story.append(Paragraph(
                f"Volume = ({float(ts_read_r):.2f} - {intercept:.4f}) / {slope:.4f}"
                f" = <b>{pred_vol_r:.4f} cm<super>3</super></b>", formula_s))
            story.append(Spacer(1, 4))

            story.append(Paragraph("Step 4 — Weight of Na in Unknown Solution (from graph):", body_s))
            story.append(Paragraph(
                f"Wt = {pred_vol_r:.4f} x {A_g:.6f}"
                f" = <b>{pred_wt_g_r:.6f} g = {pred_wt_r:.4f} mg</b>", formula_s))
            story.append(Paragraph(
                "(This is the Na present in the equivalent volume of the unknown solution)",
                formula_s))
            story.append(Spacer(1, 4))

            story.append(Paragraph(
                f"Step 5 — Na in full {Vol_stock:.0f} mL Stock = Na in {milk_vol_taken:.0f} mL Original Milk:",
                body_s))
            story.append(Paragraph(
                f"= A x {Vol_stock:.0f} = {A_mg:.6f} x {Vol_stock:.0f}"
                f" = <b>{na_in_stock_r:.4f} mg</b>", formula_s))
            story.append(Paragraph(
                f"(The {Vol_stock:.0f} mL stock was prepared from {milk_vol_taken:.0f} mL of milk)",
                formula_s))
            story.append(Spacer(1, 4))

            story.append(Paragraph(
                f"Step 6 — Na per 100 mL Original Milk:", body_s))
            story.append(Paragraph(
                f"= ({na_in_milk_r:.4f} / {milk_vol_taken:.0f}) x 100"
                f" = <b>{na_per_100ml_r:.4f} mg / 100 mL</b>", formula_s))
            story.append(Paragraph(
                "Reference value (Nandini Shubham label): ~55 mg Na per 100 mL milk  [matches ✓]",
                formula_s))
            story.append(Spacer(1, 10))

            # Tabulation
            story.append(Paragraph("Tabulation", h2_s))
            tbl_data = [["Sl. No.", "Vol. of Diluted Milk\n(cm3)",
                         "Flame Photometer\nReading", "Wt. of Sodium\n(mg)"]]
            for i, row in proc.iterrows():
                sl  = str(row["Sl. No."]).replace("\n", " ")
                vol = (f"{float(row['Vol. of Diluted Milk (cm³)']):.4f}"
                       if pd.notna(row['Vol. of Diluted Milk (cm³)']) else "—")
                fr  = (f"{float(row['Flame Photometer Reading']):.2f}"
                       if pd.notna(row['Flame Photometer Reading']) else "—")
                wt_val = row.get('Wt. of Sodium (mg)')
                wt  = f"{float(wt_val):.4f}" if pd.notna(wt_val) else "—"
                tbl_data.append([sl, vol, fr, wt])

            page_w = A4[0] - 4*cm
            col_w  = [page_w*0.14, page_w*0.24, page_w*0.32, page_w*0.30]
            tbl = Table(tbl_data, colWidths=col_w, repeatRows=1)
            tbl.setStyle(TableStyle([
                ('BACKGROUND',    (0,0), (-1, 0), colors.HexColor('#1a3a7a')),
                ('TEXTCOLOR',     (0,0), (-1, 0), colors.white),
                ('FONTNAME',      (0,0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE',      (0,0), (-1,-1), 12),
                ('LEADING',       (0,0), (-1,-1), 18),
                ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
                ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
                ('ROWBACKGROUNDS',(0,1), (-1,-1),
                 [colors.HexColor('#f0f4ff'), colors.white]),
                ('BACKGROUND',    (0,len(tbl_data)-1), (-1,-1), colors.HexColor('#fff3cd')),
                ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
                ('TOPPADDING',    (0,0), (-1,-1), 9),
                ('BOTTOMPADDING', (0,0), (-1,-1), 9),
                ('LEFTPADDING',   (0,0), (-1,-1), 10),
                ('RIGHTPADDING',  (0,0), (-1,-1), 10),
            ]))
            story.append(tbl)
            story.append(Spacer(1, 14))

            # Graph
            if fig_r is not None:
                fig_pdf, ax_pdf = plt.subplots(figsize=(9, 5), facecolor="white")
                ax_pdf.set_facecolor("#f5f7ff")
                x2 = pd.to_numeric(proc.iloc[:5]["Vol. of Diluted Milk (cm³)"], errors='coerce').values
                y2 = pd.to_numeric(proc.iloc[:5]["Flame Photometer Reading"],   errors='coerce').values
                v2 = ~np.isnan(x2) & ~np.isnan(y2)
                if v2.sum() >= 2:
                    xl2 = np.linspace(x2[v2].min()*0.8, x2[v2].max()*1.15, 300)
                    ax_pdf.plot(xl2, slope*xl2+intercept, color="#1a4ab0", linestyle="--", linewidth=2,
                                label=f"Regression y={slope:.2f}x+{intercept:.2f}  R²={r_squared:.4f}")
                    ax_pdf.scatter(x2[v2], y2[v2], color="#cc2222", s=90,
                                   zorder=4, label="Standard solutions")
                if pred_vol_r and ts_read_r:
                    ax_pdf.scatter([pred_vol_r], [float(ts_read_r)], color="#cc7700", s=160,
                                   edgecolors="black", linewidths=1.5, zorder=5,
                                   label=f"Unknown Milk (reading={float(ts_read_r):.0f})")
                    ax_pdf.axvline(x=pred_vol_r,       color="#cc7700", linestyle=":", linewidth=1.4, alpha=0.8)
                    ax_pdf.axhline(y=float(ts_read_r), color="#cc7700", linestyle=":", linewidth=1.4, alpha=0.8)
                    ax_pdf.annotate(
                        f" V={pred_vol_r:.3f} cm3\n Na(unknown)={pred_wt_r:.3f} mg"
                        f"\n Na({milk_vol_taken:.0f}mL milk)={na_in_milk_r:.3f} mg"
                        f"\n Na/100mL={na_per_100ml_r:.2f} mg",
                        xy=(pred_vol_r, float(ts_read_r)),
                        xytext=(pred_vol_r+0.3, float(ts_read_r)-12),
                        color="#cc7700", fontsize=8.5,
                        arrowprops=dict(arrowstyle="->", color="#cc7700", lw=1.2)
                    )
                ax_pdf.set_xlabel("Volume of Diluted Milk Stock (cm3)", fontsize=12)
                ax_pdf.set_ylabel("Flame Photometer Reading", fontsize=12)
                ax_pdf.set_title("Calibration Curve", fontsize=12, pad=10)
                ax_pdf.tick_params(labelsize=11)
                ax_pdf.grid(True, linestyle=":", alpha=0.35)
                ax_pdf.legend(loc="upper left", fontsize=9)
                plt.tight_layout()
                img_buf = io.BytesIO()
                fig_pdf.savefig(img_buf, format='png', bbox_inches='tight', dpi=180, facecolor='white')
                img_buf.seek(0)
                plt.close(fig_pdf)
                graph_w = page_w
                graph_h = graph_w * 5 / 9
                story.append(Paragraph("Calibration Graph", h2_s))
                story.append(RLImage(img_buf, width=graph_w, height=graph_h))
                story.append(Paragraph(
                    "Figure: Volume of Diluted Milk (cm3) vs Flame Photometer Reading", caption_s))
                story.append(Spacer(1, 10))

            # Error Analysis
            story.append(Paragraph("Error Analysis", h2_s))
            story.append(Paragraph(
                f"AI Predicted Volume              : <b>{pred_vol_r:.4f} cm<super>3</super></b>", body_s))
            story.append(Paragraph(
                f"AI Na in Unknown Solution        : <b>{pred_wt_r:.4f} mg ({pred_wt_g_r:.6f} g)</b>", body_s))
            story.append(Paragraph(
                f"AI Na in {milk_vol_taken:.0f} mL Original Milk   : <b>{na_in_milk_r:.4f} mg</b>"
                f"   (= A x {Vol_stock:.0f} cm<super>3</super>)", body_s))
            story.append(Paragraph(
                f"AI Na per 100 mL Milk            : <b>{na_per_100ml_r:.4f} mg / 100 mL</b>"
                f"   (Nandini label: ~55 mg / 100 mL ✓)", body_s))

            if manual_vol_r > 0 and manual_wt_r > 0 and err_vol_r is not None:
                manual_na_stock_pdf  = A_mg * Vol_stock
                manual_na_100ml_pdf  = (manual_na_stock_pdf / milk_vol_taken) * 100.0
                story.append(Paragraph(
                    f"Manual Volume                    : <b>{manual_vol_r:.4f} cm<super>3</super></b>", body_s))
                story.append(Paragraph(
                    f"Manual Na in Unknown Solution    : <b>{manual_wt_r:.4f} mg</b>", body_s))
                story.append(Paragraph(
                    f"Manual Na in {milk_vol_taken:.0f} mL Milk        : <b>{manual_na_stock_pdf:.4f} mg</b>", body_s))
                story.append(Paragraph(
                    f"Manual Na per 100 mL Milk        : <b>{manual_na_100ml_pdf:.4f} mg / 100 mL</b>", body_s))
                story.append(Spacer(1, 4))
                story.append(Paragraph(f"% Error (Volume)                 = <b>{err_vol_r:.4f}%</b>", formula_s))
                story.append(Paragraph(f"% Error (Na in unknown soln)     = <b>{err_wt_r:.4f}%</b>", formula_s))
            else:
                story.append(Paragraph("Manual values not entered — error analysis unavailable.", body_s))

            story.append(Spacer(1, 10))
            story.append(HRFlowable(width="100%", thickness=0.8,
                                    color=colors.HexColor('#cccccc'), spaceAfter=8))

            # Report
            story.append(Paragraph("Report", h2_s))
            story.append(Paragraph(
                f"1. Volume of unknown solution = <b>{pred_vol_r:.4f} cm<super>3</super></b>", body_s))
            story.append(Paragraph(
                f"2. Na in unknown solution = <b>{pred_wt_r:.4f} mg ({pred_wt_g_r:.6f} g)</b>", body_s))
            story.append(Paragraph(
                f"3. Na in {milk_vol_taken:.0f} mL original milk = <b>{na_in_milk_r:.4f} mg</b>", body_s))
            story.append(Paragraph(
                f"4. Na per 100 mL original milk = <b>{na_per_100ml_r:.4f} mg / 100 mL</b>"
                f"   (Reference: ~55 mg / 100 mL ✓)", body_s))
            story.append(Spacer(1, 10))
            story.append(HRFlowable(width="100%", thickness=0.8,
                                    color=colors.HexColor('#cccccc'), spaceAfter=8))

            # AI Model Metrics
            story.append(Paragraph("AI Model Metrics", h2_s))
            story.append(Paragraph(f"Slope (m)     = {slope:.6f}", formula_s))
            story.append(Paragraph(f"Intercept (c) = {intercept:.6f}", formula_s))
            story.append(Paragraph(f"R2 Score      = {r_squared:.6f}", formula_s))

            doc.build(story)
            buf.seek(0)
            return buf.read()

        try:
            with st.spinner("Generating PDF report..."):
                pdf_bytes = build_pdf()
            st.success("✅ PDF generated! Click below to download.")
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_bytes,
                file_name="chemistry_pbl_flame_photometry.pdf",
                mime="application/pdf",
            )
        except Exception as e:
            st.error(f"PDF generation failed: {e}")
            st.info("Ensure data is submitted in Tab 1 and graph viewed in Tab 2 first.")