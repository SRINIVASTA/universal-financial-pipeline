# Universal Financial Pipeline Engine

An enterprise-grade, cloud-native **automated financial ingestion dashboard** built with Streamlit and Pandas. This application provides a no-code interface to upload raw, multi-format bank statements, dynamically clean currency notations, automatically classify transactions, and export audit-ready accounting packages optimized for platforms like **Xero**.

---
🌐 **Live Interactive Web App:** [Launch Live Streamlit Dashboard](https://universal-financial-pipeline-kt44zlebx8hanzr9czlqdm.streamlit.app/)

## 📈 System Architecture

The project utilizes a decoupled, split-architecture design to isolate core business ETL logic from presentation scripts:

```text
📁 universal-financial-pipeline/

│
├── 📄 .gitignore                 # Exclusion configuration rules manifest file
├── 📄 app.py                     # Front-end workspace UI viewport presentation layer
├── 📄 data_pipe.py               # Back-end automated ETL classification routine engine
├── 📄 README.md                  # System manual and architecture specification handbook
└── 📄 requirements.txt           # Explicit system python wheel bundle dependency checklist
```


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

---

## 🛡️ Cloud-Native Security Design

* **De-coupled Architecture:** Layout routines are strictly separated from financial rulesets to ensure script logic changes do not break visual alignment blocks.
* **Encrypted Secrets Management:** Sensitive structural keyword lexicons and explicit chart account properties are safely hosted out of the open source control system via production workspace secrets encryption keys.

## 📄 License & Copyright

> ⚠️ **IMPORTANT COPYRIGHT NOTICE**
> 
> **All Rights Reserved © 2026 T A Srinivas.**
> This repository is strictly for portfolio viewing purposes. **DO NOT COPY, CLONE, OR REDISTRIBUTE** this code. Stolen copies or unauthorized forks will be reported immediately for a GitHub copyright takedown.

* **Lead Architect & Developer:** [Srinivasta](https://github.com/SRINIVASTA)

### 🌐 Let’s Connect

- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/srinivas-t-a-557637119/)  
- [![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/srinivasta)  
- [![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:tasrinivass@gmail.com)  
- [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/srinivasta)
- [![Website](https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=website&logoColor=white)](https://srinivasta.github.io)
