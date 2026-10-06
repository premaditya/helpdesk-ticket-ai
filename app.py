import os
import time

import streamlit as st
from dotenv import load_dotenv
from langsmith import Client

from llm_service import helpdesk_chain


# --------------------------------------------------
# Environment & LangSmith
# --------------------------------------------------

load_dotenv()

client = Client()

LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI IT Helpdesk",
    page_icon="🛠️",
    layout="wide"
)


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            160deg,
            #060A14 0%,
            #0D1830 40%,
            #142645 75%,
            #0A1120 100%
        );
        color: white;
    }

    .main {
        padding-top: 2rem;
    }

    .hero {
        text-align: center;
        padding: 35px 20px;
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 46px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #b8c2d9;
        max-width: 750px;
        margin: auto;
        line-height: 1.6;
    }

    .card {
        background: rgba(16, 27, 48, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
    }

    .card h3 {
        color: #f5c76b;
        margin-bottom: 15px;
    }

    .result-value {
        color: #ffffff;
        font-size: 17px;
        line-height: 1.6;
    }

    .category-value {
        color: #f5c76b;
        font-size: 22px;
        font-weight: 700;
    }

    .priority-value {
        color: #ffffff;
        font-size: 22px;
        font-weight: 700;
    }

    .action-box {
        background: rgba(245, 199, 107, 0.08);
        border-left: 4px solid #f5c76b;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
        color: #ffffff;
        line-height: 1.6;
    }

    .ticket-box {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 15px;
        color: #d7deed;
        line-height: 1.6;
    }

    .metric-card {
        background: rgba(16, 27, 48, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px;
        text-align: center;
    }

    .metric-title {
        color: #aeb9cf;
        font-size: 14px;
        margin-bottom: 5px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 22px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Hero Section
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🛠️ AI IT Helpdesk</div>
        <div class="hero-subtitle">
            Analyze IT support tickets using AI and automatically
            identify the category, priority, issue summary, and
            recommended next action.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Ticket Input
# --------------------------------------------------

st.markdown(
    """
    <div class="card">
        <h3>🎫 Support Ticket</h3>
    </div>
    """,
    unsafe_allow_html=True
)

ticket = st.text_area(
    "Enter support ticket",
    placeholder=(
        "Example: My laptop suddenly shuts down whenever "
        "I connect the external monitor."
    ),
    height=160,
    label_visibility="collapsed"
)


# --------------------------------------------------
# Analyze Button
# --------------------------------------------------

analyze_button = st.button(
    "🔍 Analyze Ticket",
    use_container_width=True
)


# --------------------------------------------------
# Analysis
# --------------------------------------------------

if analyze_button:

    if not ticket.strip():

        st.warning(
            "⚠️ Please enter a support ticket before analyzing."
        )

    else:

        try:

            # --------------------------------------------------
            # Start Application Timer
            # --------------------------------------------------

            start_time = time.perf_counter()

            with st.spinner("🤖 Analyzing support ticket..."):

                result = helpdesk_chain.invoke(
                    {
                        "ticket": ticket
                    },
                    config={
                        "run_name": "Helpdesk Ticket Request"
                    }
                )

            end_time = time.perf_counter()

            app_latency = end_time - start_time


            # --------------------------------------------------
            # Submitted Ticket
            # --------------------------------------------------

            st.markdown(
                f"""
                <div class="card">
                    <h3>📄 Submitted Ticket</h3>
                    <div class="ticket-box">
                        {ticket}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


            # --------------------------------------------------
            # Category & Priority
            # --------------------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    f"""
                    <div class="card">
                        <h3>🏷️ Category</h3>
                        <div class="category-value">
                            {result.category}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                st.markdown(
                    f"""
                    <div class="card">
                        <h3>🚨 Priority</h3>
                        <div class="priority-value">
                            {result.priority}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # --------------------------------------------------
            # Summary
            # --------------------------------------------------

            st.markdown(
                f"""
                <div class="card">
                    <h3>📝 Summary</h3>
                    <div class="result-value">
                        {result.summary}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


            # --------------------------------------------------
            # Suggested Action
            # --------------------------------------------------

            st.markdown(
                f"""
                <div class="card">
                    <h3>💡 Suggested Action</h3>
                    <div class="action-box">
                        {result.suggested_action}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


            # --------------------------------------------------
            # Retrieve LangSmith Trace
            # --------------------------------------------------

            try:

                # Give LangSmith a moment to process the trace
                time.sleep(2)

                runs = list(
                    client.list_runs(
                        project_name=LANGSMITH_PROJECT,
                        filter='eq(name, "Helpdesk Ticket Request")',
                        limit=1
                    )
                )

                if runs:

                    root_run = runs[0]

                    trace = client.read_run(
                        root_run.id,
                        load_child_runs=True
                    )

                    llm_run = None

                    for child in trace.child_runs:

                        if child.run_type == "llm":

                            llm_run = child
                            break


                    # --------------------------------------------------
                    # Request Metrics
                    # --------------------------------------------------

                    st.markdown(
                        """
                        <div class="card">
                            <h3>📊 Request Metrics</h3>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    metric1, metric2, metric3, metric4 = st.columns(4)


                    # --------------------------------------------------
                    # App Latency
                    # --------------------------------------------------

                    with metric1:

                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-title">
                                    App Latency
                                </div>
                                <div class="metric-value">
                                    {app_latency:.2f}s
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    if llm_run:

                        # --------------------------------------------------
                        # Input Tokens
                        # --------------------------------------------------

                        with metric2:

                            st.markdown(
                                f"""
                                <div class="metric-card">
                                    <div class="metric-title">
                                        Input Tokens
                                    </div>
                                    <div class="metric-value">
                                        {llm_run.prompt_tokens}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )


                        # --------------------------------------------------
                        # Output Tokens
                        # --------------------------------------------------

                        with metric3:

                            st.markdown(
                                f"""
                                <div class="metric-card">
                                    <div class="metric-title">
                                        Output Tokens
                                    </div>
                                    <div class="metric-value">
                                        {llm_run.completion_tokens}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )


                        # --------------------------------------------------
                        # Total Tokens
                        # --------------------------------------------------

                        with metric4:

                            st.markdown(
                                f"""
                                <div class="metric-card">
                                    <div class="metric-title">
                                        Total Tokens
                                    </div>
                                    <div class="metric-value">
                                        {llm_run.total_tokens}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )


                        # --------------------------------------------------
                        # Cost & LLM Latency
                        # --------------------------------------------------

                        notes = []


                        if llm_run.total_cost is not None:

                            notes.append(
                                f"💰 LangSmith estimated cost: "
                                f"${float(llm_run.total_cost):.6f}"
                            )


                        if (
                            llm_run.start_time
                            and llm_run.end_time
                        ):

                            llm_latency = (
                                llm_run.end_time
                                - llm_run.start_time
                            ).total_seconds()

                            notes.append(
                                f"⚡ LLM latency: "
                                f"{llm_latency:.2f}s"
                            )


                        for note in notes:

                            st.info(note)


                    else:

                        st.info(
                            "LangSmith trace found, but the "
                            "LLM run metrics are not available yet."
                        )

                else:

                    st.info(
                        "LangSmith trace is still being processed."
                    )


            except Exception as e:

                st.warning(
                    "The ticket was analyzed successfully, "
                    "but LangSmith metrics could not be retrieved."
                )

                st.caption(
                    f"LangSmith: {e}"
                )


        except Exception as e:

            st.error(
                f"❌ An error occurred while analyzing "
                f"the ticket: {e}"
            )