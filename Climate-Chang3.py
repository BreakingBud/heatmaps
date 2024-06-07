import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
data_url = "GlobalLandTemperaturesByMajorCity.csv"  # Update this to your file path
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
page = st.sidebar.selectbox("Select a page", ["Global Heatmap", "Country-wise Heatmap", "City-wise Heatmap", "Compare Cities"])

# Year range selection
year_range = st.sidebar.slider('Select year range', int(data['Year'].min()), int(data['Year'].max()), (2000, 2010))
heatmap_type = st.sidebar.radio('Select heatmap type', ['Yearly', 'Decadal'])

# Color palette selection
color_palette = st.sidebar.radio('Select color palette', ['RdBu', 'Viridis'])

def create_heatmap(data, index, columns, title, zmin, zmax, colorscale):
    heatmap_data = data.pivot_table(index=index, columns=columns, values='AverageTemperature', aggfunc='mean')
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale=colorscale,  # Change colorscale to the selected color palette
        reversescale=True if colorscale == 'RdBu' else False,  # Reverse the colorscale only for RdBu
        zmin=zmin,          # Fixed minimum value for the colorscale
        zmax=zmax           # Fixed maximum value for the colorscale
    ))
    fig.update_layout(
        title=title,
        xaxis_title=columns.capitalize(),
        yaxis_title=index.capitalize()
    )
    return fig

# Determine the global min and max temperatures for consistent color scale
global_min_temp = data['AverageTemperature'].min()
global_max_temp = data['AverageTemperature'].max()

# Visualization
if page == "Global Heatmap":
    st.subheader('Global Temperature Heatmap')
    filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]
    if heatmap_type == 'Yearly':
        fig = create_heatmap(filtered_data, index='Month', columns='Year', title='Global Average Temperature Yearly Heatmap', zmin=global_min_temp, zmax=global_max_temp, colorscale=color_palette)
    else:
        filtered_data['Decade'] = (filtered_data['Year'] // 10) * 10
        fig = create_heatmap(filtered_data, index='Month', columns='Decade', title='Global Average Temperature Decadal Heatmap', zmin=global_min_temp, zmax=global_max_temp, colorscale=color_palette)
    st.plotly_chart(fig)
elif page == "Country-wise Heatmap":
    st.subheader('Country-wise Temperature Heatmap')
    countries = data['Country'].unique()
    selected_country = st.sidebar.selectbox('Select a country', countries)
    filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1]) & (data['Country'] == selected_country)]
    if heatmap_type == 'Yearly':
        fig = create_heatmap(filtered_data, index='Month', columns='Year', title=f'{selected_country} Average Temperature Yearly Heatmap', zmin=global_min_temp, zmax=global_max_temp, colorscale=color_palette)
    else:
        filtered_data['Decade'] = (filtered_data['Year'] // 10) * 10
        fig = create_heatmap(filtered_data, index='Month', columns='Decade', title=f'{selected_country} Average Temperature Decadal Heatmap', zmin=global_min_temp, zmax=global_max_temp, colorscale=color_palette)
    st.plotly_chart(fig)
elif page == "City-wise Heatmap":
    st.subheader('City-wise Temperature Heatmap')
    countries = data['Country'].unique()
    selected_country = st.sidebar.selectbox('Select a country', countries)
    cities = data[data['Country'] == selected_country]['City'].unique()
    selected_city = st.sidebar.selectbox('Select a city', cities)
    filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1]) & (data['Country'] == selected_country) & (data['City'] == selected_city)]
    if heatmap_type == 'Yearly':
        fig = create_heatmap(filtered_data, index='Month', columns='Year', title=f'{selected_city}, {selected_country} Average Temperature Yearly Heatmap', zmin=global_min_temp, zmax=global_max_temp, colorscale=color_palette)
    else:
        filtered_data['Decade'] = (filtered_data['Year'] // 10) * 10
        fig = create_heatmap(filtered_data, index='Month', columns='Decade', title=f'{selected_city}, {selected_country} Average Temperature Decadal Heatmap', zmin=global_min_temp, zmax=global_max_temp, colorscale=color_palette)
    st.plotly_chart(fig)
elif page == "Compare Cities":
    st.subheader('Compare Cities Temperature Heatmap')
    countries = data['Country'].unique()
    selected_country_1 = st.sidebar.selectbox('Select the first country', countries, key='country_1')
    cities_1 = data[data['Country'] == selected_country_1]['City'].unique()
    selected_city_1 = st.sidebar.selectbox('Select the first city', cities_1, key='city_1')
    
    selected_country_2 = st.sidebar.selectbox('Select the second country', countries, key='country_2')
    cities_2 = data[data['Country'] == selected_country_2]['City'].unique()
    selected_city_2 = st.sidebar.selectbox('Select the second city', cities_2, key='city_2')

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"Heatmap for {selected_city_1}, {selected_country_1}")
        filtered_data_1 = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1]) & (data['Country'] == selected_country_1) & (data['City'] == selected_city_1)]
        if heatmap_type == 'Yearly':
            fig1 = create_heatmap(filtered_data_1, index='Month', columns='Year', title=f'{selected_city_1}, {selected_country_1} Average Temperature Yearly Heatmap', zmin=global_min_temp, zmax=global_max_temp, colorscale=color_palette)
        else:
            filtered_data_1['Decade'] = (filtered_data_1['Year'] // 10) * 10
            fig1 = create_heatmap(filtered_data_1, index='Month', columns='Decade', title=f'{selected_city_1}, {selected_country_1} Average Temperature Decadal Heatmap', zmin=global_min_temp, zmax=global_max_temp, colorscale=color_palette)
        st.plotly_chart(fig1)

    with col2:
        st.write(f"Heatmap for {selected_city_2}, {selected_country_2}")
        filtered_data_2 = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1]) & (data['Country'] == selected_country_2) & (data['City'] == selected_city_2)]
        if heatmap_type == 'Yearly':
            fig2 = create_heatmap(filtered_data_2, index='Month', columns='Year', title=f'{selected_city_2}, {selected_country_2} Average Temperature Yearly Heatmap', zmin=global_min_temp, zmax=global_max_temp, colorscale=color_palette)
        else:
            filtered_data_2['Decade'] = (filtered_data_2['Year'] // 10) * 10
            fig2 = create_heatmap(filtered_data_2, index='Month', columns='Decade', title=f'{selected_city_2}, {selected_country_2} Average Temperature Decadal Heatmap', zmin=global_min_temp, zmax=global_max_temp, colorscale=color_palette)
        st.plotly_chart(fig2)
