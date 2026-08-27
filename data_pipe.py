import streamlit as st
import pandas as pd
import numpy as np
import re

def adaptive_monetary_parser(raw_value):
    """Dynamically cleans string text noise to extract floats across global formats."""
    if pd.isnull(raw_value): return 0.0
    if isinstance(raw_value, (int, float)): return float(raw_value)
    clean_str = str(raw_value).upper().strip()
    clean_str = re.sub(r'\*\*\*\*\d+|\*\d+|\b\d{2}/\d{2}/\d{2,4}\b', '', clean_str)
    currency_pattern = r'(?:[A-Z]{3}|[\$€£₹]|TRX\.\s+OF|FOR|AED|USD|EUR|GBP)\s*([-\d\.,]+)'
    match = re.search(currency_pattern, clean_str)
    target_text = match.group(1).strip() if match else clean_str
    if ',' in target_text and '.' in target_text:
        if target_text.rfind(',') > target_text.rfind('.'):
            target_text = target_text.replace('.', '').replace(',', '.')
        else:
            target_text = target_text.replace(',', '')
    elif ',' in target_text and '.' not in target_text:
        if len(target_text.split(',')) == 2: target_text = target_text.replace(',', '.')
        else: target_text = target_text.replace(',', '')
    target_text = re.sub(r'[^\d\.-]', '', target_text)
    try: return float(target_text)
    except ValueError:
        fallback = re.search(r'([-\d,]+\.\d+)', clean_str)
        if fallback: return float(fallback.group(1).replace(',', ''))
        return 0.0

def trace_file_column_indices(columns_list):
    """Header-Agnostic Fuzzy Matcher to identify indices across any layout."""
    normalized_cols = [str(c).lower().strip() for c in columns_list]
    mapping = {'date': None, 'amount': None, 'text': None, 'ref': None, 'payee': None}
    for idx, col in enumerate(normalized_cols):
        if any(tk in col for tk in ['date', 'time', 'timestamp']): mapping['date'] = idx
        elif any(tk in col for tk in ['amount', 'value', 'money', 'volume', 'parsed_amount', '*amount', 'dr', 'cr']): mapping['amount'] = idx
        elif any(tk in col for tk in ['sms', 'msg', 'description', 'narrative', 'text_line', 'memo', 'details']): mapping['text'] = idx
        elif any(tk in col for tk in ['id', 'reference', 'ref', 'trx', 'serial', 'tx']): mapping['ref'] = idx
        elif any(tk in col for tk in ['cardholder', 'payee', 'user', 'owner', 'client', 'vendor']): mapping['payee'] = idx
    if mapping['text'] is None:
        for idx, col in enumerate(normalized_cols):
            if 'string' in col or 'object' in col or 'sms' in col:
                mapping['text'] = idx
                break
    return mapping

