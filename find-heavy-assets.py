# Scan an apache web server log, in default CPanel format, and report on 
# the assets that are heaviest using bandwidth and slowing down pages

## The input format will be the apache log format as defaulted in cpanel

## This program created with the aid of Copilot

# Imports
import sys
import re
import pandas as pd
import openpyxl
import datetime


# Example of a line in the apache log format
# 63.141.251.189 - - [14/Feb/2022:07:11:15 -0500] "GET /wp-login.php HTTP/1.1" 200 1923 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53"




# Define a function that loads apache log as a dataframe, takes filename as input and outputs a dataframe


def read_apache_log_as_dataframe(file_name):
    # Open the file
    file = open(file_name, 'r')

    # Create a blank dataframe
    df = pd.DataFrame()
    

    all_list = []

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

        # append line_list to a complete_list
        complete_line_list_with_everything = line_list + request_list
        # print(line_list[6])
        # if complete)list_list_with_everything is the correct length
        if len(complete_line_list_with_everything) == 10:

            # append complete_list to a all_list
            all_list.append(complete_line_list_with_everything)
        else:
            if verbose:
                print('Error in line ' + str(i) + ': ' + line)

        
    # Close the input file
    file.close()

    # convert all_list into a dataframe called df
    df = pd.DataFrame(all_list)


    # rename the df columns to ip, dash, dash2, datetime, request, status, bytes, dash3, user_agent
    df.columns = ['ip', 'dash', 'dash2', 'datetime', 'request', 'status', 'bytes', 'dash3', 'user_agent', 'dash4']

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

    # replace dashes with 0 in column bytes
    df['bytes'] = df['bytes'].str.replace('-', '0')

    # convert bytes column to numeric
    df['bytes'] = pd.to_numeric(df['bytes'])

    # return the dataframe

    return df

        





## main so that this file can be imported as a module
if __name__ == '__main__':


    # if there is a --verbose or -v set verbose to True
    if '--verbose' in sys.argv or '-v' in sys.argv:
        verbose = True

    # if there are no arguments
    if len(sys.argv) == 1:
        print('Usage: find-heavy-assets.py [--verbose] <apache log file>')
        sys.exit(1)


    # if there is a --help or -h print help and exit
    if '--help' in sys.argv or '-h' in sys.argv:
        print('Usage: find-heavy-assets.py [--verbose] [--help] <apache log file>')
        print('--verbose or -v: print verbose output')
        print('--help or -h: print this help message')
        print('<apache log file>: apache log file to process')
        print('output will be a spreadsheet in the current directory called heavy_assets.xlsx')
        sys.exit()

    # get the input filename as the first argument that doesn't start with -
    for arg in sys.argv:
        if arg[0] != '-':
            input_file_name = arg
            break

    if verbose:
        print('reading apache log: ' + input_file_name)

    # call the apache_to_csv function using the first arg as the parameter
    apache_log_df = read_apache_log_as_dataframe(input_file_name)

    if verbose:
        # say how big the apache log is
        print('apache log has ' + str(len(apache_log_df)) + ' lines')

    report =pd.pivot_table(apache_log_df,index='request_path', values='bytes', aggfunc=['sum','mean','count'])


    # print(apache_log_df)
    

    # export the report to an excel file
    
    # put in manual labels for the columns of the pivot table
    report.columns = ['Total Bytes', 'Average Bytes', 'Count']
 
    if verbose:
        print("Writing report to excel file")

    datetimeasanumber = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    report.to_excel('heavy_assets_report_' +datetimeasanumber+ '.xlsx', sheet_name='report')


    print('Report exported to report.xlsx')    
