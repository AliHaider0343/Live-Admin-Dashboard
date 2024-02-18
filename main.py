import base64
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def home():
    st.image("Images/LogoTransparent.png", caption="Delivering Happiness", width=400)
    st.title("Monitor and Improve Support Agents Behavior With our AI")
    st.write(
        "Customer ratings only provide 2-5% of data to enhance agent performance.Our AI analyzes all conversations to improve customer service.")

def plot_graphs(df):

    col1, col2,col3=st.columns([1,1,1])
    with col1:
        conversation_category_counts = df['Conversation Catgegory'].value_counts().reset_index()
        # Plotting the pie chart using Plotly
        fig = px.pie(conversation_category_counts, values='count', names='Conversation Catgegory',
                     title='Conversation Category Distribution')
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        # Create a scatter plot
        fig = px.scatter(df, x='chat_start_time', y='chat_end_time', hover_data=['Conversations'],
                         labels={'chat_start_time': 'Chat Start Time', 'chat_end_time': 'Chat End Time'},
                         title='Conversation Start Time vs. End Time')
        st.plotly_chart(fig,use_container_width=True)

    with col3:
        # Convert Total Engaugment Time to seconds for better visualization
        df['Total Engaugment Time'] = df['Total Engaugment Time'].dt.total_seconds()
        # Plot engagement time individually
        fig1 = px.scatter(df, x=df.index, y='Total Engaugment Time', title='Engagement Time')
        st.plotly_chart(fig1,use_container_width=True)

    df['Total Engaugment Time'] = pd.to_timedelta(df['Total Engaugment Time']).dt.total_seconds()
    agent_engagement = df.groupby('Agent Name')['Total Engaugment Time'].mean().reset_index()
    fig = px.bar(agent_engagement, x='Agent Name', y='Total Engaugment Time',
                     title='Average Engagement Time per Agent',
                     labels={'Agent Name': 'Agent Name', 'Total Engaugment Time': 'Average Engagement Time (seconds)'})
    st.plotly_chart(fig,use_container_width=True)

    agent_engagement = df.groupby('Customer Name')['Total Engaugment Time'].mean().reset_index()
    fig = px.bar(agent_engagement, x='Customer Name', y='Total Engaugment Time',
                     title='Average Engagement Time per Customer',
                     labels={'Agent Name': 'Customer Name', 'Total Engaugment Time': 'Average Engagement Time (seconds)'})
    st.plotly_chart(fig,use_container_width=True)

    col1,col2=st.columns([1,1])
    with col1:
        agent_conversations_count = df['Agent Name'].value_counts().reset_index()
        agent_conversations_count.columns = ['Agent Name', 'Chats Count']
        agent_conversations_count['Percentage'] = (agent_conversations_count['Chats Count'] / agent_conversations_count['Chats Count'].sum()) * 100
        fig = px.pie(agent_conversations_count, values='Chats Count', names='Agent Name',
                     title='Number and Percentage of Conversations by Agent')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        agent_stats = df.groupby('Agent Name')[['Average Responce Time', 'Average Delay Time']].mean().reset_index()
        fig = go.Figure(data=[
            go.Bar(name='Average Responce Time', x=agent_stats['Agent Name'], y=agent_stats['Average Responce Time'],
                   marker_color='rgb(55, 83, 109)'),
            go.Bar(name='Average Delay Time', x=agent_stats['Agent Name'], y=agent_stats['Average Delay Time'],
                   marker_color='rgb(26, 118, 255)')
        ])
        fig.update_layout(barmode='group', xaxis_tickangle=-45, title='Average Response Time and Average Delay Time by Agent',
                          xaxis_title='Agent Name', yaxis_title='Time (seconds)')

        st.plotly_chart(fig,use_container_width=True)


    df['Date of Conversation'] = pd.to_datetime(df['chat_end_time'])
    df_grouped_for_responce = df.groupby(['Date of Conversation', 'Agent Name'])[['Average Responce Time']].mean().reset_index()
    fig = px.line(df_grouped_for_responce, x='Date of Conversation', y='Average Responce Time', color='Agent Name',
                  title='Average Response Time of Agents Over Time',
                  labels={'Date of Conversation': 'Date of Conversation', 'Average Response Time': 'Average Responce Time'})
    st.plotly_chart(fig,use_container_width=True)



    df_grouped = df.groupby(['Date of Conversation', 'Agent Name'])[['Average Delay Time']].mean().reset_index()
    # Plot using Plotly
    fig = px.line(df_grouped, x='Date of Conversation', y='Average Delay Time', color='Agent Name',
                  title='Average Delay Time of Agents Over Time',
                  labels={'Date of Conversation': 'Date of Conversation', 'Average Delay Time': 'Average Delay Time'})
    st.plotly_chart(fig,use_container_width=True)

    col1,col2=st.columns([1,1])
    with col1:
        df_percentage = df.groupby(['Agent Name', 'Conversation Catgegory']).size() / df.groupby('Agent Name').size() * 100
        df_percentage = df_percentage.reset_index(name='Percentage')
        fig = px.bar(df_percentage, x='Agent Name', y='Percentage', color='Conversation Catgegory',
                     title='Percentage of Conversation Categories Processed by Each Agent',
                     labels={'Agent Name': 'Agent Name', 'Percentage': 'Percentage (%)',
                             'Conversation Catgegory': 'Conversation Catgegory'})
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        satisfied_percentage = df[df['Customer Satisfied'] == True]['Customer Satisfied'].count() / len(df) * 100
        not_satisfied_percentage = df[df['Customer Satisfied'] == False]['Customer Satisfied'].count() / len(df) * 100
        fig1 = px.pie(names=['Satisfied', 'Not Satisfied'], values=[satisfied_percentage, not_satisfied_percentage],
                      title='Customer Satisfaction Percentage')
        agent_satisfaction = df.groupby(['Agent Name', 'Conversation Catgegory', 'Customer Satisfied']).size().unstack(
            fill_value=0).reset_index()
        agent_satisfaction_melted = pd.melt(agent_satisfaction, id_vars=['Agent Name', 'Conversation Catgegory'],
                                            var_name='Satisfaction', value_name='Count')
        fig2 = px.bar(agent_satisfaction_melted, x='Agent Name', y='Count', color='Satisfaction', barmode='group',
                      facet_col='Conversation Catgegory', title='Agent Satisfaction by Category')

        st.plotly_chart(fig1,use_container_width=True)

    st.plotly_chart(fig2,use_container_width=True)

    col1,col2=st.columns([1,1])
    with col1:
        df_grouped = df.groupby(['Agent Name', 'Agent Empathy Extent']).size().reset_index(name='Count')
        fig = px.bar(df_grouped, x='Agent Name', y='Count', color='Agent Empathy Extent',
                     labels={'Agent Name': 'Agent Name', 'Count': 'Number of Conversations'},
                     title='Empathy Extent Distribution in Conversations by Agent Name')
        fig.update_layout(barmode='group')
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        df_grouped = df.groupby(['Agent Name', 'Agent Politeness Extent']).size().reset_index(name='Count')
        fig = px.bar(df_grouped, x='Agent Name', y='Count', color='Agent Politeness Extent',
                     labels={'Agent Name': 'Agent Name', 'Count': 'Number of Conversations'},
                     title='Politeness Extent Distribution in Conversations by Agent Name')
        fig.update_layout(barmode='group')
        st.plotly_chart(fig,use_container_width=True)

    col1,col2=st.columns([1,1])

    with col1:
        df_grouped = df.groupby(['Agent Name', 'Agent Tone']).size().reset_index(name='Count')
        fig1 = px.bar(df_grouped, x='Agent Name', y='Count', color='Agent Tone',
                      labels={'Agent Name': 'Agent Name', 'Count': 'Number of Conversations'},
                      title='Agent Tone Distribution in Conversations')
        fig1.update_layout(barmode='group')
        st.plotly_chart(fig1,use_container_width=True)

    with col2:
        # Group by Agent Name and calculate sentiment class count, mean polarity, and subjectivity scores
        grouped_df = df.groupby(['Agent Name', 'Converastion Sentiment']).size().unstack(fill_value=0).reset_index()
        mean_scores = df.groupby('Agent Name').agg({'Polarity Score': 'mean', 'Subjectivity Score': 'mean'}).reset_index()
        grouped_df = pd.merge(grouped_df, mean_scores, on='Agent Name')
        sentiment_class_names = grouped_df.columns[1:-2]
        fig = go.Figure()
        for sentiment_class in sentiment_class_names:
            fig.add_trace(go.Bar(x=grouped_df['Agent Name'], y=grouped_df[sentiment_class],
                                 name=sentiment_class, marker_color='blue'))
            fig.add_trace(go.Bar(x=grouped_df['Agent Name'], y=grouped_df['Polarity Score'],
                                 name='Mean Polarity Score', marker_color='orange'))
            fig.add_trace(go.Scatter(x=grouped_df['Agent Name'], y=grouped_df['Subjectivity Score'],
                                      mode='markers', name='Mean Subjectivity Score', marker=dict(color='green', size=10)))
            fig.update_layout(barmode='group', title='Sentiment Analysis for Each Agent',
                              xaxis_title='Agent Name', yaxis_title='Count/Score')

        st.plotly_chart(fig,use_container_width=True)
