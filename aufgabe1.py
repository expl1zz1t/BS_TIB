import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter
from lifelines import KaplanMeierFitter 

def KaplanMeier(timestamps, T):
    ts = Counter(timestamps)
    n = sum(ts.values())
    props = []
    times = []
    prop = 1.0
    
    for t,d in ts.items():
        if T==0 or t < T:
            prop = ((n-d)/n)*prop
            n = n-d          
        times.append(t)
        props.append(prop)            
            
    kms = (times,props)
    return kms

#Import Data
data_df = pd.read_excel('./Aufgabe1_data.xlsx')
sorted_data_df = data_df.sort_values(by=[0])
time_of_fail = sorted_data_df[0].to_numpy().copy()
nr_of_fail = sorted_data_df['Unnamed: 0']

# print and sort whole sheet data
plt.figure(num="Import Data")
plt.xlabel("Ausfall Nr") 
plt.ylabel("Zeit in Jahre")
plt.title('Ausfälle nach Jahre')
plt.bar(nr_of_fail,time_of_fail,width=3)
plt.plot(time_of_fail,'r')
plt.legend(('Sorted Data', 'Import Data'), loc='upper center', shadow=True)

#Print Plots with Data
plt.figure(num="Zuverlässigkeitsfunktion")
plt.ylabel('Ausfallrate') 
plt.xlabel("Jahre") 
plt.title('Zuverlässigkeitsfunktion')

#Aufgabe a)
#Kaplan-Maier-Schätzer
kmf = KaplanMeierFitter() 
kmf.fit(time_of_fail,nr_of_fail)
kmf.plot() #Gegenprobe

kms = KaplanMeier(time_of_fail, 0)
plt.plot(kms[0],kms[1],'g')

#Aufgabe b)
# #Zuverlässigkeitsfunktion Maximum-Liklihood
# lamda berechnen
n = len (data_df)
lam = n / data_df[0].sum()
R_t = lambda t: np.exp(-lam*t)
t = np.linspace(0,2)
plt.plot(t, R_t(t))

plt.legend(('KM-Fitter', 'KMS-Streuung', 'Kaplan-Maier', 'Maximum-Liklihood'), loc='upper right', shadow=True)


# --------------------------------------
## Zensierte Daten
# --------------------------------------

#Import Data
data_df_cens = pd.read_excel('./Aufgabe1_data_cens.xlsx')
sorted_data_df_cens = data_df_cens.sort_values(by=[0])
time_of_fail_cens = sorted_data_df_cens[0].to_numpy().copy()
nr_of_fail_cens = sorted_data_df_cens['Unnamed: 0']

# print and sort whole sheet data
plt.figure(num="Import Data Cens")
plt.xlabel("Ausfall Nr") 
plt.ylabel("Zeit in Jahre")
plt.title('Ausfälle nach Jahre')
plt.bar(nr_of_fail_cens, time_of_fail_cens, width=3)
plt.plot(time_of_fail_cens,'r')
plt.legend(('Sorted Data', 'Import Data'), loc='upper center', shadow=True)

#Print Plots with Data
plt.figure(num="Zuverlässigkeitsfunktion Cens")
plt.ylabel('Ausfallrate') 
plt.xlabel("Jahre") 
plt.title('Zuverlässigkeitsfunktion Cens')
T = 0.25

#Aufgabe c)
kmf = KaplanMeierFitter()
kmf.fit(time_of_fail_cens,nr_of_fail_cens)
kmf.plot() #Gegenprobe

kms = KaplanMeier(time_of_fail_cens, T)
plt.plot(kms[0],kms[1],'g')

#Aufgabe d)
list_ti = [ti for ti in time_of_fail_cens if ti != 0.25]
sum_ti = sum(list_ti)
# r: ausgefallen
# n-r: nicht ausgefallen
n = len(time_of_fail_cens)
r = len(list_ti)
lam_cens = r / (sum_ti+(n-r)*T)

R_t_cens = lambda t: np.exp(-lam_cens*t)
t = np.linspace(0,T)
plt.plot(t, R_t_cens(t))
plt.legend(('KM-Fitter', 'KMS-Streuung', 'Kaplan-Maier', 'Maximum-Liklihood'), loc='upper right', shadow=True)

plt.show()