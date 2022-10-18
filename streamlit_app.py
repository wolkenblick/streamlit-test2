import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import math
import plotly.express as px


def read_log(logger):
	global data

	data = pd.read_csv(datapath+logger+".txt".format(), sep = '\s+', header = 0, dtype = {'YYMMDDHHMMSS': str})
      	#data = pd.read_csv(datapath+"2021_"+logger+".txt".format(), sep = '\s+', header = 0, dtype = {'YYMMDDHHMMSS': str})
	#Umwandeln des Datums in datetime-Objekt
	data['date']=pd.to_datetime(data['YYMMDDHHMMSS'], format = '%y%m%d%H%M%S')
	#daten_r.set_index('date', inplace = True)
	data.drop(['YYMMDDHHMMSS'],axis = 1, inplace = True)

	return data


#=================================================================
#   T A U P U N K T F O R M E L
#=================================================================
def dewpoint(t, h):
        a1 = 7.45
        b1 = 235
        dp = t
        fw = h
        x1=(a1*dp)/(b1+dp)
        e1=6.1*math.exp(x1*2.3025851)
        e2=e1*fw/100
        x2=e2/6.1
        if x2 <= 0:
                print(x2)
                x2=0.00000001
        x3=0.434292289*math.log(x2)
        dew=(235*x3)/(7.45-x3)*100
        dew=math.floor(dew)/100
        dew =  "%02.2f" % (dew)
        dew = '{: >5}'.format(dew)
        return dew
#=================================================================



# based on tutorial here: https://www.youtube.com/watch?v=1TPyF_3nHzs
st.set_page_config(layout="wide" )
bildurl = "https://www.ipa.uni-mainz.de/files/2022/10/IMG_1994-1024x501.jpeg"
st.image(bildurl, use_column_width="always")

st.markdown("# Wetterdaten des Instituts für Physik der Atmosphäre")


datapath=""
read_log("logger4")
log4 = data

zeit_4 = log4['date']
t5cm = log4['t5cm']
t20cm = log4['t20cm']
t2m = log4['t2m']
rh = log4['relHum']
p = log4['Press']

# Get Dewpoint

df = pd.DataFrame([t2m,rh]).T

n = len(df)
tau = [None]*n
i = 0
while i < n-1:
	tau[i]=dewpoint(df.iat[i,0],df.iat[i,1])
	tau[i]=float(tau[i])
	i=i+1

log4

# lets get interactive
cols = log4.columns.values.tolist()
cols = [c for c, t in zip(cols, log4.dtypes.values.tolist()) if "float" in str(t).lower() or "int" in str(t).lower()]
our_chosen_col = st.selectbox(label="Select a Column", options=cols)


fig = px.scatter(log4, x=zeit_4, y=our_chosen_col)
st.plotly_chart(fig, use_container_width=True)