import streamlit as st
import pandas as pd
import plotly.express as px

from database import get_complaints, update_status
from style import apply_style


def show_dashboard():

    apply_style()

    st.markdown(
        """
        <div style="background:linear-gradient(135deg,#6C63FF,#7C5CFC);
        padding:25px 30px;border-radius:16px;margin-bottom:20px;">
        <h1 style="color:white!important;margin:0;">
        📊 CampusIQ Admin Dashboard
        </h1>
        <p style="color:#F5F3FF!important;margin:6px 0 0;">
        Monitor campus problems, workload and resolution progress.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    complaints = get_complaints()

    if not complaints:
        st.info("No complaints available yet.")
        return

    columns = [
        "Complaint ID", "Name", "Email / Student ID", "Category",
        "Location", "Description", "Priority", "Department",
        "Status", "Created At"
    ]

    df = pd.DataFrame(complaints, columns=columns)

    # ---------------- Filters ----------------

    st.subheader("🔎 Filter Issues")

    c1, c2, c3, c4, c5 = st.columns(5)

    def options(col):
        return ["All"] + sorted(df[col].dropna().unique().tolist())

    with c1:
        category = st.selectbox("Category", options("Category"))
    with c2:
        priority = st.selectbox("Priority", options("Priority"))
    with c3:
        department = st.selectbox("Department", options("Department"))
    with c4:
        status = st.selectbox("Status", options("Status"))
    with c5:
        location = st.selectbox("Location", options("Location"))

    filtered = df.copy()

    filters = {
        "Category": category,
        "Priority": priority,
        "Department": department,
        "Status": status,
        "Location": location
    }

    for column, value in filters.items():
        if value != "All":
            filtered = filtered[filtered[column] == value]

    st.caption(f"Showing {len(filtered)} of {len(df)} issues")
    st.divider()

    # ---------------- KPI ----------------

    st.subheader("📌 Campus Overview")

    total = len(filtered)
    high = filtered["Priority"].isin(["High", "Critical"]).sum()
    pending = (filtered["Status"] == "Pending").sum()
    resolved = (filtered["Status"] == "Resolved").sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📌 Total Issues", total)
    c2.metric("🔴 High Priority", high)
    c3.metric("⏳ Pending", pending)
    c4.metric("✅ Resolved", resolved)

    st.divider()

    # ---------------- Insights ----------------

    st.subheader("💡 CampusIQ Insights")

    if filtered.empty:
        st.info("No issues match the selected filters.")
        return

    most_category = filtered["Category"].value_counts().idxmax()
    category_count = filtered["Category"].value_counts().max()

    most_location = filtered["Location"].value_counts().idxmax()
    location_count = filtered["Location"].value_counts().max()

    most_department = filtered["Department"].value_counts().idxmax()
    department_count = filtered["Department"].value_counts().max()

    unresolved_high = (
        filtered["Priority"].isin(["High", "Critical"])
        & (filtered["Status"] != "Resolved")
    ).sum()

    c1, c2 = st.columns(2)

    with c1:
        st.info(
            f"📂 **Most Reported Category**\n\n"
            f"{most_category} ({category_count} issues)"
        )
        st.info(
            f"📍 **Most Affected Location**\n\n"
            f"{most_location} ({location_count} issues)"
        )

    with c2:
        st.info(
            f"🏢 **Highest Department Workload**\n\n"
            f"{most_department} ({department_count} issues)"
        )

        if unresolved_high:
            st.warning(
                f"🔴 **Attention Required**\n\n"
                f"{unresolved_high} high-priority issue(s) unresolved."
            )
        else:
            st.success(
                "✅ **Attention Required**\n\n"
                "No unresolved high-priority issues."
            )

    st.divider()

    # ---------------- Status Update ----------------

    st.subheader("🔧 Update Issue Status")

    c1, c2, c3 = st.columns([1, 1, 1])

    with c1:
        selected_id = st.selectbox(
            "Complaint ID",
            filtered["Complaint ID"].tolist()
        )

    with c2:
        new_status = st.selectbox(
            "New Status",
            ["Pending", "Assigned", "In Progress", "Resolved"]
        )

    with c3:
        st.write("")
        st.write("")
        if st.button("🔄 Update Status", use_container_width=True):
            update_status(selected_id, new_status)
            st.success(
                f"Complaint #{selected_id} updated to '{new_status}'."
            )
            st.rerun()

    st.divider()

    # ---------------- Charts ----------------

    st.subheader("📈 Campus Analytics")

    def chart_layout(fig):
        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="#1F2937"),
            margin=dict(l=20, r=20, t=55, b=20)
        )
        return fig

    c1, c2 = st.columns(2)

    with c1:
        data = filtered["Category"].value_counts().reset_index()
        data.columns = ["Category", "Count"]

        fig = px.bar(
            data,
            x="Category",
            y="Count",
            title="Issues by Category",
            text="Count"
        )
        fig.update_traces(marker_color="#6C63FF")
        st.plotly_chart(
            chart_layout(fig),
            use_container_width=True
        )

    with c2:
        data = filtered["Priority"].value_counts().reset_index()
        data.columns = ["Priority", "Count"]

        fig = px.pie(
            data,
            names="Priority",
            values="Count",
            title="Priority Distribution"
        )
        st.plotly_chart(
            chart_layout(fig),
            use_container_width=True
        )

    data = filtered["Department"].value_counts().reset_index()
    data.columns = ["Department", "Count"]

    fig = px.bar(
        data,
        x="Department",
        y="Count",
        title="Department Workload",
        text="Count"
    )
    fig.update_traces(marker_color="#7C5CFC")

    st.plotly_chart(
        chart_layout(fig),
        use_container_width=True
    )

    # ---------------- Location Intelligence ----------------

    st.subheader("📍 Location Intelligence")

    locations = sorted(filtered["Location"].dropna().unique())

    selected_location = st.selectbox(
        "Select a Location",
        locations
    )

    location_df = filtered[
        filtered["Location"] == selected_location
    ]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📌 Total Issues", len(location_df))
    c2.metric(
        "📂 Common Category",
        location_df["Category"].mode()[0]
    )

    order = ["Critical", "High", "Medium", "Low"]
    available = [
        x for x in order
        if x in location_df["Priority"].values
    ]

    c3.metric(
        "⚡ Highest Priority",
        available[0] if available else "N/A"
    )

    c4.metric(
        "✅ Resolved",
        (location_df["Status"] == "Resolved").sum()
    )

    data = filtered["Location"].value_counts().head(10).reset_index()
    data.columns = ["Location", "Count"]

    fig = px.bar(
        data,
        x="Location",
        y="Count",
        title="Top Issue Locations",
        text="Count"
    )
    fig.update_traces(marker_color="#6C63FF")

    st.plotly_chart(
        chart_layout(fig),
        use_container_width=True
    )

    # ---------------- Resolution Status ----------------

    st.subheader("📈 Resolution Status")

    data = filtered["Status"].value_counts().reset_index()
    data.columns = ["Status", "Count"]

    fig = px.bar(
        data,
        x="Status",
        y="Count",
        title="Issue Resolution Status",
        text="Count"
    )
    fig.update_traces(marker_color="#6C63FF")

    st.plotly_chart(
        chart_layout(fig),
        use_container_width=True
    )

    # ---------------- Issues Table ----------------

    st.subheader("📋 All Reported Issues")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )