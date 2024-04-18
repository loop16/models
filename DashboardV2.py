import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


github_raw_url6= 'https://raw.githubusercontent.com/loop16/models/main/ESM7JOE.csv'
github_raw_url7= 'https://raw.githubusercontent.com/loop16/models/main/normalized_data_rounded2.txt'


def load_data_from_github(url):
    try:
        # Read CSV data using pandas
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None
    

st.set_page_config(layout="wide")

df5 = load_data_from_github(github_raw_url6)

df6 = load_data_from_github(github_raw_url7)

instrument_options = ['CL','CL M7','NQ','NQ M7', 'ES' , 'ES M7']



c1, c7, c5, c6 = st.columns([1,3,4,4])

c2,c3,c4 = c7.columns(3)


##### GENERAL FILTERS ##############################################################################

filtered_model_df = df5
#Day selector
DAY_options = ['All'] + list(filtered_model_df['Day'].unique())


DAYw = c1.selectbox('Day' , options=DAY_options)



if DAYw == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['Day'] == DAYw]

#ADR Model####################
RdrAdr_options = ['All'] + list(filtered_model_df['ADR_Model'].unique())
RDRtoADR = c1.selectbox('ADR Model' , options=RdrAdr_options)


if RDRtoADR == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADR_Model'] == RDRtoADR]

#ADR long short################
#ADRConf_options = ['All'] + list(df['ADR_Confirmation'].unique())
#ADRConf = c1.selectbox('ADR Confirmation' , options=ADRConf_options)

#if ADRConf == 'All':
#    filtered_model_df = filtered_model_df
#else:
#    filtered_model_df = filtered_model_df[filtered_model_df['ADR_Confirmation']==ADRConf]

#ADR true false################
#ADRTF_options = ['All'] + list(df['ADR_True_False'].unique())
#ADRTFx = c1.selectbox('ADR True/False' , options=ADRTF_options)

#if ADRTFx == 'All':
#    filtered_model_df = filtered_model_df
#else:
#    filtered_model_df = filtered_model_df[filtered_model_df['ADR_True_False']==ADRTFx]

#ODR model #####################
#ADRtoODR_options = ['All'] + list(df['ODR_Model'].unique())
#ADRtoODR = c1.selectbox('ODR Model' , options=ADRtoODR_options)

#if ADRtoODR == 'All':
#        filtered_model_df = filtered_model_df # No filtering
#else:
#        filtered_model_df = filtered_model_df[filtered_model_df['ODR_Model'] == ADRtoODR] 



##### ODR Model###############
unique_values2 = filtered_model_df['ODR_Model'].str.split(', ').explode().unique()
unique_values2 = [str(value) for value in unique_values2]
unique_values2.sort()

# Create a multiselect dropdown to select multiple values
selected_values2 = c1.multiselect('Select ODR Model(s)', options=unique_values2)

# Create a selectbox to choose filtering options
filter_option2 = c1.selectbox('Select filter ODR ON/OFF', options=['All', 'Selected'])

if filter_option2 == 'All':
    filtered_model_df = filtered_model_df  # No filtering
else:
    # Filter DataFrame based on selected values
    filtered_model_df = filtered_model_df[filtered_model_df['ODR_Model'].str.split(', ').explode().isin(selected_values2)]

##ODR confirmation time ########
TIMEConfirm_options = ['All'] + sorted(filtered_model_df['ODR_CONF_TIME'].dropna().unique())
TIMEConfirm = c1.selectbox('ODR Confirmation Time' , options=TIMEConfirm_options)

if TIMEConfirm == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR_CONF_TIME'] == TIMEConfirm]   

##ODR Confirmation #############

ODRConfirm_options = ['All'] + list(filtered_model_df['ODR_Confirmation'].unique())
ODRConfirm = c1.selectbox('Confirmation' , options=ODRConfirm_options)

if ODRConfirm == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR_Confirmation'] == ODRConfirm]

