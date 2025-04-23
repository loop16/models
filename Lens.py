import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


def load_data_from_github(url):
    try:
        # Read CSV data using pandas
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None
    
st.set_page_config(layout="wide")


github_urls = {
    'CL': ('/Users/orlandocantoni/Desktop/RBC auto model/CL_RDR.V1_2025.csv'),
    'NQ': ('/Users/orlandocantoni/Desktop/RBC auto model/NQ_RDR.V1_2025.csv'),
    'ES': ('/Users/orlandocantoni/Desktop/RBC auto model/ES_RDR.V1_2025.csv')
}

c1, c2, c3 ,c4 , c5 = st.columns([1,2,2,2,2])




##### GENERAL FILTERS ##############################################################################
selected_instrument = c1.selectbox('Instrument', ['CL', 'NQ', 'ES'])

# Load data based on selected instrument
if selected_instrument in github_urls:
    dash_url= github_urls[selected_instrument]
    filtered_model_df = load_data_from_github(dash_url)
    filtered_model_df = filtered_model_df.dropna()
    # Drop rows with 'Sunday' in the 'Day_of_Week' column
    filtered_model_df = filtered_model_df[filtered_model_df['Day_of_Week'] != 'Sunday']

    
else:
    st.error("Selected instrument not recognized.")

filtered_model_df=filtered_model_df
#Day selector
DAY_options = ['All'] + list(filtered_model_df['Day_of_Week'].unique())


DAYw = c1.selectbox('Day_of_Week' , options=DAY_options)

if DAYw == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['Day_of_Week'] == DAYw]
        

#ADR Model####################
RdrAdr_options = ['All'] + list(filtered_model_df['RDR_Trade_Direction'].unique())
RDRtoADR = c1.selectbox('RDR_Trade_Direction' , options=RdrAdr_options)


if RDRtoADR == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['RDR_Trade_Direction'] == RDRtoADR]

RdrAdr_options2 = ['All'] + list(filtered_model_df['RDR_Session_True'].unique())
RDRtoADR2 = c1.selectbox('RDR_Session_True' , options=RdrAdr_options2)


if RDRtoADR2 == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['RDR_Session_True'] == RDRtoADR2]

##ODR confirmation time ########
TIMEConfirm_options = ['All'] + sorted(filtered_model_df['RDR_Confirmation_Candle'].dropna().unique())
TIMEConfirm = c1.selectbox('Confirmation_5min' , options=TIMEConfirm_options)

if TIMEConfirm == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['RDR_Confirmation_Candle'] == TIMEConfirm]   

TIMEConfirm_options2 = ['All'] + sorted(filtered_model_df['RDR_Confirmation_Candle_15min'].dropna().unique())
TIMEConfirm2 = c1.selectbox('Confirmation_15min' , options=TIMEConfirm_options2)

if TIMEConfirm2 == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['RDR_Confirmation_Candle_15min'] == TIMEConfirm2]   

TIMEConfirm_options3 = ['All'] + sorted(filtered_model_df['RDR_Confirmation_Candle_30min'].dropna().unique())
TIMEConfirm3 = c1.selectbox('Confirmation_30min' , options=TIMEConfirm_options3)

if TIMEConfirm3 == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['RDR_Confirmation_Candle_30min'] == TIMEConfirm3]   


RetVAL_options = ['All'] + sorted(filtered_model_df['RDR_Box_STD'].dropna().unique())
RetVAL = c1.selectbox('RDR_Box_STD' , options=RetVAL_options)

if RetVAL == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['RDR_Box_STD'] == RetVAL]  

filtered_model_df['RDR_Box_STD']=np.round(np.array(filtered_model_df['RDR_Box_STD']) - 0.05, 1)

c2_1, c2_2 = c2.columns(2)
c3_1, c3_2 = c3.columns(2)
c4_1, c4_2 = c4.columns(2)
c5_1, c5_2 = c5.columns(2)

c2_1.metric("Total Datasets", f"{len(filtered_model_df):,}")

# c2_2: True rate percentage 
true_rate = filtered_model_df['RDR_Session_True'].mean() * 100
c2_2.metric("True Rate", f"{true_rate:.2f}%")

# c3_1: Median RDR_Max_Ext_STD
median_max_ext = filtered_model_df['RDR_Max_Ext_STD'].median()
c3_1.metric("Median RDR_Max_Ext_STD", f"{median_max_ext:.2f}")

