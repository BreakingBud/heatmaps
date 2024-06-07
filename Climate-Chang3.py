import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
data_url = "C:\\Users\\goela\\OneDrive\\Desktop\\New folder\\GlobalLandTemperaturesByMajorCity.csv"  # Update this to your file path
data = pd.read_csv(data_url)

# Filter out NaN values
data = data.dropna(subset=['AverageTemperature'])

# Extract the year and month from the 'dt' column
data['Year'] = pd.to_datetime(data['dt']).dt.year
data['Month'] = pd.to_datetime(data['dt']).dt.month

# Streamlit app
st.title('Temperature Analysis')

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page", ["Global Heatmap", "Country-wise Heatmap", "City-wise Heatmap"])

# Year range selection
year_range = st.sidebar.slider('Select year range', int(data['Year'].min()), int(data['Year'].max()), (2000, 2010))
heatmap_type = st.sidebar.radio('Select heatmap type', ['Yearly', 'Decadal'])

def create_heatmap(data, index, columns, title):
    heatmap_data = data.pivot_table(index=index, columns=columns, values='AverageTemperature', aggfunc='mean')
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='RdBu',  # Change colorscale to RdBu for red to blue color theme
        reversescale=True   # Reverse the colorscale to have high values as red and low values as blue
    ))
    fig.update_layout(
        title=title,
        xaxis_title=columns.capitalize(),
        yaxis_title=index.capitalize()
    )
    return fig

# Visualization
if page == "Global Heatmap":
    st.subheader('Global Temperature Heatmap')
    filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]
    if heatmap_type == 'Yearly':
        fig = create_heatmap(filtered_data, index='Month', columns='Year', title='Global Average Temperature Yearly Heatmap')
    else:
        filtered_data['Decade'] = (filtered_data['Year'] // 10) * 10
        fig = create_heatmap(filtered_data, index='Month', columns='Decade', title='Global Average Temperature Decadal Heatmap')
    st.plotly_chart(fig)
elif page == "Country-wise Heatmap":
    st.subheader('Country-wise Temperature Heatmap')
    countries = data['Country'].unique()
    selected_country = st.sidebar.selectbox('Select a country', countries)
    filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1]) & (data['Country'] == selected_country)]
    if heatmap_type == 'Yearly':
        fig = create_heatmap(filtered_data, index='Month', columns='Year', title=f'{selected_country} Average Temperature Yearly Heatmap')
    else:
        filtered_data['Decade'] = (filtered_data['Year'] // 10) * 10
        fig = create_heatmap(filtered_data, index='Month', columns='Decade', title=f'{selected_country} Average Temperature Decadal Heatmap')
    st.plotly_chart(fig)
elif page == "City-wise Heatmap":
    st.subheader('City-wise Temperature Heatmap')
    countries = data['Country'].unique()
    selected_country = st.sidebar.selectbox('Select a country', countries)
    cities = data[data['Country'] == selected_country]['City'].unique()
    selected_city = st.sidebar.selectbox('Select a city', cities)
    filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1]) & (data['Country'] == selected_country) & (data['City'] == selected_city)]
    if heatmap_type == 'Yearly':
        fig = create_heatmap(filtered_data, index='Month', columns='Year', title=f'{selected_city}, {selected_country} Average Temperature Yearly Heatmap')
    else:
        filtered_data['Decade'] = (filtered_data['Year'] // 10) * 10
        fig = create_heatmap(filtered_data, index='Month', columns='Decade', title=f'{selected_city}, {selected_country} Average Temperature Decadal Heatmap')
    st.plotly_chart(fig)