def base_data(merged_data):
    filtered_df=merged_data
    st.markdown('---')
    st.subheader('Chats Data Filters')
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        agent_filter = st.selectbox('Select Agent', ['All'] + merged_data['Agent Name'].unique().tolist())
        if agent_filter != 'All':
            filtered_df = filtered_df[filtered_df['Agent Name'] == agent_filter]
    with col2:
        customer_filter = st.selectbox('Select Customer', ['All'] + merged_data['Customer Name'].unique().tolist())
        if customer_filter != 'All':
            filtered_df = filtered_df[filtered_df['Customer Name'] == customer_filter]
    with col3:
        cat_filter = st.selectbox('Select Conversation Category',
                                  ['All'] + merged_data['Conversation Catgegory'].unique().tolist())
        if cat_filter != 'All':
            filtered_df = filtered_df[filtered_df['Conversation Catgegory'] == cat_filter]
    with col4:
        satisfaction_filter = st.selectbox('Select Satisfaction Status',
                                           ['All'] + merged_data['Customer Satisfied'].unique().tolist())
        if satisfaction_filter != 'All':
            filtered_df = filtered_df[filtered_df['Customer Satisfied'] == satisfaction_filter]

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        tone_filter = st.selectbox('Select Tone', ['All'] + merged_data['Agent Tone'].unique().tolist())
        if tone_filter != 'All':
            filtered_df = filtered_df[filtered_df['Agent Tone'] == tone_filter]
    with col2:
        sentiment_filter = st.selectbox('Select Sentiment Class',
                                        ['All'] + merged_data['Converastion Sentiment'].unique().tolist())
        if sentiment_filter != 'All':
            filtered_df = filtered_df[filtered_df['Converastion Sentiment'] == sentiment_filter]
    with col3:
        empathy_filter = st.selectbox('Select Agent Empathy Extent',
                                      ['All'] + merged_data['Agent Empathy Extent'].unique().tolist())
        if empathy_filter != 'All':
            filtered_df = filtered_df[filtered_df['Agent Empathy Extent'] == empathy_filter]
    with col4:
        politness_filter = st.selectbox('Select Agent Politeness Extent',
                                        ['All'] + merged_data['Agent Politeness Extent'].unique().tolist())
        if politness_filter != 'All':
            filtered_df = filtered_df[filtered_df['Agent Politeness Extent'] == politness_filter]

    st.markdown('---')

    if len(filtered_df) > 0:
        average_engagement_time_minutes = filtered_df['Total Engaugment Time'].mean().total_seconds() / 60
        filtered_df['Average Responce Time'] = pd.to_numeric(filtered_df['Average Responce Time'], errors='coerce')
        filtered_df['Average Delay Time'] = pd.to_numeric(filtered_df['Average Delay Time'], errors='coerce')
        filtered_df['Polarity Score'] = pd.to_numeric(filtered_df['Polarity Score'], errors='coerce')

        average_responce_time = filtered_df['Average Responce Time'].mean()
        average_delay_time = filtered_df['Average Delay Time'].mean()
        average_polaity_score = filtered_df['Polarity Score'].mean()

        col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
        with col1:
            st.metric(label="Total Chats", value=len(filtered_df))
        with col2:
            st.metric(label="Sales Support Chats",
                      value=f'{round(len(filtered_df[filtered_df["Conversation Catgegory"] == "Sales Support"]) / len(filtered_df) * 100, 2)} %')
        with col3:
            st.metric(label="Customer Support Chats",
                      value=f'{round(len(filtered_df[filtered_df["Conversation Catgegory"] == "Customer Support"]) / len(filtered_df) * 100, 2)} %')
        with col4:
            satisfation = filtered_df["Customer Satisfied"].value_counts()
            st.metric(label="Satisfaction Percentage",
                      value=f'{round(satisfation[True] / len(filtered_df) * 100, 2)} %')
        with col5:
            st.metric(label="Total Customers", value=(filtered_df['Customer Name'].nunique()))
        with col6:
            st.metric(label="Total Agents", value=(filtered_df['Agent Name'].nunique()))

        col7, col8, col9, col10, col11, col12 = st.columns([1, 1, 1, 1, 1, 1])
        with col7:
            st.metric(label="AVG Engaugement Time (Minutes)", value=f"{round(average_engagement_time_minutes, 2)}")
        with col8:
            st.metric(label="AVG Response (Seconds)", value=f"{round(average_responce_time, 2)}")
        with col9:
            st.metric(label="AVG Delay (Seconds)", value=f"{round(average_delay_time, 2)}")
        with col10:
            st.metric(label="AVG Polarity Score", value=f"{round(average_polaity_score, 2)}")
        with col11:
            empathy_high_percentage = f'{round((filtered_df["Agent Empathy Extent"].value_counts(normalize=True).get("High", 0) * 100), 2)} %'
            st.metric(label="High Empathy", value=empathy_high_percentage)
        with col12:
            politeness_high_percentage = f'{round((filtered_df["Agent Politeness Extent"].value_counts(normalize=True).get("High", 0) * 100), 2)} %'
            st.metric(label="High Politeness", value=politeness_high_percentage)

        st.markdown('---')
        st.subheader('Processed Chats')
        st.write(filtered_df)
        plot_graphs(filtered_df)
    else:
        st.warning('No Data Available after Filteration.')
