import re
import pandas as pd
def data_extraction(raw_data):
    data = re.split('\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w+\s-\s', raw_data)[2:]
    raw_date = re.findall('\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w+', raw_data)[2:]
    users = []
    messages = []
    date = []
    for x, y in zip(data, raw_date):
        z = x.split(":")
        if len(z) == 1:
            continue
        users.append(z[0])
        messages.append(z[1])
        date.append(y)
    df = pd.DataFrame({'msg': messages, 'user': users, 'date': date})
    strs = "status??\n"
    strs.replace("\n", "")

    df["msg"] = df["msg"].apply(lambda x: x.replace("\n", ""))
    df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    return df