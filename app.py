import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Obesity Analysis", layout="wide")

# Custom CSS to limit multiselect height
st.markdown("""
    <style>
    div[data-baseweb="select"] > div {
        max-height: 200px;
        overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('expanded_years_data.csv')
    return df

# Load the data
df = load_data()

# Initialize session state for selected entities
if 'selected_entities' not in st.session_state:
    st.session_state.selected_entities = sorted(df['entity'].unique())

# Sidebar filters
st.sidebar.header('Filters')

# Entity (Country) selection
entities = sorted(df['entity'].unique())
col1, col2, col3 = st.sidebar.columns([3, 1, 1])

# Clear and Select All buttons
if col2.button('Clear'):
    st.session_state.selected_entities = []
if col3.button('All'):
    st.session_state.selected_entities = entities

selected_entities = col1.multiselect(
    'Select Countries',
    entities,
    default=st.session_state.selected_entities
)
# Update session state
st.session_state.selected_entities = selected_entities

# Year range
min_year = int(df['year'].min())
max_year = int(df['year'].max())
year_range = st.sidebar.slider(
    'Select Year Range',
    min_year, max_year,
    (min_year, max_year)
)

# Color by selection
color_by = st.sidebar.radio(
    'Color by:',
    ['entity', 'year', 'None'],
    index=0  # Default to entity
)

# Filter data
filtered_df = df[
    (df['entity'].isin(selected_entities)) &
    (df['year'].between(year_range[0], year_range[1]))
]

# Main content
st.title('Obesity Analysis Dashboard')

# Create scatter plot
fig = px.scatter(
    filtered_df,
    x='pct_cals_from_carbs',
    y='overweight_or_obese',
    color=None if color_by == 'None' else color_by,
    hover_data=['entity', 'year', 'pct_cals_from_carbs', 'overweight_or_obese'],
    labels={
        'pct_cals_from_carbs': 'Percentage of Calories from Carbohydrates',
        'overweight_or_obese': 'Percentage Overweight or Obese',
        'entity': 'Country',
        'year': 'Year'
    },
    title='Relationship between Carbohydrate Intake and Obesity Rates'
)

# Update layout
fig.update_layout(
    height=600,
    hovermode='closest',
    plot_bgcolor='white'
)

# Display plot
st.plotly_chart(fig, use_container_width=True)

# Display filtered data
st.subheader('Filtered Data')
st.dataframe(filtered_df)