#### ODR true or False##########
ODRTF_options = ['All'] + list(filtered_model_df['ODR_True_False'].unique())
ODRTFx = c1.selectbox('ODR True/False' , options=ODRTF_options)

if ODRTFx == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR_True_False'] == ODRTFx]

##### ODR max retrace time #####
RetTime_options = ['All'] + sorted(filtered_model_df['ODR MAX RET TIME'].dropna().unique())
RetTime = c1.selectbox('ODR Max Retrace Time' , options=RetTime_options)

if RetTime == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR MAX RET TIME'] == RetTime]   




##### RDR Model###############
unique_values = filtered_model_df['RDR_Model'].str.split(', ').explode().unique()
unique_values = [str(value) for value in unique_values]
unique_values.sort()


# Create a multiselect dropdown to select multiple values
selected_values = c1.multiselect('Select RDR Model(s)', options=unique_values)

# Create a selectbox to choose filtering options
filter_option = c1.selectbox('Select filtering RDR ON/OFF', options=['All', 'Selected'])

if filter_option == 'All':
    filtered_model_df = filtered_model_df  # No filtering
else:
    # Filter DataFrame based on selected values
    filtered_model_df = filtered_model_df[filtered_model_df['RDR_Model'].str.split(', ').explode().isin(selected_values)]

######## ODR CLOSE location ##########

ODRlocation_options = ['All'] + list(filtered_model_df['ODR Close Location'].unique())
ODRlocation = c1.selectbox('ODR Close Location' , options=ODRlocation_options)

if ODRlocation == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR Close Location'] == ODRlocation]

RDRcon_options = ['All'] + list(filtered_model_df['RDR_Confirmation'].unique())
RDRcon = c1.selectbox('RDR Confirmation' , options=RDRcon_options)

if RDRcon == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['RDR_Confirmation'] == RDRcon]


######## INTACT TRANSITION FILTERS #############################################



color_scale = alt.Scale(domain=['intact', 'broken'],
                        range=['#aec7e8', '#1f77b4'])
#aec7e8
#1f77b4
##ADR Mid Trans


ADRtrans_options = ['All'] + list(filtered_model_df['ADR Mid Trans'].unique())
ADRtrans = c2.selectbox('ADR Mid Trans' , options=ADRtrans_options)

if ADRtrans == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADR Mid Trans'] == ADRtrans]

ADRBx_options = ['All'] + list(filtered_model_df['ADR Mid Box'].unique())
ADRBx = c3.selectbox('ADR Mid Box' , options=ADRBx_options)

if ADRBx == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADR Mid Box'] == ADRBx]

ADRSess_options = ['All'] + list(filtered_model_df['ADR Mid Session'].unique())
ADRSess = c4.selectbox('ADR Mid Session' , options=ADRSess_options)

if ADRSess == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADR Mid Session'] == ADRSess]

ODRtrans_options = ['All'] + list(filtered_model_df['ODR Mid Trans'].unique())
ODRtrans = c2.selectbox('ODR Mid Trans' , options=ODRtrans_options)

if ODRtrans == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR Mid Trans'] == ODRtrans]

ODRBx_options = ['All'] + list(filtered_model_df['ODR Mid Box'].unique())
ODRBx = c3.selectbox('ODR Mid Box' , options=ODRBx_options)

if ODRBx == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR Mid Box'] == ODRBx]

ODRSess_options = ['All'] + list(filtered_model_df['ODR Mid Session'].unique())
ODRSess = c4.selectbox('ODR Mid Session' , options=ODRSess_options)

if ODRSess == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR Mid Session'] == ODRSess]

RDRtrans_options = ['All'] + list(filtered_model_df['ADR Mid RDR Trans'].unique())
RDRtrans = c2.selectbox('ADR Mid RDR Trans' , options=RDRtrans_options)

if RDRtrans == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADR Mid RDR Trans'] == RDRtrans]

