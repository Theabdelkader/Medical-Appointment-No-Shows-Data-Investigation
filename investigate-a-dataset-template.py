#!/usr/bin/env python
# coding: utf-8

# > **Tip**: Welcome to the Investigate a Dataset project! You will find tips in quoted sections like this to help organize your approach to your investigation. Before submitting your project, it will be a good idea to go back through your report and remove these sections to make the presentation of your work as tidy as possible. First things first, you might want to double-click this Markdown cell and change the title so that it reflects your dataset and investigation.
# 
# # Project: Investigate a Dataset (Medical Appointment No Shows)
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# > **Tip**: In this section of the report, provide a brief introduction to the dataset you've selected for analysis. At the end of this section, describe the questions that you plan on exploring over the course of the report. Try to build your report around the analysis of at least one dependent variable and three independent variables.
# >
# > If you haven't yet selected and downloaded your data, make sure you do that first before coming back here. If you're not sure what questions to ask right now, then make sure you familiarize yourself with the variables and the dataset context for ideas of what to explore.

# In[899]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html

get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# > **Tip**: In this section of the report, you will load in the data, check for cleanliness, and then trim and clean your dataset for analysis. Make sure that you document your steps carefully and justify your cleaning decisions.
# 
# ### General Properties

# In[900]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df = pd.read_csv('noshowappointments-kagglev2-may-2016.csv')
df.head()


# In[901]:


# check last rows
df.tail(10)


# In[902]:


# shape of df
df.shape


# In[903]:


# data types
df.dtypes


# In[904]:


# number of unique values for each column 
df.nunique()


# #PatientId          62299  AND AppointmentID     110527
# #this means many many patients had more than one appointments 
# # AND this CSV is about 27 Days 

# In[905]:


#first day 
df['AppointmentDay'].min()


# In[906]:


#last day
df['AppointmentDay'].max()


# In[907]:


#then some days aren't mentioned


# In[908]:


# check for lost parts
df.isnull().sum()
# as you see no data entry is missed 


# In[909]:


# check for duplicated inputs
duplicates = df.duplicated()
duplicates.sum()
# as you see no duplicates


# In[910]:


df.describe()
# to describe the CSV


# #age has many issues like max is 115 and min is -1 

# > **Tip**: You should _not_ perform too many operations in each cell. Create cells freely to explore your data. One option that you can take with this project is to do a lot of explorations in an initial notebook. These don't have to be organized, but make sure you use enough comments to understand the purpose of each code cell. Then, after you're done with your analysis, create a duplicate notebook where you will trim the excess and organize your steps so that you have a flowing, cohesive report.
# 
# > **Tip**: Make sure that you keep your reader informed on the steps that you are taking in your investigation. Follow every code cell, or every set of related code cells, with a markdown cell to describe to the reader what was found in the preceding cell(s). Try to make it so that the reader can then understand what they will be seeing in the following cell(s).
# 
# ### Data Cleaning (Replace this with more specific notes!)

# In[911]:


# After discussing the structure of the data and any problems that need to be
#   cleaned, perform those cleaning steps in the second part of this section.
df.head(0)


# In[912]:


#removing irrelevant columns which we won't use 
df.drop(['PatientId', 'AppointmentID'],axis = 1 , inplace=True)


# In[913]:


df.head(0)
#NEW LABELS


# In[914]:


def mod_string(col):
    """modifies a given string"""
    if 'Day' in col:  # ScheduledDay, AppointmentDay
        col = (col[:-3] + '_' + col[-3:])  # split the name and put _ 
    if 'No-show' in col :
        col = 'No_show'
    return col
df.rename(columns = lambda x: mod_string(x),inplace=True)
df.head(0)


# fixing data in AGE

# In[915]:


# find negative values in age
Error = df.query('Age < 0')
Error


# In[916]:


#deleting that error
df.drop(99832, axis = 0 ,inplace=True)


# In[917]:


Error = df.query('Age < 0')
Error
# NO MORE ERRORS IN AGE


# Fix data types
# convert object to datetime and keep only the date : scheduled_day ,appointment_day
# 

# In[918]:


# convert string to datetime and keep only the date
Data = ['Scheduled_Day', 'Appointment_Day']
for col in Data:
    df[col] = pd.to_datetime(pd.to_datetime(df[column]).dt.date)
df.dtypes


# In[919]:


df.head()


# In[920]:


df.dtypes
 
# Error fixed 


# In[921]:


df.Handcap.value_counts()


# we don't need to know how many handicaps 
# 

# In[922]:


df.Handcap = np.where(df['Handcap'] >= 1, 1,0)


# In[923]:


df.Handcap.value_counts()


# In[924]:


#No_show column contains YES AND NO instead of yes= 1 and No = 0 


