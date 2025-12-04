 Campus Energy-Use Dashboard — Capstone Project  
Programming for Problem Solving using Python (Semester 1)

This project analyzes electricity consumption across multiple campus buildings and generates:
- Cleaned dataset
- Daily & weekly usage summaries
- Visualization dashboard
- OOP-based building reports
- Executive summary

---

## 📁 Project Files

Assignment-5/
│
├── buildingA.csv
├── buildingB.csv
├── buildingC.csv
│
├── capstone.py
├── building_summary.csv
├── cleaned_energy_data.csv
├── dashboard.png
├── summary.txt
│
└── README.md

yaml
Copy code

---

## 🎯 Objective

To build a complete energy-analysis pipeline that:
1. Reads and validates multiple CSV files.  
2. Performs daily and weekly energy usage calculations.  
3. Models buildings using Object-Oriented Programming.  
4. Creates visual dashboards using Matplotlib.  
5. Generates an automated summary for decision-making.

---

## ✔ Tasks Completed (Merged Explanation)

### **1. Data Ingestion & Validation**
- Loaded all CSV files inside the data folder.  
- Added building names automatically from filenames.  
- Converted timestamps to `datetime`.  
- Handled missing/invalid rows using `on_bad_lines='skip'`.  
- Merged all datasets into one DataFrame.

---

### **2. Aggregation Logic**
Using Pandas:
- Daily totals calculated with `resample('D')`
- Weekly totals calculated with `resample('W')`
- Building-wise summary generated with `groupby()`

Exported summary → `building_summary.csv`

---

### **3. Object-Oriented Modeling**
Implemented:
- **MeterReading** → stores timestamp and kWh  
- **Building** → stores readings, calculates totals, generates reports  
- **BuildingManager** → manages multiple building objects  

Improves readability and modularity of the project.

---

### **4. Visualization Dashboard**
Created `dashboard.png` with:
1. Daily energy trend line  
2. Weekly average bar chart  
3. Peak-load scatter plot  

All charts generated using Matplotlib.

---

### **5. Persistence & Summary**
The script exports:
- `cleaned_energy_data.csv`
- `building_summary.csv`
- `summary.txt` (executive report)

Summary includes:
- Total campus consumption  
- Highest consuming building  
- Peak load time  
- Overall usage trend  

---

## 🛠 How to Run the Project

### Install required libraries:
pip install pandas matplotlib

shell
Copy code

### Run the script:
python capstone.py

yaml
Copy code

Output files will be created automatically in your project folder.

---

## 📊 Example Summary Output (from summary.txt)
Total campus consumption: 142,281 kWh
Highest consuming building: Engineering
Peak load time: varies by building
Main trend: daily totals fluctuate; weekly averages highlight usage.

yaml
Copy code

---

## 📘 Dataset Format
Each CSV follows:
timestamp,kwh
2024-01-01 00:00,12
2024-01-01 01:00,15
...

yaml
Copy code

Buildings used:
- Engineering  
- Hostel  
- Library  

---

## 🧰 Technologies Used
- Python 3  
- Pandas  
- Matplotlib  
- OOP (Object-Oriented Programming)

---

## ✨ Author
**Avijit B**  
B.Tech CSE (AI & ML)  
K.R. Mangalam University

