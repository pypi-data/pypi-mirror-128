import pandas as pd


class ProcessCSV:
    """Loads csv files in to a dataframe by taking a list of csv files names.
     The dataframes created are joined on a common column between the 2 dataframes.
     Reorders newly created dataframe columns.

        Args:
            csv_files (list): list of csv files that will be read to dataframe
            df_list (list): Empty list to hold or contain dataframes convert from csv
            temp_col (list): Empty list to hold or contain columns that is being reordered.
    """

    def __init__(self, col_name: [], position: []):
        self.csv_files = ['GDPData', 'APIData']
        self.col_name = col_name
        self.position = position
        self.df_list = []
        self.temp_col = []

    def read_csv_to_df(self):
        for i in range(len(self.csv_files)):
            self.df_list.append(pd.read_csv(self.csv_files[i] + ".csv"))
        data1 = self.df_list[0].iloc[:, :65]
        data2 = self.df_list[1].iloc[:, :5]
        # Join dataset and drop redundant columns
        data = pd.merge(data1, data2, on='Country Code', how='inner').drop(['TableName'], axis=1)
        return data

    def reorder_df_columns(self):
        data = self.read_csv_to_df()
        dataframe = data.drop(columns=self.col_name)
        for x in range(len(self.col_name)):
            self.temp_col.append(data[self.col_name[x]])
        for y in range(len(self.position)):
            dataframe.insert(loc=self.position[y], column=self.col_name[y], value=self.temp_col[y])
        return dataframe


if __name__ == '__main__':
    pc = ProcessCSV(['Region', 'IncomeGroup', 'SpecialNotes'], [4, 5, 6])
    pc.reorder_df_columns()