def plot_graphs_for_sales_support(df):
    # Calculate percentage of leads generated
    leads_generated_percentage = df['Lead-Generated'].value_counts(normalize=True) * 100

    # Plot for leads generated/not generated
    fig_leads = go.Figure(go.Pie(labels=leads_generated_percentage.index, values=leads_generated_percentage.values,
                                 textinfo='label+percent', name='Lead Generation Status'))

    fig_leads.update_layout(title='Percentage of Leads Generated/Not Generated')

    # Calculate percentage participation of reasons
    reasons_generated_percentage = df[df['Lead-Generated']]['Reason'].value_counts(normalize=True) * 100
    reasons_not_generated_percentage = df[~df['Lead-Generated']]['Reason'].value_counts(normalize=True) * 100

    # Plot for reasons behind lead generation
    fig_reasons_generated = go.Figure(
        go.Pie(labels=reasons_generated_percentage.index, values=reasons_generated_percentage.values,
               textinfo='label+percent', name='Reasons - Generated'))

    fig_reasons_generated.update_layout(title='Reasons Behind Lead Generation')

    # Plot for reasons behind lead not generation
    fig_reasons_not_generated = go.Figure(
        go.Pie(labels=reasons_not_generated_percentage.index, values=reasons_not_generated_percentage.values,
               textinfo='label+percent', name='Reasons - Not Generated'))

    fig_reasons_not_generated.update_layout(title='Reasons Behind Lead Not Generated')



    col1,col2=st.columns([1,1])
    with col1:
        st.plotly_chart(fig_leads,user_container_width=True)
    with col2:
        # Count leads generated and not generated by each agent
        leads_generated = df[df['Lead-Generated']].groupby('Agent Name').size().reset_index(name='Lead Generated')
        leads_not_generated = df[~df['Lead-Generated']].groupby('Agent Name').size().reset_index(
            name='Lead Not Generated')

        # Merge the two dataframes to ensure all agents are included
        merged_df = pd.merge(leads_generated, leads_not_generated, on='Agent Name', how='outer').fillna(0)

        # Plot
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=merged_df['Agent Name'],
            y=merged_df['Lead Generated'],
            name='Leads Generated',
            marker_color='skyblue'
        ))

        fig.add_trace(go.Bar(
            x=merged_df['Agent Name'],
            y=merged_df['Lead Not Generated'],
            name='Leads Not Generated',
            marker_color='salmon'
        ))

        fig.update_layout(
            barmode='group',
            title='Leads Generated and Not Generated by Each Agent',
            xaxis_title='Agent Name',
            yaxis_title='Number of Leads',
            legend_title='Lead Status'
        )
        st.plotly_chart(fig,user_container_width=True)
    col3,col4=st.columns([1,1])
    with col3:
        st.plotly_chart(fig_reasons_generated,user_container_width=True)
    with col4:
        st.plotly_chart(fig_reasons_not_generated,user_container_width=True)

    df['chat_end_time'] = pd.to_datetime(df['chat_end_time'])
    leads_by_agent_date = df.groupby(['Agent Name', df['chat_end_time'].dt.date]).size().reset_index(name='Lead Count')
    pivot_leads = leads_by_agent_date.pivot(index='chat_end_time', columns='Agent Name', values='Lead Count').fillna(0)
    cumulative_leads = pivot_leads.cumsum()
    fig = go.Figure()
    for agent in cumulative_leads.columns:
        fig.add_trace(go.Scatter(x=cumulative_leads.index, y=cumulative_leads[agent], mode='lines', name=agent))
    fig.update_layout(
        title='Cumulative Leads Generated Over Time by Each Agent',
        xaxis_title='Date',
        yaxis_title='Cumulative Leads Count'
    )
    st.plotly_chart(fig,use_container_width=True)
