import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns


def add_one(number):
    '''
    A test function to check if all the functions here are loading correctly
    '''
    return number + 1


def get_categorical_and_boolean_columns_summary_statistics(df_to_process):
    '''
    Return summary stats for all categorical columns.
    Parameters:
        df_to_process
        
    Returns:
        pd.DataFrame: Return summary stats for all categorical columns.   
    '''
    categoricals = ['object', 'bool', 'category']

    if(len(df_to_process.select_dtypes(include=categoricals).columns) == 0):
        return("No categorical or boolean columns found!")

    string_cols_summary_stats = ['count', pd.Series.nunique, pd.Series.unique]

    df_result = df_to_process.select_dtypes(include=categoricals).agg(string_cols_summary_stats).transpose()
    
    df_result = df_result.join(
        pd.DataFrame({
            'null_count' : df_to_process.select_dtypes(include=categoricals).isna().sum(),
            'na_count' : df_to_process.select_dtypes(include=categoricals).isnull().sum()
        }))

    df_result = df_result.round(2)
    
    return(df_result)


def get_float_and_int_columns_summary_statistics(df_to_process):
    '''
    Return summary stats for all numeric columns.
    Parameters:
        df_to_process
        
    Returns:
        pd.DataFrame: Return summary stats for all numeric columns.   
    '''

    numerics = ['int8', 'int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    
    if(len(df_to_process.select_dtypes(include=numerics).columns) == 0):
        return("No numeric found!")

    float_and_int_cols_summary_stats = ['count', 'min', 'max', 'median', 'std', 'mean', 'skew', pd.Series.nunique, 'sum']

    df_result = df_to_process.select_dtypes(include=numerics).agg(float_and_int_cols_summary_stats).transpose()
    
    df_result = df_result.join(
        pd.DataFrame({
            'null_count' : df_to_process.select_dtypes(include=numerics).isna().sum(),
            'na_count' : df_to_process.select_dtypes(include=numerics).isnull().sum()
        }))

    df_result = df_result.round(2)

    return(df_result)


def plot_box_plots_categorical_vs_numeric(df_to_plot, categorical_variables, numeric_variables, n_max_categories_to_plot = 10):
    '''
    Plots box plots of categorical columns vs numeric columns.
    Parameters:
        df_to_plot : pandas dataframe to plot
        categorical_variables : list of categorical variables
        numeric_variables :  list of numeric variables
        n_max_categories_to_plot : (default 10)max number of categories to show on plot   
    '''

    if  (categorical_variables is None) or \
        (numeric_variables is None) or \
        (len(categorical_variables) == 0) or \
        (len(numeric_variables) == 0) or \
        (n_max_categories_to_plot < 1):

        print("Nothing to plot!")
        return()


    n_plot_rows = len(categorical_variables)
    n_plot_columns = len(numeric_variables)

    f, axs = plt.subplots(n_plot_rows, n_plot_columns, 
                    figsize = (15, n_plot_rows * 5))

    temp_color = '#618ad5'

    row_index = 0

    if(len(df_to_plot) > 50000):
        df_to_plot_sampled = df_to_plot.sample(n = 50000)
    else:
        df_to_plot_sampled = df_to_plot

    for temp_categorical_var_name in categorical_variables:

        temp_value_counts = df_to_plot[temp_categorical_var_name].value_counts()

        if(len(temp_value_counts) > n_max_categories_to_plot):
            col_index = 0
            for temp_numeric_var_name in numeric_variables:
                axs[row_index][col_index].text(0.5, 0.3, 
                        "Plot skipped\nToo many categories(" + str(len(temp_value_counts)) +") in\n" + temp_categorical_var_name, 
                                                ha="center",  size=30)
                col_index = col_index + 1
        else: 
            col_index = 0
            for temp_numeric_var_name in numeric_variables:
                if len(numeric_variables) > 1:
                    plot_on_ax = axs[row_index][col_index]
                else:
                    plot_on_ax = axs[row_index]

                temp_ax = sns.boxplot(x = temp_numeric_var_name, y = temp_categorical_var_name,
                        data = df_to_plot_sampled, 
                        order = temp_value_counts.index, 
                        ax = plot_on_ax,
                        color = temp_color)
                        
                temp_ax.set_title('Box-plot')
                if col_index > 0:
                    temp_ax.set(ylabel = None, yticks = [])
                col_index = col_index + 1
        
        row_index = row_index + 1

    sns.despine(offset=10, trim=True)
    plt.tight_layout()
    plt.show()


def plot_frequency_plots_for_categorical_variables(df_to_plot, categorical_variables, n_max_categories_to_plot = 10):
    '''
    Plots frequency plots of categorical columns.
    Parameters:
        df_to_plot : pandas dataframe to plot
        categorical_variables : list of categorical variables
        n_max_categories_to_plot : (default 10)max number of categories to show on plot   
    '''

    if  (categorical_variables is None) or \
        (len(categorical_variables) == 0) or \
        (n_max_categories_to_plot < 1):
        
        print("Nothing to plot!")
        return()

    number_of_rows = int(np.ceil(len(categorical_variables)/2))
    number_of_columns = 1 if len(categorical_variables) == 1 else 2

    f, axs = plt.subplots(number_of_rows, number_of_columns, 
                figsize = (15, number_of_rows * 5))

    temp_color = '#618ad5'

    row_index = 0
    col_index = 0
    for temp_var_name in categorical_variables:

        if (number_of_rows > 1) and (number_of_columns > 1):
            temp_ax_to_plot = axs[row_index][col_index]
        elif number_of_columns > 1:
            temp_ax_to_plot = axs[col_index]
        else:
            temp_ax_to_plot = axs
            
        temp_value_counts = df_to_plot[temp_var_name].value_counts()

        if(len(temp_value_counts) > n_max_categories_to_plot):
            temp_ax_to_plot.text(0.5, 0.3,
                        "Plot skipped\nToo many categories(" + str(len(temp_value_counts)) +") in\n" + temp_var_name, 
                                                ha="center",  size=30)
        else:
            temp_ax = sns.barplot(x = temp_value_counts, y= temp_value_counts.index, 
                        ax=temp_ax_to_plot,
                        order = temp_value_counts.index,
                        color = temp_color, )

            temp_i = 0
            for index, row in pd.DataFrame(temp_value_counts).iterrows():
                temp_ax.text(row[temp_var_name], temp_i, round(row[temp_var_name], 2), color='black', ha="right")
                temp_i = temp_i + 1

            temp_ax.set_title('Frequency barplot')
            #temp_ax.set(ylabel = None, xlabel = None, yticks = [])

        col_index = 1 if (col_index == 0) else 0
        if col_index == 0:
            row_index = row_index + 1

    sns.despine(offset=10, trim=True)
    plt.tight_layout()
    plt.show()