
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from pandas import DataFrame

df=pd.read_csv('Crimes_-_2001_to_present copy.csv', sep=',',low_memory=False)


a=df.groupby(['Primary Type','District']).count()['ID']
a_1=df.groupby(['Primary Type']).count()['ID']

Crime_rate= a_1/np.sum(a_1)

crimes_set=set(df['Primary Type'])
district=set(df['District'])
district={x for x in district if x==x}
mydict = {}
for cr in crimes_set:
	for j in district:
		if j in a[cr].keys():
			mydict[(cr,j)]=(a[cr,j]/np.sum(a[j]))/Crime_rate[cr]

crime_ind={}
for j in district:
	crimes_dist={}
	for cr in crimes_set:
		if (cr,j) in mydict:
			crimes_dist[cr]=mydict[(cr,j)]
	crime_ind[j]=sorted(crimes_dist.items(), key=lambda x: x[1])


b=df.groupby(['Location Description','Primary Type']).count()['ID']
c=df.groupby(['Year','Primary Type']).count()['ID']
ten_top=b.sort_values(ascending=False).head(10)

indx=(df['Location Description'].str.contains('SCHOOL', regex=False).replace(np.NaN,False))
e=df.loc[indx].groupby(['Primary Type']).count()['ID']
e.sort_values(ascending=False).head(10)

Crime_Type=set(df['Primary Type'])
Crime_Type.remove('NON - CRIMINAL')
Crime_Type.remove('NON-CRIMINAL (SUBJECT SPECIFIED)')
Crime_Type=list(Crime_Type)
Years = set(df['Year'])

crime_year=np.zeros((len(Years),len(Crime_Type)))

for i,crime in enumerate(Crime_Type):
	for j in range(2015,2020):
		crime_year[j-2015,i]=(c[j][crime])
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

x=[2015,2016,2017,2018,2019]
for i in range(31):
	plt.plot(x,crime_year[:,i],label=Crime_Type[i])

plt.legend()
plt.show()

x_axis=['2015','2016','2017','2018','2019']
ind = [x for x, _ in enumerate(x_axis)]
for i in range(31):
	plt.bar(ind, crime_year[0:4,i], width=0.8, label=Crime_Type[i])
plt.xticks(ind, x_axis)
plt.ylabel("#Crimes")
plt.xlabel("Year")
plt.legend(loc="upper right")
plt.title("Crime Type Per Year")

plt.show()






###########################
#Ten Top Criminal Type  Per Year
# # of Each Type Per Year
###########################
x_axis=['2015','2016','2017','2018','2019']
ind = [x for x, _ in enumerate(x_axis)]
ten_top_count=np.zeros((5,10))
cime_group=df.groupby(['Primary Type']).count()['ID']
temp=cime_group.sort_values(ascending=False).head(10)
ten_top_crimes=list(temp.keys())
for i in range(2015,2020):
	indx=(df['Year']==i)
	crime_per_year=df.loc[indx].groupby(['Primary Type']).count()['ID']
	for j,c in enumerate(ten_top_crimes):
		ten_top_count[i-2015,j]=crime_per_year[c] /len(np.where(indx)[0])
	
for i in range(10):
	plt.bar(ind, ten_top_count[:,i] , width=0.8, label=ten_top_crimes[i])
plt.xticks(ind, x_axis)
plt.ylabel("# of Crimes")
plt.xlabel("Year")
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15),ncol=5, fancybox=True, shadow=True)
plt.title("Ten Top Crime Per Year")

plt.show()

data1=[]
x_axis=['2015','2016','2017','2018','2019']
for i in range(len(x_axis)):
	data1.append([x_axis[i]]+list(ten_top_count[i,:]))

ten_top_crimes=['Year']+ten_top_crimes
colors = sns.color_palette("cubehelix", n_colors=len(ten_top_crimes))
cmap1 = LinearSegmentedColormap.from_list("my_colormap", colors)
df2 = DataFrame(data=data1)
df2.columns = ten_top_crimes
df2 = df2.set_index(ten_top_crimes[0])
df2.plot(kind='bar', stacked=True, colormap=cmap1,rot=0)

