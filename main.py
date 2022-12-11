import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache
def loadData():
   data=pd.read_excel("wages.xlsx")
   return data

wages = loadData()

image = Image.open('CareerExploration.png')
st.image(image,use_column_width='always')

#Rename columns
wages = wages.rename(columns={"NAICS_TITLE":"Industry",
                              "OCC_TITLE":"Occupation",
                              "TOT_EMP":"Employment Count",
                              "PRIM_STATE":"State",
                              "O_GROUP":"View",
                              "A_MEDIAN":"Median Annual Salary ($)"})

#Masks
maskUS=wages["State"]=="US"
maskStates=wages["State"]!="US"
maskCrossIndustry=wages["Industry"]=="Cross-industry"
maskMajor=wages["View"]=="major"
maskDetailed=wages["View"]=="detailed"
maskTotal=wages["View"]=="total"
maskArea=wages["AREA_TYPE"]==2

##Scatter Plot
#Employment and Salary
st.subheader("Employment Count & Salary")

SPMajor=wages[maskUS & maskCrossIndustry & maskMajor]
SPDetailed=wages[maskUS & maskCrossIndustry & maskDetailed]

#SPStateEmployMajor=wages[maskStates & maskArea & maskMajor]
#SPStateEmployDetailed=wages[maskStates & maskDetailed & maskArea]
#st.dataframe(SPStateEmployDetailed)

##Map
wagesMap=wages[maskTotal & maskArea]

#Scatter Plots
figUSG = px.scatter(SPMajor, x="Median Annual Salary ($)", y="Employment Count", hover_name="Occupation")
figUSG.update_layout(title='General Occupations')

figUSD = px.scatter(SPDetailed, x="Median Annual Salary ($)", y="Employment Count", hover_name="Occupation")
figUSD.update_layout(title='Specific Occupations')

#Select view for scatter plot
SelectView=st.selectbox("Select view:",("General","Specific"))
if SelectView=="General":
   st.plotly_chart(figUSG)
if SelectView == "Specific":
    st.plotly_chart(figUSD)

#Employment Count Map
st.subheader("Employment Count by State")
figEmployMap = go.Figure(data=go.Choropleth(
  locations=wagesMap["State"],
   z=wagesMap["Employment Count"].astype(float),
   locationmode="USA-states",
   colorscale="Blues",
   colorbar_title="Employment Count",
   text=wagesMap['State']
))
figEmployMap.update_layout(geo_scope='usa')
st.plotly_chart(figEmployMap)

#Median Annual Salary Map
st.subheader("Median Annual Salary by State")
figSalaryMap = go.Figure(data=go.Choropleth(
  locations=wagesMap["State"],
   z=wagesMap["Median Annual Salary ($)"].astype(float),
   locationmode="USA-states",
   colorscale="Blues",
   colorbar_title="Median Annual Salary ($)",
   text=wagesMap['State']
))
figSalaryMap.update_layout(geo_scope='usa')
st.plotly_chart(figSalaryMap)

st.write("Source: [U.S. Bureau of Labor Statistics](https://www.bls.gov/oes/current/oes_nat.htm)")
st.write("For further exploration, visit [My Next Move](https://www.mynextmove.org)")
