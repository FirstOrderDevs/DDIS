import pandas as pd;

def get_marks_dataframe(subjects, schools, terms = [1,2,3,4,5,6,7,8,9], index = 'no'):

    """
    Returns a data frame with marks for given subjects and terms for given schools

    Parameters
        ----------
        subjects : list of subjects ["History","Sinhala","English"]
        schools : list of schools ["Sirisaman","Southland"]
        terms : list of terms from 1 to 9 [1,2]
                if not specified return marks for all the terms.
        index : {'yes','no'} adds index number of the student for the data frame
    """

    files = [];

    for school in schools:
        files.append(school + " - Performance.csv");

    path = "/home/wolfpack/FYP/DDIS/Data/"

    if(index == 'yes'):
        columns = ['Index No.'];

    elif(index == 'no'):
        columns = [];

    for subject in subjects :

        columns.append(subject)

        for term in terms:
            if(term > 1):
                columns.append(subject + "." + str(term-1));

    dataframes = [];

    for file in files:

        df = pd.read_csv(path+file, header=1, usecols=columns);

        dataframes.append(df);

    merged_df = dataframes[0];

    for dataframe in dataframes[1:]:
        merged_df = merged_df.append(dataframe);

    return merged_df;

def handle_absent(dataframe, how='fill_0'):

    """
    Manages absent values in a data frame

    Parameters
        ----------
        dataframe : dataframe to be modified
        how : {'fill_0', 'fill_prev_avg', 'fill_this_avg', 'drop'}
    """

    if(how == 'fill_0'):
         dataframe.replace('ab', 0, inplace=True);

#     elif(how == 'fill_prev_avg'):
#         # put previous average here for the subject
#
#     elif(how == 'fill_this_avg'):
#         # put average mark for this term
#
    elif(how == 'drop'):
         columns = list(dataframe.columns.values);

         for column in columns:
            dataframe = dataframe[dataframe[column] != 0]

    return dataframe;


def handle_nan(dataframe, how='fill_0'):

    """
        Manages nan values in a data frame

        Parameters
            ----------
            dataframe : dataframe to be modified
            how : {'fill_0', 'fill_prev_avg', 'fill_this_avg', 'drop'}
        """

    if (how == 'fill_0'):
        dataframe.fillna(0, inplace=True);

    #     elif(how == 'fill_prev_avg'):
    #         # put previous average here for the subject
    #
    #     elif(how == 'fill_this_avg'):
    #         # put average mark for this term
    #
    elif (how == 'drop'):
        dataframe.dropna(inplace=True);

    return dataframe;