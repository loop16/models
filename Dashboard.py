import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

github_raw_url = 'https://raw.githubusercontent.com/loop16/models/main/Dash.csv'


def load_data_from_github(url):
    try:
        # Read CSV data using pandas
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None
    

st.set_page_config(layout="wide")


df = load_data_from_github(github_raw_url)


c1, c7, c5, c6 = st.columns([1,3,4,4])

c2,c3,c4 = c7.columns(3)


##### GENERAL FILTERS ##############################################################################

#Day selector
DAY_options = ['All'] + list(df['Day'].unique())
DAYw = c1.selectbox('Day' , options=DAY_options)

filtered_model_df = df

if DAYw == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['Day'] == DAYw]

#ADR Model####################
RdrAdr_options = ['All'] + list(df['ADR_Model'].unique())
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
TIMEConfirm_options = ['All'] + sorted(df['ODR_CONF_TIME'].dropna().unique())
TIMEConfirm = c1.selectbox('ODR Confirmation Time' , options=TIMEConfirm_options)

if TIMEConfirm == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR_CONF_TIME'] == TIMEConfirm]   

##ODR Confirmation #############

ODRConfirm_options = ['All'] + list(df['ODR_Confirmation'].unique())
ODRConfirm = c1.selectbox('Confirmation' , options=ODRConfirm_options)

if ODRConfirm == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR_Confirmation'] == ODRConfirm]

#### ODR true or False##########
ODRTF_options = ['All'] + list(df['ODR_True_False'].unique())
ODRTFx = c1.selectbox('ODR True/False' , options=ODRTF_options)

if ODRTFx == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR_True_False'] == ODRTFx]

##### ODR max retrace time #####
RetTime_options = ['All'] + sorted(df['ODR MAX RET TIME'].dropna().unique())
RetTime = c1.selectbox('ODR Max Retrace Time' , options=RetTime_options)

if RetTime == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR MAX RET TIME'] == RetTime]   




##### RDR Model###############
unique_values = filtered_model_df['RDR_Model'].str.split(', ').explode().unique()

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

ODRlocation_options = ['All'] + list(df['ODR Close Location'].unique())
ODRlocation = c1.selectbox('ODR Close Location' , options=ODRlocation_options)

if ODRlocation == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR Close Location'] == ODRlocation]

RDRcon_options = ['All'] + list(df['RDR_Confirmation'].unique())
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


ADRtrans_options = ['All'] + list(df['ADR Mid Trans'].unique())
ADRtrans = c2.selectbox('ADR Mid Trans' , options=ADRtrans_options)

if ADRtrans == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADR Mid Trans'] == ADRtrans]

word_counts = filtered_model_df['ADR Mid Trans'].value_counts().reset_index()
word_counts.columns = ['ADR Mid Trans', 'Count']

