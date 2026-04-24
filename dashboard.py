import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Face Attendance Dashboard", layout="wide")

st.title("📊 Face Attendance Dashboard")

file_path = "Attendance.csv"

# ========================
# CHECK FILE
# ========================
if not os.path.exists(file_path):
    st.error("❌ Attendance.csv not found")
    st.stop()

# ========================
# LOAD DATA
# ========================
df = pd.read_csv(file_path)

# CLEAN DATA
df["Name"] = df["Name"].str.strip()
df["Status"] = df["Status"].str.strip()

# SORT LATEST FIRST
df = df.sort_values(by=["Date", "Time"], ascending=False)

# ========================
# 🔍 FILTER SECTION
# ========================
st.markdown("## 🔍 Filter Attendance")

col1, col2, col3 = st.columns(3)

with col1:
    status_filter = st.selectbox("Select Status", ["All", "Present", "Mismatch"])

with col2:
    name_filter = st.selectbox(
        "Select Name",
        ["All"] + sorted(df["Name"].unique())
    )

with col3:
    date_filter = st.selectbox(
        "Select Date",
        ["All"] + sorted(df["Date"].unique(), reverse=True)
    )

# ========================
# APPLY FILTERS
# ========================
df_filtered = df.copy()

if status_filter != "All":
    df_filtered = df_filtered[df_filtered["Status"] == status_filter]

if name_filter != "All":
    df_filtered = df_filtered[df_filtered["Name"] == name_filter]

if date_filter != "All":
    df_filtered = df_filtered[df_filtered["Date"] == date_filter]

# ========================
# 🆕 LATEST ENTRY
# ========================
st.markdown("## 🆕 Latest Entry")

latest = df.iloc[0]
st.success(
    f"{latest['Name']} | {latest['Date']} {latest['Time']} | {latest['Status']}"
)

# ========================
# 📋 ATTENDANCE RECORDS
# ========================
st.markdown("## 📋 Attendance Records")

st.dataframe(df_filtered, use_container_width=True)

# ========================
# 📊 COUNTS
# ========================
col1, col2 = st.columns(2)

present_count = df[df["Status"] == "Present"].shape[0]
mismatch_count = df[df["Status"] == "Mismatch"].shape[0]

col1.metric("✅ Present", present_count)
col2.metric("❌ Mismatch", mismatch_count)

# ========================
# 👤 ATTENDANCE BY PERSON
# ========================
st.markdown("## 👤 Attendance by Person")

df_present = df[df["Status"] == "Present"]
person_count = df_present["Name"].value_counts()

st.bar_chart(person_count)

# ========================
# 📊 STATUS DISTRIBUTION
# ========================
st.markdown("## 📊 Status Distribution")

status_count = df["Status"].value_counts()
st.bar_chart(status_count)

# ========================
# ⬇️ DOWNLOAD CSV
# ========================
st.markdown("## ⬇️ Download Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Attendance CSV",
    data=csv,
    file_name="Attendance.csv",
    mime="text/csv"
)