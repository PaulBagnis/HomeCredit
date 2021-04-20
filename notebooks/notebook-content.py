import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
import imblearn
from sklearn.utils import resample
#from imblearn.combine import SMOTETomek

df = pd.read_csv("C:/Users/owcha/Desktop/application_train.csv")



#Rendu compte de nombreuses données manquantes entrée 28 et 44.
df = df.dropna(axis=0)


print('Datashape: ', df.shape)
df.head()


#Besoin de split notre dataset car cross validation->def de cross validation.

dfTrain = df.iloc[:round(df.shape[0] * 0.9),:] #90%
dfRow = df.iloc[round(df.shape[0] * 0.9):,:]  
dfTest = dfRow.iloc[:(dfRow.shape[0]-5),:]
dfKeep = dfRow.iloc[(dfRow.shape[0]-5):,:]

print('dfTrain: ',dfTrain.shape)
print('dfTest: ',dfTest.shape)
print('dfKeep: ',dfKeep.shape)



#On regarde la sortie
print( pd.value_counts(dfTrain['TARGET'], normalize=True) )

dfTrain['TARGET'].astype(int).plot.hist();



#Oversampling car jeu de données réduit

# Separate majority and minority classes
df_majority = dfTrain[dfTrain['TARGET']==0]
df_minority = dfTrain[dfTrain['TARGET']==1]
 
# Upsample minority class
df_minority_upsampled = resample(df_minority, 
                                 replace=True,     # sample with replacement
                                 n_samples=round(dfTrain.shape[0] * 0.918744),  # to match majority class
                                 random_state=123) # reproducible results
 
# Combine majority class with upsampled minority class
dfTrainUpsampled = pd.concat([df_majority, df_minority_upsampled])
 
# Display new class counts
dfTrainUpsampled['TARGET'].value_counts()
print('Training data shape: ', dfTrainUpsampled.shape)

dfTrainUpsampled['TARGET'].astype(int).plot.hist();






#Traitement des données manquantes.
def missing_values_table(df):
        # Total missing values
        mis_val = df.isnull().sum()
        
        # Percentage of missing values
        mis_val_percent = 100 * df.isnull().sum() / len(df)
        
        # Make a table with the results
        mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        
        # Rename the columns
        mis_val_table_ren_columns = mis_val_table.rename(
        columns = {0 : 'Missing Values', 1 : '% of Total Values'})
        
        # Sort the table by percentage of missing descending
        mis_val_table_ren_columns = mis_val_table_ren_columns[
            mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
        
        # Print some summary information
        print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
            "There are " + str(mis_val_table_ren_columns.shape[0]) +
              " columns that have missing values.")
        
        # Return the dataframe with missing information
        return mis_val_table_ren_columns

missing_values_table(dfTrainUpsampled)



def missing_values_by_row(df):
    count = 0
    for index, row in df.iterrows():
        for prop in row:
            if not prop:
                count += 1
                break;
                
    print(count) 
    
missing_values_by_row(dfKeep)




print( dfTrain.dtypes.value_counts() )