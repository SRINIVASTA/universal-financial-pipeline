import streamlit as st
import pandas as pd
import re
import io
import plotly.express as px
from data_pipe import execute_universal_etl_pipeline

# Configure Web Presentation Viewport Layout for Premium Desktop View
st.set_page_config(
    page_title="Universal Financial Pipeline Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS Styling for Corporate UI Depth
st.markdown("""
    <style>
        div[data-testid="stMetricValue"] {
            font-size: 28px;
            font-weight: 700;
            color: #1E3A8A;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 14px;
            color: #4B5563;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .reportview-container .main .block-container{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1 {
            color: #1E3A8A;
            font-weight: 800;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR CONTROL CONSOLE LAYER
# ==============================================================================
with st.sidebar:
    st.image("https://icons8.com", width=70)
    st.markdown("## **Control Console**")
    st.markdown("Configure ledger parameters and process source file import wrappers cleanly.")
    st.markdown("---")
    
    # Drag and Drop File Import Interface Viewport inside Sidebar
    uploaded_file = st.file_uploader(
        "⚡ Ingest Transaction Profile File", 
        type=["csv", "xlsx", "xls", "txt"],
        help="Supports generic banking rows, SMS sheets, or standard statement data."
    )
    
    st.markdown("---")
    st.markdown("### **System Status**")
    if uploaded_file is not None:
        st.info("🟢 File loaded successfully. Ready for processing pass.")
    else:
        st.warning("⚠️ Awaiting financial source file upload wrapper...")

# ==============================================================================
# MAIN DASHBOARD INITIALIZATION LAYER
# ==============================================================================
if uploaded_file is None:
    st.title("📊 Universal Financial Data Pipeline Dashboard")
    st.markdown("Welcome to the general ledger pipeline suite. Please use the left **Control Console** sidebar to ingest your raw banking files, clean decimal notation, filter unmapped balances, and generate a standardized, multi-tab reporting package ready for Xero import.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("#### ⚙️ Automated Engine Processing Features\n"
                "* **Fuzzy Header Matcher:** Automatically detects Date, Description, and Amount columns.\n"
                "* **Currency Decimals Sorter:** Autocorrects European and localized float types on the fly.\n"
                "* **Liability Loops Shield:** Prevents double-counting with dedicated clearing codes.")
    with col2:
        st.info("#### 🛡️ Cloud-Native Security Design\n"
                "* **De-coupled Architecture:** Business logic is isolated entirely from layout scripts.\n"
                "* **Streamlit Cloud Secrets Encryption:** Sensitive keyword structures and chart account properties are safely hosted out of the open GitHub codebase.")
else:
    file_name = uploaded_file.name
    file_ext = re.sub(r'.*(\..*)$', r'\1', file_name).lower()
    raw_input_df = None
    
    try:
        if file_ext in ['.xlsx', '.xls']:
            excel_file_object = pd.ExcelFile(uploaded_file)
            sheet_names_list = excel_file_object.sheet_names
            
            if len(sheet_names_list) > 1:
                selected_sheet = st.sidebar.selectbox(
                    "📁 Target Sheet Selection Panel:",
                    options=sheet_names_list
                )
                raw_input_df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
            else:
                raw_input_df = pd.read_excel(uploaded_file, sheet_name=0)
                
        elif file_ext == '.csv':
            raw_input_df = pd.read_csv(uploaded_file)
        else:
            raw_input_df = pd.read_csv(uploaded_file, sep=None, engine='python')
            
    except Exception as e:
        st.error(f"Critical Ingestion Error: {e}")
        raw_input_df = None
    if raw_input_df is not None:
        final_xero_df, reconciliation_df, global_distribution_df, dynamic_layout_indices = execute_universal_etl_pipeline(raw_input_df)
        
        grand_total_rows = int(global_distribution_df["Total_Row_Count"].sum())
        total_activity_weight = global_distribution_df["Global Ledger Activity Weight (%)"].sum()
        
        totals_row = pd.DataFrame([{
            'Xero_Account_Code': 'TOTALS',
            'Ledger Category Title Sorter Name': 'Grand Total Summary Slices',
            'Net_Balance': final_xero_df['*Amount'].sum(),
            'Inbound_Receipts_Volume': global_distribution_df['Inbound_Receipts_Volume'].sum(),
            'Outbound_Expenditures_Volume': global_distribution_df['Outbound_Expenditures_Volume'].sum(),
            'Total_Row_Count': grand_total_rows,
            'Global Ledger Activity Weight (%)': round(total_activity_weight, 2)
        }])
        
        display_distribution_df = pd.concat([global_distribution_df, totals_row], ignore_index=True)

        st.title("📊 General Ledger Audit & Ingestion Workspace")
        st.markdown(f"Currently analyzing worksheet data matrix. Ingested profile table footprint contains **{grand_total_rows:,} records**.")

        # Top Executive KPI Indicator Dashboard Block Containers
        st.markdown("### 📋 GENERAL LEDGER PERFORMANCE RECONCILIATION CARDS")
        kpi_container = st.container()
        with kpi_container:
            kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
            with kpi_col1:
                st.metric(label="✨ Grand Sum Row Footprint", value=f"{grand_total_rows:,} Transactions")
            with kpi_col2:
                st.metric(label="💰 Statement Net Cash-Flow", value=f"AED {final_xero_df['*Amount'].sum():,.2f}")
            with kpi_col3:
                st.metric(label="📊 Active Chart Codes Mapped", value=f"{len(global_distribution_df)} Accounts")
            with kpi_col4:
                unmapped_rows = int(global_distribution_df[global_distribution_df['Xero_Account_Code'] == '4999']['Total_Row_Count'].sum())
                st.metric(label="⚠️ Unmapped Supplier Fallbacks", value=f"{unmapped_rows} Rows")

        st.markdown("---")

        # ==============================================================================
        # DATA VISUALIZATION LAYER (HIGH-IMPACT INTERACTIVE DESKTOP CHARTS)
        # ==============================================================================
        st.markdown("### 📊 INTERACTIVE SPEND WEIGHTS & ACTIVITY DISPERSION LOGS")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            spend_chart_df = global_distribution_df[global_distribution_df['Outbound_Expenditures_Volume'] > 0].copy()
            if not spend_chart_df.empty:
                fig_spend = px.bar(
                    spend_chart_df,
                    x='Outbound_Expenditures_Volume',
                    y='Ledger Category Title Sorter Name',
                    orientation='h',
                    title='Total Outbound Spend Dispersal by General Ledger Account Group',
                    labels={'Outbound_Expenditures_Volume': 'Total Value (Local Currency)', 'Ledger Category Title Sorter Name': 'Account Category'},
                    color='Outbound_Expenditures_Volume',
                    color_continuous_scale='Blues',
                    template='plotly_white'
                )
                fig_spend.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False, height=350, margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_spend, use_container_width=True)
            else:
                st.info("No outbound general ledger expense records available to render charts.")

        with chart_col2:
            fig_pie = px.pie(
                global_distribution_df,
                values='Total_Row_Count',
                names='Xero_Account_Code',
                title='General Ledger Activity Row Concentration (%)',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Blues_r,
                template='plotly_white'
            )
            fig_pie.update_layout(height=350, margin=dict(l=0, r=0, t=40, b=0))
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("---")

        # ==============================================================================
        # DATA GRIDS LAYOUT RECONCILIATION TABS
        # ==============================================================================
        st.subheader("📋 GENERAL LEDGER VERIFICATION SHEETS & IMPORT GENERATION AUDIT")
        tab1, tab2, tab3 = st.tabs(["Xero Bank Import layout", "Balance Verification Audit", "Global Ledger Spend & Activity Sorter"])
        
        with tab1:
            st.markdown("##### Cleaned bank import formatting structure mapped to target platform upload specifications.")
            st.dataframe(final_xero_df, use_container_width=True, height=300)
        with tab2:
            st.markdown("##### Pre-import generalization scorecard analysis balancing inflow gross velocities vs outflows.")
            st.dataframe(reconciliation_df, use_container_width=True, height=300)
            
        with tab3:
            st.markdown("##### Global activity summary matrix. Select any row checkbox to instantly load specific account entries underneath.")
            
            clicked_event = st.dataframe(
                display_distribution_df,
                use_container_width=True,
                height=300,
                on_select="rerun",
                selection_mode="multi-row"
            )
            
            selected_row_indices = clicked_event.get("selection", {}).get("rows", [])
            if len(selected_row_indices) > 0:
                target_row_index = int(selected_row_indices[0])
                clicked_code = display_distribution_df.iloc[target_row_index]['Xero_Account_Code']
                
                if pd.notnull(clicked_code) and clicked_code != 'TOTALS':
                    secrets_titles = st.secrets["group_titles"]
                    st.markdown(f"### 🎯 Underlying Transactions Sorter Preview for Account `[{clicked_code}] - {secrets_titles.get(clicked_code, 'Base Account')}`")
                    
                    # Filter and extract specific account logs array segments
                    tgt_logs_df = final_xero_df[final_xero_df['Xero_Account_Code'] == clicked_code]
                    
                    sub_col1, sub_col2, sub_col3 = st.columns(3)
                    with sub_col1:
                        st.markdown(f"**Account Net Sorter Balance:** `AED {tgt_logs_df['*Amount'].sum():,.2f}`")
                    with sub_col2:
                        st.markdown(f"**Total Entry Rows Density:** `{len(tgt_logs_df)} Rows`")
                    with sub_col3:
                        st.markdown(f"**Relative Activity Weight:** `{round((len(tgt_logs_df)/grand_total_rows)*100, 2)}%` of tab data profile")
                        
                    st.dataframe(tgt_logs_df, use_container_width=True, height=200)
            
        # Stream structured analytics sheets tab to virtual memory byte stream
        buffer_memory_stream = io.BytesIO()
        with pd.ExcelWriter(buffer_memory_stream, engine='xlsxwriter') as workbook_writer:
            final_xero_df.to_excel(workbook_writer, sheet_name='Xero Bank Import layout', index=False)
            reconciliation_df.to_excel(workbook_writer, sheet_name='Balance Verification Audit', index=False)
            global_distribution_df.to_excel(workbook_writer, sheet_name='Global Activity Sorter', index=False)
            
        st.markdown("---")
        st.download_button(
            label="💾 Download Compiled Multi-Tab Xero Reporting Package (.XLSX)",
            data=buffer_memory_stream.getvalue(),
            file_name="Universal_Xero_Purified_Financial_Package.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
        # Diagnostic Sorter Column Mapping Log Block hidden safely at base footer
        with st.expander("🛠️ Advanced Ingestion Metadata Mapping Logs", expanded=False):
            st.json({k: (f"Detected at column index [{v}] ({raw_input_df.columns[v]})" if v is not None else "Missing - Using Fallback Parsing Engine") for k, v in dynamic_layout_indices.items()})
