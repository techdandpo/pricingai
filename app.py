import streamlit as st
from bidding_sheet_builder import bidding_sheet_builder
from catalog_sheet_builder import catalog_sheet_builder
from catalog_qc import catalog_qc


st.set_page_config(page_title="📊 Bidding Sheet Builder", layout="wide")

# Inject custom CSS for brand styling and logo
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stApp {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #000000;
        }
        .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
            color: #185f5d;
            font-weight: 600;
        }
        .stApp h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        .stApp h2 {
            font-size: 2rem;
        }
        .stApp h3 {
            font-size: 1.5rem;
        }
        header .block-container {
            padding-top: 2rem;
        }
        .reportview-container .main footer {visibility: hidden;}
        .logo-header {
            display: flex;
            align-items: left;
            justify-content: left;
        }
        .title-section {
            text-align: left;
            margin-bottom: 2rem;
        }
        .title-section h1 {
            margin-bottom: 0.5rem;
        }
        .separator-line {
            height: 3px;
            background-color: #185f5d;
            margin: 0 auto;
            width: 100%;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            padding: 0 1rem;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #e9ecef;
            border-radius: 8px 8px 0 0;
            color: #000000;
            font-weight: 500;
            padding: 0.75rem 1.5rem;
            min-width: 120px;
            text-align: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .stTabs [aria-selected="true"] {
            background-color: #185f5d;
            color: white;
        }
        .stTabs [data-baseweb="tab"] span {
            font-size: 0.9rem;
            line-height: 1.2;
        }
        .stButton > button {
            background-color: #185f5d;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #0f4a48;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(24, 95, 93, 0.3);
        }
        .stFileUploader > div {
            border: 2px dashed #185f5d;
            border-radius: 8px;
            background-color: #f8f9fa;
        }
        .stFileUploader > div:hover {
            border-color: #0f4a48;
            background-color: #e9ecef;
        }
        .stDataFrame {
            border: 1px solid #185f5d;
            border-radius: 8px;
        }
        .stDataFrame th {
            background-color: #185f5d !important;
            color: white !important;
        }
        .stDataFrame td {
            border-bottom: 1px solid #e9ecef;
        }
        .stDataFrame tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        .stDataFrame tr:hover {
            background-color: #e9ecef;
        }
        .stAlert {
            border-left: 4px solid #185f5d;
            background-color: #e9ecef;
        }
        .stAlert [data-testid="stMarkdown"] {
            color: #000000;
        }
        .stInfo {
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
        }
        .stError {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        .stSuccess {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .stNumberInput > div {
            max-width: 300px !important;
        }
        .stNumberInput > div > div {
            max-width: 300px !important;
        }
        .stNumberInput input {
            max-width: 300px !important;
        }
        .stButton > button:disabled {
            background-color: #e9ecef !important;
            color: #6c757d !important;
            border: 1px solid #dee2e6 !important;
            cursor: not-allowed !important;
            opacity: 0.6 !important;
        }
        .stButton > button:disabled:hover {
            background-color: #e9ecef !important;
            color: #6c757d !important;
            transform: none !important;
            box-shadow: none !important;
        }
    </style>
    <div class="logo-header">
        <img src="https://www.dandpo.com/media/logo/stores/1/dandpo-logo-01.svg" alt="Logo" style="height: 60px;">
    </div>
    <div class="title-section">
        <h1>Supplier Sheet Builder</h1>
        <div class="separator-line"></div>
    </div>
""", unsafe_allow_html=True)

tabs = st.tabs(["Bidding Sheet Builder", "Catalog Sheet Builder", "Catalog QC"])

with tabs[0]:
    bidding_sheet_builder()

with tabs[1]:
    catalog_sheet_builder()

with tabs[2]:
    catalog_qc()