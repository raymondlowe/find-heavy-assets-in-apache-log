# Scan an apache web server log, in default CPanel format, and report on 
# the assets that are heaviest using bandwidth and slowing down pages

## The input format will be the apache log format as defaulted in cpanel

## This program created with the aid of Copilot

# Imports
import sys
import re
import pandas as pd


# Example of a line in the apache log format
# 63.141.251.189 - - [14/Feb/2022:07:11:15 -0500] "GET /wp-login.php HTTP/1.1" 200 1923 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53"




# Define a function that loads apache log as a dataframe, takes filename as input and outputs a dataframe


def read_apache_log_as_dataframe(file_name):
    # Open the file
    file = open(file_name, 'r')

    # Create a blank dataframe
    df = pd.DataFrame()
    


    i = 0
    for line in file:
        #inc i
        i += 1
        # Split the line into a list

        # convert [ and ] to " in line
        line = line.replace('[', '"').replace(']', '"')

        # split line on spaces but consider quoted strings as one word
        line_list = [p for p in re.split("( |\\\".*?\\\"|'.*?')", line) if p.strip()]      

        # split line_list[4] on spaces and insert into list
        request_list = [p for p in re.split("( |\\\".*?\\\"|'.*?')", line_list[4]) if p.strip()]

        # insert request_list into line_list in the 4th place
        # line_list.insert(4, request_list)


        # append line_list as a new row at the end of the dataframe df
        df = df.append(pd.Series(line_list), ignore_index=True)

    # Close the input file
    file.close()

    # rename the df columns to ip, dash, dash2, datetime, request, status, bytes, dash3, user_agent
    df.columns = ['ip', 'dash', 'dash2', 'datetime', 'request', 'status', 'bytes', 'dash3', 'user_agent', 'dash4', 'dash5']

    # remove quotes from requests column
    df['request'] = df['request'].str.replace('"', '')

    # split column request into three columns on space
    df[['request_type', 'request_path', 'request_query']] = df['request'].str.split(' ', 2, expand=True)

    # delete columns, dash, dash2 and dash3, request, user_agent
    df = df.drop(['dash', 'dash2', 'dash3', 'request','user_agent'], axis=1)

    # remove double quote from datetime column
    df['datetime'] = df['datetime'].str.replace('"', '')

    # parse apache log date time with timezone into datetime format
    df['datetime'] = pd.to_datetime(df['datetime'], format='%d/%b/%Y:%H:%M:%S %z')

    # return the dataframe

    return df

        





## main so that this file can be imported as a module
if __name__ == '__main__':
    # call the apache_to_csv function using the first arg as the parameter
    apache_log_df = read_apache_log_as_dataframe(sys.argv[1])

    report =pd.pivot_table(apache_log_df,index=['request_type', 'request_path'], values='bytes', aggfunc=['sum','mean','count'])


    print(apache_log_df)
    print(report) 