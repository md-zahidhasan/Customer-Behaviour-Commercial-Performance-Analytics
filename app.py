import ast
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Customer Behaviour & Commercial Performance Intelligence",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
.metric-card {padding: 0.6rem 0;}
.small-note {color:#6b7280; font-size:0.85rem;}
</style>
""", unsafe_allow_html=True)

DATA_DIR = Path(__file__).resolve().parent

@st.cache_data(show_spinner="Loading dashboard data...")
def load_data(data_dir):
    master = pd.read_csv(data_dir / "customer_master_full1.csv")
    master["became_member_on"] = pd.to_datetime(master["became_member_on"], errors="coerce")
    master["age"] = pd.to_numeric(master["age"], errors="coerce")
    master["income"] = pd.to_numeric(master["income"], errors="coerce")
    offers = pd.read_csv(data_dir / "offers.csv")
    offers["channels_list"] = offers["channels"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else (x or [])
    )
    events = pd.read_csv(data_dir / "events_clean.csv.gz", compression="gzip")
    events["time"] = pd.to_numeric(events["time"], errors="coerce")
    events["amount"] = pd.to_numeric(events["amount"], errors="coerce")
    events["reward"] = pd.to_numeric(events["reward"], errors="coerce")
    return master, offers, events

try:
    master, offers, events = load_data(DATA_DIR)
except Exception as e:
    st.error(f"Could not load dashboard data: {e}")
    st.stop()

# ---------- Helpers ----------
def money(x):
    return f"${x:,.2f}"

def pct(x):
    return f"{x * 100:.1f}%"

def safe_div(a, b):
    return a / b if b else np.nan

# ---------- Sidebar ----------
st.sidebar.title("Customer Analytics")
st.sidebar.caption("Interactive customer, offer and commercial performance analytics")

pages = [
    "Executive Overview",
    "Sales & Transactions",
    "Customer Analytics",
    "Offer Performance",
    "Customer Journey",
    "Data Explorer",
]
page = st.sidebar.radio("Dashboard section", pages)

st.sidebar.divider()
st.sidebar.subheader("Global Filters")

genders = sorted(master["gender"].dropna().unique().tolist())
gender_filter = st.sidebar.multiselect("Gender", genders, default=genders)

age_min = int(np.nanmin(master["age"])) if master["age"].notna().any() else 18
age_max = int(np.nanmax(master["age"])) if master["age"].notna().any() else 80
age_range = st.sidebar.slider("Age", age_min, age_max, (age_min, age_max))

income_valid = master["income"].dropna()
inc_min = float(income_valid.min()) if len(income_valid) else 0
inc_max = float(income_valid.max()) if len(income_valid) else 1
income_range = st.sidebar.slider(
    "Annual income ($)",
    min_value=float(inc_min),
    max_value=float(inc_max),
    value=(float(inc_min), float(inc_max)),
    step=1000.0,
)

member_min = master["became_member_on"].min().date()
member_max = master["became_member_on"].max().date()
member_range = st.sidebar.date_input(
    "Membership date",
    value=(member_min, member_max),
    min_value=member_min,
    max_value=member_max,
)

offer_type_filter = st.sidebar.multiselect(
    "Offer types received",
    ["bogo", "discount", "informational"],
    default=["bogo", "discount", "informational"],
)

# Apply filters
filtered = master[
    master["gender"].isin(gender_filter)
    & master["age"].fillna(-1).between(age_range[0], age_range[1])
    & master["income"].fillna(-1).between(income_range[0], income_range[1])
    & master["became_member_on"].dt.date.between(member_range[0], member_range[1])
].copy()

selected_offer_cols = {
    "bogo": "bogo_received",
    "discount": "discount_received",
    "informational": "informational_received",
}
if offer_type_filter:
    mask = filtered[[selected_offer_cols[x] for x in offer_type_filter]].sum(axis=1) > 0
    filtered = filtered[mask]
else:
    filtered = filtered.iloc[0:0]

st.sidebar.caption(f"{len(filtered):,} customers after filters")

# ---------- Header ----------
st.title("Customer Behaviour & Commercial Performance Intelligence Dashboard")
st.caption(
    "Interactive visualization of customer demographics, transactions, "
    "offer engagement and campaign events."
)

# ---------- Executive Overview ----------
if page == "Executive Overview":
    total_customers = len(filtered)
    transactions = filtered["transactions_count"].sum()
    revenue = filtered["total_amount"].sum()
    offers_received = filtered["offers_received"].sum()
    offers_completed = filtered["offers_completed"].sum()
    avg_order = safe_div(revenue, transactions)
    view_rate = safe_div(filtered["offers_viewed"].sum(), offers_received)
    completion_rate = safe_div(offers_completed, offers_received)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Customers", f"{total_customers:,}")
    c2.metric("Transactions", f"{transactions:,.0f}")
    c3.metric("Revenue", money(revenue))
    c4.metric("Avg transaction", money(avg_order) if pd.notna(avg_order) else "N/A")
    c5.metric("Offer view rate", pct(view_rate) if pd.notna(view_rate) else "N/A")
    c6.metric("Offer completion", pct(completion_rate) if pd.notna(completion_rate) else "N/A")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        gender = filtered["gender"].value_counts().reset_index()
        gender.columns = ["gender", "customers"]
        fig = px.bar(gender, x="gender", y="customers", title="Customers by gender")
        fig.update_layout(height=360)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        age_data = filtered["age"].dropna()
        fig = px.histogram(age_data, x="age", nbins=20, title="Age distribution")
        fig.update_layout(height=360)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        member = (
            filtered.assign(member_year=filtered["became_member_on"].dt.year)
            .groupby("member_year")
            .size()
            .reset_index(name="customers")
        )
        fig = px.line(member, x="member_year", y="customers", markers=True,
                      title="Customers by membership year")
        fig.update_layout(height=360)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        offer_mix = pd.DataFrame({
            "offer_type": ["BOGO", "Discount", "Informational"],
            "received": [
                filtered["bogo_received"].sum(),
                filtered["discount_received"].sum(),
                filtered["informational_received"].sum(),
            ],
        })
        fig = px.bar(offer_mix, x="offer_type", y="received",
                     title="Offers received by type")
        fig.update_layout(height=360)
        st.plotly_chart(fig, use_container_width=True)

# ---------- Sales ----------
elif page == "Sales & Transactions":
    c1, c2, c3 = st.columns(3)
    c1.metric("Revenue", money(filtered["total_amount"].sum()))
    c2.metric("Transactions", f"{filtered['transactions_count'].sum():,.0f}")
    c3.metric(
        "Average transaction value",
        money(filtered["total_amount"].sum() / filtered["transactions_count"].sum())
        if filtered["transactions_count"].sum() else "N/A",
    )

    # Event-level transaction trend, filtered to customers
    fe = events[events["customer_id"].isin(filtered["customer_id"])].copy()
    tx = fe[fe["event"] == "transaction"].copy()
    tx["day"] = tx["time"] // 24

    daily = tx.groupby("day").agg(
        revenue=("amount", "sum"),
        transactions=("customer_id", "size")
    ).reset_index()

    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(daily, x="day", y="revenue", markers=True,
                      title="Daily transaction revenue")
        fig.update_layout(height=380, yaxis_title="Revenue ($)", xaxis_title="Campaign day")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(daily, x="day", y="transactions",
                     title="Daily transaction count")
        fig.update_layout(height=380, xaxis_title="Campaign day")
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        spend_bins = pd.cut(
            filtered["total_amount"],
            bins=[-0.01, 25, 50, 100, 200, np.inf],
            labels=["$0–25", "$25–50", "$50–100", "$100–200", "$200+"],
        )
        spend = spend_bins.value_counts().sort_index().reset_index()
        spend.columns = ["spend_band", "customers"]
        fig = px.bar(spend, x="spend_band", y="customers",
                     title="Customers by total spend")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(filtered, x="avg_transaction_value", nbins=30,
                           title="Average transaction value distribution")
        fig.update_layout(xaxis_title="Average transaction value ($)")
        st.plotly_chart(fig, use_container_width=True)

# ---------- Customer ----------
elif page == "Customer Analytics":
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Customers", f"{len(filtered):,}")
    c2.metric("Avg income", money(filtered["income"].mean()) if filtered["income"].notna().any() else "N/A")
    c3.metric("Avg spend", money(filtered["total_amount"].mean()))
    c4.metric("Avg transactions", f"{filtered['transactions_count'].mean():.2f}")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.scatter(
            filtered.dropna(subset=["income", "total_amount"]),
            x="income", y="total_amount",
            size="transactions_count",
            color="gender",
            hover_data=["age", "offers_received", "completion_rate"],
            title="Income vs total spend",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(
            filtered.dropna(subset=["age", "total_amount"]),
            x="age", y="total_amount",
            size="transactions_count",
            color="gender",
            hover_data=["income", "offers_received", "completion_rate"],
            title="Age vs total spend",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top customers by spend")
    top = filtered.nlargest(20, "total_amount")[
        ["customer_id", "gender", "age", "income", "transactions_count",
         "total_amount", "offers_received", "offers_completed", "completion_rate"]
    ].copy()
    top["completion_rate"] = top["completion_rate"].map(lambda x: f"{x:.1%}" if pd.notna(x) else "N/A")
    st.dataframe(top, use_container_width=True, hide_index=True)

# ---------- Offer Performance ----------
elif page == "Offer Performance":
    # Build offer funnel directly from event data to preserve event-level logic
    fe = events[events["customer_id"].isin(filtered["customer_id"])].copy()
    offer_events = fe[fe["event"].isin(
        ["offer received", "offer viewed", "offer completed"]
    )].copy()

    offer_pivot = offer_events.pivot_table(
        index=["customer_id", "offer_id"],
        columns="event",
        values="time",
        aggfunc="min",
    ).reset_index()
    offer_pivot.columns.name = None
    offer_pivot = offer_pivot.rename(columns={
        "offer received": "received_time",
        "offer viewed": "viewed_time",
        "offer completed": "completed_time",
    })
    for c in ["received_time", "viewed_time", "completed_time"]:
        if c not in offer_pivot:
            offer_pivot[c] = np.nan

    offer_pivot = offer_pivot.merge(
        offers[["offer_id", "offer_type", "difficulty", "reward", "duration"]],
        on="offer_id", how="left"
    )

    summary = offer_pivot.groupby("offer_type").agg(
        received=("received_time", "count"),
        viewed=("viewed_time", "count"),
        completed=("completed_time", "count"),
        avg_view_delay=("viewed_time", lambda s: np.nan),
        avg_completion_delay=("completed_time", lambda s: np.nan),
    ).reset_index()

    # Calculate delays row-by-row first
    offer_pivot["view_delay"] = offer_pivot["viewed_time"] - offer_pivot["received_time"]
    offer_pivot["completion_delay"] = offer_pivot["completed_time"] - offer_pivot["received_time"]

    delay_summary = offer_pivot.groupby("offer_type").agg(
        avg_view_delay=("view_delay", "mean"),
        avg_completion_delay=("completion_delay", "mean"),
    ).reset_index()

    summary = summary.drop(columns=["avg_view_delay", "avg_completion_delay"]).merge(
        delay_summary, on="offer_type", how="left"
    )
    summary["view_rate"] = summary["viewed"] / summary["received"]
    summary["completion_rate"] = summary["completed"] / summary["received"]

    st.subheader("Offer funnel by type")
    display_summary = summary.copy()
    display_summary["view_rate"] = display_summary["view_rate"].map(lambda x: f"{x:.1%}")
    display_summary["completion_rate"] = display_summary["completion_rate"].map(lambda x: f"{x:.1%}")
    st.dataframe(display_summary, use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        long_rates = summary.melt(
            id_vars="offer_type",
            value_vars=["view_rate", "completion_rate"],
            var_name="metric", value_name="rate"
        )
        long_rates["metric"] = long_rates["metric"].map({
            "view_rate": "View rate",
            "completion_rate": "Completion rate"
        })
        fig = px.bar(long_rates, x="offer_type", y="rate", color="metric",
                     barmode="group", title="View and completion rates")
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        offer_duration = offers.groupby("offer_type", as_index=False)["duration"].mean()
        fig = px.bar(offer_duration, x="offer_type", y="duration",
                     title="Average offer duration by type")
        fig.update_yaxes(title="Days")
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        channel_rows = []
        for _, r in offers.iterrows():
            for ch in r["channels_list"]:
                channel_rows.append({"offer_type": r["offer_type"], "channel": ch})
        channels = pd.DataFrame(channel_rows)
        channel_counts = channels.groupby(["offer_type", "channel"]).size().reset_index(name="offers")
        fig = px.bar(channel_counts, x="offer_type", y="offers", color="channel",
                     barmode="group", title="Offer channels by type")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        rewards = offers.groupby("reward").size().reset_index(name="offer_count")
        fig = px.bar(rewards, x="reward", y="offer_count",
                     title="Reward value frequency")
        fig.update_xaxes(title="Reward ($)")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("View and completion delay")
    delay_long = offer_pivot.melt(
        id_vars="offer_type",
        value_vars=["view_delay", "completion_delay"],
        var_name="delay_type",
        value_name="hours"
    ).dropna()
    delay_long["delay_type"] = delay_long["delay_type"].map({
        "view_delay": "View delay",
        "completion_delay": "Completion delay",
    })
    fig = px.histogram(
        delay_long, x="hours", color="delay_type", facet_row="offer_type",
        nbins=30, barmode="overlay", opacity=0.65,
        title="Offer engagement delay distributions"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------- Journey ----------
elif page == "Customer Journey":
    fe = events[events["customer_id"].isin(filtered["customer_id"])].copy()
    daily = (
        fe.assign(day=fe["time"] // 24)
        .groupby(["day", "event"])
        .size()
        .reset_index(name="count")
    )

    fig = px.line(
        daily, x="day", y="count", color="event", markers=True,
        title="Customer events per campaign day"
    )
    fig.update_layout(xaxis_title="Campaign day", yaxis_title="Events")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Event mix")
    event_mix = fe["event"].value_counts().reset_index()
    event_mix.columns = ["event", "count"]
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(event_mix, x="event", y="count", title="Event volume")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.pie(event_mix, names="event", values="count",
                     title="Event share")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Offer journey")
    offer_events = fe[fe["event"].isin(
        ["offer received", "offer viewed", "offer completed"]
    )]
    funnel_counts = pd.DataFrame({
        "stage": ["Offer received", "Offer viewed", "Offer completed"],
        "count": [
            (offer_events["event"] == "offer received").sum(),
            (offer_events["event"] == "offer viewed").sum(),
            (offer_events["event"] == "offer completed").sum(),
        ],
    })
    fig = px.funnel(funnel_counts, y="stage", x="count", title="Offer funnel")
    st.plotly_chart(fig, use_container_width=True)

# ---------- Data Explorer ----------
elif page == "Data Explorer":
    st.subheader("Customer master data")
    st.caption("The table below is generated from the supplied database using the supplied notebook's cleaning and feature-engineering logic.")

    search = st.text_input("Search customer ID", "")
    view_df = filtered.copy()
    if search:
        view_df = view_df[view_df["customer_id"].str.contains(search, case=False, na=False)]

    st.dataframe(view_df, use_container_width=True, hide_index=True)

    csv_bytes = view_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered customer data",
        data=csv_bytes,
        file_name="filtered_customer_master.csv",
        mime="text/csv",
    )

    st.subheader("Offer reference table")
    st.dataframe(offers.drop(columns=["channels_list"]), use_container_width=True, hide_index=True)

    offer_csv = offers.drop(columns=["channels_list"]).to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download offer reference",
        data=offer_csv,
        file_name="offers.csv",
        mime="text/csv",
    )

st.divider()
st.caption("Source: supplied Coffee Rewards dataset and analysis notebook. Metrics follow the supplied cleaning and feature-engineering approach.")
