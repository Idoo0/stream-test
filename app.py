# import pandas as pd
# import streamlit as st
import plotly.graph_objects as go

# st.title("Sentimen Analysis Dashboard")

# st.markdown("Prototype v0.0")

# def 

import streamlit as st
import pandas as pd
import plotly.express as px

st.text("Last updated: June 28th 2024 at 22:12 (UTC+8)")

with st.sidebar:
  st.header("Configuration")
  upload_file = st.file_uploader("Choose a a file")

# Set light mode theme using custom CSS
light_mode_css = """
    <style>
        body {
            color: #2f2f2f;
            background-color: #ffffff;
        }
        .st-dq {
            color: #2f2f2f;
        }
    </style>
"""
st.markdown(light_mode_css, unsafe_allow_html=True)

# Load data
data = pd.read_csv("DATA_VIS.CSV")

############################################## PIE CHART ################################

# Calculate total positive and negative mentions
total_positive = data['Positive'].sum()
total_negative = data['Negative'].sum()

# Calculate percentages
positive_percentage = (total_positive / (total_positive + total_negative)) * 100
negative_percentage = (total_negative / (total_positive + total_negative)) * 100

# Determine the most used sentiment
most_used_sentiment = 'Positive' if total_positive >= total_negative else 'Negative'

# Create a donut chart
fig = go.Figure(data=[go.Pie(
    labels=['Positive', 'Negative'],
    values=[total_positive, total_negative],
    hole=0.6,
    marker=dict(colors=['#00cc96', '#EF553B']),
    textinfo='none'
)])

# Add a central annotation
fig.add_annotation(text=most_used_sentiment,
                   x=0.5, y=0.5, showarrow=False,
                   font=dict(size=24, color='black'))

# Update layout for title and subtitle
fig.update_layout(
    title={
        'text': "Analysis Result<br><span style='font-size:16px;'>Sentiment analysis</span>",
        'y':0.92,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    annotations=[
        dict(
            x=0.5,
            y=-0.1,
            showarrow=False,
            text=f"<span style='color:#00cc96;'>●</span> Positive - {positive_percentage:.2f}%<br><span style='color:#EF553B;'>●</span> Negative - {negative_percentage:.2f}%",
            xanchor='center',
            yanchor='top'
        )
    ],
    showlegend=False,
    margin=dict(t=100, b=100)
)

# Streamlit app
st.title('Sentiment Analysis Dashboard')
st.plotly_chart(fig)

############################################## BAR PLOT ################################

# import streamlit as st
# import pandas as pd
import altair as alt

# # Load your CSV data (replace 'your_data.csv' with the actual file path)
# data = pd.read_csv('your_data.csv')

# Create a bar chart for positive mentions
positive_chart = alt.Chart(data).mark_bar().encode(
    x='Entity',
    y='Positive',
    color=alt.value('green'),
    tooltip=['Entity', 'Positive']
).properties(
    title='Positive Mentions by Entity'
)


# Create a bar chart for negative mentions
negative_chart = alt.Chart(data).mark_bar().encode(
    x='Entity',
    y='Negative',
    color=alt.value('red'),
    tooltip=['Entity', 'Negative']
).properties(
    title='Negative Mentions by Entity'
)

# Create a bar chart for total mentions
total_chart = alt.Chart(data).mark_bar().encode(
    x='Entity',
    y='total_mention',
    color=alt.value('blue'),
    tooltip=['Entity', 'total_mention']
).properties(
    title='Total Mentions by Entity'
)

# Combine the charts into a single layout
st.title('Sentiment Analysis Dashboard')
st.altair_chart(positive_chart | negative_chart | total_chart, use_container_width=True)

####################################################### ORIGINAL #####################

# Calculate keypoints
most_positive = data.loc[data['Positive'].idxmax()]['Entity']
most_negative = data.loc[(data['Negative'] - data['Positive']).idxmax()]['Entity']
most_mention = data.loc[data['total_mention'].idxmax()]['Entity']
less_mention = data.loc[data['total_mention'].idxmin()]['Entity']

# CSS style for boxed key points
keypoint_style = """
    <style>
        .keypoint-box {
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 10px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
            background-color: #f0f0f0;
            color: #000000;
            font-size: 25px;
        }
    </style>
"""

# Inject CSS for boxed key points
st.markdown(keypoint_style, unsafe_allow_html=True)

# Layout keypoints in two rows
st.header("Keypoints", anchor=None)
col1, col2 = st.columns(2)

with col1:
    st.markdown(f'<div class="keypoint-box">Most Positive<br><span style="font-size: 15px">{most_positive}<span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="keypoint-box">Most Negative<br><span style="font-size: 15px">{most_negative}<span></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="keypoint-box">Most Mention<br> <span style="font-size: 15px">{most_mention}<span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="keypoint-box">Less Mention<br><span style="font-size: 15px">{less_mention}<span></div>', unsafe_allow_html=True)

st.header('Data Table')
st.dataframe(data, height=600, width=1500)  # Increase the height and width for better visualization

# Prepare data for the horizontal bar chart with two bars for each entity
top10_mentions = data.nlargest(10, 'total_mention')
melted_data = pd.melt(top10_mentions, id_vars=['Entity'], value_vars=['Positive', 'Negative'],
                      var_name='Sentiment', value_name='Mentions')

# Plot horizontal bar chart
st.header("Top 10 Entities by Total Mentions", anchor=None)
bar_chart = px.bar(melted_data,
                   x='Mentions', y='Entity', color='Sentiment', orientation='h',
                   title='Top 10 Entities by Positive and Negative Mentions',
                   hover_data=['Mentions', 'Sentiment'],
                   color_discrete_map={'Positive': 'green', 'Negative': 'red'},
                   labels={'Mentions': 'Total Mentions', 'Entity': 'Entity'},
                   width=1000, height=600)  # Adjust size as needed
bar_chart.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(bar_chart, use_container_width=True)

st.header("Top 10 Entities by Positive Mentions", anchor=None)
top10_positive = data.nlargest(10, 'Positive')
pie_chart = px.pie(top10_positive, values='Positive', names='Entity',
                   title='Top 10 Entities by Positive Mentions',
                   hover_data=['Positive', 'Negative', 'total_mention'],
                   width=1000, height=600)  # Adjust size as needed
st.plotly_chart(pie_chart, use_container_width=True)