# c3_2: Median RDR_Max_Ret_STD
median_max_ret = filtered_model_df['RDR_Max_Ret_STD'].median()
c3_2.metric("Median RDR_Max_Ret_STD", f"{median_max_ret:.2f}")

# c4_1: Median Confirmation_Size_STD
median_conf_size = filtered_model_df['Confirmation_Size_STD'].median()
c4_1.metric("Median Confirmation Size", f"{median_conf_size:.2f}")

# c4_2: Percent RDR_Max_Ext_STD > 0.5
pct_ext_above = (filtered_model_df['RDR_Max_Ext_STD'] > 0.5).mean() * 100
c4_2.metric("% RDR_Max_Ext_STD > 0.5", f"{pct_ext_above:.2f}%")

# c5_1: Percent RDR_Max_Ret_STD > -0.5
pct_ret_above = (filtered_model_df['RDR_Max_Ret_STD'] > -0.5).mean() * 100
c5_1.metric("% RDR_Max_Ret_STD > -0.5", f"{pct_ret_above:.2f}%")

# c5_2: Percent RDR_M7_Retrace > -0.5
pct_m7_above = (filtered_model_df['RDR_M7_Retrace'] > -0.5).mean() * 100
c5_2.metric("% RDR_M7_Retrace > -0.5", f"{pct_m7_above:.2f}%")



filtered_model_df['RDR_M7_Retrace']=np.round(np.array(filtered_model_df['RDR_M7_Retrace']) - 0.05, 1)

filtered_model_df['RDR_Max_Ext_STD']=np.round(np.array(filtered_model_df['RDR_Max_Ext_STD']) - 0.05, 1)

filtered_model_df['RDR_Max_Ret_STD']=np.round(np.array(filtered_model_df['RDR_Max_Ret_STD']) - 0.05, 1)

filtered_model_df['RDR_RBC_STD']=np.round(np.array(filtered_model_df['RDR_RBC_STD']) - 0.05, 1)

# Create metric display with background color matching chart


# Create a complete range of values for x-axis from -1.5 to 1.0 with 0.1 increments
all_values = pd.DataFrame({
    'RDR_M7_Retrace': [round(x * 0.1, 1) for x in range(-15, 11)]  # -1.5 to 1.0
})

# Get actual value counts within the filtered range for DISPLAY purposes
actual_counts = filtered_model_df[
    (filtered_model_df['RDR_M7_Retrace'] >= -1.5) & 
    (filtered_model_df['RDR_M7_Retrace'] <= 1.0)
]['RDR_M7_Retrace'].value_counts().reset_index()
actual_counts.columns = ['RDR_M7_Retrace', 'count']

# Merge to ensure all values are represented
complete_data = pd.merge(all_values, actual_counts, on='RDR_M7_Retrace', how='left')
complete_data['count'] = complete_data['count'].fillna(0)
complete_data['total'] = complete_data['count'].sum()
complete_data['percentage'] = complete_data['count'] / complete_data['total']

# Bar chart with complete x-axis (limited to -1.5 to 1.0)
bar1 = alt.Chart(complete_data).mark_bar().encode(
    x=alt.X('RDR_M7_Retrace:N', sort='x', title='RDR_M7_Retrace'),
    y=alt.Y('percentage:Q', axis=alt.Axis(format='.0%'), title='')
)

# Calculate median using ALL data (not just the filtered range)
median_value = round(filtered_model_df['RDR_M7_Retrace'].median(), 1)

# Add median line (showing the true median of ALL data)
median_rule = alt.Chart(pd.DataFrame({'median': [median_value]})).mark_rule(
    color='white',
    strokeWidth=2
).encode(
    x='median:N',
    tooltip=[alt.Tooltip('median:N', title='Median Value (50%) of ALL data')]
)

# Only include the median line if it falls within our display range
if -1.5 <= median_value <= 1.0:
    final_chart = bar1 + median_rule
else:
    final_chart = bar1
    # Optionally show a message that the median is outside the display range
    c2.write(f"Note: The median value ({median_value:.1f}) is outside the display range.")

c2.altair_chart(final_chart, theme=None, use_container_width=True)


all_values2 = pd.DataFrame({
    'RDR_Max_Ret_STD': [round(x * 0.1, 1) for x in range(-15, 11)]  # -1.5 to 1.0
})