# In[925]:


df.No_show.value_counts()


# In[926]:


df.No_show = np.where(df.No_show == "Yes", 1, 0)


# In[927]:


df.No_show.value_counts()
#already changed to zeros and ones


# In[928]:


df.head()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# > **Tip**: Now that you've trimmed and cleaned your data, you're ready to move on to exploration. Compute statistics and create visualizations with the goal of addressing the research questions that you posed in the Introduction section. It is recommended that you be systematic with your approach. Look at one variable at a time, and then follow it up by looking at relationships between variables.
# 
# ### Research Question 1 (Replace this header name!)

# gender column

# In[929]:


df.Gender.value_counts()


# In[930]:


sorted_counts = df.Gender.value_counts()
explode = (0, 0.1)
plt.pie(sorted_counts, labels = ['Female', 'Male'], startangle = 90,
        explode=explode,shadow=True,counterclock = False, autopct='%1.1f%%');
plt.title('Genders');


# no_show column

# In[931]:


df['No_show'].hist();
#Most showed up 


# In[932]:


df['Age'].hist(facecolor='r',density=True);
plt.xlabel('Age')
plt.ylabel('Num.')
plt.title('Histogram Age')

# Most patients are young


# scholarship column
# 

# In[933]:


df['Scholarship'].hist()
# Most patients had no scholarship


# In[934]:


df['Alcoholism'].hist();


# In[935]:


df['Diabetes'].hist();


# In[936]:


df['Handcap'].hist();


# In[937]:


df['Hipertension'].hist();


# In[938]:


df.head()


# Most patients didn't suffer from alcoholism, diabetes, hypertension, or handicap.

# In[939]:


# calculate days between scheduled_day and appointment_day
Days_inbetween = (df['Appointment_Day'] - df['Scheduled_Day']).dt.days
# insert a new column (days_between) before column 3
df.insert(3, 'Days_inbetween', Days_inbetween)
df.head()


# In[940]:


# make sure there are no negative values
negative = df.query('Days_inbetween < 0')
negative


# no negative days

# make age in four groups 

# In[941]:


df['Age'].describe()


# In[942]:


edges = [0, 18, 37, 55, 115]
names = ['0-18','19-37','38-55','56 and above']
age_group = pd.cut(df['Age'], edges, labels=names)
df.insert(5, 'age_group', age_group)
df.head()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# > **Tip**: Now that you've trimmed and cleaned your data, you're ready to move on to exploration. Compute statistics and create visualizations with the goal of addressing the research questions that you posed in the Introduction section. It is recommended that you be systematic with your approach. Look at one variable at a time, and then follow it up by looking at relationships between variables.
# 
# ### Research Question 1 (Can the age be used to predict if a patient will show up for their appointment?)

# In[943]:


# percentages of no show patients based on age group
no_show_perc_age = df.groupby('age_group').No_show.mean() * 100
plt.figure(figsize = [10, 7])
plt.bar(x = no_show_perc_age.index, height = no_show_perc_age)
plt.title('The Percentages of No Show Patients By Age Group')
plt.xlabel('Age')
plt.ylabel('No Show Percentage');


# (56 and above) were the most committed to showing up for their appointments
# the older the person is the more likely he is going to show up

# ### Research Question 2  (Can a scholarship affect if a patient will show up for their scheduled appointment?)

# In[944]:


# percentages of no show patients based on scholarship
no_show_perc_scholarship = df.groupby('Scholarship').No_show.mean() * 100
plt.bar(x = no_show_perc_scholarship.index, height = no_show_perc_scholarship)
plt.title('The Percentages of No Show Patients Based on Scholarship')
plt.xlabel(['No Scholarship', 'Scholarship'])
plt.ylabel('No Show Percentage');


# having a scholarship could help us to predict if a patient will show up for their scheduled appointment.
# mostly the scholarship make person shows up 

# In[945]:


# Continue to explore the data to address your additional research
#   questions. Add more headers as needed if you have more questions to
#   investigate.


# <a id='conclusions'></a>
# ## Conclusions
# 
# > **Tip**: Finally, summarize your findings and the results that have been performed. Make sure that you are clear with regards to the limitations of your exploration. If you haven't done any statistical tests, do not imply any statistical conclusions. And make sure you avoid implying causation from correlation!
# 
# > **Tip**: Once you are satisfied with your work, you should save a copy of the report in HTML or PDF form via the **File** > **Download as** submenu. Before exporting your report, check over it to make sure that the flow of the report is complete. You should probably remove all of the "Tip" quotes like this one so that the presentation is as tidy as possible. Congratulations!

# -the younger the patient is the more likely he/she is going to miss the appointment
# -it seems like a patient with a scholarship is more likely to not show up for the appointment.
