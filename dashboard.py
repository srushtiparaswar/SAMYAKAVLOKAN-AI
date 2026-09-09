import streamlit as st
import sqlite3
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="SAMYAKAVLOKAN AI",
    page_icon="🛡️",
    layout="wide"
)

# Auto Refresh Every 3 Seconds
st_autorefresh(interval=3000, key="refresh")

st.title("🛡️ SAMYAKAVLOKAN AI")
st.caption("Women Safety Surveillance System")

# DATABASE CONNECTION
conn = sqlite3.connect("samyakavlokan.db")

df = pd.read_sql_query(
    "SELECT * FROM events",
    conn
)

live_data = pd.read_sql_query(
    "SELECT * FROM live_stats ORDER BY id DESC LIMIT 1",
    conn
)

# DEFAULT VALUES
person_count = 0
object_count = 0

if not live_data.empty:
    person_count = int(live_data.iloc[0]["person_count"])
    object_count = int(live_data.iloc[0]["object_count"])

total_events = len(df)

# =========================
# TOP METRICS
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📋 Total Events", total_events)

with col2:
    st.metric("👤 Person Count", person_count)

with col3:
    st.metric("📦 Object Count", object_count)

with col4:
    st.metric("🚨 Alerts", total_events)

st.markdown("---")

# =========================
# ALERT STATUS
# =========================

if total_events > 0:
    st.error("🚨 ALERT SYSTEM ACTIVE")
else:
    st.success("✅ SYSTEM NORMAL")

st.markdown("---")

# =========================
# LATEST ALERT
# =========================

st.subheader("🚨 Latest Alert")

if not df.empty:

    latest = df.iloc[-1]

    st.info(
        f"""
Event Type: {latest['event_type']}

Time: {latest['timestamp']}

Status: {latest['alert_status']}
"""
    )

else:
    st.info("No Alerts Yet")

st.markdown("---")

# =========================
# EVENT ANALYTICS
# =========================

st.subheader("📈 Event Analytics")

if not df.empty:
    event_counts = df["event_type"].value_counts()
    st.bar_chart(event_counts)

st.markdown("---")

# =========================
# LIVE CAMERA
# =========================

st.subheader("📹 Live Camera Feed")
st.info("Camera Feed Running In OpenCV Window")

st.markdown("---")

# =========================
# EVENT TYPE SUMMARY
# =========================

st.subheader("📅 Event Type Summary")

if not df.empty:

    summary = (
        df["event_type"]
        .value_counts()
        .reset_index()
    )

    summary.columns = [
        "Event Type",
        "Count"
    ]

    st.dataframe(
        summary,
        use_container_width=True
    )

st.markdown("---")

# =========================
# DAILY ALERT TREND
# =========================

st.subheader("📈 Daily Alert Trend")

if not df.empty:

    df["date"] = pd.to_datetime(
        df["timestamp"]
    ).dt.date

    daily_trend = (
        df.groupby("date")
        .size()
        .reset_index(name="alerts")
    )

    st.line_chart(
        daily_trend.set_index("date")
    )

st.markdown("---")

# =========================
# EVENT HISTORY
# =========================

st.subheader("📊 Event History")

st.dataframe(
    df,
    use_container_width=True
)

conn.close()