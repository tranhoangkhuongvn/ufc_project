import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import colors as mcolors

st.title('UFC Summary')
st.write('Here is our data:')



@st.cache
def load_clean_data():
	data = pd.read_csv('./UFC_clean.csv')
	return data


df_clean = load_clean_data()
st.write(df_clean.head())

st.write("""
#### Fight weight class: 
- Weight class : 'Lightweight','Welterweight','Middleweight','Featherweight','Light Heavyweight' 
- Data from 2006 - T6/2019 
- Championship Fights At 3 Rounds: '3 Rnd (5-5-5)' 
""")

weight_select = ['Lightweight','Welterweight','Middleweight','Featherweight','Light Heavyweight']
df = df_clean[df_clean['fight_year']>= 2006]
df = df_clean[df_clean['weight_class'].isin(weight_select)]
df = df[df['Format'].isin(['3 Rnd (5-5-5)'])]

df.describe()


R_fighter = df[['R_fighter','fight_year','Winner','R_SIG_STR_pct','R_TD_pct','R_SIG_STR._landed','R_TOTAL_STR._landed', 'R_TOTAL_STR._att','R_DISTANCE_landed','R_CLINCH_landed','R_GROUND_landed','R_GROUND_att',
               'R_HEAD_landed','R_BODY_landed','R_LEG_landed','total_time_fought(minutes)','last_round']]
B_fighter = df[['B_fighter','fight_year','Winner','B_SIG_STR_pct','B_TD_pct','B_SIG_STR._landed','B_TOTAL_STR._landed','B_TOTAL_STR._att','B_DISTANCE_landed','B_CLINCH_landed','B_GROUND_landed', 'B_GROUND_att',
               'B_HEAD_landed','B_BODY_landed','B_LEG_landed','total_time_fought(minutes)','last_round']]

R_fighter.columns = ['fighter','fight_year','Winner','SIG_STR_pct','TD_pct','SIG_STR._landed','TOTAL_STR._landed','TOTAL_STR._att','DISTANCE_landed','CLINCH_landed','GROUND_landed','GROUND_att',
               'HEAD_landed','BODY_landed','LEG_landed','total_time_min','last_round']

B_fighter.columns = ['fighter','fight_year','Winner','SIG_STR_pct','TD_pct','SIG_STR._landed','TOTAL_STR._landed','TOTAL_STR._att','DISTANCE_landed','CLINCH_landed','GROUND_landed','GROUND_att',
               'HEAD_landed','BODY_landed','LEG_landed','total_time_min','last_round']


RB_fighter = R_fighter.append(B_fighter)  
RB_fighter['Winner_T'] = RB_fighter['Winner'] == RB_fighter['fighter']
RB_fighter['Winner_label'] = np.where(RB_fighter['Winner'] == RB_fighter['fighter'],'Winner','Loser')  
RB_fighter['TOTAL_STR_pct']= np.where(RB_fighter['TOTAL_STR._att'] == 0, 0, RB_fighter['TOTAL_STR._landed']/RB_fighter['TOTAL_STR._att'])
RB_fighter.describe()



st.write("""
#### Best timing to get advantages

""")
fig = plt.figure(constrained_layout=False, figsize=(20, 5))
fig.suptitle('BOUT DURATION AND PERFROMANCE INDICATORS')
gs = fig.add_gridspec(nrows=1, ncols=3,top = 0.8, wspace=0.3, hspace=0.3)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])

sns.scatterplot(data=RB_fighter, y="TOTAL_STR_pct", x="total_time_min", hue="Winner_label", hue_order = ['Loser','Winner'], ax = ax1 )
ax1.set(title = 'Total strike accuracy' , xlabel = 'Time_bout_min' , ylabel = 'Total strike accuracy %' , xticks = [0,5,10,15])
ax1.axhline(y = 0.6)

sns.scatterplot(data=RB_fighter, y="SIG_STR_pct", x="total_time_min", hue="Winner_label", hue_order = ['Loser','Winner'],ax = ax2)
ax2.set(title = 'Significant strike accuracy' , xlabel = 'Time_bout_min' , ylabel = 'Significant strike accuracy %', xticks = [0,5,10,15])
ax2.axhline(y = 0.5)

sns.scatterplot(data=RB_fighter, y="TD_pct", x="total_time_min", hue="Winner_label", ax = ax3, hue_order = ['Loser','Winner'])
ax3.set(title = 'Takedown accuracy', xlabel = 'Time_bout_min' , ylabel = 'Takedown accuracy %' , xticks = [0,5,10,15])
#plt.show()
st.pyplot(fig)