def plot_graphs_for_customer_support(df):
    # Calculate percentage of leads generated
    leads_generated_percentage = df['Query-Resolved'].value_counts(normalize=True) * 100

    # Plot for leads generated/not generated
    fig_leads = go.Figure(go.Pie(labels=leads_generated_percentage.index, values=leads_generated_percentage.values,
                                 textinfo='label+percent', name='Query Resolution Status'))

    fig_leads.update_layout(title='Percentage of Query Resolution status')

    # Calculate percentage participation of reasons
    reasons_generated_percentage = df[df['Query-Resolved']]['Reason'].value_counts(normalize=True) * 100
    reasons_not_generated_percentage = df[~df['Query-Resolved']]['Reason'].value_counts(normalize=True) * 100

    # Plot for reasons behind lead generation
    fig_reasons_generated = go.Figure(
        go.Pie(labels=reasons_generated_percentage.index, values=reasons_generated_percentage.values,
               textinfo='label+percent', name='Reasons - Query Resolved'))

    fig_reasons_generated.update_layout(title='Reasons Behind Query Resolution')

    # Plot for reasons behind lead not generation
    fig_reasons_not_generated = go.Figure(
        go.Pie(labels=reasons_not_generated_percentage.index, values=reasons_not_generated_percentage.values,
               textinfo='label+percent', name='Reasons - Non Resolution'))

    fig_reasons_not_generated.update_layout(title='Reasons Behind Query not Resolved')

    col1,col2=st.columns([1,1])
    with col1:
        st.plotly_chart(fig_leads,user_container_width=True)
    with col2:
        # Count leads generated and not generated by each agent
        leads_generated = df[df['Query-Resolved']].groupby('Agent Name').size().reset_index(name='Query-Resolved')
        leads_not_generated = df[~df['Query-Resolved']].groupby('Agent Name').size().reset_index(
            name='Query not Resolved')

        # Merge the two dataframes to ensure all agents are included
        merged_df = pd.merge(leads_generated, leads_not_generated, on='Agent Name', how='outer').fillna(0)

        # Plot
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=merged_df['Agent Name'],
            y=merged_df['Query-Resolved'],
            name='Query-Resolved',
            marker_color='skyblue'
        ))

        fig.add_trace(go.Bar(
            x=merged_df['Agent Name'],
            y=merged_df['Query not Resolved'],
            name='Query not Resolved',
            marker_color='salmon'
        ))

        fig.update_layout(
            barmode='group',
            title='Query Resolved or not Resolved by Each Agent',
            xaxis_title='Agent Name',
            yaxis_title='Number of Queries',
            legend_title='Resolution Status'
        )
        st.plotly_chart(fig,user_container_width=True)
    col3,col4=st.columns([1,1])
    with col3:
        st.plotly_chart(fig_reasons_generated,user_container_width=True)
    with col4:
        st.plotly_chart(fig_reasons_not_generated,user_container_width=True)

    df['chat_end_time'] = pd.to_datetime(df['chat_end_time'])
    leads_by_agent_date = df.groupby(['Agent Name', df['chat_end_time'].dt.date]).size().reset_index(name='Resolution Count')
    pivot_leads = leads_by_agent_date.pivot(index='chat_end_time', columns='Agent Name', values='Resolution Count').fillna(0)
    cumulative_leads = pivot_leads.cumsum()
    fig = go.Figure()
    for agent in cumulative_leads.columns:
        fig.add_trace(go.Scatter(x=cumulative_leads.index, y=cumulative_leads[agent], mode='lines', name=agent))
    fig.update_layout(
        title='Cumulative Query Resolution Over Time by Each Agent',
        xaxis_title='Date',
        yaxis_title='Cumulative Queries Count'
    )
    st.plotly_chart(fig,use_container_width=True)