# Get actual value counts within the filtered range for DISPLAY purposes
actual_counts2 = filtered_model_df[
    (filtered_model_df['RDR_Max_Ret_STD'] >= -1.5) & 
    (filtered_model_df['RDR_Max_Ret_STD'] <= 1.0)
]['RDR_Max_Ret_STD'].value_counts().reset_index()
actual_counts2.columns = ['RDR_Max_Ret_STD', 'count']

# Merge to ensure all values are represented
complete_data = pd.merge(all_values2, actual_counts2, on='RDR_Max_Ret_STD', how='left')
complete_data['count'] = complete_data['count'].fillna(0)
complete_data['total'] = complete_data['count'].sum()
complete_data['percentage'] = complete_data['count'] / complete_data['total']

# Bar chart with complete x-axis (limited to -1.5 to 1.0)
bar1 = alt.Chart(complete_data).mark_bar().encode(
    x=alt.X('RDR_Max_Ret_STD:N', sort='x', title='RDR_Max_Ret_STD'),
    y=alt.Y('percentage:Q', axis=alt.Axis(format='.0%'), title='')
)

# Calculate median using ALL data (not just the filtered range)

median_value = round(filtered_model_df['RDR_Max_Ret_STD'].median(), 1)


# Add median line (showing the true median of ALL data)
median_rule = alt.Chart(pd.DataFrame({'median': [median_value]})).mark_rule(
    color='white',
    strokeWidth=2
).encode(
    x='median:N',
    tooltip=[alt.Tooltip('median:N', title='Median Value (50%) of ALL data')]
)

# Only include the median line if it falls within our display range
if -1.5 <= median_value <= 1.0:
    final_chart = bar1 + median_rule
else:
    final_chart = bar1
    # Optionally show a message that the median is outside the display range
    c3.write(f"Note: The median value ({median_value:.1f}) is outside the display range.")

c3.altair_chart(final_chart, theme=None, use_container_width=True)

all_values2 = pd.DataFrame({
    'RDR_Max_Ext_STD': [round(x * 0.1, 1) for x in range(0, 31)]  # -1.5 to 1.0
})

# Get actual value counts within the filtered range for DISPLAY purposes
actual_counts2 = filtered_model_df[
    (filtered_model_df['RDR_Max_Ext_STD'] >= 0) & 
    (filtered_model_df['RDR_Max_Ext_STD'] <= 3.0)
]['RDR_Max_Ext_STD'].value_counts().reset_index()
actual_counts2.columns = ['RDR_Max_Ext_STD', 'count']

# Merge to ensure all values are represented
complete_data = pd.merge(all_values2, actual_counts2, on='RDR_Max_Ext_STD', how='left')
complete_data['count'] = complete_data['count'].fillna(0)
complete_data['total'] = complete_data['count'].sum()
complete_data['percentage'] = complete_data['count'] / complete_data['total']

# Bar chart with complete x-axis (limited to -1.5 to 1.0)
bar1 = alt.Chart(complete_data).mark_bar().encode(
    x=alt.X('RDR_Max_Ext_STD:N', sort='x', title='RDR_Max_Ext_STD'),
    y=alt.Y('percentage:Q', axis=alt.Axis(format='.0%'), title='')
)

# Calculate median using ALL data (not just the filtered range)

median_value = round(filtered_model_df['RDR_Max_Ext_STD'].median(), 1)

# Add median line (showing the true median of ALL data)
median_rule = alt.Chart(pd.DataFrame({'median': [median_value]})).mark_rule(
    color='white',
    strokeWidth=2
).encode(
    x='median:N',
    tooltip=[alt.Tooltip('median:N', title='Median Value (50%) of ALL data')]
)

# Only include the median line if it falls within our display range
if 0 <= median_value <= 3.0:
    final_chart = bar1 + median_rule
else:
    final_chart = bar1
    # Optionally show a message that the median is outside the display range
    c4.write(f"Note: The median value ({median_value:.1f}) is outside the display range.")

c4.altair_chart(final_chart, theme=None, use_container_width=True)

all_values2 = pd.DataFrame({
    'RDR_RBC_STD': [round(x * 0.1, 1) for x in range(-16, 2)]  # -1.5 to 1.0
})

# Get actual value counts within the filtered range for DISPLAY purposes
actual_counts2 = filtered_model_df[
    (filtered_model_df['RDR_RBC_STD'] >= -1.6) & 
    (filtered_model_df['RDR_RBC_STD'] <= 0.2)
]['RDR_RBC_STD'].value_counts().reset_index()
actual_counts2.columns = ['RDR_RBC_STD', 'count']

