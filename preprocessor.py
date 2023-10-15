'''Importing Libraries'''

import re
import pandas as pd



'''Loading the chat file to a variable named 'data'''

# Opening the chat file and storing it to variable 'f'
f = open('Chat File.txt', 'r', encoding='utf-8')

# To read the contents of the chat file in a string format, the following expression was used
data = f.read()

# Viewing the chat file to check how the data is organised
print(data)

print(type(data))



'''To better understand what the data is saying, it first has to be broken down into different columns on the basis of similarity'''

# Breaking the string into 2 different expressions using a common pattern
pattern = '\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'

messages = re.split(pattern, data)[1:] # This contains all the textual messages shared
dates = re.findall(pattern, data) # This contains all the information about the date and time the messages when the messages were shared



'''As the chat is in string format, it has to be converted into a Pandas Dataframe for further analysis'''

# Making a Pandas dataframe named 'df'
df = pd.DataFrame({'date': dates, 'user_message': messages})

# Converting 'message_date' type to datetime format
df['date'] = pd.to_datetime(df['date'], format = '%d/%m/%y, %I:%M %p - ')

df.head()

# Checking the shape of data
df.shape



'''Since in the 'user_message' column the values are combined, the name of the sender and the message they sent. They must be seperated into different columns.'''

users = [] # An empty list to store usernames
messages = [] # An empty list to store messages


# A forloop to iterate over each message in the 'user_message' column of the DataFrame 'df'
for message in df['user_message']:
    # Split the message using a regular expression pattern '([\w\W]+?):\s':
    # '([\w\W]+?)' captures any sequence of characters (including non-word characters) up to the first colon and space
    # ':\s' matches the colon and space that separates the username from the message content
    entry = re.split('([\w\W]+?):\s', message)


    if entry[1:]: # Checks if there is a username (the slicing [1:] skips the first empty string in the split result)
        users.append(entry[1]) # Appends the captured username to the 'users' list
        messages.append(" ".join(entry[2:])) # Append the message content (joined as a string) to the 'messages' list
    else:
        users.append('Group_Notification') # If no username is found, the code will assume it's a group notification and add a placeholder
        messages.append(entry[0]) # Appends the entire message (without username) to the 'messages' list


# Add the 'users' and 'messages' lists as new columns to the DataFrame 'df'
df['user'] = users
df['message'] = messages

# Dropping the unnecessary column
df.drop(columns=['user_message'], inplace=True) 

# Date, User (Message Sender), and Message are now in 3 seperate columns
df.head()



'''Now,the problem with the date column is that it contains the date as well as the time the message was shared.

This needs to be addressed by dividing them into seperate columns.'''

# Creating a new column 'only_date' that contains only the date part of the 'date' column.
df['only_date'] = df['date'].dt.date

# Creating a new column 'year' that contains the year extracted from the 'date' column.
df['year'] = df['date'].dt.year

# Creating a new column 'month_num' that contains the month (as a number) extracted from the 'date' column.
df['month_num'] = df['date'].dt.month

# Creating a new column 'month' that contains the full name of the month extracted from the 'date' column.
df['month'] = df['date'].dt.month_name()

# Creating a new column 'day' that contains the day of the month extracted from the 'date' column.
df['day'] = df['date'].dt.day

# Creating a new column 'day_name' that contains the name of the day of the week extracted from the 'date' column.
df['day_name'] = df['date'].dt.day_name()

# Creating a new column 'hour' that contains the hour extracted from the 'date' column.
df['hour'] = df['date'].dt.hour

# Creating a new column 'minute' that contains the minute extracted from the 'date' column.
df['minute'] = df['date'].dt.minute


# Removing the 'date' column as it is not useful anymore
df.drop(columns=['date'], inplace=True)
df.head()



'''To create an automated process for extracting data from a WhatsApp chat file, preprocessing it, and returning the result as a Pandas DataFrame, the code provided above should be encapsulated within a function

To be called and reused in different Python scripts or files, the function is written into this same Python file named 'preprocessor.py'''


def preprocess(data):

    import re
    import pandas as pd

    pattern = '\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'date': dates, 'user_message': messages})

    df['date'] = pd.to_datetime(df['date'], format = '%d/%m/%y, %I:%M %p - ')

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)


        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'], inplace=True)


    df['only_date'] = df['date'].dt.date

    df['year'] = df['date'].dt.year

    df['month_num'] = df['date'].dt.month

    df['month'] = df['date'].dt.month_name()

    df['day'] = df['date'].dt.day

    df['day_name'] = df['date'].dt.day_name()

    df['hour'] = df['date'].dt.hour

    df['minute'] = df['date'].dt.minute

    df.drop(columns=['date'], inplace=True)

    return df