def generic_xero_pipeline_classifier(sms_narrative, numeric_valuation):
    """Universal classification router queried directly from Cloud Secrets runtime."""
    if pd.isnull(sms_narrative) or str(sms_narrative).strip() == "":
        return "⚠️ Suspense Profile", "9999", "UNCLASSIFIED ROW"
    text = str(sms_narrative).upper()
    val = float(numeric_valuation)
    
    secrets_titles = st.secrets["group_titles"]
    secrets_lexicon = st.secrets["universal_lexicon"]

    if val == 0.0 or any(flag in text for flag in ["SECURITY CODE", "CREATED FOR YOU", "OPENING A NEW"]):
        return "⚠️ Suspense Profile", "9999", "SYSTEM ALERT MATRIX"
    if "APPLE PAY" in text: return secrets_titles["8500"], "8500", secrets_titles["8500"]
    if "REVERSED" in text or "REFUND" in text: return secrets_titles["4999"], "4999", "REVERSAL CREDIT CORRECTION"
    if abs(val) in [1.05, 1.20, 4.65]: return secrets_titles["2500"], "2500", "BANK SYSTEM CHARGE PROCESSING"
    if "SALARY" in text or "PAYROLL" in text or "STIPEND" in text: return secrets_titles["2000"], "2000", "REVENUE REMUNERATION INFLOW"
    if val > 10000.0 and not any(tk in text for tk in ["TRANSFER", "TRFX", "IFT", "IBAN", "CLEARING", "CHQ", "CHEQUE"]):
        return secrets_titles["7000"], "7000", "DIRECT SYSTEM CAPITAL INJECTION"
    if "WITHDRAWAL" in text or "ATM" in text or "CASH OUT" in text: return secrets_titles["1000"], "1000", "ATM VAULT LIQUID DISBURSEMENT"
    if "CHICO" in text: return secrets_titles["4600"], "4600", "STAFF PROVISIONS & FOOD DELIVERY"
    
    for account_code, patterns in secrets_lexicon.items():
        for pattern in patterns:
            is_match = False
            if pattern.startswith(r"\b") or pattern.endswith(r"\b"):
                if re.search(pattern, text): is_match = True
            elif pattern in text: is_match = True
            if is_match:
                group_info = secrets_titles[str(account_code)]
                return group_info, str(account_code), group_info

    if val > 0:
        if any(tk in text for tk in ["TRANSFER", "TRFX", "IFT", "IBAN", "CLEARING", "CHQ", "CHEQUE"]): return secrets_titles["1050"], "1050", secrets_titles["1050"]
        return secrets_titles["2100"], "2100", secrets_titles["2100"]
    else:
        if any(tk in text for tk in ["TRANSFER", "TRFX", "IFT", "IBAN", "CLEARING"]): return secrets_titles["1050"], "1050", secrets_titles["1050"]
        return secrets_titles["4999"], "4999", secrets_titles["4999"]
def assemble_universal_audit_trail(df):
    """Calculates ledger receipts vs disbursements balance reconciliation matrices."""
    inflows = df[df['*Amount'] > 0]['*Amount'].sum()
    outflows = df[df['*Amount'] < 0]['*Amount'].sum()
    net_bal = df['*Amount'].sum()
    
    secrets_titles = st.secrets["group_titles"]
    audit_rows = []
    for code, metadata in secrets_titles.items():
        code_sum = df[df['Xero_Account_Code'] == code]['*Amount'].sum()
        audit_rows.append([f"Account {code} Balance ({metadata})", code_sum, metadata])
        
    audit_rows.extend([
        ["Total Receipts Volume (+)", inflows, "Gross Inbound Velocity Summary"],
        ["Total Disbursements Volume (-)", outflows, "Gross Outbound Velocity Summary"],
        ["Statement General Ledger Net Balance Check", net_bal, "Financial Baseline Check"]
    ])
    
    recon_df = pd.DataFrame(audit_rows, columns=["Audit Ledger Evaluation Metric", "Aggregated Balance", "Meta Classification Group"])
    
    opex_mask = df['Xero_Account_Code'].str.startswith('4')
    opex_df = df[opex_mask].copy()
    if not opex_df.empty:
        opex_df['Abs_Val'] = opex_df['*Amount'].abs()
        ops_matrix = opex_df.groupby('Xero_Account_Code').agg(Spend_Volume=('Abs_Val', 'sum'), Row_Count=('Xero_Account_Code', 'count')).reset_index()
        ops_matrix['Category Sorter Title'] = ops_matrix['Xero_Account_Code'].map(lambda x: secrets_titles.get(x, ["-", "Other Expenses"]))
        tot_ops = ops_matrix['Spend_Volume'].sum()
        ops_matrix['Operational Allocation Weight (%)'] = ((ops_matrix['Spend_Volume'] / tot_ops) * 100).round(2) if tot_ops > 0 else 0
        ops_matrix = ops_matrix.sort_values(by='Spend_Volume', ascending=False)
    else:
        ops_matrix = pd.DataFrame(columns=['Xero_Account_Code', 'Category Sorter Title', 'Spend_Volume', 'Row_Count', 'Operational Allocation Weight (%)'])
    return recon_df, ops_matrix

