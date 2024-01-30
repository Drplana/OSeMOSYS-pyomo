#%%
import pandas as pd
import numpy as np
import calendar
#%%
# Read in your data as a pandas DataFrame
data = pd.read_excel('DatosCub.xlsx', sheet_name = "Sheet1" )
cfwind = pd.read_excel('DatosCub.xlsx', sheet_name = "Sheet2" )
cfpv = pd.read_excel('DatosCub.xlsx', sheet_name = "CFSOL" )
#%%
start_date = '2023-01-01'
end_date = '2024-01-01'
date_range = pd.date_range(start=start_date, end=end_date, freq='H')
hourly_data = pd.DataFrame({'Date': date_range})

# Convert the 'Date' column to a datetime object
#data['Date'] = pd.to_datetime(data['Date'])
data = pd.concat([hourly_data, data], axis=1)

data['Total'] =data.loc[:,'Node1':].sum(axis=1)

data['Hour'] = data['Date'].dt.hour
data['Weekend'] = data['Date'].dt.dayofweek >= 5
data['Month'] = data['Date'].dt.month

def season_mapping(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Autumn'
    else:
        return 'Unknown'
#%%

data['Season'] =  data['Month'].apply(season_mapping)
season_order = (data['Season'].unique()) 
data = pd.concat([data, cfpv['Average'], cfwind['Wind']], axis=1)
#%%
# Define the time ranges for the different groups of hours
night_hours = list(range(20, 24)) + list(range(0, 1))
dawn_hours = range(1, 6)
sunrise_hours = range(6, 8)
morning_hours = range(8, 11)
noonpeak_hour = range(11, 13)
afternoon_hours = range(13, 16)
eveningpeak_hours = range(16,18)
night_hours_2 = list(range(18, 20)) 

# Filter the data to only include workdays and weekends
workdays = data[data['Weekend'] == False]
weekends = data[data['Weekend'] == True]


hour_group_order = ['Night', 'Dawnn', 'Sunrise', 'Morning', 'NoonPeak', 'Afternoon', 'EveningPeak', 'Night 2']
# Create a new column indicating the hour group for each observation
workdays['Hour_Group'] = pd.Categorical( np.select([workdays['Hour'].isin(night_hours), workdays['Hour'].isin(dawn_hours), 
                                    workdays['Hour'].isin(sunrise_hours), workdays['Hour'].isin(morning_hours), 
                                    workdays['Hour'].isin(noonpeak_hour), workdays['Hour'].isin(afternoon_hours), 
                                    workdays['Hour'].isin(eveningpeak_hours), workdays['Hour'].isin(night_hours_2)], 
                                    ['Night', 'Dawnn', 'Sunrise', 'Morning', 'NoonPeak', 'Afternoon', 'EveningPeak', 'Night 2']),
                                        categories=hour_group_order, ordered=True)
weekends['Hour_Group'] = pd.Categorical(np.select([weekends['Hour'].isin(night_hours), weekends['Hour'].isin(dawn_hours), 
                                    weekends['Hour'].isin(sunrise_hours), weekends['Hour'].isin(morning_hours), 
                                    weekends['Hour'].isin(noonpeak_hour), weekends['Hour'].isin(afternoon_hours), 
                                    weekends['Hour'].isin(eveningpeak_hours), weekends['Hour'].isin(night_hours_2)], 
                                    ['Night', 'Dawnn', 'Sunrise', 'Morning', 'NoonPeak', 'Afternoon', 'EveningPeak', 'Night 2']),
                                         categories=hour_group_order, ordered=True)
#%%
cfpv = pd.concat([workdays, weekends]) \
    .groupby(['Season','Weekend','Hour_Group']) \
        ['Average'].mean().dropna().reset_index(name = 'Average')
cfpv ['Season']= pd.Categorical(cfpv['Season'], categories=season_order, ordered=True)        
cfpv = cfpv.sort_values(['Season', 'Weekend', 'Hour_Group'])     
   
cfwind = pd.concat([workdays, weekends]) \
    .groupby(['Season','Weekend','Hour_Group']) \
        ['Wind'].mean().dropna().reset_index(name = 'Wind')
cfwind ['Season']= pd.Categorical(cfwind['Season'], categories=season_order, ordered=True)        
cfwind = cfwind.sort_values(['Season', 'Weekend', 'Hour_Group'])          
# Calcular la suma de las horas 
hourly_sum_by_season_month_hour_group = pd.concat([workdays, weekends]) \
    .groupby(['Season','Weekend','Hour_Group']) \
        ['Total'].sum()
hourly_sum_by_season_month_hour_group = hourly_sum_by_season_month_hour_group[hourly_sum_by_season_month_hour_group != 0]
total_sum = data['Total'].sum()

normalized_hourly_sum = hourly_sum_by_season_month_hour_group.div(total_sum).reset_index(name='Value')
normalized_hourly_sum ['Season'] = pd.Categorical(normalized_hourly_sum['Season'], categories=season_order, ordered=True)
normalized_hourly_sum = normalized_hourly_sum.sort_values(['Season', 'Weekend', 'Hour_Group'])

#data['fraction'] = normalized_hourly_sum
#hourly_sum_by_season_month_hour_group.to_excel('postdatas.xlsx')
# Group the workday data by month and hour and calculate the sum of the 'Value' column
hourly_sum_workdays_by_month = workdays.groupby(['Month', 'Hour'])['Total'].sum()

# Group the weekend data by month and hour and calculate the sum of the 'Value' column
hourly_sum_weekends_by_month = weekends.groupby(['Month', 'Hour'])['Total'].sum()

#%%
# Create a list of dates with the start and end date of the data
dates = pd.date_range(start='1/1/2023', end='12/31/2023')

# Create a DataFrame with a column of dates
df = pd.DataFrame({'date': dates})

# Extract the month and day of week from the date column

df['Month'] = df['date'].dt.month_name()
df['Type'] = df['date'].apply(lambda x: 'Weekday' if x.weekday() < 5 else 'Weekend')
df['Season'] = df['date'].dt.month.map(season_mapping)
# Create a new DataFrame with the number of weekdays and weekends by month

monthly_counts = df.groupby(['Season', 'Type']).size().reset_index(name='Value')
#%%
# Sort the order of the months chronologically
#month_order = [calendar.month_name[i] for i in range(1, 13)]
monthly_counts['Season'] = pd.Categorical(monthly_counts['Season'], categories=season_order, ordered=True)

# Sort the rows of the monthly_counts DataFrame
monthly_counts = monthly_counts.sort_values(['Season', 'Type'])
# Para multiplicar los valores de una lista con otra.
lengths = [len(night_hours), len(dawn_hours), len(sunrise_hours), len(morning_hours), len(noonpeak_hour), len(afternoon_hours), len(eveningpeak_hours), len(night_hours_2)]

result = []
for i in monthly_counts['Value']:
    for j in lengths:
        result.append(i*j/8760)
result = pd.DataFrame({'result': result}, index = None)

season = range(1,5)
daytype = range(1, 3)
dailytimebracket = range (1, 9)

timeslices = []

for s in season:
    for o in daytype:
        for f in dailytimebracket:
            num = str(s) + str(o) + str(f)
            timeslices.append(int(num))
timeslices = pd.DataFrame({'timeslices': timeslices}, index = None)
hourratio = pd.concat([timeslices,result],axis=1)



with pd.ExcelWriter('output4.xlsx') as writer:
    # write the first dataframe to a sheet named 'Sheet1'
    hourratio.to_excel(writer, sheet_name='YS', index=False)
    # write the second dataframe to a sheet named 'Sheet2'
    normalized_hourly_sum.to_excel(writer, sheet_name='SDP', index=True)
    cfpv.to_excel(writer, sheet_name='CFPV', index=True)
    cfwind.to_excel(writer, sheet_name='CFWIND', index=True)
# Filter the data to only include workdays
"""
workdays = data[data['Date'].dt.dayofweek < 5]
weekends = data[data['Date'].dt.dayofweek >= 5]
workdays['Hour'] = workdays['Date'].dt.hour
workdays['Month'] = workdays['Date'].dt.month
weekends['Hour'] = weekends['Date'].dt.hour
"""

#%%
# Filter the data to only include the first hour of each day
"first_hour = workdays[workdays['Date'].dt.hour == 0]"
# Group the data by month, then hour and calculate the mean of the 'Value' column
hourly_avg_by_month = workdays.groupby(['Month', 'Hour'])['Total'].mean()
hourly_sum_by_month = workdays.groupby(['Month', 'Hour'])['Total'].sum()
# Group the data by month and calculate the mean of the 'Value' column
"monthly_avg = first_hour.groupby(pd.Grouper(key='Date', freq='M'))['Total'].mean()"

# Print the resulting monthly averages

# %%
