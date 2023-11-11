import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

github_raw_url = 'https://raw.githubusercontent.com/loop16/models/main/Data.csv'

# Function to load data from a GitHub raw file URL
def load_data_from_github(url):
    try:
        # Read CSV data using pandas
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Load data from GitHub
df2 = load_data_from_github(github_raw_url)

# Check if data is loaded successfully
if df is not None:
    # Display the loaded data
    st.dataframe(df)
else:
    st.error("Failed to load data from GitHub.")
df = pd.read_csv(df2)

st.header('Model Matrix')
con = st.expander('Enter')
with con:
    c1, c2, c3 = con.columns(3)

    c1.write('RDR -> ADR')
    RdrAdr_options = ['All'] + list(df['RDRtoADR'].unique())
    RDRtoADR = c1.selectbox('Select Model for RDR to ADR' , options=RdrAdr_options)
    filtered_model_df = df
    if RDRtoADR == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['RDRtoADR'] == RDRtoADR]
    

    ADRConfirm_options = ['All'] + list(df['ADRConfirm'].unique())
    ADRConfirm = c1.selectbox('ADR Confirmation' , options=ADRConfirm_options)

    if ADRConfirm == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADRConfirm'] == ADRConfirm]


    ADRbox_options = ['All'] + list(df['ADRBOX'].unique())
    ADRbox = c1.selectbox('ADR box Color' , options=ADRbox_options)

    if ADRbox == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADRBOX'] == ADRbox]

    BrokenADR_options = ['All'] + list(df['BrokenADR'].unique())
    BrokenADR = c1.selectbox('Broken Model' , options=BrokenADR_options)

    if BrokenADR == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['BrokenADR'] == BrokenADR]


    bar_chart = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('RDRtoADR:N',sort='-y'),
        y=alt.Y('count():Q')
    )
    c1.altair_chart(bar_chart, use_container_width=True)

    word_counts = filtered_model_df['ADRConfirm'].value_counts().reset_index()
    word_counts.columns = ['ADR Confirm', 'Count']

    light_blue = '#62c8e7'  # Light Blue
    dark_blue = '#2157c2'     
    dark_red = '#c43b58'
    color_mapping = {
    'long': dark_blue,
    'long false': light_blue,
    'short': dark_red,
    'short false': 'pink',
    'na':'#388e3c',
    # Add more colors and words as needed
    }

    chart = alt.Chart(word_counts).mark_arc().encode(
    color=alt.Color('ADR Confirm:N' , scale=alt.Scale(domain=list(color_mapping.keys()), range=list(color_mapping.values()))),
    theta='Count:Q' 
    )
    c1.altair_chart(chart, use_container_width=True)


    word_counts2 = filtered_model_df['ADRBOX'].value_counts().reset_index()
    word_counts2.columns = ['ADR Box Color', 'Count']

    color_mapping2 = {
        'green':'#388e3c',
        'red':dark_red,
        'na':'grey',


    # Add more colors and words as needed
    }

    chart2 = alt.Chart(word_counts2).mark_arc().encode(
    color=alt.Color('ADR Box Color:N' , scale=alt.Scale(domain=list(color_mapping2.keys()), range=list(color_mapping2.values()))),
    theta='Count:Q' 
    )




    c1.altair_chart(chart2, use_container_width=True)

    bar_chart2 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('MaxExtensionADR:N',),
        y=alt.Y('count():Q')
    )
    c1.altair_chart(bar_chart2, use_container_width=True)


    bar_chart3 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('MaxRetraceADR:N',),
        y=alt.Y('count():Q')
    )
    c1.altair_chart(bar_chart3, use_container_width=True)



    c2.write('ADR -> ODR')

    adr_options = ['All'] + list(df['ADRtoODR'].unique())
    ADRtoODR = c2.selectbox('Select Model for ADR to ODR', options=adr_options)
    if ADRtoODR == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADRtoODR'] == ADRtoODR]

    ODRConfirm_options = ['All'] + list(df['ODRConfirm'].unique())
    ODRConfirm = c2.selectbox('ODR Confirmation' , options=ODRConfirm_options)

    if ODRConfirm == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODRConfirm'] == ODRConfirm]


    ODRbox_options = ['All'] + list(df['ODRBOX'].unique())
    ODRbox = c2.selectbox('ODR box Color' , options=ODRbox_options)

    if ODRbox == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODRBOX'] == ODRbox]

    BrokenODR_options = ['All'] + list(df['BrokenODR'].unique())
    BrokenODR = c2.selectbox('Broken Model' , options=BrokenODR_options)

    if BrokenODR == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['BrokenODR'] == BrokenODR]







    bar_chart = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('ADRtoODR:N',sort='-y'),
        y=alt.Y('count():Q')
    )

    c2.altair_chart(bar_chart, use_container_width=True)

    
    word_counts3 = filtered_model_df['ODRConfirm'].value_counts().reset_index()
    word_counts3.columns = ['ODR Confirm', 'Count']


    color_mapping3 = {
    'long': dark_blue,
    'long false': light_blue,
    'short': dark_red,
    'short false': 'pink',
    'na':'#388e3c',
    # Add more colors and words as needed
    }

    chart3 = alt.Chart(word_counts3).mark_arc().encode(
    color=alt.Color('ODR Confirm:N' , scale=alt.Scale(domain=list(color_mapping3.keys()), range=list(color_mapping3.values()))),
    theta='Count:Q' 
    )
    c2.altair_chart(chart3, use_container_width=True)


    word_counts4 = filtered_model_df['ODRBOX'].value_counts().reset_index()
    word_counts4.columns = ['ODR Box Color', 'Count']

    color_mapping4 = {
        'green':'#388e3c',
        'red':dark_red,
        'na':'grey',


    # Add more colors and words as needed
    }

    chart4 = alt.Chart(word_counts4).mark_arc().encode(
    color=alt.Color('ODR Box Color:N' , scale=alt.Scale(domain=list(color_mapping4.keys()), range=list(color_mapping4.values()))),
    theta='Count:Q' 
    )




    c2.altair_chart(chart4, use_container_width=True)

    bar_chart2 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('MaxExtensionODR:N',),
        y=alt.Y('count():Q')
    )
    c2.altair_chart(bar_chart2, use_container_width=True)


    bar_chart3 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('MaxRetraceODR:N',),
        y=alt.Y('count():Q')
    )
    c2.altair_chart(bar_chart3, use_container_width=True)


    ################################

    c3.write('ODR -> RDR')
    rdr_options = ['All'] + list(df['ODRtoRDR'].unique())
    ODRtoRDR = c3.selectbox('Select Model for ODR to RDR', options=rdr_options)
    if ODRtoRDR == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODRtoRDR'] == ODRtoRDR]

    RDRConfirm_options = ['All'] + list(df['RDRConfirm'].unique())
    RDRConfirm = c3.selectbox('RDR Confirmation' , options=RDRConfirm_options)

    if RDRConfirm == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['RDRConfirm'] == RDRConfirm]


    RDRbox_options = ['All'] + list(df['RDRBOX'].unique())
    RDRbox = c3.selectbox('RDR box Color' , options=RDRbox_options)

    if RDRbox == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['RDRBOX'] == RDRbox]

    BrokenRDR_options = ['All'] + list(df['BrokenRDR'].unique())
    BrokenRDR = c3.selectbox('Broken Model' , options=BrokenRDR_options)

    if BrokenRDR == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['BrokenRDR'] == BrokenRDR]


    bar_chart = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('ODRtoRDR:N',sort='-y'),
        y=alt.Y('count():Q')
    )

    c3.altair_chart(bar_chart, use_container_width=True)


    
    word_counts5 = filtered_model_df['RDRConfirm'].value_counts().reset_index()
    word_counts5.columns = ['RDR Confirm', 'Count']


    color_mapping5 = {
    'long': dark_blue,
    'long false': light_blue,
    'short': dark_red,
    'short false': 'pink',
    'na':'#388e3c',
    # Add more colors and words as needed
    }

    chart5 = alt.Chart(word_counts5).mark_arc().encode(
    color=alt.Color('RDR Confirm:N' , scale=alt.Scale(domain=list(color_mapping5.keys()), range=list(color_mapping5.values()))),
    theta='Count:Q' 
    )
    c3.altair_chart(chart5, use_container_width=True)


    word_counts6 = filtered_model_df['RDRBOX'].value_counts().reset_index()
    word_counts6.columns = ['RDR Box Color', 'Count']

    color_mapping6 = {
        'green':'#388e3c',
        'red':dark_red,
        'na':'grey',


    # Add more colors and words as needed
    }

    chart6 = alt.Chart(word_counts6).mark_arc().encode(
    color=alt.Color('RDR Box Color:N' , scale=alt.Scale(domain=list(color_mapping6.keys()), range=list(color_mapping6.values()))),
    theta='Count:Q' 
    )




    c3.altair_chart(chart6, use_container_width=True)

    bar_chart2 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('MaxExtensionRDR:N',),
        y=alt.Y('count():Q')
    )
    c3.altair_chart(bar_chart2, use_container_width=True)


    bar_chart3 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('MaxRetraceRDR:N',),
        y=alt.Y('count():Q')
    )
    c3.altair_chart(bar_chart3, use_container_width=True)
