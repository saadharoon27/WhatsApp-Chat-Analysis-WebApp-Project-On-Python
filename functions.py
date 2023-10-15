# Importing necessary libraries
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji



# Creating an instance of URLExtract for extracting URLs from messages
extract = URLExtract()



# Defining a function to fetch statistics based on the selected user and DataFrame
def fetch_stats(selected_user, df):
    # Filter the DataFrame based on the selected user (if not 'Overall')
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Fetch the number of messages (rows)
    num_messages = df.shape[0]

    # Fetch the total number of words by splitting and counting words in messages
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Fetch the number of media messages (messages with '<Media omitted>\n')
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # Fetch the number of links shared in messages using URLExtract
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)



# Defining a function to find the most active users
def most_busy_users(df):
    # Count the number of messages sent by each user and return the top 5
    x = df['user'].value_counts().head()

    # Calculating the percentage of messages sent by each user
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})

    return x, df



# Defining a function to create a Word Cloud for messages
def create_wordcloud(selected_user, df):
    # Open and read a file containing filler words, by removing these words the wordcloud will be able to represent a better quality data
    f = open('filler_words.txt', 'r')
    filler_words = f.read()

    # Filter the DataFrame based on the selected user (if not 'Overall')
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

# Removing the filler words from messages will result in better data visualization.
    temp = df[df['user'] != 'Group_Notification']  # Filter out 'Group_Notification'.
    temp = temp[temp['message'] != '<Media omitted>\n']  # Filter out '<Media omitted>'.

# Define a function remove_filler_words that takes a message and removes filler words from it.
    def remove_filler_words(message):
        y = []
        # Loop through each word in the message (splitting by spaces).
        for word in message.lower().split():
            # Check if the word is not in the filler_words list.
            if word not in filler_words:
                # If it's not a filler word, add it to the list.
                y.append(word)
        # Join the non-filler words back into a single string with spaces.
        return " ".join(y)

    # Generate a Word Cloud object with specified settings.
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')

    # Apply the remove_filler_words function to each message in the DataFrame 'temp'.
    temp['message'] = temp['message'].apply(remove_filler_words)

    # Generate a Word Cloud based on the cleaned messages by concatenating them.
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    # Return the generated Word Cloud object.
    return df_wc



# Defining a function to find the most common words in messages
def most_common_words(selected_user, df):
    # Open and read a file containing filler words
    f = open('filler_words.txt', 'r')
    filler_words = f.read()

    # Filter the DataFrame based on the selected user (if not 'Overall')
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Removing the filler words from messages will result in better data visualisation
    temp = df[df['user'] != 'Group_Notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    # Removing the filler words, and keeping the rest into a different dataset (words)
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in filler_words:
                words.append(word)

    # Create a DataFrame with the most common words (top 20)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df



# Define a function to extract and count emojis used in messages
def emoji_helper(selected_user, df):
    # Check if the selected_user is not 'Overall'
    if selected_user != 'Overall':
        # If selected_user is not 'Overall', filter the DataFrame df to only include rows where 'user' column matches selected_user
        df = df[df['user'] == selected_user]

    # Create an empty list called 'emojis' to store emojis found in messages
    emojis = []

    # Iterate over each message in the 'message' column of the DataFrame df
    for message in df['message']:
        # For each message, extend the 'emojis' list with any characters (emojis) that are in the emoji.UNICODE_EMOJI['en'] dictionary
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    # Create a DataFrame 'emoji_df' to store the counts of each emoji, sorted by frequency (most common first)
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    # Return the emoji_df DataFrame containing the most common emojis and their counts
    return emoji_df



# Defining a function to create a monthly timeline of message counts
def monthly_timeline(selected_user, df):
    # Check if a specific user is selected or 'Overall'
    if selected_user != 'Overall':
        # If a specific user is selected, filter the DataFrame to include only their messages
        df = df[df['user'] == selected_user]

    # Grouping messages by year, month number, and month name, and counting them
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # Create a list to store formatted time strings
    time = []

    # Loop through each row in the 'timeline' DataFrame
    for i in range(timeline.shape[0]):
        # Concatenate the 'month' and 'year' values with a hyphen and store in the 'time' list
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    # Create a new column 'time' in the 'timeline' DataFrame with the formatted time strings
    timeline['time'] = time

    # Return the resulting timeline DataFrame
    return timeline



# Creating a function for the daily timeline of message counts
def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Grouping messages by date and counting them for each date
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline



# Defining a function to create a weekly activity column
def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # This will count the number of messages for each day of the week
    return df['day_name'].value_counts()



# A function to create a chart of monthly activity
def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # This will count the number of messages for each month
    return df['month'].value_counts()



# Defining a function to create an activity heatmap
def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Creating a heatmap of message counts plotted against two variables: 'day_name' and 'period'.
    # This will show which time period has the highest message activity for the selected user.
    # The 'pivot_table' function reshapes the DataFrame and calculates counts of messages for each combination of 'day_name' and 'period'.
    # Any missing (NaN) values are filled with 0.
    user_heatmap = df.pivot_table(index='day_name', columns='hour', values='message', aggfunc='count').fillna(0)

    # Return the resulting heatmap.
    return user_heatmap