def simplify_bank_description(text):
    if not isinstance(text, str): return ""
    text_clean = text.strip()
    if " at " in text_clean:
        parts_after_at = text_clean.split(" at ", 1)
        if len(parts_after_at) > 1:
            vendor_desc_raw = parts_after_at[1]
            cleaned_vendor_parts = re.split(r'\. Avl|\.  Your|\. Your| on \d| in ', vendor_desc_raw, flags=re.IGNORECASE)
            return cleaned_vendor_parts[0].strip().upper()[:60] # FIXED: Grab element [0] safely out of list match
        else: return text_clean.upper()[:60]
    clean_text = re.split(r'\. Your available|" Your avl|\. WAS CREDITED|\. WAS DEBITED', text_clean, flags=re.IGNORECASE)
    return clean_text[0].strip().upper()[:60] # FIXED: Grab element [0] safely out of list match

def execute_universal_etl_pipeline(raw_input_df):
    layout_map = trace_file_column_indices(raw_input_df.columns)
    normalized_output_df = pd.DataFrame()
    
    if layout_map['date'] is not None:
        raw_dates = raw_input_df.iloc[:, layout_map['date']]
        normalized_output_df['*Date'] = pd.to_datetime(raw_dates, errors='coerce').dt.strftime('%Y-%m-%d')
        normalized_output_df['*Date'] = normalized_output_df['*Date'].fillna(pd.Timestamp.now().strftime('%Y-%m-%d'))
    else:
        normalized_output_df['*Date'] = pd.Timestamp.now().strftime('%Y-%m-%d')
        
    text_index = layout_map['text'] if layout_map['text'] is not None else 0
    raw_narratives = raw_input_df.iloc[:, text_index].astype(str).fillna("")
    
    if layout_map['amount'] is not None:
        interim_amounts = raw_input_df.iloc[:, layout_map['amount']].apply(adaptive_monetary_parser)
    else:
        interim_amounts = raw_narratives.apply(adaptive_monetary_parser)
        
    normalized_output_df['Payee'] = raw_input_df.iloc[:, layout_map['payee']].astype(str).fillna("General Account Payee") if layout_map['payee'] is not None else "General Corporate Account"
    normalized_output_df['Reference'] = raw_input_df.iloc[:, layout_map['ref']].astype(str).fillna("") if layout_map['ref'] is not None else ""
    normalized_output_df['Cheque Number'] = ""
    normalized_output_df['Reference'] = normalized_output_df['Reference'].apply(lambda x: str(int(float(x))) if x != "" and re.match(r'^\d+(\.\d+)?$', str(x)) else str(x))

    engine_classifications = [generic_xero_pipeline_classifier(narrative, amt)[1] for narrative, amt in zip(raw_narratives, interim_amounts)]
    normalized_output_df['Description'] = [simplify_bank_description(narrative) for narrative in raw_narratives]
    normalized_output_df['Xero_Account_Code'] = [item for item in engine_classifications]
    
    final_amounts = []
    for desc, val in zip(raw_narratives, interim_amounts):
        desc_lower = desc.lower()
        if any(tk in desc_lower for tk in ["debited", "withdrawal", "spent", "paid at", "purchase", "outward"]): final_amounts.append(-abs(val))
        elif any(tk in desc_lower for tk in ["credited", "deposited", "received", "inward"]): final_amounts.append(abs(val))
        else: final_amounts.append(val)
    normalized_output_df['*Amount'] = final_amounts
    
    final_xero_import_layout = normalized_output_df[['*Date', '*Amount', 'Payee', 'Description', 'Reference', 'Xero_Account_Code', 'Cheque Number']]
    reconciliation_report_sheet, opex_distribution_sheet = assemble_universal_audit_trail(final_xero_import_layout)
    
    return final_xero_import_layout, reconciliation_report_sheet, opex_distribution_sheet, layout_map