RDRBx_options = ['All'] + list(filtered_model_df['ADR Mid RDR Box'].unique())
RDRBx = c3.selectbox('ADR Mid RDR Box' , options=RDRBx_options)

if RDRBx == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADR Mid RDR Box'] == RDRBx]

RDRSess_options = ['All'] + list(filtered_model_df['ADR Mid RDR Session'].unique())
RDRSess = c4.selectbox('ADR Mid RDR Session' , options=RDRSess_options)

if RDRSess == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADR Mid RDR Session'] == RDRSess]

word_counts = filtered_model_df['ADR Mid Trans'].value_counts().reset_index()
word_counts.columns = ['ADR Mid Trans', 'Count']

chart = alt.Chart(word_counts).mark_arc(innerRadius=30).encode(
        color=alt.Color('ADR Mid Trans:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True 
).properties(
    title='ADR Mid Trans',  # Set the chart title
    padding={'left': 0, 'right': 0, 'top': 0, 'bottom': 0}  # Adjust padding to leave space for the title
).configure_title(
    fontSize=12,  # Adjust the font size of the title if needed
    anchor='middle'
)

chart = chart.properties(height=150)

c2.altair_chart(chart, theme=None, use_container_width=True)

#ADR MID BOX


word_counts1 = filtered_model_df['ADR Mid Box'].value_counts().reset_index()
word_counts1.columns = ['ADR Mid Box', 'Count']

chartA = alt.Chart(word_counts1).mark_arc(innerRadius=30).encode(
        color=alt.Color('ADR Mid Box:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True 
).properties(
    title='ADR Mid Box',  # Set the chart title
    padding={'left': 0, 'right': 0, 'top': 0, 'bottom': 0}  # Adjust padding to leave space for the title
).configure_title(
    fontSize=12,  # Adjust the font size of the title if needed
    anchor='middle'
)

chartA = chartA.properties(height=150)

c3.altair_chart(chartA, theme=None, use_container_width=True)


### ADR MID SESSION @@



word_counts2 = filtered_model_df['ADR Mid Session'].value_counts().reset_index()
word_counts2.columns = ['ADR Mid Session', 'Count']

chartB = alt.Chart(word_counts2).mark_arc(innerRadius=30).encode(
        color=alt.Color('ADR Mid Session:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True
).properties(
    title='ADR Mid Session',  # Set the chart title
    padding={'left': 0, 'right': 0, 'top': 0, 'bottom': 0}  # Adjust padding to leave space for the title
).configure_title(
    fontSize=12,  # Adjust the font size of the title if needed
    anchor='middle'
)

chartB = chartB.properties(height=150)
c4.altair_chart(chartB, theme=None, use_container_width=True)

### ODR MID Transition



word_counts3 = filtered_model_df['ODR Mid Trans'].value_counts().reset_index()
word_counts3.columns = ['ODR Mid Trans', 'Count']

chartC = alt.Chart(word_counts3).mark_arc(innerRadius=30).encode(
        color=alt.Color('ODR Mid Trans:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True 
).properties(
    title='ODR Mid Trans',  # Set the chart title
    padding={'left': 0, 'right': 0, 'top': 0, 'bottom': 0}  # Adjust padding to leave space for the title
).configure_title(
    fontSize=12,  # Adjust the font size of the title if needed
    anchor='middle'
)

chartC = chartC.properties(height=150)

c2.altair_chart(chartC, theme=None, use_container_width=True)


##ODR MID BOX ####




word_counts4 = filtered_model_df['ODR Mid Box'].value_counts().reset_index()
word_counts4.columns = ['ODR Mid Box', 'Count']

chartD = alt.Chart(word_counts4).mark_arc(innerRadius=30).encode(
        color=alt.Color('ODR Mid Box:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True 
).properties(
    title='ODR Mid Box',  # Set the chart title
    padding={'left': 0, 'right': 0, 'top': 0, 'bottom': 0}  # Adjust padding to leave space for the title
).configure_title(
    fontSize=12,  # Adjust the font size of the title if needed
    anchor='middle'
)
chartD = chartD.properties(height=150)


c3.altair_chart(chartD, theme=None, use_container_width=True)

#### ODR MID SESSION######




word_counts5 = filtered_model_df['ODR Mid Session'].value_counts().reset_index()
word_counts5.columns = ['ODR Mid Session', 'Count']

chartE = alt.Chart(word_counts5).mark_arc(innerRadius=30).encode(
        color=alt.Color('ODR Mid Session:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True
).properties(
    title='ODR Mid Session',  # Set the chart title
    padding={'left': 0, 'right': 0, 'top': 0, 'bottom': 0}  # Adjust padding to leave space for the title
).configure_title(
    fontSize=12,  # Adjust the font size of the title if needed
    anchor='middle'
)

chartE = chartE.properties(height=150)
c4.altair_chart(chartE, theme=None, use_container_width=True)

##### RDR ADR MID TRansition 



word_counts6 = filtered_model_df['ADR Mid RDR Trans'].value_counts().reset_index()
word_counts6.columns = ['ADR Mid RDR Trans', 'Count']

chartF = alt.Chart(word_counts6).mark_arc(innerRadius=30).encode(
        color=alt.Color('ADR Mid RDR Trans:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True
).properties(
    title='ADR Mid RDR Trans',  # Set the chart title
    padding={'left': 0, 'right': 0, 'top': 0, 'bottom': 0}  # Adjust padding to leave space for the title
).configure_title(
    fontSize=12,  # Adjust the font size of the title if needed
    anchor='middle'
)

chartF = chartF.properties(height=150)

c2.altair_chart(chartF, theme=None, use_container_width=True)


#### RDR ADR MID BOX #########



word_counts7 = filtered_model_df['ADR Mid RDR Box'].value_counts().reset_index()
word_counts7.columns = ['ADR Mid RDR Box', 'Count']

chartG = alt.Chart(word_counts7).mark_arc(innerRadius=30).encode(
        color=alt.Color('ADR Mid RDR Box:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True
).properties(
    title='ADR Mid RDR Box',  # Set the chart title
    padding={'left': 0, 'right': 0, 'top': 0, 'bottom': 0}  # Adjust padding to leave space for the title
).configure_title(
    fontSize=12,  # Adjust the font size of the title if needed
    anchor='middle'
)
chartG = chartG.properties(height=150)

c3.altair_chart(chartG, theme=None, use_container_width=True)


###### RDR SESSION ############




word_counts8 = filtered_model_df['ADR Mid RDR Session'].value_counts().reset_index()
word_counts8.columns = ['ADR Mid RDR Session', 'Count']

chartH = alt.Chart(word_counts8).mark_arc(innerRadius=30).encode(
    color=alt.Color('ADR Mid RDR Session:N',scale=color_scale),
    theta='Count:Q'
).properties(
    height=150  # Set chart height
).configure_legend(
    disable=True
).properties(
    title='ADR Mid RDR Session',  # Set the chart title
    padding={'left': 0, 'right': 0, 'top': 0, 'bottom': 0}  # Adjust padding to leave space for the title
).configure_title(
    fontSize=12,  # Adjust the font size of the title if needed
    anchor='middle'
)


chartH = chartH.properties(height=150)
c4.altair_chart(chartH, theme=None, use_container_width=True)

Cc,Ch = c7.columns([1,2])

#####close location chart

bar_chart = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('ODR Close Location',sort='-y'),
        y=alt.Y('count():Q')
    ).properties(
    height=250,
    width=400
    ).configure_legend(
    disable=True
    )  # Set chart height

Cc.altair_chart(bar_chart,theme=None, use_container_width=True)


bar_chart2 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('RDR_Model:N',sort='-y'),
        y=alt.Y('count():Q')
    ).properties(
    height=250,
    width=325
    )

Ch.altair_chart(bar_chart2,theme = None, use_container_width=True)

bar_chart3 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('ODR_Model:N',sort='-y'),
        y=alt.Y('count():Q')
    ).properties(
    height=250,
    width=325
    )

c1.altair_chart(bar_chart3,theme = None, use_container_width=True)

selected_columns = ['ODR Close Price', 'TRANS MAX RET', 'TRANS MAX EXT', 'RDR IDR MID']

# Create a multiselect dropdown to select columns
column_order = ['ODR Close Price', 'TRANS MAX RET', 'TRANS MAX EXT', 'RDR IDR MID']

# Check if any columns are selected

# Melt the DataFrame to create a long-form DataFrame for the selected columns
melted_df = filtered_model_df[selected_columns].melt(var_name='Column', value_name='Value')

switch_state = Cc.checkbox("Pricemodels")

#melted_df['binned_value'] = pd.cut(melted_df['Value'], bins=pd.interval_range(start=0, end=10, freq=0.5))

normalized_data = df6

# Convert 'timestamp' column to datetime
normalized_data['timestamp'] = pd.to_datetime(normalized_data['timestamp'])

normalized_data['date'] = normalized_data['timestamp'].dt.date
normalized_data['time'] = normalized_data['timestamp'].dt.time

filtered_model_df['date'] = pd.to_datetime(filtered_model_df['date']).dt.date
if switch_state:
    st.write("The switch is ON")
    selected_option = c2.selectbox("Select an option", ["All"] + filtered_model_df['date'].tolist())
# Filter normalized_data based on the list of dates

    if selected_option == "All":
        date_list = filtered_model_df['date']
        selected_data = normalized_data[normalized_data['date'].isin(date_list)]
        selected_dates=date_list
    else:
        selected_dates = pd.to_datetime(filtered_model_df[filtered_model_df['date'] == selected_option]['date']).dt.date
        selected_data = normalized_data[normalized_data['date'].isin(selected_dates)]

    charts = []
    for date in selected_dates:
        data_for_date = selected_data[selected_data['date'] == date]
        chart = alt.Chart(data_for_date).mark_line().encode(
            x='time:T',
            y='normalized_close:Q',
            color=alt.value('blue'),  # Set color to blue for all lines
            tooltip=['time', 'normalized_close']
        ).properties(
            width=800,
            height=800,
            title=f"Normalized Close for {date}"
        )
        chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('08:25:00').time()]})).mark_rule(color='white',strokeDash=[3, 3]).encode(
            x='time:T'
        )
        chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('09:30:00').time()]})).mark_rule(color='white',strokeDash=[3, 3]).encode(
            x='time:T'
        )
        chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('04:00:00').time()]})).mark_rule(color='white',strokeDash=[3, 3]).encode(
            x='time:T'
        )
        chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('10:30:00').time()]})).mark_rule(color='white',strokeDash=[3, 3]).encode(
            x='time:T'
        )



    
        charts.append(chart)

    c5.altair_chart(alt.layer(*charts), use_container_width=True)   

    median_data = selected_data.groupby('time')['normalized_close'].median().reset_index()

    median_high_low_data = selected_data.groupby('time').agg({'normalized_high': 'median', 'normalized_low': 'median'}).reset_index()

    range_3_to_355_data = median_data[(median_data['time'] >= pd.to_datetime('03:00:00').time()) & 
                                     (median_data['time'] <= pd.to_datetime('03:55:00').time())]
    range_3_to_355_datav2 = median_high_low_data[(median_high_low_data['time'] >= pd.to_datetime('03:00:00').time()) & 
                                     (median_high_low_data['time'] <= pd.to_datetime('03:55:00').time())]
    max_close = range_3_to_355_data['normalized_close'].max()
    min_close = range_3_to_355_data['normalized_close'].min()
    max_high = pd.concat([range_3_to_355_datav2['normalized_high'], range_3_to_355_datav2['normalized_low']]).max()
    min_low = pd.concat([range_3_to_355_datav2['normalized_high'], range_3_to_355_datav2['normalized_low']]).min()

    mid=(max_close+min_close)/2

    range_930_to_1030_data = median_data[(median_data['time'] >= pd.to_datetime('09:30:00').time()) & 
                                     (median_data['time'] <= pd.to_datetime('10:25:00').time())]
    range_930_to_1030_datav2 = median_high_low_data[(median_high_low_data['time'] >= pd.to_datetime('09:30:00').time()) & 
                                     (median_high_low_data['time'] <= pd.to_datetime('10:25:00').time())]

    max_closeRDR = range_930_to_1030_data['normalized_close'].max()
    min_closeRDR = range_930_to_1030_data['normalized_close'].min()
    max_highRDR = pd.concat([range_930_to_1030_datav2['normalized_high'], range_930_to_1030_datav2['normalized_low']]).max()
    min_lowRDR = pd.concat([range_930_to_1030_datav2['normalized_high'], range_930_to_1030_datav2['normalized_low']]).min()
    midRDR=(max_closeRDR+min_closeRDR)/2

    if pd.to_datetime('02:55:00').time() in median_data['time'].tolist():
        close_255 = median_data[median_data['time'] == pd.to_datetime('02:55:00').time()]['normalized_close'].iloc[0]
    else:
        close_255 = None

    if pd.to_datetime('03:55:00').time() in median_data['time'].tolist():
        close_355 = median_data[median_data['time'] == pd.to_datetime('03:55:00').time()]['normalized_close'].iloc[0]
    else:
        close_355 = None

    if pd.to_datetime('09:25:00').time() in median_data['time'].tolist():
        close_925 = median_data[median_data['time'] == pd.to_datetime('09:25:00').time()]['normalized_close'].iloc[0]
    else:
        close_925 = None

    if pd.to_datetime('10:25:00').time() in median_data['time'].tolist():
        close_1025 = median_data[median_data['time'] == pd.to_datetime('10:25:00').time()]['normalized_close'].iloc[0]
    else:
        close_1025 = None

