# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 17:06:02 2026

@author: Harsh
"""

import pandas as pd 
import matplotlib.pyplot as plt 

#loading data

#Confirmed cases

confirmed_cases = pd.read_excel(r"C:\Users\Harsh\Downloads\covid_19_dataset.xlsx",
                              sheet_name='covid_19_confirmed_v1')

#Death cases

death_cases = pd.read_excel(r"C:\Users\Harsh\Downloads\covid_19_dataset.xlsx",
                            sheet_name='covid_19_deaths_v1')

#Recovered cases 

recovered_cases = pd.read_excel(r"C:\Users\Harsh\Downloads\covid_19_dataset.xlsx",
                               sheet_name='covid_19_recovered_v1')

#structure of datasets
#confirmed cases 

#rows
print("\nCovid-19 case study data analysis") 
print('\nConfirmed cases dataset shape:\n')
print("Rows:",confirmed_cases.shape[0])
#columns
print('Columns:',confirmed_cases.shape[1])
#datatypes 
print('\nConfirmed cases dataset datatypes: \n')
print(confirmed_cases.dtypes)

#Death cases 

#rows 
print("\nDeath cases dataset shape:\n")
print('Rows:',death_cases.shape[0])
#columns
print('Columns:',death_cases.shape[1])
#datatypes 
print('\nDeath cases dataset datatypes: \n')
print(death_cases.dtypes)

#Recovered cases 

#rows
print('\nRecovered cases dataset:\n')
print("Rows:",recovered_cases.shape[0])
#columns
print("Columns:",recovered_cases.shape[1])
#datatypes
print("\nRecovered cases dataset datatypes: \n")
print(recovered_cases.dtypes)


#generating plot of confirmed cases overtime for top countries

country_df = confirmed_cases.groupby('Country/Region').sum(numeric_only=True)
country_df = country_df.drop(columns=['Lat','Long'])
country_df.columns = pd.to_datetime(country_df.columns)
country_df = country_df.reindex(columns=sorted(country_df.columns))
top_5_countries = country_df.iloc[:,-1].sort_values(ascending=False).head(5).index 
top_5 = country_df.loc[top_5_countries]

all_dates = top_5.columns 
monthly = []

for i in range(len(all_dates)-1):
    if all_dates[i].month!=all_dates[i+1].month:
        monthly.append(all_dates[i])
monthly.append(all_dates[-1])

top_5_countries_monthly = top_5[monthly]

plt.figure(figsize=(14,8))
for country in top_5.index:
    plt.plot(top_5_countries_monthly.columns ,top_5_countries_monthly.loc[country],
             label=country,marker='o',linewidth=2)
    
plt.title("Covid confirmed cases of top 5 countries overtime",fontsize=19)
plt.xlabel('Confirmed cases by months',fontsize=15)    
plt.ylabel('Count of Confirmed Cases',fontsize=15)
plt.xticks(rotation=45,fontsize=13)
plt.yticks(fontsize=13)
plt.legend(title="Countries")
plt.grid(True,linestyle='--',alpha=0.5)
plt.tight_layout()
plt.show()

        
# generating a plot for China confirmed cases overtime

china_df = country_df.loc[['China']]
all_dates_china = china_df.columns 
china_monthly = []

for i in range(len(all_dates_china)-1):
    if all_dates_china[i].month != all_dates_china[i+1].month:
        china_monthly.append(all_dates_china[i])
china_monthly.append(all_dates_china[-1])

china_monthly_data = china_df[china_monthly]

plt.figure(figsize=(14,8))
plt.plot(china_monthly_data.columns,china_monthly_data.loc['China'],label=country,
         marker='o',linewidth=2,color='red')
plt.title('China confirmed cases monthly overtime',fontsize=19)
plt.xlabel('Confirmed cases by months',fontsize=15)
plt.ylabel("Count of confirmed cases",fontsize=15)
plt.xticks(rotation=45,fontsize=13)
plt.yticks(fontsize=13)
plt.grid(True,linestyle='--',alpha=0.5)
plt.tight_layout()
plt.show()
        
#handling missing values 
#count of missing values in confirmed cases
print('\nMissing values in each column of confirmed cases\n\n',confirmed_cases.isnull().sum(),sep='')

#count of rows with missing values 
print("\nTotal rows with missing values in confirmed cases:\n",confirmed_cases[confirmed_cases.isnull().any(axis=1)].shape[0],sep='')

#count of missing values in death cases
print('\nMissing values in each column of death cases\n\n',death_cases.isnull().sum(),sep='')

#count of rows with missing values 
print("\nTotal rows with missing values in death cases:\n",death_cases[death_cases.isnull().any(axis=1)].shape[0],sep='')

#count of missing values in recovered cases
print('\nMissing values in each column of recovered cases\n\n',recovered_cases.isnull().sum(),sep='')

#count of rows with missing values 
print("\nTotal rows with missing values in recovered cases:\n",recovered_cases[recovered_cases.isnull().any(axis=1)].shape[0],sep='')


#replacing blank value in province/state in every cases

confirmed_cases['Province/State'] = confirmed_cases['Province/State'].fillna('All Provinces')

death_cases['Province/State'] = death_cases['Province/State'].fillna('All Provinces')

recovered_cases['Province/State'] = recovered_cases['Province/State'].fillna('All Provinces')
       
#indepenent data analysis 
# analyzing peak number of cases in Germany,France and Italy

countries = ['Germany','France','Italy']
selected_df = country_df.loc[countries]
daily_cases = selected_df.diff(axis=1)
daily_cases.iloc[:,0] = selected_df.iloc[:,0]

result = []
for country in countries:
    peak_cases = daily_cases.loc[country].max()
    peak_date = daily_cases.loc[country].idxmax()
    
    result.append({'Country':country,"Peak date":peak_date,'Peak cases':peak_cases})
    

result_df = pd.DataFrame(result)

print('\n',result_df,'\n')

highest = result_df.loc[result_df['Peak cases'].idxmax()]

print(f"\nCountry with highest single day peak is {highest['Country']} with cases {highest['Peak cases']} on {highest['Peak date']}.\n")

#comparing the recovery rate (recoveries/confirmed) between Canada and Australia on 
# December 31 2020

recovery_df = recovered_cases.groupby('Country/Region').sum(numeric_only=True)
recovery_df = recovery_df.drop(columns=['Lat','Long'])
recovery_df.columns = pd.to_datetime(recovery_df.columns)

date = pd.Timestamp('2020-12-31')
recovered_countries = ['Canada','Australia']
recovered_rate = []
for country in recovered_countries:
    recovery_count = recovery_df.loc[country,date]
    confirmed_count = country_df.loc[country,date]
    
    recovery_rate = (recovery_count/confirmed_count)*100
    recovered_rate.append({"Country":country,"Recovery rate":round(recovery_rate,2)})
    
recovered_df = pd.DataFrame(recovered_rate)
highest = recovered_df.loc[recovered_df['Recovery rate'].idxmax()]
print(recovered_df)
print(f"\nCountry with better recovery rate between Canada,Australia is {highest['Country']} with the recovery rate of {highest['Recovery rate']}.\n")    
    
#identifying the distribution of death rates among provinces in Canada and 
#finding provinces with max and lowest rate at latest date

latest_date = country_df.columns[-1]
canada_confirmed = confirmed_cases[confirmed_cases['Country/Region']=='Canada']
canada_deaths = death_cases[death_cases['Country/Region']=='Canada']

canada_merge = pd.merge(canada_confirmed[["Province/State",latest_date]],
                        canada_deaths[['Province/State',latest_date]],
                        on='Province/State',suffixes=('_confirmed',"_deaths"))
canada_merge.rename(columns={f"{latest_date}_confirmed":"Confirmed",
                             f"{latest_date}_deaths":'Deaths'},inplace=True)

canada_merge['Death rate (%)'] = (canada_merge['Deaths']/canada_merge['Confirmed'])*100

canada_merge = canada_merge[canada_merge['Confirmed']>0]
canada_merge = canada_merge.sort_values(by='Death rate (%)',ascending=False)

highest_death_rate = canada_merge.loc[canada_merge['Death rate (%)'].idxmax()]
lowest_death_rate = canada_merge.loc[canada_merge['Death rate (%)'].idxmin()]




print("Merged Canada data for confirmed and death cases\n\n",canada_merge,sep='')
print("\nCanada province with highest death rate:\n")
print(highest_death_rate)

print("\nCanada province with lowest death rate:\n")
print(lowest_death_rate)

#data transform 
#transforming death data 

death_long = pd.melt(death_cases,id_vars=['Province/State','Country/Region','Lat','Long'],
                     var_name='Date',value_name='Deaths')
death_long['Date'] = pd.to_datetime(death_long['Date'])
death_long = death_long.sort_values(by=['Country/Region','Province/State','Date'])
print("\nTransformed death dataset\n\n",death_long,sep='')

#total of deaths reported per country 
last_date_col = death_cases.columns[-1]
total_deaths = death_long[death_long['Date']==last_date_col].groupby("Country/Region")['Deaths'].sum().reset_index().sort_values('Deaths',ascending=False)


print(f"\nLatest Date : {last_date_col}")
print('\nTotal Deaths in every country as per latest date:\n\n',total_deaths,sep='')
country_deaths = death_long.groupby(["Country/Region",'Date'])['Deaths'].sum().reset_index()
#top 5 countries with the highest average daily deaths 
country_deaths["Daily Deaths"] = (
    country_deaths
    .groupby("Country/Region")["Deaths"]
    .diff()
) 
country_deaths["Daily Deaths"] = country_deaths["Daily Deaths"].fillna(country_deaths["Deaths"])

top_5_avg_deaths = (
    country_deaths
    .groupby("Country/Region")["Daily Deaths"]
    .mean()
    .reset_index()
    .sort_values("Daily Deaths", ascending=False)
)

print("\n--- Top 5 Countries by Highest Average Daily Deaths ---\n")
print(top_5_avg_deaths.head(5))

us_death_data = country_deaths[country_deaths['Country/Region']=='US'].copy()
us_death_data['Months'] = us_death_data['Date'].dt.to_period('M')

us_death_final = us_death_data.sort_values('Date').groupby('Months',as_index=False).last().reset_index()

plt.figure(figsize=(12,8))
plt.plot(us_death_final['Months'].astype(str),us_death_final['Deaths'],marker='o',linewidth=2)
plt.xlabel("Month wise")
plt.ylabel('Covid death cases')
plt.title('US covid deaths overtime')
plt.xticks(rotation=45)
plt.grid(True,linestyle='--',linewidth=2)
plt.tight_layout()
plt.show()

#data merging 
#merging the transformed data
#since death dataset is already transformed we do not need to transfom it 

#confirm cases
confirmed_long = pd.melt(confirmed_cases,id_vars=['Province/State','Country/Region','Lat','Long'],
                     var_name='Date',value_name='Confirmed')
confirmed_long['Date'] = pd.to_datetime(confirmed_long["Date"]) 

recovered_long = pd.melt(recovered_cases,id_vars=['Province/State','Country/Region','Lat','Long'],
                     var_name='Date',value_name='Recovered')
recovered_long['Date'] = pd.to_datetime(recovered_long["Date"]) 
merge_df = pd.merge(confirmed_long,death_long,how='inner',on=['Province/State','Country/Region','Lat','Long','Date'])
merge_df = pd.merge(merge_df,recovered_long,how='inner',on=['Province/State','Country/Region','Lat','Long','Date'])

#analyzing the monthly confirmed,deaths,recoveries

merge_df['Month'] = merge_df['Date'].dt.to_period('M')
monthly_summary = merge_df.groupby(["Country/Region",'Month'])["Confirmed",'Recovered','Deaths'].sum().reset_index()
print("\nMonthly summary of combined transformed data\n\n",monthly_summary,sep='')

#Redoing the analyses in the last question of monthly summary for 'Brazil','US','Italy' and puting it on plot

countries = ['Brazil','US','Italy']

selected = monthly_summary[monthly_summary['Country/Region'].isin(countries)]
fig,axes = plt.subplots(3,1,figsize=(14,15))
metrics = ['Confirmed','Deaths','Recovered']
for ax,metric in zip(axes,metrics):
    for country in countries:
        country_data = selected[selected['Country/Region']==country]
        ax.plot(country_data['Month'].astype(str),
                country_data[metric],
                label=country,
                marker='o'
                )
    ax.set_title(f"Monthly {metric}")
    ax.set_xlabel("Months")
    ax.set_ylabel(metric)
    ax.tick_params(axis='x',labelrotation=45)
    ax.grid(True,linestyle='--',alpha=0.5)
    ax.legend() 
plt.tight_layout()
plt.show()

#with the combined dataset identifying the three countries with the highest 
#average death rates in the year 2020

merge_2020 = merge_df[merge_df['Date'].dt.year==2020].copy()

merge_2020 = merge_2020[merge_2020['Confirmed']>0]

merge_2020['Death rate'] = (merge_2020['Deaths']/merge_2020['Confirmed'])*100

average_df = merge_2020.groupby("Country/Region")['Death rate'].mean().reset_index()

top_3 = average_df.sort_values(by='Death rate',ascending=False).head(3)

print("\nTop three countries with the highest death rate in the year 2020\n\n",top_3,sep='')

#using the merged dataset to find total number of recoveres to death in South Africa

south_africa = merge_df[merge_df['Country/Region']=='South Africa']

latest_date = south_africa['Date'].max()

latest_data = south_africa[south_africa['Date']==latest_date]

recoveries_southafrica = latest_data['Recovered'].sum()
deaths_southafrica = latest_data['Deaths'].sum()

ratio = recoveries_southafrica/deaths_southafrica
print('\nRatio of total number of recoveries/total number of deaths in South Africa:\n',round(ratio,2),sep='')

#analyzing the ratio of recoveries to confirmed cases monthly for US from March 2020 to May 2021

us = merge_df[merge_df['Country/Region']=='US'].copy()
us = us[(us['Date']>='2020-03-01') & (us['Date']<='2021-05-31')]
us['Month'] = us['Date'].dt.to_period('M')

us_groupby = us.groupby('Month')[['Confirmed','Recovered','Deaths']].sum().reset_index()
us_groupby['Ratio'] = (us_groupby['Recovered']/us_groupby['Confirmed'])*100 

highest = us_groupby.loc[us_groupby['Ratio'].idxmax()]
print('\nMonth with the Highest ratio of recovered to confirmed cases in US:\n\n',highest,sep='')
