'''Importing necessary libraries'''
import streamlit as st  # Streamlit for creating the web app
import preprocessor  # A custom module for preprocessing WhatsApp chat data
import functions  # A custom module for additional helper functions
import matplotlib.pyplot as plt  # Matplotlib for plotting
import seaborn as sns  # Seaborn for advanced data visualization



""" Set the title for the sidebar """
st.sidebar.title("WhatsApp Chat Analyser")



'''Create a file uploader widget in the sidebar
Users can upload a WhatsApp chat file for analysis'''
uploaded_file = st.sidebar.file_uploader("Please choose the WhatsApp file that you want to analyze")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the uploaded file as bytes and decode it as UTF-8
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Preprocess the WhatsApp chat data using a custom preprocessor
    df = preprocessor.preprocess(data)

    # Display the preprocessed data as a Pandas DataFrame in the main content area
    st.dataframe(df)



'''To provide users with the flexibility to conduct both group and individual-level analyses
A new dropdown menu should be introduced, allowing users to choose individual selections'''

# Fetching unique users to make up the elements of the dropdown list
user_list = df['user'].unique().tolist()
    
# Removing 'Group_Notification' as a group user
user_list.remove('group_notification')

# Sorting the 'user_list' in ascending order
user_list.sort()

# Adding an 'Overall' element to the list, if the user wants to perform a group level analysis
user_list.insert(0,"Overall")

selected_user = st.sidebar.selectbox("Show analysis with respect to",user_list)

'''The Analysis Part'''