def leads_data(sales_support_data):
    filtered_df = sales_support_data
    st.subheader('Chats Data Filters')
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        agent_filter = st.selectbox('Select Agent ', ['All'] + sales_support_data['Agent Name'].unique().tolist())
        if agent_filter != 'All':
            filtered_df = filtered_df[filtered_df['Agent Name'] == agent_filter]
    with col2:
        customer_filter = st.selectbox('Select Customer ', ['All'] + sales_support_data['Customer Name'].unique().tolist())
        if customer_filter != 'All':
            filtered_df = filtered_df[filtered_df['Customer Name'] == customer_filter]
    with col3:
        lead_filter = st.selectbox('Select Lead Status ',
                                  ['All'] + sales_support_data['Lead-Generated'].unique().tolist())
        reasons = sales_support_data['Reason'].unique().tolist()

        if lead_filter != 'All':
            filtered_df = filtered_df[filtered_df['Lead-Generated'] == lead_filter]
            reasons = filtered_df['Reason'].unique().tolist()

    with col4:
        reasons_filter = st.selectbox('Select Reason ',
                                           ['All'] + reasons)

        if reasons_filter != 'All' and lead_filter!="All" :
            filtered_df = filtered_df[filtered_df['Reason'] == reasons_filter]

    st.markdown('---')

    if len(filtered_df) > 0:
        average_engagement_time_minutes = filtered_df['Total Engaugment Time'].mean().total_seconds() / 60
        filtered_df['Average Responce Time'] = pd.to_numeric(filtered_df['Average Responce Time'], errors='coerce')
        filtered_df['Average Delay Time'] = pd.to_numeric(filtered_df['Average Delay Time'], errors='coerce')
        filtered_df['Polarity Score'] = pd.to_numeric(filtered_df['Polarity Score'], errors='coerce')

        average_responce_time = filtered_df['Average Responce Time'].mean()
        average_delay_time = filtered_df['Average Delay Time'].mean()
        average_polaity_score = filtered_df['Polarity Score'].mean()

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            st.metric(label="Total Sales Support Chats", value=len(filtered_df))
        with col2:
            satisfation = filtered_df["Customer Satisfied"].value_counts()
            st.metric(label="Satisfaction Percentage",
                      value=f'{round(satisfation[True] / len(filtered_df) * 100, 2)} %')
        with col3:
            st.metric(label="Total Customers", value=(filtered_df['Customer Name'].nunique()))
        with col4:
            st.metric(label="Total Agents", value=(filtered_df['Agent Name'].nunique()))

        col7, col8, col9, col10= st.columns([1, 1, 1, 1])
        with col7:
            st.metric(label="AVG Engaugement Time (Minutes)", value=f"{round(average_engagement_time_minutes, 2)}")
        with col8:
            st.metric(label="AVG Response (Seconds)", value=f"{round(average_responce_time, 2)}")
        with col9:
            st.metric(label="AVG Delay (Seconds)", value=f"{round(average_delay_time, 2)}")
        with col10:
            st.metric(label="AVG Polarity Score", value=f"{round(average_polaity_score, 2)}")

        st.markdown('---')
        st.subheader('Processed Chats')
        st.write(filtered_df)
        plot_graphs_for_sales_support(filtered_df)
    else:
        st.warning('No Data Available after Filteration.')
