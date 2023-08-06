import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

def characteristics(data):
    
    # Shape of the data
    print('\n')
    print(f"Shape of the data: {data.shape}")
    print(f"Number of Rows in the data: {data.shape[0]}")
    print(f"Number of Columns in the data: {data.shape[1]}\n")
    print("-"*80)
    
    # Checking Data Types
    print('\n')
    print(data.info())
    print('\n')
    print("-"*80)
    
    # Understanding the Numerical & Non-Numberical Data
    numerical_features = data.select_dtypes(include=[np.number])
    categorical_features = data.select_dtypes(exclude=[np.number])
    
    print('\n')
    print(f"Number of Numerical Features: {numerical_features.shape[1]}\n")
    print(f"All Numerical Features: {numerical_features.columns}\n")
    print("-"*80)
    print('\n')
    print(f"Number of Categorical Features: {categorical_features.shape[1]}\n")
    print(f"All Categorical Features: {categorical_features.columns}\n")
    print("-"*80)
    
    
    # Null Values present in the data
    print('\n')
    print("Null Values Present in the dataset:\n")
    print(data.isna().sum(),'\n')
    print("-"*80)
    
    if data.isnull().values.any() == True:
        null_per = (data.isnull().sum()/len(data))*100
    
        try:
            # dropping columns having null percentage to 0
            mask = (null_per != 0.0)
            null_per = null_per[mask].sort_values(ascending = False)

            # Plot the Bar of %
            plt.figure(figsize=(20,12))
            null_plot = sns.barplot(x = null_per.index, y = null_per)
            plt.xticks(rotation='90')
            plt.title("Percentage of the null values in the dataset")
            plt.show()

        except:
            print("There is no null values in the dataset")
            print("Returning the dataset...")
            return data

        print(null_plot)

    else:
        print("No Null Values")
        
        print("-"*80)
        
    
    
    return data.head()