# Merge to ensure all values are represented
complete_data = pd.merge(all_values2, actual_counts2, on='RDR_RBC_STD', how='left')
complete_data['count'] = complete_data['count'].fillna(0)
complete_data['total'] = complete_data['count'].sum()
complete_data['percentage'] = complete_data['count'] / complete_data['total']

# Bar chart with complete x-axis (limited to -1.5 to 1.0)
bar1 = alt.Chart(complete_data).mark_bar().encode(
    x=alt.X('RDR_RBC_STD:N', sort='x', title='RDR_RBC_STD'),
    y=alt.Y('percentage:Q', axis=alt.Axis(format='.0%'), title='')
)

# Calculate median using ALL data (not just the filtered range)

median_value = round(filtered_model_df['RDR_RBC_STD'].median(), 1)

# Add median line (showing the true median of ALL data)
median_rule = alt.Chart(pd.DataFrame({'median': [median_value]})).mark_rule(
    color='white',
    strokeWidth=2
).encode(
    x='median:N',
    tooltip=[alt.Tooltip('median:N', title='Median Value (50%) of ALL data')]
)

# Only include the median line if it falls within our display range
if -1.6 <= median_value <= 0.2:
    final_chart = bar1 + median_rule
else:
    final_chart = bar1
    # Optionally show a message that the median is outside the display range
    c5.write(f"Note: The median value ({median_value:.1f}) is outside the display range.")

c5.altair_chart(final_chart, theme=None, use_container_width=True)





time_range = pd.date_range("10:30", "16:00", freq="15min")
time_values = [time.strftime("%H:%M:%S") for time in time_range]

time_range2 = pd.date_range("10:30", "12:00", freq="5min")
time_values2 = [time.strftime("%H:%M:%S") for time in time_range2]

# Create a dataframe with all possible time values to ensure they all appear on the x-axis
all_times_df = pd.DataFrame({'RDR_Max_RET_Time_15min': time_values})

# Calculate time distribution
time_counts = filtered_model_df['RDR_M7_Time_15min'].value_counts().reset_index()
time_counts.columns = ['time', 'count']
time_counts = time_counts.sort_values('time')
time_counts['percentage'] = time_counts['count'] / time_counts['count'].sum()
time_counts['cumulative'] = time_counts['percentage'].cumsum()

# Find median time (where cumulative percentage crosses 50%)
median_df = time_counts[time_counts['cumulative'] >= 0.5]
if not median_df.empty:
    median_time = median_df.iloc[0]['time']

# Create the bar chart with forced domain
bar_chart = alt.Chart(filtered_model_df).transform_aggregate(
    count='count()',
    groupby=['RDR_M7_Time_15min']
).transform_joinaggregate(
    total='sum(count)'
).transform_calculate(
    percentage='datum.count / datum.total'
).mark_bar().encode(
    x=alt.X('RDR_M7_Time_15min:N', 
            sort=time_values,  # Sort according to our predefined order
            scale=alt.Scale(domain=time_values),  # Force domain to include all time values
            axis=alt.Axis(values=time_values)),
    y=alt.Y('percentage:Q', axis=alt.Axis(format='.0%'), title='')
)

# Add median line if median was found
if 'median_time' in locals():
    median_rule = alt.Chart(pd.DataFrame({'median': [median_time]})).mark_rule(
        color='white',
        strokeWidth=2
    ).encode(
        x='median:N',
        tooltip=[alt.Tooltip('median:N', title='Median Time (50%)')],
    )
    final_chart = bar_chart + median_rule
else:
    final_chart = bar_chart

c2.altair_chart(final_chart, theme=None, use_container_width=True)




time_counts2 = filtered_model_df['RDR_Max_RET_Time_15min'].value_counts().reset_index()
time_counts2.columns = ['time', 'count']
time_counts2 = time_counts2.sort_values('time')
time_counts2['percentage'] = time_counts2['count'] / time_counts2['count'].sum()
time_counts2['cumulative'] = time_counts2['percentage'].cumsum()

# Find median time (where cumulative percentage crosses 50%)
median_df2 = time_counts2[time_counts2['cumulative'] >= 0.5]
if not median_df2.empty:
    median_time2 = median_df2.iloc[0]['time']