chart = alt.Chart(word_counts).mark_arc(innerRadius=30).encode(
        color=alt.Color('ADR Mid Trans:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True  # Hide legend
)

chart = chart.properties(height=150)

c2.altair_chart(chart, theme=None, use_container_width=True)

#ADR MID BOX
ADRBx_options = ['All'] + list(df['ADR Mid Box'].unique())
ADRBx = c3.selectbox('ADR Mid Box' , options=ADRBx_options)

if ADRBx == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADR Mid Box'] == ADRBx]

word_counts1 = filtered_model_df['ADR Mid Box'].value_counts().reset_index()
word_counts1.columns = ['ADR Mid Box', 'Count']

chartA = alt.Chart(word_counts1).mark_arc(innerRadius=30).encode(
        color=alt.Color('ADR Mid Box:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True  # Hide legend
)

chartA = chartA.properties(height=150)

c3.altair_chart(chartA, theme=None, use_container_width=True)


### ADR MID SESSION @@

ADRSess_options = ['All'] + list(df['ADR Mid Session'].unique())
ADRSess = c4.selectbox('ADR Mid Session' , options=ADRSess_options)

if ADRSess == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADR Mid Session'] == ADRSess]

word_counts2 = filtered_model_df['ADR Mid Session'].value_counts().reset_index()
word_counts2.columns = ['ADR Mid Session', 'Count']

chartB = alt.Chart(word_counts2).mark_arc(innerRadius=30).encode(
        color=alt.Color('ADR Mid Session:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True  # Hide legend
)

chartB = chartB.properties(height=150)
c4.altair_chart(chartB, theme=None, use_container_width=True)

### ODR MID Transition

ODRtrans_options = ['All'] + list(df['ODR Mid Trans'].unique())
ODRtrans = c2.selectbox('ODR Mid Trans' , options=ODRtrans_options)

if ODRtrans == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR Mid Trans'] == ODRtrans]


word_counts3 = filtered_model_df['ODR Mid Trans'].value_counts().reset_index()
word_counts3.columns = ['ODR Mid Trans', 'Count']

chartC = alt.Chart(word_counts3).mark_arc(innerRadius=30).encode(
        color=alt.Color('ODR Mid Trans:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True  # Hide legend
)

chartC = chartC.properties(height=150)

c2.altair_chart(chartC, theme=None, use_container_width=True)


##ODR MID BOX ####

ODRBx_options = ['All'] + list(df['ODR Mid Box'].unique())
ODRBx = c3.selectbox('ODR Mid Box' , options=ODRBx_options)

if ODRBx == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR Mid Box'] == ODRBx]


word_counts4 = filtered_model_df['ODR Mid Box'].value_counts().reset_index()
word_counts4.columns = ['ODR Mid Box', 'Count']

chartD = alt.Chart(word_counts4).mark_arc(innerRadius=30).encode(
        color=alt.Color('ODR Mid Box:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True  # Hide legend
)

chartD = chartD.properties(height=150)


c3.altair_chart(chartD, theme=None, use_container_width=True)

#### ODR MID SESSION######


ODRSess_options = ['All'] + list(df['ODR Mid Session'].unique())
ODRSess = c4.selectbox('ODR Mid Session' , options=ODRSess_options)

if ODRSess == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ODR Mid Session'] == ODRSess]

word_counts5 = filtered_model_df['ODR Mid Session'].value_counts().reset_index()
word_counts5.columns = ['ODR Mid Session', 'Count']

chartE = alt.Chart(word_counts5).mark_arc(innerRadius=30).encode(
        color=alt.Color('ODR Mid Session:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True  # Hide legend
)

chartE = chartE.properties(height=150)
c4.altair_chart(chartE, theme=None, use_container_width=True)

##### RDR ADR MID TRansition 


RDRtrans_options = ['All'] + list(df['ADR Mid RDR Trans'].unique())
RDRtrans = c2.selectbox('ADR Mid RDR Trans' , options=RDRtrans_options)

if RDRtrans == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADR Mid RDR Trans'] == RDRtrans]

word_counts6 = filtered_model_df['ADR Mid RDR Trans'].value_counts().reset_index()
word_counts6.columns = ['ADR Mid RDR Trans', 'Count']

chartF = alt.Chart(word_counts6).mark_arc(innerRadius=30).encode(
        color=alt.Color('ADR Mid RDR Trans:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True  # Hide legend
)

chartF = chartF.properties(height=150)

c2.altair_chart(chartF, theme=None, use_container_width=True)


#### RDR ADR MID BOX #########

RDRBx_options = ['All'] + list(df['ADR Mid RDR Box'].unique())
RDRBx = c3.selectbox('ADR Mid RDR Box' , options=RDRBx_options)

if RDRBx == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADR Mid RDR Box'] == RDRBx]

word_counts7 = filtered_model_df['ADR Mid RDR Box'].value_counts().reset_index()
word_counts7.columns = ['ADR Mid RDR Box', 'Count']

chartG = alt.Chart(word_counts7).mark_arc(innerRadius=30).encode(
        color=alt.Color('ADR Mid RDR Box:N',scale=color_scale),
        theta='Count:Q',
    ).configure_legend(
    disable=True  # Hide legend
)

chartG = chartG.properties(height=150)

c3.altair_chart(chartG, theme=None, use_container_width=True)


###### RDR SESSION ############


RDRSess_options = ['All'] + list(df['ADR Mid RDR Session'].unique())
RDRSess = c4.selectbox('ADR Mid RDR Session' , options=RDRSess_options)

if RDRSess == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['ADR Mid RDR Session'] == RDRSess]

word_counts8 = filtered_model_df['ADR Mid RDR Session'].value_counts().reset_index()
word_counts8.columns = ['ADR Mid RDR Session', 'Count']

chartH = alt.Chart(word_counts8).mark_arc(innerRadius=30).encode(
    color=alt.Color('ADR Mid RDR Session:N',scale=color_scale),
    theta='Count:Q'
).properties(
    height=150  # Set chart height
).configure_legend(
    disable=True  # Hide legend
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

melted_df['binned_value'] = pd.cut(melted_df['Value'], bins=pd.interval_range(start=0, end=10, freq=0.5))

# Create the box plot
box_plot = alt.Chart(melted_df).mark_boxplot(color='white',size=150).encode(
        x=alt.X('Column:N', title='Column', axis=alt.Axis(labelAngle=0),sort=column_order),
        y=alt.Y('Value:Q'),
        color=alt.value('#4c78a8'),
).properties(
    height=500
    )
        
    

# Display the box plot

c5.altair_chart(box_plot, theme=None, use_container_width=True)

layered_histogram = alt.Chart(melted_df).transform_filter(
    alt.FieldRangePredicate(field='Value', range=[-12.5, 12.5])).mark_bar(
       opacity=0.3,
       binSpacing=0,
).encode(
        x=alt.X('Value:Q', bin=alt.Bin(step=0.5)),
        y=alt.Y('count()', stack=None),
        color='Column:N'
).properties(
    height=400
    )
c6.altair_chart(layered_histogram, use_container_width=True)


c5A,c5B=c5.columns(2)


bar_chart16 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('TRANS MAX RET:Q',bin=alt.Bin(step=0.5)),
        y=alt.Y('count():Q')
    ).properties(
    height=250
    
    )

bar_chart17 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('TRANS MAX EXT:Q',bin=alt.Bin(step=0.5)),
        y=alt.Y('count():Q')
    ).properties(
    height=250
    
    )
c5A.altair_chart(bar_chart16,theme=None, use_container_width=True)
c5B.altair_chart(bar_chart17,theme=None, use_container_width=True)

time_range = pd.date_range( "08:30", "09:25", freq="5min")
time_values = [time.strftime("%H:%M") for time in time_range]

bar_chart3 = alt.Chart(filtered_model_df).mark_bar().encode(
x=alt.X('TRANS LOW TIME:N', sort=alt.SortField(field='TRANS LOW TIME', order='ascending'), axis=alt.Axis(values=time_values)),
y=alt.Y('count():Q')
).properties(
    height=200
    
    )
c5A.altair_chart(bar_chart3,theme=None, use_container_width=True)

bar_chart3 = alt.Chart(filtered_model_df).mark_bar().encode(
x=alt.X('TRANS HIGH TIME:N', sort=alt.SortField(field='TRANS HIGH TIME', order='ascending'), axis=alt.Axis(values=time_values)),
y=alt.Y('count():Q')
).properties(
    height=200
    
    )
c5B.altair_chart(bar_chart3, theme=None, use_container_width=True)



numeric_values1 = filtered_model_df['ODR Close Price'].apply(pd.to_numeric, errors='coerce')
numeric_values2 = filtered_model_df['TRANS MAX RET'].apply(pd.to_numeric, errors='coerce')
numeric_values3 = filtered_model_df['TRANS MAX EXT'].apply(pd.to_numeric, errors='coerce')
numeric_values4 = filtered_model_df['RDR IDR MID'].apply(pd.to_numeric, errors='coerce')

medianClose=numeric_values1.median()
medianRET=numeric_values2.median()
medianEXT=numeric_values3.median()
medianMID=numeric_values4.median()

medianClose_rounded = round(medianClose, 2)
medianRET_rounded = round(medianRET, 2)
medianEXT_rounded = round(medianEXT, 2)
medianMID_rounded = round(medianMID, 2)

c6.write(f"Median Close: {medianClose_rounded}&nbsp;  |  Median Trans RET: {medianRET_rounded}&nbsp;  |  Median Trans EXT: {medianEXT_rounded}&nbsp;  |  Median IDR MID: {medianMID_rounded}")

c6A,c6B = c6.columns(2)

bar_chart16 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('rdr_idr_highSD',bin=alt.Bin(step=0.5)),
        y=alt.Y('count():Q')
    ).properties(
    height=250
    
    )

bar_chart17 = alt.Chart(filtered_model_df).mark_bar().encode(
        x=alt.X('rdr_idr_lowSD:Q',bin=alt.Bin(step=0.5)),
        y=alt.Y('count():Q')
    ).properties(
    height=250
    
    )
c6A.altair_chart(bar_chart16,theme=None, use_container_width=True)
c6B.altair_chart(bar_chart17,theme=None, use_container_width=True)


c6AA,c6BB,c6CC = c6.columns(3)


#####RDR BOX CONFIRMS######
RDRbox_options = ['All'] + list(filtered_model_df['RDR Box Color'].unique())
RDRbox = c6AA.selectbox('RDR Box Color' , options=RDRbox_options)

if RDRbox == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['RDR Box Color'] == RDRbox]

RDRLong_options = ['All'] + list(filtered_model_df['RDR_Confirmation'].unique())
RDRLong = c6BB.selectbox('RDR_Confirmation' , options=RDRLong_options)

if RDRLong == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['RDR_Confirmation'] == RDRLong]

RDRTRUE_options = ['All'] + list(filtered_model_df['RDR_True_False'].unique())
RDRxTRUE = c6CC.selectbox('RDR_True_False' , options=RDRTRUE_options)

if RDRxTRUE == 'All':
        filtered_model_df = filtered_model_df # No filtering
else:
        filtered_model_df = filtered_model_df[filtered_model_df['RDR_True_False'] == RDRxTRUE]





word_counts9 = filtered_model_df['RDR Box Color'].value_counts().reset_index()
word_counts9.columns = ['RDR Box Color', 'Count']

chartI = alt.Chart(word_counts9).mark_arc(innerRadius=30).encode(
    color=alt.Color('RDR Box Color:N',scale=alt.Scale(scheme='category20')),
    theta='Count:Q'
).properties(
    height=150  # Set chart height
).configure_legend(
    disable=True  # Hide legend
)


chartI = chartI.properties(height=150)
c6AA.altair_chart(chartI, use_container_width=True)

word_counts10 = filtered_model_df['RDR_Confirmation'].value_counts().reset_index()
word_counts10.columns = ['RDR_Confirmation', 'Count']

chartJ = alt.Chart(word_counts10).mark_arc(innerRadius=30).encode(
    color=alt.Color('RDR_Confirmation:N',scale=alt.Scale(scheme='category20')),
    theta='Count:Q'
).properties(
    height=150  # Set chart height
).configure_legend(
    disable=True  # Hide legend
)


chartJ = chartJ.properties(height=150)
c6BB.altair_chart(chartJ, use_container_width=True)


word_counts11 = filtered_model_df['RDR_True_False'].value_counts().reset_index()
word_counts11.columns = ['RDR_True_False', 'Count']

chartk = alt.Chart(word_counts11).mark_arc(innerRadius=30).encode(
    color=alt.Color('RDR_True_False:N',scale=alt.Scale(scheme='category20')),
    theta='Count:Q'
).properties(
    height=150  # Set chart height
).configure_legend(
   disable=True  # Hide legend
)


# Display the combined chart
c6CC.altair_chart(chartk, use_container_width=True)



finalDf=filtered_model_df
lengthwe=len(filtered_model_df)

Cc.write(f"Total Data: {lengthwe}")

string_to_remove = 'NO_CONF'

finalDf['RDR_True_False'] = finalDf['RDR_True_False'].replace(string_to_remove, '')
finalDf['RDR Box Color'] = finalDf['RDR_Confirmation'].replace(string_to_remove, '')

Truefalse_counts = finalDf['RDR_True_False'].value_counts()
ConfirmationCounts=finalDf['RDR_Confirmation'].value_counts()
GreenRedCounts = finalDf['RDR Box Color'].value_counts()


percent_true = (Truefalse_counts['True'] /len(finalDf) ) * 100




try:
    percent_long = (ConfirmationCounts['Long'] / len(finalDf)) * 100
except Exception as e:
    percent_long = 0 



percent_true_rounded = round(percent_true, 2)
percent_longrounded = round(percent_long, 2)

c6BB.write(f" RDR Long: {percent_longrounded}%")
c6CC.write(f" RDR True: {percent_true_rounded}%")

