import streamlit as st
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
    raw_input_df = None
    
    try:
        if file_ext in ['.xlsx', '.xls']:
            excel_file_object = pd.ExcelFile(uploaded_file)
            sheet_names_list = excel_file_object.sheet_names
            
            if len(sheet_names_list) > 1:
                selected_sheet = st.selectbox(
                    f"📂 This workbook contains {len(sheet_names_list)} tabs. Please select the target sheet to parse:",
                    options=sheet_names_list
                )
                raw_input_df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
            else:
                raw_input_df = pd.read_excel(uploaded_file, sheet_name=0)
                
        elif file_ext == '.csv':
            raw_input_df = pd.read_csv(uploaded_file)
        else:
            raw_input_df = pd.read_csv(uploaded_file, sep=None, engine='python')
            
        if raw_input_df is not None:
            st.success(f"✔️ Loaded Target Data Matrix! Shape Dimensions: {raw_input_df.shape[0]} Rows, {raw_input_df.shape[1]} Columns")
    except Exception as e:
        st.error(f"❌ Critical Ingestion Error: Failed to structure input streams. Details: {e}")
        raw_input_df = None

    if raw_input_df is not None:
        # Trigger general ledger processing pass
        final_xero_df, reconciliation_df, global_distribution_df, dynamic_layout_indices = execute_universal_etl_pipeline(raw_input_df)
        
        # Calculate Grand Sum of Rows for Visual KPI Cards Tracker
        grand_total_rows = int(global_distribution_df["Total_Row_Count"].sum())
        total_activity_weight = global_distribution_df["Global Ledger Activity Weight (%)"].sum()
        
        # Inject structural Summary Totals Row directly onto the screen view dataframe
        totals_row = pd.DataFrame([{
            'Xero_Account_Code': 'TOTALS',
            'Ledger Category Title Sorter Name': 'Grand Total Summary Slices',
            'Net_Balance': final_xero_df['*Amount'].sum(),
            'Inbound_Receipts_Volume': global_distribution_df['Inbound_Receipts_Volume'].sum(),
            'Outbound_Expenditures_Volume': global_distribution_df['Outbound_Expenditures_Volume'].sum(),
            'Total_Row_Count': grand_total_rows,
            'Global Ledger Activity Weight (%)': round(total_activity_weight, 2)
        }])
        
        # Concatenate summary totals safely to the bottom of the analytical frame
        display_distribution_df = pd.concat([global_distribution_df, totals_row], ignore_index=True)
        
        with st.expander("🔍 Ingestion Mapping Sorter Metadata Insight Logs", expanded=False):
            st.json({k: (f"Detected at column index [{v}] ({raw_input_df.columns[v]})" if v is not None else "Missing - Using Fallback Parsing Engine") for k, v in dynamic_layout_indices.items()})

        # Top Executive KPI Indicator Dashboard Block
        st.markdown("### 📋 General Ledger Core Vital Cards")
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        with kpi_col1:
            st.metric(label="✨ Grand Sum of Total Transactions Rows", value=f"{grand_total_rows} Rows")
        with kpi_col2:
            st.metric(label="💰 Statement Net Ledger Balance", value=f"AED {final_xero_df['*Amount'].sum():,.2f}")
        with kpi_col3:
            st.metric(label="⚡ Active Code Accounts Mapped", value=f"{len(global_distribution_df)} Active Accounts")

        # Render output dashboards tabs panels
        st.subheader("📊 General Ledger Audit Sorter Analytics")
        tab1, tab2, tab3 = st.tabs(["Xero Bank Import layout", "Balance Verification Audit", "Global Ledger Spend & Activity Sorter"])
        
        with tab1:
            st.markdown("#### Normalized general ledger format structured for direct Xero statement uploads.")
            st.dataframe(final_xero_df, use_container_width=True)
        with tab2:
            st.markdown("#### Post-ETL General Ledger balance scorecard summary calculations.")
            st.dataframe(reconciliation_df, use_container_width=True)
        with tab3:
            st.markdown("#### Global Activity weights distribution analysis matrix showing **Grand Sum Totals** row.")
            st.dataframe(display_distribution_df, use_container_width=True)
            
        # Stream structured sheets to buffer stream
        buffer_memory_stream = io.BytesIO()
        with pd.ExcelWriter(buffer_memory_stream, engine='xlsxwriter') as workbook_writer:
            final_xero_df.to_excel(workbook_writer, sheet_name='Xero Bank Import layout', index=False)
            reconciliation_df.to_excel(workbook_writer, sheet_name='Balance Verification Audit', index=False)
            # Exports the clean structural matrix dataset page
            global_distribution_df.to_excel(workbook_writer, sheet_name='Global Activity Sorter', index=False)
            
        st.markdown("---")
        st.download_button(
            label="💾 Download Compiled Multi-Tab Xero Reporting Package (.XLSX)",
            data=buffer_memory_stream.getvalue(),
            file_name="Universal_Xero_Purified_Financial_Package.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