#close_255 = median_data[median_data['time'] == pd.to_datetime('02:55:00').time()]['normalized_close'].iloc[0]
#close_355 = median_data[median_data['time'] == pd.to_datetime('03:55:00').time()]['normalized_close'].iloc[0]

#close_925 = median_data[median_data['time'] == pd.to_datetime('09:25:00').time()]['normalized_close'].iloc[0]
#close_1025 = median_data[median_data['time'] == pd.to_datetime('10:25:00').time()]['normalized_close'].iloc[0]

# Plot the median high-low values using Altair
    chart = alt.Chart(median_high_low_data).mark_line().encode(
        x=alt.X('time:T'),
        y=alt.Y('normalized_high:Q', axis=alt.Axis(title=None)),
        tooltip=['time', 'normalized_high'],
        color=alt.value('#aec7e8')
    ).properties(
        width=800,
        height=800,
        title="Median High-Low Chart Across Selected Dates"
    )

    chart += alt.Chart(median_high_low_data).mark_line().encode(
        x=alt.X('time:T'),
        y=alt.Y('normalized_low:Q', axis=alt.Axis(title=None)),
        tooltip=['time', 'normalized_low'],
        color=alt.value('#1f77b4')
    )


    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('08:25:00').time()]})).mark_rule(color='white',strokeDash=[3, 3]).encode(
        x='time:T'
    )
    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('09:30:00').time()]})).mark_rule(color='white',strokeDash=[3, 3]).encode(
        x='time:T'
    )

    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('03:00:00').time(), pd.to_datetime('08:25:00').time()],
                                      'max_high': [max_high, max_high]})).mark_line(color='grey',strokeWidth=1).encode(
        x='time:T',
        y=alt.Y('max_high:Q', axis=alt.Axis(title=None)) 
    )

    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('03:00:00').time(), pd.to_datetime('08:25:00').time()],
                                      'min_low': [min_low, min_low]})).mark_line(color='grey',strokeWidth=1).encode(
        x='time:T',
        y=alt.Y('min_low:Q', axis=alt.Axis(title=None))
    )
    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('03:00:00').time(), pd.to_datetime('08:25:00').time()],
                                      'max_close': [max_close, max_close]})).mark_line(color='red', strokeDash=[5, 5],strokeWidth=1).encode(
        x='time:T',
        y=alt.Y('max_close:Q', axis=alt.Axis(title=None))
    )

    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('03:00:00').time(), pd.to_datetime('08:25:00').time()],
                                  'min_close': [min_close, min_close]})).mark_line(color='red', strokeDash=[5, 5],strokeWidth=1).encode(
        x='time:T',
        y=alt.Y('min_close:Q', axis=alt.Axis(title=None))
    )

    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('03:00:00').time(), pd.to_datetime('15:55').time()],
                                      'mid': [mid, mid]})).mark_line(color='blue').encode(
        x='time:T',
        y=alt.Y('mid:Q', axis=alt.Axis(title=None))
    )

    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('09:30:00').time(), pd.to_datetime('15:55:00').time()],
                                      'max_highRDR': [max_highRDR, max_highRDR]})).mark_line(color='grey',strokeWidth=1).encode(
        x='time:T',
        y=alt.Y('max_highRDR:Q', axis=alt.Axis(title=None)) 
    )

    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('09:30:00').time(), pd.to_datetime('15:55:00').time()],
                                      'min_lowRDR': [min_lowRDR, min_lowRDR]})).mark_line(color='grey',strokeWidth=1).encode(
        x='time:T',
        y=alt.Y('min_lowRDR:Q', axis=alt.Axis(title=None))
    )
    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('09:30:00').time(), pd.to_datetime('15:55:00').time()],
                                      'max_closeRDR': [max_closeRDR, max_closeRDR]})).mark_line(color='red', strokeDash=[5, 5],strokeWidth=1).encode(
        x='time:T',
        y=alt.Y('max_closeRDR:Q', axis=alt.Axis(title=None))
    )

    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('09:30:00').time(), pd.to_datetime('15:55:00').time()],
                                      'min_closeRDR': [min_closeRDR, min_closeRDR]})).mark_line(color='red', strokeDash=[5, 5],strokeWidth=1).encode(
        x='time:T',
        y=alt.Y('min_closeRDR:Q', axis=alt.Axis(title=None))
    )

    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('09:30:00').time(), pd.to_datetime('15:55').time()],
                                      'midRDR': [midRDR, midRDR]})).mark_line(color='blue').encode(
        x='time:T',
        y=alt.Y('midRDR:Q', axis=alt.Axis(title=None))
    )

    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('09:30:00').time(), pd.to_datetime('15:55').time()],
                                  'close_925': [close_925, close_925]})).mark_line(color='green').encode(
        x='time:T',
        y=alt.Y('close_925:Q', axis=alt.Axis(title=None))
    )
    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('10:30:00').time(), pd.to_datetime('15:55').time()],
                                      'close_1025': [close_1025, close_1025]})).mark_line(color='red').encode(
        x='time:T',
        y=alt.Y('close_1025:Q', axis=alt.Axis(title=None))
    )

    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('03:00:00').time(), pd.to_datetime('8:25').time()],
                                      'close_255': [close_255, close_255]})).mark_line(color='green').encode(
        x='time:T',
        y=alt.Y('close_255:Q', axis=alt.Axis(title=None))
    )
    chart += alt.Chart(pd.DataFrame({'time': [pd.to_datetime('3:55:00').time(), pd.to_datetime('8:25').time()],
                                      'close_355': [close_355, close_355]})).mark_line(color='red').encode(
        x='time:T',
        y=alt.Y('close_355:Q', axis=alt.Axis(title=None))
    )

    c6.altair_chart(chart, use_container_width=True)
else:
    c5.write("Price models are off")