def supports_data(customer_support_data):
    filtered_df = customer_support_data
    st.subheader('Chats Data Filters')
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        agent_filter = st.selectbox('Select Agent ', ['All'] + customer_support_data['Agent Name'].unique().tolist())
        if agent_filter != 'All':
            filtered_df = filtered_df[filtered_df['Agent Name'] == agent_filter]
    with col2:
        customer_filter = st.selectbox('Select Customer ', ['All'] + customer_support_data['Customer Name'].unique().tolist())
        if customer_filter != 'All':
            filtered_df = filtered_df[filtered_df['Customer Name'] == customer_filter]
    with col3:
        lead_filter = st.selectbox('Select Query Resolution Status ',
                                  ['All'] + customer_support_data['Query-Resolved'].unique().tolist())
        reasons = customer_support_data['Reason'].unique().tolist()

        if lead_filter != 'All':
            filtered_df = filtered_df[filtered_df['Query-Resolved'] == lead_filter]
            reasons = filtered_df['Reason'].unique().tolist()

    with col4:
        reasons_filter = st.selectbox('Select Reason ',
                                           ['All'] + reasons)

        if reasons_filter != 'All' and lead_filter!="All" :
            filtered_df = filtered_df[filtered_df['Reason'] == reasons_filter]

    st.markdown('---')

    if len(filtered_df) > 0:
        average_engagement_time_minutes = filtered_df['Total Engaugment Time'].mean().total_seconds() / 60
        filtered_df['Average Responce Time'] = pd.to_numeric(filtered_df['Average Responce Time'], errors='coerce')
        filtered_df['Average Delay Time'] = pd.to_numeric(filtered_df['Average Delay Time'], errors='coerce')
        filtered_df['Polarity Score'] = pd.to_numeric(filtered_df['Polarity Score'], errors='coerce')

        average_responce_time = filtered_df['Average Responce Time'].mean()
        average_delay_time = filtered_df['Average Delay Time'].mean()
        average_polaity_score = filtered_df['Polarity Score'].mean()

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            st.metric(label="Total Customer Support Chats", value=len(filtered_df))
        with col2:
            satisfation = filtered_df["Customer Satisfied"].value_counts()
            st.metric(label="Satisfaction Percentage",
                      value=f'{round(satisfation[True] / len(filtered_df) * 100, 2)} %')
        with col3:
            st.metric(label="Total Customers", value=(filtered_df['Customer Name'].nunique()))
        with col4:
            st.metric(label="Total Agents", value=(filtered_df['Agent Name'].nunique()))

        col7, col8, col9, col10= st.columns([1, 1, 1, 1])
        with col7:
            st.metric(label="AVG Engaugment Time (Minutes)", value=f"{round(average_engagement_time_minutes, 2)}")
        with col8:
            st.metric(label="AVG Response (Seconds)", value=f"{round(average_responce_time, 2)}")
        with col9:
            st.metric(label="AVG Delay (Seconds)", value=f"{round(average_delay_time, 2)}")
        with col10:
            st.metric(label="AVG Polarity Score", value=f"{round(average_polaity_score, 2)}")

        st.markdown('---')
        st.subheader('Processed Chats')
        st.write(filtered_df)
        plot_graphs_for_customer_support(filtered_df)
    else:
        st.warning('No Data Available after Filteration.')

