from typing import final

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from streamlit import header

import preprocess,helper

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocess.preprocessor(df,region_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image('olympic.jpeg')
user_menu = st.sidebar.radio(
    'select an option',
    ('medall telly','overall analysis','country wise analysis','athlete wise analysis')
)

# st.dataframe(df)

if user_menu =='medall telly':

    st.sidebar.header('medal_tally')

    year,country = helper.country_year_list(df) # calling dusri file helper

    selected_year = st.sidebar.selectbox('select Year',year)
    selected_country = st.sidebar.selectbox('select country', country)


    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)# calling fetch_medal_tally function from helper

    if selected_year =='All' and selected_country == 'All':
        st.title('All Medal Tally')

    if selected_year != 'All' and selected_country == 'All':
        st.title(f'Medal Tally of {str(selected_year)} Olymics')

    if selected_year == 'All' and selected_country != 'All':
        st.title(f'{selected_country} All performance Olymics')

    if selected_year != 'All' and selected_country != 'All':
        st.title(f'{selected_country} performance {selected_year} Olymics')

    st.table(medal_tally)

# # OverAll ananlysis
# - No. of edition
# - No. of cities
# - No. of events/sports
# - No. of Athletes
# - participating nations

if user_menu == 'overall analysis':

    edition = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    Athletes = df['Name'].unique().shape[0]
    Nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Edition")
        st.title(edition)

    with col2:
        st.header("Hosts")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Nations")
        st.title(Nations)

    with col3:
        st.header("Athletes")
        st.title(Athletes)

    nation_over_time = helper.data_over_time(df,'region')
    fig = px.line(nation_over_time, x='Year', y='region')
    st.title("participating nations over the years")
    st.plotly_chart(fig)

    Even_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(Even_over_time, x='Year', y='Event')
    st.title("participating Event over the years")
    st.plotly_chart(fig)

    Athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(Athletes_over_time, x='Year', y='Name')
    st.title("participating Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)


    st.title('most successful athletes')

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('select sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'country wise analysis':

    st.sidebar.title('country wise analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('select country',country_list)

    country_df = helper.yearwise_medal_tally(df , selected_country)
    fig= px.line(country_df,x='Year',y='Medal')
    st.title(selected_country+'medal tally over the years')
    st.plotly_chart(fig)




    st.title(selected_country + 'even tally over the years')
    pt = helper.Country_even_heatmap(df,selected_country)

    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)


    st.title(selected_country+'most successful athletes')
    top10_df = helper.most_successful_country(df,selected_country)
    st.table(top10_df)


if user_menu == 'athlete wise analysis':
    st.title('Kde plot Age vs Medals')
    a_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = a_df['Age'].dropna()
    x2 = a_df[a_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = a_df[a_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = a_df[a_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['All', 'Gold medalist', 'Silver medalist', 'Bronze medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=700)
    st.plotly_chart(fig)



    st.title('male vs female comparison')
    final = helper.men_women_comparison(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=700, title_text='Male vs Female Comparison')
    st.plotly_chart(fig)