import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from folium.plugins import FastMarkerCluster

st.markdown("<h1 style='text-align: center;'>Zomato Dashboard</h1>", unsafe_allow_html=True)

path= 'updated_zomato.csv'
df= pd.read_csv(path)
df.set_index('Unnamed: 0',inplace=True)

page = st.sidebar.selectbox(
    "Go to",
    ("Insights", "Geographical Analysis")
)

if page == 'Insights':

    cities = ['All'] + list(df['City'].unique())
    selected_option = st.selectbox("Select the city", cities)
    st.write(selected_option)

    if selected_option == 'All':
        data = df
    else:
        data = df[df['City'] == selected_option]
        
    df_cat= data.select_dtypes(include=['object'])
    df_num = data.select_dtypes(include=[np.number])
    col = st.columns((7, 4), gap='small')

    with col[0]:

        cuisines_values = df_cat['Cuisines'].value_counts().values
        cuisines_index = df_cat['Cuisines'].value_counts().index

        fig = go.Figure(data=[go.Pie(labels=cuisines_index[:5], 
                             values=cuisines_values[:5], 
                             hoverinfo='label+percent', 
                             textinfo='percent',
                             textfont_size=15, 
                             showlegend=True)])
        fig.update_layout(title_text='Top 5 Cuisines Ordered',
                          title_x=0.1,
                          title_y=0.8,
                          legend=dict(
                            x=1.1,
                            y=0.5,
                            traceorder='normal'),
                            width=500,
                            height=400)
        st.plotly_chart(fig)

        
    costlyrest = data.groupby(['Restaurant Name'])['Average Cost for two'].mean().reset_index()
    costlyrest = costlyrest.sort_values(by='Average Cost for two', ascending=False).head(10)

    fig = go.Figure(data=[
    go.Bar(
    x=costlyrest['Restaurant Name'],
    y=costlyrest['Average Cost for two'],
    marker=dict(color='blue')
    )
    ])

    fig.update_layout(
        title='Top 10 High Priced Restaurants',
        title_x=0.3,
        title_font=dict(size=24),
        xaxis_title='Restaurant Name',
        yaxis_title='Average Cost for Two',
        xaxis=dict(tickangle=-45), 
        width=2000)

    st.plotly_chart(fig)

    votes = data.groupby("Restaurant Name")["Votes"].sum().reset_index()
    votes = votes.sort_values(by="Votes", ascending=False).head(10)

    fig = go.Figure(data=[
    go.Bar(
        x=votes['Votes'],
        y=votes['Restaurant Name'],
        orientation='h',
        marker=dict(color='blue')
    )
    ])

    fig.update_layout(
    title='TOP 10 RESTAURANTS BASED ON VOTES',
    title_font=dict(size=24),
    xaxis_title='Votes',
    yaxis_title='Restaurant Name',
    yaxis=dict(autorange='reversed'),
    xaxis=dict(tickangle=-45)
    )

    st.plotly_chart(fig)

    votes_loc = data.groupby("Locality")["Votes"].sum().reset_index()
    votes_loc = votes_loc.sort_values(by="Votes", ascending=False).head(5)

    fig = go.Figure(data=[
    go.Bar(
        x=votes_loc['Votes'],
        y=votes_loc['Locality'],
        orientation='h',
        marker=dict(color='blue')
    )
    ])

    fig.update_layout(
    title='TOP 5 Localities BASED ON VOTES',
    title_font=dict(size=24),
    xaxis_title='Votes',
    yaxis_title='Locality',
    yaxis=dict(autorange='reversed'),
    xaxis=dict(tickangle=30)
    )

    st.plotly_chart(fig)

elif page == 'Geographical Analysis':

    cuisines = ['All'] + list(df['Cuisines'].unique())
    selected_option = st.selectbox("Select the cuisine", cuisines)
    st.write(selected_option)

    if selected_option == 'All':
        data = df
    else:
        data = df[df['Cuisines'] == selected_option]

    map = folium.Map(location=[28.4595, 77.4565], zoom_start=9.5)

    marker_data = list(zip(data['Latitude'], data['Longitude'], data['Restaurant Name']))

    FastMarkerCluster(
    data=marker_data,
    callback='''function (row) {
                    var marker = L.marker(new L.LatLng(row[0], row[1]));
                    marker.bindPopup(row[2]);
                    return marker;
                };'''
    ).add_to(map)

    st.markdown('#### Restaurant Locations')
    st_folium(map, width=1000)
        
        