def Dashboard():
    # Read the image file as binary data
    with open("Images/header-logo-updated.png", "rb") as f:
        image_data = f.read()
    # Encode the image data as base64
    base64_encoded_image = base64.b64encode(image_data).decode()
    html = """
    <div style='text-align:center;'>
        <img src="data:image/png;base64,{encoded_image}" alt='Live Admin Chats Dashboard' width='400'>
        <p>Live Admin Chats Dashboard</p>
    </div>
    """
    # Insert the base64 encoded image data into the HTML
    html = html.format(encoded_image=base64_encoded_image)
    st.markdown(html, unsafe_allow_html=True)

    ###########################################################################
    sales_support_data = pd.read_excel('Sales-Support.xlsx')
    customer_support_data = pd.read_excel('Customer-Support.xlsx')
    merged_data = pd.concat([
        sales_support_data.drop(columns=['Lead-Generated', 'Reason']),
        customer_support_data.drop(columns=['Complaint-Category', 'Query-Resolved', 'Reason'])
    ], ignore_index=True)
    merged_data['chat_end_time'] = pd.to_datetime(merged_data['chat_end_time'], format='%m/%d/%Y %I:%M:%S %p')
    merged_data['chat_start_time'] = pd.to_datetime(merged_data['chat_start_time'], format='%m/%d/%Y %I:%M:%S %p')
    merged_data['Total Engaugment Time'] = merged_data['chat_end_time'] - merged_data['chat_start_time']
    sales_support_data['chat_end_time'] = pd.to_datetime(sales_support_data['chat_end_time'], format='%m/%d/%Y %I:%M:%S %p')
    sales_support_data['chat_start_time'] = pd.to_datetime(sales_support_data['chat_start_time'], format='%m/%d/%Y %I:%M:%S %p')
    sales_support_data['Total Engaugment Time'] = sales_support_data['chat_end_time'] - sales_support_data['chat_start_time']
    customer_support_data['chat_end_time'] = pd.to_datetime(customer_support_data['chat_end_time'], format='%m/%d/%Y %I:%M:%S %p')
    customer_support_data['chat_start_time'] = pd.to_datetime(customer_support_data['chat_start_time'], format='%m/%d/%Y %I:%M:%S %p')
    customer_support_data['Total Engaugment Time'] = customer_support_data['chat_end_time'] - customer_support_data['chat_start_time']

    st.title('Core Data Metrics and Insights')
    base_data(merged_data)
    st.markdown('----')
    st.title('Sales Support Classified Data Metrics and Insights')
    leads_data(sales_support_data)
    st.markdown('----')
    st.title('Customer Support Classified  Data Metrics and Insights')
    supports_data(customer_support_data)
    st.markdown('----')

# Set the title at the top of the Streamlit app
st.set_page_config(
    page_title="Hsieh-Dashboard",
    page_icon="Images/LogoSmall.png",
    layout="wide",  # Set the layout to wide
    # You can use an emoji or provide a URL to an icon
)
st.markdown("""
<script>
document.body.style.zoom = 0.7;
</script>
""", unsafe_allow_html=True)


# Main function to handle page navigation
def main():
    pages = {
        "Home": home,
        "Dashboard": Dashboard,
    }
    st.sidebar.image("Images/Logo.png", caption="Delivering Happiness", use_column_width=True)

    st.sidebar.title("Hsieh")

    st.sidebar.markdown(
        f'<span style="text-decoration:none; color:white ;">Live Admin Dashboard</span>',
        unsafe_allow_html=True)
    selection = st.sidebar.selectbox("Select Page to Navigate", list(pages.keys()))
    page = pages[selection]
    page()

if __name__ == "__main__":
    main()
