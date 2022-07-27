import datetime

#Convert timestamp from human form (2022-07-02 00:00:00) to unix form (1656633600) to use it in stackoverflow api
def function_convert_timestamp(timestamp_from_query):
    convert_to_timestamp_datetime = datetime.datetime.strptime(timestamp_from_query, "%Y-%m-%d %H:%M:%S")
    unix_time_for_api_request = int(datetime.datetime.timestamp(convert_to_timestamp_datetime))
    return unix_time_for_api_request