plt.ylabel("Crimes Ratio")

plt.xlabel("Year")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),ncol=5, fancybox=True, shadow=True)

plt.show()

#######################################################
# The most Crime in Public Places eg SCHOOL AIRPORT TAXI BUS HOSPITAL 'STATION'
# GOVERNMENT BUILDING, LIBRARY, NURSING HOME
################################################

interest_location=['SCHOOL', 'AIRPORT', 'TAXI', 'GOVERNMENT BUILDING', 'LIBRARY']
crimes=[]
for loc in interest_location:
	indx=(df['Location Description'].str.contains(loc, regex=False).replace(np.NaN,False))
	temp=df.loc[indx].groupby(['Primary Type']).count()['ID']
	top_ten=temp.sort_values(ascending=False).head(5)/(len(np.where(indx)[0]))
	crimes=crimes+list(top_ten.keys())
	print(loc,top_ten)

crimes=list(set(crimes))

mat_crimes_count=np.zeros((len(interest_location),len(crimes)))

for i,loc in enumerate(interest_location):
	for j,cr in enumerate(crimes):
		indx=(df['Location Description'].str.contains(loc, regex=False).replace(np.NaN,False) )
		temp=df.loc[indx].groupby(['Primary Type']).count()['ID']
		mat_crimes_count[i,j]=temp[cr]/(len(np.where(indx)[0]))
		print(cr,loc,mat_crimes_count[i,j])

data1=[]
for i in range(len(interest_location)):
	data1.append([interest_location[i]]+list(mat_crimes_count[i,:]))


matplotlib.style.use('ggplot')
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 8}

matplotlib.rc('font', **font)
from pandas import DataFrame

crimes2=['Location']+crimes
colors = sns.color_palette("cubehelix", n_colors=len(crimes2))
cmap1 = LinearSegmentedColormap.from_list("my_colormap", colors)
df2 = DataFrame(data=data1)
df2.columns = crimes2
df2 = df2.set_index(crimes2[0])
df2.plot(kind='bar', stacked=True, colormap=cmap1,rot=0)

plt.ylabel("Crimes Ratio")

plt.xlabel("Location")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),ncol=5, fancybox=True, shadow=True)

plt.show()


#######################################################
# The most Crime in Each District
################################################
district=set(df['District'])
district={x for x in district if x==x}

temp=df.groupby(['Primary Type','District']).count()['ID']
theft=temp['THEFT'].sort_values(ascending=False).head(5)
sex_offense=temp['SEX OFFENSE'].sort_values(ascending=False).head(3)
kidnapping=temp['KIDNAPPING'].sort_values(ascending=False).head(3)
drug=temp['NARCOTICS'].sort_values(ascending=False).head(3)

###############################
# Time of Each Crime
#############################
df['Date2']=pd.to_datetime(df['Date'])
grp = df.groupby(by=['Primary Type',df.Date2.map(lambda x : (x.hour))]).count()['ID']
a=df.groupby(['Primary Type']).count()['ID']
five_top_crimes=a.sort_values(ascending=False).head(5)
five_top_crimes=list(five_top_crimes.keys())

mat_crime_hour=np.zeros((5,24))
for h in range(24):
	for i,cr in enumerate(five_top_crimes):
		mat_crime_hour[i,h]=grp[cr][h]


ind=np.arange(0,24)
hours=[str(i) for i in ind]
colors = sns.color_palette("cubehelix", n_colors=len(five_top_crimes))
cmap1 = LinearSegmentedColormap.from_list("my_colormap", colors)
plt.plot(colormap=cmap1,rot=0)

for i in range(5):
	plt.plot(ind,mat_crime_hour[i,:],label=five_top_crimes[i])


plt.xlabel("hour")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),ncol=5, fancybox=True, shadow=True)
plt.xticks(np.arange(0, 24, step=1))
plt.show()

