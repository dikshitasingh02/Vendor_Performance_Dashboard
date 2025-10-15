# 🧠 Vendor Performance Data Analytics Dashboard

The **Vendor Performance Data Analytics** project aims to evaluate and visualize vendor performance using real purchasing data.  
It integrates **Python for data ingestion and transformation** with **Power BI for visualization**, enabling decision-makers to identify top-performing vendors, analyze purchasing patterns, and optimize procurement strategies.

This project provides:
- Automated ingestion of multiple vendor-related CSV files into a **SQLite database**.  
- Analytical computation of purchase contributions, vendor rankings, and performance KPIs.  
- Interactive **Power BI Dashboard** for clear and actionable insights.

---

## 🧩 Components Overview

### 1. **Data Ingestion Script (`ingestion_db.py`)**
- Loads all CSV files from the `data/` folder.
- Inserts them into a SQLite database (`inventory.db`).
- Uses SQLAlchemy for efficient, chunk-based ingestion.
- Maintains a log file (`logs/ingestion_db.log`) for tracking the process.

**Features:**
- Dynamic table creation (one per CSV file)
- Batch insertion for large datasets
- Detailed logging for debugging and tracking

---

### 2. **Jupyter Notebook (`Untitled.ipynb`)**
- Performs exploratory data analysis (EDA).
- Cleans and transforms the ingested data.
- Calculates metrics like:
  - Total purchase value per vendor  
  - Purchase contribution percentage  
  - Vendor performance summary tables  
- Prepares datasets used by Power BI.

---

### 3. **Power BI Dashboard (`Vendor-Performance-Dashboard.pbix`)**
- Visualizes summarized vendor data from the SQLite database or exported CSVs.
- Offers interactive visualizations, including:
  - Top vendors by purchase contribution
  - Purchase trends over time
  - Vendor category analysis
  - Purchase contribution percentage comparison
- Enables filtering and slicing by vendor or product type.

---

## ⚙️ Tech Stack

| Category | Tools / Technologies |
|-----------|----------------------|
| Programming Language | Python 3 |
| Libraries | Pandas, SQLAlchemy, Logging |
| Database | SQLite |
| Visualization | Power BI |
| Environment | Jupyter Notebook |


