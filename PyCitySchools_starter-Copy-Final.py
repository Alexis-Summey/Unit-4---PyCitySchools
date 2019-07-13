#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# * As a whole, schools with higher budgets, did not yield better test results. By contrast, schools with higher spending per student actually (\$645-675) underperformed compared to schools with smaller budgets (<\$585 per student).
# 
# * As a whole, smaller and medium sized schools dramatically out-performed large sized schools on passing math performances (89-91% passing vs 67%).
# 
# * As a whole, charter schools out-performed the public district schools across all metrics. However, more analysis will be required to glean if the effect is due to school practices or the fact that charter schools tend to serve smaller student populations per school. 
# ---

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head(10)


# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[2]:


#Pandas Unit 3 - Bugfixing Bonanza
total_schools = school_data["school_name"].count()
total_students = school_data_complete["student_name"].count()
total_budget = school_data["budget"].sum()
avg_math_score = school_data_complete["math_score"].mean()
avg_reading_score = school_data_complete["reading_score"].mean()

# Passing math score 70 +

passing_math = school_data_complete.loc[(student_data["math_score"] >= 70)]
count_passing_math = passing_math["math_score"].count()
percent_math_pass = (count_passing_math/total_students)*100

# Passing reading score 70 +

passing_reading = school_data_complete.loc[(student_data["reading_score"] >= 70)]
count_passing_reading = passing_reading["reading_score"].count()
percent_reading_pass = (count_passing_reading/total_students)*100

#Overall passing rate (0verall score)

overall_passing_rate = (count_passing_math + count_passing_reading)/2

# Create new data fram to mirror the table in the homework instructions

district_summary = {"Total Schools" : total_schools,
                   "Total Students" : total_students,
                   "Total Budget" : total_budget,
                   "Average Math Score" : avg_math_score,
                   "Average Reading Score" : avg_reading_score,
                   "% Passing Math" : percent_math_pass,
                   "% Passing Reading" : percent_reading_pass,
                   "% Overall Passing Rate" : overall_passing_rate}
district_summary_df = pd.DataFrame([district_summary])
district_summary_df = district_summary_df[["Total Schools", "Total Students", "Total Budget", "Average Math Score",
                                          "Average Reading Score", "% Passing Math", "% Passing Reading",
                                          "% Overall Passing Rate"]]
district_summary_df


# ## School Summary

# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)
#   
# * Create a dataframe to hold the above results

# In[3]:


#School Summary

copy_school_sum = school_data.copy()
avg_math_reading_table = school_data_complete.groupby(['school_name'])['reading_score', 
                                                                       'math_score'].mean().reset_index()
copy_school_sum['Per Student Budget'] = copy_school_sum['budget']/copy_school_sum['size']

copy_school_sum = copy_school_sum.merge(avg_math_reading_table, on='school_name', how="outer")

summary_passing_reading = school_data_complete[school_data_complete['reading_score'] >=70]

summary_passing_math = school_data_complete[school_data_complete['math_score'] >=70]

# How many students are passing in reading & math?

count_pass_reading = summary_passing_reading.groupby(["school_name"])['reading_score'].count().reset_index()

count_pass_math = summary_passing_math.groupby(["school_name"])['math_score'].count().reset_index()


# Rename columns to Math and Reading Count

count_pass_reading.rename_axis({'reading_score' : 'Reading Count'}, axis=1, inplace=True)

count_pass_math.rename_axis({'math_score' : 'Math Count'}, axis=1, inplace=True)


# Overall Pass Rate -- Need to merge

overall_pass_count = count_pass_math.merge(count_pass_reading, on="school_name", how='outer')

copy_school_sum = copy_school_sum.merge(overall_pass_count, on="school_name", how='outer')


# % Passing Reading and Math

copy_school_sum['% Passing Reading'] = (copy_school_sum['Reading Count']/copy_school_sum['size'])*100
copy_school_sum['% Passing Math'] = (copy_school_sum['Math Count']/copy_school_sum['size'])*100


# % Overall Pass Rate

copy_school_sum['% Overall Passing Rate'] = (copy_school_sum['% Passing Math'] + copy_school_sum['% Passing Reading'])/2

# Needed to name columns

copy_school_sum.rename_axis({'reading_score' : 'Average Reading Score', 'math_score' : 'Average Math Score'}, axis=1, inplace=True)
copy_school_sum.rename_axis({'school_name' : 'School Name'}, axis=1, inplace=True)
copy_school_sum.rename_axis({'type' : 'School Type'}, axis=1, inplace=True)
copy_school_sum.rename_axis({'size' : 'Size'}, axis=1, inplace=True)
copy_school_sum.rename_axis({'budget' : 'School Budget'}, axis=1, inplace=True)

# I noticed that I needed to delete some columns from the table

del copy_school_sum['Math Count']
del copy_school_sum['Reading Count']
del copy_school_sum['School ID']


copy_school_sum.head(10)