# This code block will execute when the "Show Analysis" button in the sidebar is clicked
if st.sidebar.button("Show Analysis"):

    # Statistical Analysis

    # Call the 'fetch_stats' function with 'selected_user' and 'df' as arguments and unpack the returned values
    num_messages, words, num_media_messages, num_links = functions.fetch_stats(selected_user, df)

    # Set the title of the web page to "Top Statistics"
    st.title("Top Statistics")

    # Divide the page into four columns
    col1, col2, col3, col4 = st.columns(4)

    # Inside the first column
    with col1:
        # Display a header with the text "Total Messages"
        st.header("Total Messages")
        # Display the value of 'num_messages' as a title
        st.title(num_messages)

    # Inside the second column
    with col2:
        # Display a header with the text "Total Words"
        st.header("Total Words")
        # Display the value of 'words' as a title
        st.title(words)

    # Inside the third column
    with col3:
        # Display a header with the text "Media Shared"
        st.header("Media Shared")
        # Display the value of 'num_media_messages' as a title
        st.title(num_media_messages)

    # Inside the fourth column
    with col4:
        # Display a header with the text "Links Shared"
        st.header("Links Shared")
        # Display the value of 'num_links' as a title
        st.title(num_links)



    # Monthly Timeline Graph

    # Set the title to "Monthly Timeline"
    st.title("Monthly Timeline")

    # Call a function 'monthly_timeline' from a module 'functions' with parameters 'selected_user' and 'df' and store the result in 'timeline'
    timeline = functions.monthly_timeline(selected_user, df)

    # Create a new figure and axis for plotting
    fig, ax = plt.subplots()

    # Plot the data from the 'timeline' DataFrame, where 'time' is the x-axis and 'message' is the y-axis, using a green line
    ax.plot(timeline['time'], timeline['message'], color='green')

    # Rotate the x-axis labels vertically for better readability
    plt.xticks(rotation='vertical')

    # Display the matplotlib figure using Streamlit's 'st.pyplot()' function
    st.pyplot(fig)



    # Daily Timeline Graph
    
    # Setting the title
    st.title("Daily Timeline")

    # Calling the 'daily_timeline' function to generate data for the timeline
    daily_timeline = functions.daily_timeline(selected_user, df)

    # Create a new figure and axis for plotting using Matplotlib
    fig, ax = plt.subplots()

    # Plot the data from the 'daily_timeline' DataFrame
    # 'daily_timeline['only_date']' contains the x-axis data (dates)
    # 'daily_timeline['message']' contains the y-axis data (message counts)
    ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')

    # Customize the x-axis tick labels to be vertical (rotated)
    plt.xticks(rotation='vertical')

    # Display the Matplotlib figure within the Streamlit app
    st.pyplot(fig)



    # Activity Maps

    # Setting the title
    st.title('Activity Map')
    # Diving the area into 2 columns
    col1,col2 = st.columns(2)

    # Inside the first column (col1)
    with col1:
        # Set a header for this section
        st.header("Most busy day")
        
        # Call a function (helper.week_activity_map) to get data related to the user's weekly activity and store it in busy_day
        busy_day = functions.week_activity_map(selected_user, df)
        
        # Create a new figure and axis for plotting
        fig, ax = plt.subplots()
        
        # Create a bar chart using data from busy_day
        ax.bar(busy_day.index, busy_day.values, color='purple')
        
        # Rotate x-axis labels vertically for better readability
        plt.xticks(rotation='vertical')
        
        # Display the matplotlib figure in the Streamlit app
        st.pyplot(fig)

    # Inside the second column (col2)
    with col2:
        # Set a header for this section
        st.header("Most busy month")
        
        # Call a function (helper.month_activity_map) to get data related to the user's monthly activity and store it in busy_month
        busy_month = functions.month_activity_map(selected_user, df)
        
        # Create a new figure and axis for plotting
        fig, ax = plt.subplots()
        
        # Create a bar chart using data from busy_month
        ax.bar(busy_month.index, busy_month.values, color='orange')
        
        # Rotate x-axis labels vertically for better readability
        plt.xticks(rotation='vertical')
        
        # Display the matplotlib figure in the Streamlit app
        st.pyplot(fig)


        # Setting the title of heatmap
        st.title("Weekly Activity Map")

    # Set the title for the Streamlit app as "Weekly Activity Map"
    st.title("Weekly Activity Map")

    # Call a function 'activity_heatmap' from a functions module to generate a heatmap
    user_heatmap = functions.activity_heatmap(selected_user, df)

    # Creating a new figure and axis for plotting
    fig, ax = plt.subplots()

    # Generate a heatmap using Seaborn library
    ax = sns.heatmap(user_heatmap)

    # Display the heatmap using Streamlit's 'st.pyplot' function
    st.pyplot(fig)

    if selected_user == 'Overall':
        # Setting the title for the busiest users section
        st.title('Most Busy Users')
        
        # Calling a function 'most_busy_users' from a functions module to find the busiest users
        x, new_df = functions.most_busy_users(df)
        
        # Create a new figure and axis for plotting
        fig, ax = plt.subplots()
        
        # Create two columns for layout using 'st.columns' function
        col1, col2 = st.columns(2)

        # In the first column (col1), plot a bar chart
        with col1:
            ax.bar(x.index, x.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        # In the second column (col2), display a dataframe using 'st.dataframe'
        with col2:
            st.dataframe(new_df)



    # Word Cloud

    # Set the title of the page to "Wordcloud"
    st.title("Wordcloud")

    # Creating a word cloud using the 'create_wordcloud' function from the 'functions' module.
    df_wc = functions.create_wordcloud(selected_user, df)

    # Create a subplot for displaying the word cloud image.
    fig, ax = plt.subplots()

    # Display the word cloud image in the subplot.
    ax.imshow(df_wc)

    # Show the word cloud image using 'st.pyplot'.
    st.pyplot(fig)



    # Most Common Words

    # Calculating the most common words
    most_common_df = functions.most_common_words(selected_user, df)

    # Create a new subplot for displaying the bar chart of most common words.
    fig, ax = plt.subplots()

    # Create a horizontal bar chart displaying the most common words and their frequencies.
    ax.barh(most_common_df[0], most_common_df[1])

    # Rotate the x-axis labels vertically for better readability.
    plt.xticks(rotation='vertical')

    # Set the title for this section.
    st.title('Most common words')

    # Show the bar chart using 'st.pyplot'.
    st.pyplot(fig)



    # Emoji Analysis

    # Performing emoji analysis using the 'emoji_helper' function from the 'functions' module.
    emoji_df = functions.emoji_helper(selected_user, df)

    # Setting the title for the emoji analysis section.
    st.title("Emoji Analysis")

    # Creating a two-column layout for displaying data and a pie chart side by side.
    col1, col2 = st.columns(2)

    # In the left column, displaying the emoji analysis DataFrame.
    with col1:
        st.dataframe(emoji_df)

    # In the right column, creating a subplot for displaying a pie chart of the top emojis and their percentages.
    with col2:
        fig, ax = plt.subplots()

        # Creating a pie chart showing the top emojis and their percentages.
        ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")

        # Showing the pie chart using 'st.pyplot'.
        st.pyplot(fig)