# Universal Financial Pipeline Engine

An enterprise-grade, cloud-native **automated financial ingestion dashboard** built with Streamlit and Pandas. This application provides a no-code interface to upload raw, multi-format bank statements, dynamically clean currency notations, automatically classify transactions, and export audit-ready accounting packages optimized for platforms like **Xero**.

---

## 📈 System Architecture

The project utilizes a decoupled, split-architecture design to isolate core business ETL logic from presentation scripts:

📁 universal-financial-pipeline/
│
├── 📄 .gitignore                 # Exclusion configuration rules manifest file
├── 📄 app.py                     # Front-end workspace UI viewport presentation layer
├── 📄 data_pipe.py               # Back-end automated ETL classification routine engine
├── 📄 README.md                  # System manual and architecture specification handbook
└── 📄 requirements.txt           # Explicit system python wheel bundle dependency checklist


---

## ✨ Core Features

* **Header-Agnostic Fuzzy Parsing:** Dynamically detects `Date`, `Description`, `Amount`, `Payee`, and `Reference` columns across various ledger schemas without requiring rigid templates.
* **Global Currency Sorter:** Uses regex filters to auto-clean text noise, strip transaction codes, and sanitize localized float formatting (such as swapping European commas and decimal markers).
* **Automated Rules Classifier:** Scans unstructured narratives against custom pattern lists to securely assign chart-of-accounts codes.
* **Executive Performance KPIs:** Instantly aggregates net cash flows, active ledger footprints, row concentrations, and unmapped balances in real time.
* **Interactive Drill-Down Grids:** Utilizes Streamlit's structural selection mode (`on_select="rerun"`) to allow auditors to click any row summary and review underlying raw ledger logs.
* **Virtual In-Memory Compilation:** Leverages `io.BytesIO` streams to package multiple analysis dataframes into a multi-sheet `.xlsx` file download on the fly.

---

---

## 🚀 Quick Start Execution

1. **Clone or save** both `app.py` and `data_pipe.py` into your working root directory.
2. Ensure you have installed the required baseline visualization and calculation libraries:
   ```bash
   pip install streamlit pandas numpy plotly xlsxwriter openpyxl
   ```
3. Initialize the local server using your terminal session execution panel:
   ```bash
   streamlit run app.py
   ```
4. Access your interactive dashboard via the native local desktop viewport (`http://localhost:8501`).

---

## 🛡️ Cloud-Native Security Design

* **De-coupled Architecture:** Layout routines are strictly separated from financial rulesets to ensure script logic changes do not break visual alignment blocks.
* **Encrypted Secrets Management:** Sensitive structural keyword lexicons and explicit chart account properties are safely hosted out of the open source control system via production workspace secrets encryption keys.