# ## Top Performing Schools (By Passing Rate)

# * Sort and display the top five schools in overall passing rate

# In[4]:


# Top Performing Schools (by passing rate)

top_performing_pass_rate = copy_school_sum.sort_values(by=['% Overall Passing Rate'], ascending=False).head(10)
top_performing_pass_rate


# ## Bottom Performing Schools (By Passing Rate)

# * Sort and display the five worst-performing schools

# In[5]:


worst_performing_pass_rate = copy_school_sum.sort_values(by=['% Overall Passing Rate']).head(10)
worst_performing_pass_rate


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[33]:


# Math scores by grade

#math_nineth = student_data.loc[student_data['grade'] == '9th'].groupby('school_name')['math_score'].mean()
#math_tenth = student_data.loc[student_data['grade'] == '10th'].groupby('school_name')['math_score'].mean()
#math_eleventh = student_data.loc[student_data['grade'] == '11th'].groupby('school_name')['math_score'].mean()
#math_twelfth = student_data.loc[student_data['grade'] == '12th'].groupby('school_name')['math_score'].mean()

#math_scores_df = pd.DataFrame({"9th" : math_nineth, 
#                              "10th" : math_tenth,
#                              "11th" : math_eleventh,
#                              "12th" : math_twelfth})
#math_scores_df = ['9th', '10th', '11th', '12th']


#math_scores_df.head(10)

math_nineth = student_data.loc[student_data['grade'] == '9th'].groupby('school_name')['math_score'].mean()
math_tenth = student_data.loc[student_data['grade'] == '10th'].groupby('school_name')['math_score'].mean()
math_eleventh = student_data.loc[student_data['grade'] == '11th'].groupby('school_name')['math_score'].mean()
math_twelfth = student_data.loc[student_data['grade'] == '12th'].groupby('school_name')['math_score'].mean()

math_scores_df = pd.DataFrame({"9th" : math_nineth, 
                               "10th" : math_tenth,
                               "11th" : math_eleventh,
                               "12th" : math_twelfth})

math_scores_grade = school_data_complete.groupby(["school_name"])['grade'].count().reset_index()
math_scores_grade

## Reading Score by Grade 
# * Perform the same operations as above for reading scores

# In[34]:


reading_nineth = student_data.loc[student_data['grade'] == '9th'].groupby('school_name')['reading_score'].mean()
reading_tenth = student_data.loc[student_data['grade'] == '10th'].groupby('school_name')['reading_score'].mean()
reading_eleventh = student_data.loc[student_data['grade'] == '11th'].groupby('school_name')['reading_score'].mean()
reading_twelfth = student_data.loc[student_data['grade'] == '12th'].groupby('school_name')['reading_score'].mean()

reading_scores_df = pd.DataFrame({"9th" : reading_nineth, 
                               "10th" : reading_tenth,
                               "11th" : reading_eleventh,
                               "12th" : reading_twelfth})

reading_scores_grade = school_data_complete.groupby(["school_name"])['grade'].count().reset_index()
reading_scores_grade


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[38]:


# Sample bins. Feel free to create your own bins.
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]


# In[47]:


#print(school_data_complete["math_score"].mean())
#print(school_data_complete["reading_score"].mean())

school_spending_bins = pd.cut(copy_school_sum['Per Student Budget'], spending_bins, labels=group_names)

school_spending_bins = pd.DataFrame(school_spending_bins)

copy_school_sum['Spending Level'] = school_spending_bins

scores_by_school_spending = copy_school_sum.groupby(['Spending Level'])['Average Reading Score', 
                                                                       'Average Math Score',
                                                                       '% Passing Reading',
                                                                       '% Passing Math',
                                                                       '% Overall Passing Rate'].mean()
scores_by_school_spending


# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[49]:


# Sample bins. Feel free to create your own bins.
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[51]:


school_size_bins = pd.cut(copy_school_sum['Size'], size_bins, labels=group_names)

school_size_bins = pd.DataFrame(school_size_bins)

copy_school_sum['Size Level'] = school_size_bins

scores_by_school_size = copy_school_sum.groupby(['Size Level'])['Average Reading Score', 
                                                                       'Average Math Score',
                                                                       '% Passing Reading',
                                                                       '% Passing Math',
                                                                       '% Overall Passing Rate'].mean()
scores_by_school_size.head()


# ## Scores by School Type

# * Perform the same operations as above, based on school type.

# In[58]:


#type_bins = [0, 1000, 2000]
#group_names = [Charter, District]


# In[60]:


scores_by_school_type = copy_school_sum.copy()

scores_by_school_type = pd.DataFrame(scores_by_school_type)

scores_by_school_type = copy_school_sum.groupby(['School Type'])['Average Reading Score',
                                                         'Average Math Score',
                                                         '% Passing Reading', 
                                                         '% Passing Math',
                                                         '% Overall Passing Rate'].mean()
scores_by_school_type.head()


# In[ ]:




