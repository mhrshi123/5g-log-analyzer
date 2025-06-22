import streamlit as st
import re
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="5G Log Analyzer", layout="centered")
st.title("📶 5G Log Analyzer")
st.markdown("Upload a 5G `.log` or `.txt` file to start analysis.")

# File uploader
uploaded_file = st.file_uploader("Choose a log file", type=["log", "txt"])

if uploaded_file is not None:
    # Read and decode lines
    lines = uploaded_file.readlines()
    decoded_lines = [line.decode("utf-8").strip() for line in lines]

    # Preview raw log
    st.subheader("📄 Raw Log Preview")
    st.text_area("Log Contents", "\n".join(decoded_lines[:20]), height=300)
    st.success(f"Loaded {len(decoded_lines)} log lines.")

    # Initialize counters and data storage
    packet_count = 0
    error_count = 0
    warning_count = 0
    timestamps = []
    latencies = []
    log_data = []

    for line in decoded_lines:
        entry = {"timestamp": None, "rtt": None, "type": "Info"}

        match = re.search(r"\[(\d+:\d+:\d+)\].*RTT=(\d+)ms", line)
        if match:
            timestamp = match.group(1)
            rtt = int(match.group(2))
            entry["timestamp"] = timestamp
            entry["rtt"] = rtt
            timestamps.append(timestamp)
            latencies.append(rtt)

        if "Error" in line:
            entry["type"] = "Error"
            error_count += 1
        elif "Warning" in line:
            entry["type"] = "Warning"
            warning_count += 1
        elif "Packet" in line:
            packet_count += 1
            entry["type"] = "Packet"

        if entry["timestamp"] and entry["rtt"] is not None:
            log_data.append(entry)

    # === Metrics ===
    st.subheader("📊 Log Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Packets", packet_count)
    col2.metric("Errors", error_count)
    col3.metric("Warnings", warning_count)

    # === Latency Stats ===
    if latencies:
        st.subheader("📈 Latency Stats")
        st.write(f"Average RTT: {sum(latencies) / len(latencies):.2f} ms")
        st.write(f"Max RTT: {max(latencies)} ms")
        st.write(f"Min RTT: {min(latencies)} ms")

        # === Latency Chart with Spikes Highlighted ===
        st.subheader("📉 Latency Over Time")
        fig, ax = plt.subplots()

        # Highlight RTT spikes in red
        colors = ['red' if rtt >= 100 else 'green' for rtt in latencies]
        ax.scatter(timestamps, latencies, color=colors)
        ax.plot(timestamps, latencies, linestyle='--', color='gray', alpha=0.5)

        ax.set_xlabel("Timestamp")
        ax.set_ylabel("RTT (ms)")
        ax.set_title("Latency Trend (Red = Spike ≥ 100ms)")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.warning("No RTT (latency) data found in this log.")

    # === Data Table + CSV Export ===
    if log_data:
        df = pd.DataFrame(log_data)
        st.subheader("🧾 Parsed Log Table")

        # Highlight spike rows in table
        def highlight_spikes(row):
            if row["rtt"] >= 100:
                return ['background-color: #ffcccc'] * len(row)
            return [''] * len(row)

        st.dataframe(df.style.apply(highlight_spikes, axis=1))

        # CSV export
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name='parsed_log.csv',
            mime='text/csv',
        )
else:
    st.info("Please upload a file to continue.")
