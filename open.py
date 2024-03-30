import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

github_raw_url = 'https://raw.githubusercontent.com/loop16/models/main/mpath.csv'



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

st.header('')
con = st.expander('Enter')
with con:
    c1, c2, c3 = con.columns(3)

    c1.write('Filters')
    RdrAdr_options = ['All'] + list(df['Day'].unique())
    RDRtoADR = c1.selectbox('Day' , options=RdrAdr_options)

    filtered_model_df = df

    if RDRtoADR == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['Day'] == RDRtoADR]


    DRbox_options = ['All'] + list(df['ADR Model'].unique())
    DRbox = c1.selectbox('ADR Model' , options=DRbox_options)

    if DRbox == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADR Model'] == DRbox]

    


    BrokenADR_options = ['All'] + list(df['ODR Model'].unique())
    BrokenADR = c1.selectbox('ODR Model' , options=BrokenADR_options)

    if BrokenADR == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR Model'] == BrokenADR] 

    


    TIMEConfirm_options = ['All'] + sorted(df['odr_conf_time'].dropna().unique())
    TIMEConfirm = c1.selectbox('TIME of Confirmation' , options=TIMEConfirm_options)

    if TIMEConfirm == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['odr_conf_time'] == TIMEConfirm]   

    ADRConfirm_options = ['All'] + list(df['ODR CONFO'].unique())
    ADRConfirm = c1.selectbox('Confirmation' , options=ADRConfirm_options)

    if ADRConfirm == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR CONFO'] == ADRConfirm]

    Size_options = ['All'] + list(df['ODR TRUERUE'].unique())
    Size = c1.selectbox('TRUE OR FALSE?' , options=Size_options)

    if Size == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR TRUERUE'] == Size]


    ADRbox_options = ['All'] + list(df['ODR BOX'].unique())
    ADRbox = c1.selectbox('ODR Color' , options=ADRbox_options)

    if ADRbox == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR BOX'] == ADRbox]

    
    RDRbox_options = ['All'] + list(df['RDR Model'].unique())
    RDRbox = c1.selectbox('RDR Model' , options=RDRbox_options)

    if RDRbox == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['RDR Model'] == RDRbox]

    RDRbox2_options = ['All'] + list(df['RDR BOX'].unique())
    RDRbox2 = c1.selectbox('RDR Color' , options=RDRbox2_options)

    if RDRbox2 == 'All':
        filtered_model_df = filtered_model_df # No filtering
    else:
        filtered_model_df = filtered_model_df[filtered_model_df['RDR BOX'] == RDRbox2]




 

    ################################

    c2.write('ODR Based Data')

    numeric_values = filtered_model_df['RDR open Based on ODR SD'].apply(pd.to_numeric, errors='coerce')
    numeric_values = numeric_values.dropna()  # Drop NaN values
    try:
        medianODR=numeric_values.median()
        meanODR=numeric_values.mean()
        quantileODR=numeric_values.quantile(0.7)
        quantile2ODR=numeric_values.quantile(0.3)    
        
        c2.write(f"Median: {medianODR}")
        c2.write(f"Average: {meanODR}")
        c2.write(f"70%: {quantileODR}")
        c2.write(f"30%: {quantile2ODR}")
    except Exception as e:
        st.write("An error occurred in the second instance:")
        st.write(e)
    bar_chart2 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('RDR open Based on ODR SD:N',bin=alt.Bin(step=0.5)),
        y=alt.Y('count():Q')
    )
    c2.altair_chart(bar_chart2, use_container_width=True)
    c2.write('Max Retracement ODR')
    numeric_values2 = filtered_model_df['ODR Max Ret'].apply(pd.to_numeric, errors='coerce')
    numeric_values2 = numeric_values2.dropna()  # Drop NaN values
    try:
        median2ODR=numeric_values2.median()
        mean2ODR=numeric_values2.mean()
        quantile2ODR=numeric_values2.quantile(0.7)
        quantile22ODR=numeric_values2.quantile(0.3)    
        
        c2.write(f"Median: {median2ODR}")
        c2.write(f"Average: {mean2ODR}")
        c2.write(f"70%: {quantile2ODR}")
        c2.write(f"30%: {quantile22ODR}")
    except Exception as e:
        st.write("An error occurred in the second instance:")
        st.write(e)

    filtered_model_df = filtered_model_df.dropna(subset=['ODR Max Ret'])
   
    bar_chart3 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('ODR Max Ret:N',bin=alt.Bin(step=0.1)),
        y=alt.Y('count():Q')
    )
    c2.altair_chart(bar_chart3, use_container_width=True)


    c3.write('False Confirmation Time') 
    c3.write(f" ")
    c3.write(f"  ")
    c3.write(f"    ")
    c3.write(f"       ")
    time_range = pd.date_range( "04:00", "08:25", freq="5min")
    time_values = [time.strftime("%H:%M") for time in time_range]
    
    filtered_model_df = filtered_model_df.dropna(subset=['odr_false_conf_time'])
    bar_chart3 = alt.Chart(filtered_model_df).mark_bar().encode(
    x=alt.X('odr_false_conf_time:N', sort=alt.SortField(field='odr_false_conf_time', order='ascending'), axis=alt.Axis(values=time_values)),
    y=alt.Y('count():Q')
    )
    c3.altair_chart(bar_chart3, use_container_width=True)

    filtered_model_df = filtered_model_df.dropna(subset=['odr_false_ret_b4_hoslos'])
    c3.write('False Retracement H0S/LOS')

    numeric_values3 = filtered_model_df['odr_false_ret_b4_hoslos'].apply(pd.to_numeric, errors='coerce')
    numeric_values3 = numeric_values3.dropna()  # Drop NaN values
    try:
        median3ODR=numeric_values3.median()
        mean3ODR=numeric_values3.mean()
        quantile3ODR=numeric_values3.quantile(0.7)
        quantile33ODR=numeric_values3.quantile(0.3)    
        
        c3.write(f"Median: {median3ODR}")
        c3.write(f"Average: {mean3ODR}")
        c3.write(f"70%: {quantile3ODR}")
        c3.write(f"30%: {quantile33ODR}")
    except Exception as e:
        st.write("An error occurred in the second instance:")
        st.write(e)



    bar_chart3 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('odr_false_ret_b4_hoslos:N',bin=alt.Bin(step=0.1)),
        y=alt.Y('count():Q')
    )
    c3.altair_chart(bar_chart3, use_container_width=True)
    