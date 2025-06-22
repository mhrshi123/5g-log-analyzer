# 📶 5G Log Analyzer

An interactive web app built with **Streamlit** to analyze and visualize 5G log files (`.log` or `.txt`). Easily detect packet latency spikes, parse error/warning patterns, and export structured results as a CSV.

---

## 🚀 Live Demo

👉 [Try it on Streamlit Cloud](https://5g-log-analyzer.streamlit.app/)

---

## 📂 Features

- ✅ Upload `.log` or `.txt` files
- ✅ Extract timestamp and RTT (Round Trip Time)
- ✅ Detect RTT spikes (≥ 100ms)
- ✅ Count packets, warnings, and errors
- ✅ Plot latency trends with spikes highlighted in red
- ✅ Export structured log data as CSV
- ✅ Highlight latency spikes in the table view

---

## 🖥️ Sample Log Format

[10:00:01] Packet sent from Node A to Node B. RTT=18ms
[10:00:02] Packet received at Node B. RTT=20ms
[10:00:05] Warning: Latency spike. RTT=85ms
[10:00:08] Error: Timeout occurred. Code=408


---

## 🔧 Technologies Used

- Python
- Streamlit
- Matplotlib
- Pandas
- Regex

---

## 📦 Install & Run Locally

```bash
git clone https://github.com/mhrshi123/5g-log-analyzer.git
cd 5g-log-analyzer
pip install -r requirements.txt
streamlit run app.py
```


