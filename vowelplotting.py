"""
Last updated November 22 2020
@author: Emily Remirez (eremirez@berkeley.edu)
"""

%matplotlib inline
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
import seaborn as sns
import matplotlib.ticker as ticker
from matplotlib.ticker import ScalarFormatter

def vowelplot (vowelcsv, F1="F1", F2="F2", vowel = "Vowel", color=None, title="Vowel Plot", unit="Hz", logscale=False):
    """
    Produce a plot in F1-F2 space for a dataframe of vowel measurements 
    --
    
    Required parameters:
    
    vowelcsv = dataframe of vowel measurements, containing minimally F1 and F2 measurements, plus labels for vowels
    
    F1 = string matching the name of the column to be plotted on the Y axis; defaults to "F1"
    
    F2 = string matching the name of the column to be plotted on the X axis; defaulty to "F2"
    
    vowel = string matching the name of the column to be used as labels for points. Defaults to "Vowel".
      If None, points will not be labeled in the plot.
    --
    
    Optional parameters:
    
    color = string matching one of the column names in data frame. Will be used to set the hue parameter in plot.
    
    title = string giving the title to be used for the plot. Defaults to "Vowel Plot"
    
    unit = string indicating what unit should be added to axis labels. Defaults to "Hz"
    
    logscale = boolean indicating whether axes should be converted to logscale
    --
    
    """
    
    
    
    #Set some parameters for the chart itself
    sns.set(style='ticks', context='talk')
    plt.figure(figsize=(10,10))
    
    # If there's an argument for color, determine whether it's likely to be categorical
    ## If it's a string (text), use a categorical color palette
    ## If it's a number, use a sequential color palette
    if color != None:
        if type(vowelcsv[color].iloc[0])==str:
            pal="husl"
        else:
            pal="viridis"
            
        pl = sns.scatterplot(x=F2,y=F1,hue=color,data=vowelcsv,palette=pal)
        
    # If no color argument is given, don't specify hue, and no palette needed
    else:
        pl = sns.scatterplot(x=F2,y=F1, data=vowelcsv)
    
    
    #Invert axes to correlate with articulatory space!
    pl.invert_yaxis()
    pl.invert_xaxis()
    
    #Add unit to the axis labels
    F1name=str("F1 ("+unit+")")
    F2name=str("F2 ("+unit+")")
    laby=plt.ylabel(F1name)
    labx=plt.xlabel(F2name)
    
    if logscale == True:
        pl.loglog()
        pl.yaxis.set_major_formatter(ticker.ScalarFormatter())
        pl.yaxis.set_minor_formatter(ticker.ScalarFormatter())
        pl.xaxis.set_major_formatter(ticker.ScalarFormatter())
        pl.xaxis.set_minor_formatter(ticker.ScalarFormatter())
    
    #Add vowel labels
    if vowel != None: 
        for line,row in vowelcsv.iterrows():
            pl.text(vowelcsv[F2][line]+0.1, vowelcsv[F1][line], vowelcsv[vowel][line], horizontalalignment='left',
                size='medium', color='black', weight='semibold')
    
        pl.set_title(title)
    
    return pl

def barkify (data, formants):
    """
    Converts Hz values in a dataframe to Bark scale, adding a column to the original dataframe
    with corresponding values prefixed with z. 
    --
    
    Required parameters:
    
    data = dataframe containing data to be converted 
    
    formants = list of columns to be converted; column name must end with a number
    
    """
    
    # For each formant listed, make a copy of the column prefixed with z
    for formant in formants:
        for ch in formant:
            if ch.isnumeric():
                num=ch
        formantchar = (formant.split(num)[0])
        name = str(formant).replace(formantchar,'z')
        # Convert each value from Hz to Bark
        data[name] = 26.81/ (1+ 1960/data[formant]) - 0.53
    # Return the dataframe with the changes
    return data


def Lobify (data,group,formants):
    """
    Applies Lobanov (z-score) normalization to vowels according to a grouping variable
    Adds a column to original dataframe for each formant, with zsc prefixed to the formant name
    --
    
    Required parameters:
    
    data = dataframe containing data to transform
    
    group = string matching the name of column to normalize by, for example "speaker" 
    
    formants = list of strings matching the names of columns to be normalized
    
    """
    zscore = lambda x: (x - x.mean()) / x.std()
    for formant in formants: 
        name = str("zsc"+formant)
        col = data.groupby([group])[formant].transform(zscore)
        data.insert(len(data.columns),name,col)
    return data 