# Create the bar chart
bar_chart2 = alt.Chart(filtered_model_df).transform_aggregate(
    count='count()',
    groupby=['RDR_Max_RET_Time_15min']
).transform_joinaggregate(
    total='sum(count)'
).transform_calculate(
    percentage='datum.count / datum.total'
).mark_bar().encode(
    x=alt.X('RDR_Max_RET_Time_15min:N',
            sort=time_values,  # Sort according to our predefined order
            scale=alt.Scale(domain=time_values),  # Force domain to include all time values
            axis=alt.Axis(values=time_values)),
    y=alt.Y('percentage:Q', axis=alt.Axis(format='.0%'), title='Percentage')
)

# Add median line if median was found
if 'median_time' in locals():
    median_rule2 = alt.Chart(pd.DataFrame({'median': [median_time2]})).mark_rule(
        color='white',
        strokeWidth=2
    ).encode(
        x='median:N',
        tooltip=[alt.Tooltip('median:N', title='Median Time (50%)')],
    )
    final_chart2 = bar_chart2 + median_rule2
else:
    final_chart2 = bar_chart2

c3.altair_chart(final_chart2, theme=None, use_container_width=True)

######3
time_counts3 = filtered_model_df['RDR_Max_EXT_Time_15min'].value_counts().reset_index()
time_counts3.columns = ['time', 'count']
time_counts3 = time_counts3.sort_values('time')
time_counts3['percentage'] = time_counts3['count'] / time_counts3['count'].sum()
time_counts3['cumulative'] = time_counts3['percentage'].cumsum()

# Find median time (where cumulative percentage crosses 50%)
median_df3 = time_counts3[time_counts3['cumulative'] >= 0.5]
if not median_df3.empty:
    median_time3 = median_df3.iloc[0]['time']

# Create the bar chart
bar_chart3 = alt.Chart(filtered_model_df).transform_aggregate(
    count='count()',
    groupby=['RDR_Max_EXT_Time_15min']
).transform_joinaggregate(
    total='sum(count)'
).transform_calculate(
    percentage='datum.count / datum.total'
).mark_bar().encode(
    x=alt.X('RDR_Max_EXT_Time_15min:N', 
            sort=time_values,  # Sort according to our predefined order
            scale=alt.Scale(domain=time_values),  # Force domain to include all time values
            axis=alt.Axis(values=time_values)),
    y=alt.Y('percentage:Q', axis=alt.Axis(format='.0%'), title='')
)

# Add median line if median was found
if 'median_time' in locals():
    median_rule3 = alt.Chart(pd.DataFrame({'median': [median_time3]})).mark_rule(
        color='white',
        strokeWidth=2
    ).encode(
        x='median:N',
        tooltip=[alt.Tooltip('median:N', title='Median Time (50%)')],
    )
    final_chart3 = bar_chart3 + median_rule3
else:
    final_chart3 = bar_chart3

c4.altair_chart(final_chart3, theme=None, use_container_width=True)

time_counts4 = filtered_model_df['RDR_RBC_Time'].value_counts().reset_index()
time_counts4.columns = ['time', 'count']
time_counts4 = time_counts4.sort_values('time')
time_counts4['percentage'] = time_counts4['count'] / time_counts4['count'].sum()
time_counts4['cumulative'] = time_counts4['percentage'].cumsum()

# Find median time (where cumulative percentage crosses 50%)
median_df4 = time_counts4[time_counts4['cumulative'] >= 0.5]
if not median_df4.empty:
    median_time4 = median_df4.iloc[0]['time']

# Create the bar chart
bar_chart4 = alt.Chart(filtered_model_df).transform_aggregate(
    count='count()',
    groupby=['RDR_RBC_Time']
).transform_joinaggregate(
    total='sum(count)'
).transform_calculate(
    percentage='datum.count / datum.total'
).mark_bar().encode(
    x=alt.X('RDR_RBC_Time:N', 
        sort=time_values2,  # Sort according to our predefined order
        scale=alt.Scale(domain=time_values2),  # Force domain to include all time values
        axis=alt.Axis(values=time_values2)),
    y=alt.Y('percentage:Q', axis=alt.Axis(format='.0%'), title='')
)

# Add median line if median was found
if 'median_time' in locals():
    median_rule4 = alt.Chart(pd.DataFrame({'median': [median_time4]})).mark_rule(
        color='white',
        strokeWidth=2
    ).encode(
        x='median:N',
        tooltip=[alt.Tooltip('median:N', title='Median Time (50%)')],
    )
    final_chart4 = bar_chart4 + median_rule4
else:
    final_chart4 = bar_chart4

c5.altair_chart(final_chart4, theme=None, use_container_width=True)





