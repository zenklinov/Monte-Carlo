import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# --- App Configuration ---
st.set_page_config(
    page_title="Monte Carlo Data Generator",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- App Title and Description ---
st.title("🎲 Monte Carlo Data Generator")
st.markdown("""
Welcome to the Monte Carlo Data Generator! This tool allows you to generate random data based on various statistical distributions. 
Use the sidebar to configure the generation parameters. The results, including a data table, summary statistics, and a histogram, will be displayed below.
""")

# --- Sidebar for User Inputs ---
with st.sidebar:
    st.header("⚙️ Generation Parameters")

    # --- Distribution Selection ---
    distribution = st.selectbox(
        "Select a Distribution",
        [
            "Normal",
            "Uniform",
            "Exponential",
            "Lognormal",
            "Binomial",
            "Poisson"
        ],
        help="Choose the statistical distribution for data generation."
    )

    # --- Number of Data Points ---
    num_points = st.number_input(
        "Number of Data Points to Generate",
        min_value=10,
        max_value=100000,
        value=1000,
        step=100,
        help="Specify how many random numbers to generate."
    )

    st.markdown("---")
    st.subheader(f"{distribution} Distribution Parameters")

    # --- Conditional Parameter Inputs based on Distribution ---
    params = {}
    if distribution == "Normal":
        st.markdown("<p style='font-size: small;'>Generates data following a bell curve. Defined by its mean (center) and standard deviation (spread).</p>", unsafe_allow_html=True)
        params['loc'] = st.number_input("Mean (μ)", value=0.0, step=0.1, help="The center of the distribution.")
        params['scale'] = st.number_input("Standard Deviation (σ)", value=1.0, min_value=0.01, step=0.1, help="The spread or width of the distribution.")
    
    elif distribution == "Uniform":
        st.markdown("<p style='font-size: small;'>Generates data where every value within a given range is equally likely.</p>", unsafe_allow_html=True)
        params['low'] = st.number_input("Lower Bound (a)", value=0.0, step=0.1, help="The minimum value in the range.")
        params['high'] = st.number_input("Upper Bound (b)", value=1.0, step=0.1, help="The maximum value in the range.")
        if params['low'] >= params['high']:
            st.error("Error: Lower Bound must be less than Upper Bound.")

    elif distribution == "Exponential":
        st.markdown("<p style='font-size: small;'>Often used to model the time between events in a Poisson process. The scale parameter is the inverse of the rate (λ).</p>", unsafe_allow_html=True)
        params['scale'] = st.number_input("Scale (β = 1/λ)", value=1.0, min_value=0.01, help="The inverse of the rate parameter (lambda).")

    elif distribution == "Lognormal":
        st.markdown("<p style='font-size: small;'>A distribution where the logarithm of the variable is normally distributed. Often used for modeling asset prices.</p>", unsafe_allow_html=True)
        params['mean'] = st.number_input("Log Mean (μ)", value=0.0, step=0.1, help="Mean of the underlying normal distribution.")
        params['sigma'] = st.number_input("Log Standard Deviation (σ)", value=1.0, min_value=0.01, step=0.1, help="Standard deviation of the underlying normal distribution.")

    elif distribution == "Binomial":
        st.markdown("<p style='font-size: small;'>Models the number of successes in a fixed number of independent trials, each with the same probability of success.</p>", unsafe_allow_html=True)
        params['n'] = st.number_input("Number of Trials (n)", value=10, min_value=1, step=1, help="The number of independent trials.")
        params['p'] = st.slider("Probability of Success (p)", min_value=0.0, max_value=1.0, value=0.5, step=0.01, help="The probability of success on each trial.")

    elif distribution == "Poisson":
        st.markdown("<p style='font-size: small;'>Models the number of events occurring in a fixed interval of time or space, given a constant mean rate.</p>", unsafe_allow_html=True)
        params['lam'] = st.number_input("Rate (λ)", value=3.0, min_value=0.1, step=0.1, help="The average number of events in an interval.")

    # --- Generate Button ---
    generate_button = st.button("🚀 Generate Data", type="primary", use_container_width=True)


# --- Main Panel for Displaying Results ---
if generate_button:
    # --- Data Generation Logic ---
    try:
        if distribution == "Normal":
            data = np.random.normal(loc=params['loc'], scale=params['scale'], size=num_points)
        elif distribution == "Uniform":
            if params['low'] < params['high']:
                 data = np.random.uniform(low=params['low'], high=params['high'], size=num_points)
            else:
                st.error("Generation failed. Please ensure the Lower Bound is less than the Upper Bound.")
                st.stop()
        elif distribution == "Exponential":
            data = np.random.exponential(scale=params['scale'], size=num_points)
        elif distribution == "Lognormal":
            data = np.random.lognormal(mean=params['mean'], sigma=params['sigma'], size=num_points)
        elif distribution == "Binomial":
            data = np.random.binomial(n=params['n'], p=params['p'], size=num_points)
        elif distribution == "Poisson":
            data = np.random.poisson(lam=params['lam'], size=num_points)

        # Create a pandas DataFrame
        df = pd.DataFrame(data, columns=['Generated Value'])

        st.success(f"Successfully generated {num_points} data points from a {distribution} distribution.")
        
        # --- Display Results in Tabs ---
        tab1, tab2, tab3 = st.tabs(["📊 Histogram", "📈 Summary Statistics", "📋 Raw Data"])

        with tab1:
            # --- Plotting ---
            st.subheader("Distribution Histogram")
            fig = px.histogram(
                df, 
                x='Generated Value', 
                nbins=50, 
                title=f'Histogram of {distribution} Distribution',
                labels={'Generated Value': 'Value'},
                marginal="box" # Adds a box plot to visualize quartiles
            )
            fig.update_layout(
                title_x=0.5,
                bargap=0.1,
                xaxis_title="Value",
                yaxis_title="Frequency"
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            # --- Summary Statistics ---
            st.subheader("Summary Statistics")
            st.dataframe(df.describe(), use_container_width=True)

        with tab3:
            # --- Data Table ---
            st.subheader("Generated Data Table")
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred during data generation: {e}")

else:
    st.info("Adjust the parameters in the sidebar and click 'Generate Data' to begin.")

