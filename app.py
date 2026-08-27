mport streamlit as st
import pandas as pd
import re
import io
from data_pipe import execute_universal_etl_pipeline

# Configure Web Presentation Viewport Layout
st.set_page_config(
    page_title="Universal Financial Pipeline Engine",
    page_icon="📊",
    layout="wide"
)

st.title("🌐 Global Financial Data Pipeline Dashboard")
st.markdown("Modular decoupled pipeline reading data parameters directly from encrypted Cloud Secrets environments.")

# Drag and Drop File Import Interface Viewport
uploaded_file = st.file_uploader("📥 Drag and drop your transaction statement profile (CSV, XLSX, XLS, TXT)...", type=["csv", "xlsx", "xls", "txt"])

if uploaded_file is not None:
    file_name = uploaded_file.name
    file_ext = re.sub(r'.*(\..*)$', r'\1', file_name).lower()
    
    try:
        if file_ext in ['.xlsx', '.xls']: raw_input_df = pd.read_excel(uploaded_file, sheet_name=0)
        elif file_ext == '.csv': raw_input_df = pd.read_csv(uploaded_file)
        else: raw_input_df = pd.read_csv(uploaded_file, sep=None, engine='python')
        st.success(f"✔️ Loaded Target Profile: '{file_name}' | Ingested: {raw_input_df.shape} Rows")
    except Exception as e:
        st.error(f"Critical Ingestion Error: {e}")
        raw_input_df = None

    if raw_input_df is not None:
        # Trigger dynamic general ledger extraction parameters pass
        final_xero_df, reconciliation_df, opex_weights_df, dynamic_layout_indices = execute_universal_etl_pipeline(raw_input_df)
        
        # Diagnostic Sorter Column Mapping Log Block
        with st.expander("🔍 Ingestion Mapping Sorter Metadata Insight Logs", expanded=False):
            st.json({k: (f"Detected at column index [{v}] ({raw_input_df.columns[v]})" if v is not None else "Missing - Using Fallback Parsing Engine") for k, v in dynamic_layout_indices.items()})

        # Render output sheets tab screens
        st.subheader("📊 General Ledger Audit Sorter Analytics")
        tab1, tab2, tab3 = st.tabs(["Xero Bank Import layout", "Balance Verification Audit", "OpEx Spend Analytics Sorter"])
        
        with tab1:
            st.markdown("#### Normalized general ledger format structured for direct Xero statement uploads.")
            st.dataframe(final_xero_df, use_container_width=True)
        with tab2:
            st.markdown("#### Post-ETL General Ledger balance scorecard summary calculations.")
            st.dataframe(reconciliation_df, use_container_width=True)
        with tab3:
            st.markdown("#### Absolute OpEx spending weights distribution analysis matrix.")
            st.dataframe(opex_weights_df, use_container_width=True)
            
        # Stream structured sheets to buffer stream for download
        buffer_memory_stream = io.BytesIO()
        with pd.ExcelWriter(buffer_memory_stream, engine='xlsxwriter') as workbook_writer:
            final_xero_df.to_excel(workbook_writer, sheet_name='Xero Bank Import layout', index=False)
            reconciliation_df.to_excel(workbook_writer, sheet_name='Balance Verification Audit', index=False)
            opex_weights_df.to_excel(workbook_writer, sheet_name='OpEx Spend Analytics Sorter', index=False)
            
        st.markdown("---")
        # Visual File Export Asset Trigger Button
        st.download_button(
            label="💾 Download Compiled Multi-Tab Xero Reporting Package (.XLSX)",
            data=buffer_memory_stream.getvalue(),
            file_name="Universal_Xero_Purified_Financial_Package.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
