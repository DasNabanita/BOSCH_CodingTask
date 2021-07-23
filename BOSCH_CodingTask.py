import pandas as pd
import sys


def fix_dataframe(df):
    s = ';'
    flag = 0
    for rowIndex, row in df.iterrows():  # iterate over rows
        for columnIndex, value in row.items():
            if s in str(value) and flag == 0:
                word = str(value)
                str1, str2 = word.split(s)
                df.iloc[rowIndex] = df.iloc[rowIndex].shift(periods=1, axis=0)
                df.loc[rowIndex, columnIndex] = str1
                flag = 1
            elif flag == 1:
                df.loc[rowIndex, columnIndex] = str2
                flag = 0
    return df


def new_dataframeFormat(df):
    df['TimeStamp'] = pd.to_datetime(df['timestamp'])
    df['Date'] = df['TimeStamp'].dt.date
    df['Hour'] = df['TimeStamp'].dt.hour

    df['Concat'] = df['station_id'] + '_sensor_ ' + df['sensor']
    df = pd.crosstab(index=[df['Date'], df['Hour'], df['prod_id'], df['part_id']], columns=df['Concat'],
                     values=df['value'], aggfunc=sum)
    return df


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Path to csv file missing !!!')

    dataframe = pd.read_csv(sys.argv[1])
    dataframe = fix_dataframe(dataframe)
    dataframe = new_dataframeFormat(dataframe)
    dataframe.to_csv('Final_manuf_data.csv')
    print('Done !!!')
