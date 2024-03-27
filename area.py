import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


github_raw_url = 'https://raw.githubusercontent.com/loop16/models/main/AREA.csv'



# Function to load data from a GitHub raw file URL
def load_data_from_github(url):
    try:
        # Read CSV data using pandas
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None
    

st.set_page_config(layout="wide")

df = load_data_from_github(github_raw_url)



st.header('SEND IT MONEY MATRIX')
con = st.expander('Enter')
with con:
    c1, c2, c3 = con.columns(3)

    filtered_model_df = df

    RdrAdr_options = ['All'] + list(df['DAY'].unique())
    RDRtoADR = c1.selectbox('Day Filter' , options=RdrAdr_options)

    
    if RDRtoADR == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['DAY'] == RDRtoADR]
    

    ADRConfirm_options = ['All'] + list(df['WORKS'].unique())
    ADRConfirm = c1.selectbox('WORKS' , options=ADRConfirm_options)

    if ADRConfirm == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['WORKS'] == ADRConfirm]


    
    bar_chart3 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('RETRACEMENT:N',bin=alt.Bin(step=0.1)),
        y=alt.Y('count():Q')
    )

    c1.altair_chart(bar_chart3, use_container_width=True)

    
    



    