#############


##############

import geopandas as gpd

indx=pd.notna(df['District'])
df_map=df.loc[indx].groupby(['District']).count()['ID']

data1=[]
for i in district:
	data1=data1+[[str(np.int64(i)), df_map[i]]]

map_df=pd.DataFrame(np.array(data1),columns=['Distict', 'CrimeRatio'])
map_df.Distict.apply(str) 
map_df["CrimeRatio"] = pd.to_numeric(map_df["CrimeRatio"])
map_df['Distict']= map_df['Distict'].astype(str)


import folium
import json


with open('Boundaries - Police Districts (current).geojson','r') as jasonfile:
	data_zip=json.load(jasonfile)
tmp=data_zip
dist_police=[str(np.int32(i)) for i in district]
geozips=[]
l=[]
flag=True
for i in range(len(tmp['features'])):
	if ((tmp['features'][i]['properties']['dist_num'] in dist_police) and (flag or not (tmp['features'][i]['properties']['dist_num']=='31'))):
		geozips.append(tmp['features'][i])
		if tmp['features'][i]['properties']['dist_num']=='31':
			flag=False
		l.append(tmp['features'][i]['properties']['dist_num'])
new_json=dict.fromkeys(['type','features'])
new_json['type']='FeatureCollection'
new_json['features']=geozips

open('chicago_zip_updated.json',"w").write(json.dumps(new_json,sort_keys=True,indent=4, separators=(',',':')))

chicago=r'chicago_zip_updated.json'
m=folium.Map(location=[41.836559146, -87.620223934],zoom_start=11)
m.choropleth(geo_data=chicago,data=map_df,key_on='feature.properties.dist_num',fill_color='BuGn',columns=['Distict','CrimeRatio'])
folium.LayerControl().add_to(m)
m.save(outfile='test.html')


##################
###
####
##################

indx=pd.notna(df['District'])
df_map=df.loc[indx].groupby(['Primary Type','District']).count()['ID']

data1=[]
for i in district:
	data1=data1+[[str(np.int64(i)), df_map['NARCOTICS'][i]]]

map_df=pd.DataFrame(np.array(data1),columns=['Distict', 'CrimeRatio'])
map_df.Distict.apply(str) 
map_df["CrimeRatio"] = pd.to_numeric(map_df["CrimeRatio"])
map_df['Distict']= map_df['Distict'].astype(str)




chicago=r'chicago_zip_updated.json'
m=folium.Map(location=[41.836559146, -87.620223934],zoom_start=11)
m.choropleth(geo_data=chicago,data=map_df,key_on='feature.properties.dist_num',fill_color='BuGn',columns=['Distict','CrimeRatio'])
folium.LayerControl().add_to(m)
m.save(outfile='test.html')


# {'CRIMINAL TRESPASS', 'NON - CRIMINAL', 'WEAPONS VIOLATION', 
# 'KIDNAPPING', 'HOMICIDE', 'CRIM SEXUAL ASSAULT', 'OTHER OFFENSE',
#  'ASSAULT', 'CONCEALED CARRY LICENSE VIOLATION', 'DECEPTIVE PRACTICE',
#   'OFFENSE INVOLVING CHILDREN', 'THEFT', 'GAMBLING',
#    'INTERFERENCE WITH PUBLIC OFFICER', 'INTIMIDATION', 'BATTERY',
#     'CRIMINAL DAMAGE', 'HUMAN TRAFFICKING', 'PUBLIC PEACE VIOLATION',
#      'OBSCENITY', 'ROBBERY', 'PUBLIC INDECENCY', 'NON-CRIMINAL', 'OTHER NARCOTIC VIOLATION',
#       'LIQUOR LAW VIOLATION', 'BURGLARY', 'NARCOTICS', 'PROSTITUTION', 'SEX OFFENSE',
#        'MOTOR VEHICLE THEFT', 'STALKING', 'NON-CRIMINAL (SUBJECT SPECIFIED)', 'ARSON'}

