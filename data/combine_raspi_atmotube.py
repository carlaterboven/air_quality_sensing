import pandas as pd

class DataCombiner:
    def __init__(self):
        self.__data = pd.DataFrame()
        self.__all_data = pd.DataFrame()

    def __del__(self):
        pass

    def import_raspi_data(self, data_files):
        for filename in data_files:
            file = pd.read_csv(filename)
            # clear NaN locations (usually due to startup)
            file.dropna(subset=['lat', 'lon', 'alt', 'time'], inplace=True)
            # convert to timezone of Potsdam
            file['time'] = pd.to_datetime(file['time'], format='%Y-%m-%d %H:%M:%S.%f').dt.tz_convert('CET')
            file['time'] = file['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
            # string back to datetime format
            file['time'] = pd.to_datetime(file['time'])
            # use timestamp as new index
            file.drop('LogID', axis=1, inplace=True)
            file.set_index('time', inplace=True)
            # add all files to one dataframe
            self.__data = pd.concat([self.__data, file])

    def combine_atmotube_data(self, atmotube_files):
        for filename in atmotube_files:
            file = pd.read_csv(filename)
            file.rename(columns={"Date": "time"}, inplace=True)
            file['time'] = pd.to_datetime(file['time'], format='%Y-%m-%d %H:%M:%S.%f')
            # remove redundant measurements outside the test route
            date = file['time'][0].date()
            date_data = self.__data[self.__data.apply(lambda row : row.name.date() == date,axis=1)]
            min_time = date_data.index.min() - pd.Timedelta(minutes=1)
            max_time = date_data.index.max()
            file.drop(file[file['time'] < min_time].index, inplace=True)
            file.drop(file[file['time'] > max_time].index, inplace=True)
            # order dataframe with ascending time (needed for merge)
            file = file.iloc[::-1]
            file['time'] = pd.to_datetime(file['time'])
            file.set_index('time', inplace=True)
            # enriching the data points with the atmotube data per minute
            combined_data = pd.merge_asof(date_data, file, on='time', direction='backward')
            combined_data.name = str(date)
            self.__all_data = pd.concat([self.__all_data, combined_data])

    def write_combined_data(self):
        self.__all_data.to_csv('all_data.csv', index=False)


if __name__ ==  '__main__':
    data_files = ['log_oct25.csv', 'log_oct26.csv']
    atmotube_files = ['atmotube_oct25.csv', 'atmotube_oct26.csv']
    datacombiner = DataCombiner()
    datacombiner.import_raspi_data(data_files)
    datacombiner.combine_atmotube_data(atmotube_files)
    datacombiner.write_combined_data()
