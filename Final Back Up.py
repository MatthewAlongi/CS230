import streamlit as st
import pydeck as pdk
import pandas as pd
import random as rd
import matplotlib.pyplot as plt
import csv

df_pubs = pd.read_csv("open_pubs_8000_sample.csv")
df_pubs.rename(columns={"latitude":"Latitude", "longitude": "Longitude"}, inplace= True)

new_title = '<p style="font-family:verdana; color:aqua; font-weight: bold;font-size: 34px;">Matthew Alongi CS230 Final Project ''</p>'
st.markdown(new_title, unsafe_allow_html=True)


authority_list = []
new_authority_list = []
for c in df_pubs.local_authority:
    if c.strip() not in authority_list:
        authority_list.append(c.strip())
        new_authority_list.append(c.strip())

authority_list.sort()
authority_list.insert(0,"")


sub_df_list = []

for c in new_authority_list:
    sub_df = df_pubs[df_pubs["local_authority"].str.strip() == c]
    sub_df_list.append(sub_df)

for c in authority_list:
    sub_df = df_pubs[df_pubs["local_authority"].str.strip() == c]
    sub_df_list.append(sub_df)

print(new_authority_list)

count = 0
with open('bar_count.csv', 'w', newline='') as bar_count:
    writer = csv.writer(bar_count)
    writer.writerow(['Local_Authority_UK', 'Bar_Count'])
    for i in new_authority_list:
        count = df_pubs["local_authority"].value_counts()[i]
        writer.writerow([i, count])



layer_list = []
for sub_df in sub_df_list:
    layer = pdk.Layer(type = 'ScatterplotLayer',
                  data=sub_df,
                  get_position='[Longitude, Latitude]',
                  get_radius=800,
                  get_color=[rd.randint(0,255),rd.randint(0,255),rd.randint(0,255)],
                  pickable=True
                  )
    layer_list.append(layer)

tool_tip = {"html": "Pub Name: <b>{name}</b> <br/> Local Authority: <b>{local_authority}</b>",
            "style": { "backgroundColor": "Black",
                        "color": "white"}
          }

view_state = pdk.ViewState(
                latitude=df_pubs["Latitude"].mean(),
                longitude=df_pubs["Longitude"].mean(),
                zoom=11,
                pitch=0)

st.sidebar.text("----------------------------------------")
st.sidebar.text("Map of England Pubs")
selected_authority = st.sidebar.selectbox("Please select an local authority", authority_list)
st.sidebar.text("----------------------------------------")
if bool(selected_authority) == False:
    for i in range(len(new_authority_list)):
        map = pdk.Deck(
            map_style='mapbox://styles/mapbox/outdoors-v11',
            initial_view_state=view_state,
            layers = layer_list,
            tooltip = tool_tip
            )
else:
    for i in range(len(new_authority_list)):
        if selected_authority == new_authority_list[i]:
            map = pdk.Deck(
            map_style='mapbox://styles/mapbox/outdoors-v11',
            initial_view_state=view_state,
            layers=[layer_list[i]],
            tooltip= tool_tip
            )

st.pydeck_chart(map)



st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("----------------------------------------")
st.sidebar.text("Number of Pubs Charts")
pie_or_bar = st.sidebar.radio("Chart Type", ("None","Pie Chart", "Bar Chart"))
selected_authority_chart = st.sidebar.multiselect("Please select an local authority", authority_list)
st.sidebar.text("----------------------------------------")
chart_list_name = []
chart_list_value = []
color_list = []
color_sub_list = ()

def bar_chart():
    for i in selected_authority_chart:
        color_sub_list = []
        count = df_pubs["local_authority"].value_counts()[i]
        chart_list_name.append(i)
        chart_list_value.append(count)
        color_sub_list = (rd.random(),rd.random(),rd.random(),1)
        color_list.append(color_sub_list)
    fig, ax = plt.subplots()
    plt.bar(chart_list_name,chart_list_value, edgecolor = "black" , color = color_list , width = .75)
    for i in range(len(chart_list_name)):
        plt.text(i, chart_list_value[i],chart_list_value[i], ha="center", va="bottom")
    plt.xlabel("Authority")
    plt.ylabel("Number of Pubs")
    plt.title("Number of Pubs in Local Authority")
    st.pyplot(fig)

def pie_chart():
    for i in selected_authority_chart:
        color_sub_list = []
        count = df_pubs["local_authority"].value_counts()[i]
        chart_list_name.append(i)
        chart_list_value.append(count)
        color_sub_list = (rd.random(),rd.random(),rd.random(),1)
        color_list.append(color_sub_list)
    fig, ax = plt.subplots()
    plt.pie(chart_list_value, colors = color_list , labels = chart_list_name, wedgeprops = { 'linewidth' : 1, 'edgecolor' : 'white' }, autopct = '%.1f')
    plt.xlabel("Authority")
    plt.ylabel("Number of Pubs")
    plt.title("Number of Pubs in Local Authority")
    st.pyplot(fig)

if pie_or_bar == "Bar Chart":
    bar_chart()
if pie_or_bar == "Pie Chart":
    pie_chart()

pd.set_option('display.max_rows', None)
df_pub_count = pd.read_csv("bar_count.csv")


st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("----------------------------------------")
st.sidebar.text("Authorities with Most or Least Bars")
table_or_bar = st.sidebar.radio("", ("None","Table", "Bar Chart"))
ascending_or_decending = st.sidebar.radio("", ("Most", "Least"))
number_authorities = st.sidebar.number_input("How Many Authorities? ", 0,25)
st.sidebar.text("----------------------------------------")

if ascending_or_decending == "Most":
    df_bar_sort = df_pub_count.sort_values('Bar_Count',ascending=False)
else:
    df_bar_sort = df_pub_count.sort_values('Bar_Count',ascending=True)



def bar_count_table():
    df_bar_sort.rename(columns={"Local_Authority_UK":"Local Authority", "Bar_Count": "Number of Bars"}, inplace= True)
    if ascending_or_decending == "Most":
        display_table = df_bar_sort.head(n =number_authorities)
        display_table_1 = display_table.reset_index()
        display_table_1.index = display_table_1.index +1
        st.text("Authorities with the Most Pubs")
        st.write(display_table_1[['Local Authority', 'Number of Bars']])
    else:
        display_table = df_bar_sort.head(n =number_authorities)
        display_table_1 = display_table.reset_index()
        display_table_1.index = display_table_1.index +1
        st.text("Authorities with the Least Pubs")
        st.write(display_table_1[['Local Authority', 'Number of Bars']])


if table_or_bar == "Table":
    bar_count_table()
#if table_or_bar == "Bar Chart":
   #bar_count_chart()

st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("----------------------------------------")
selected_authority_bar_list = st.sidebar.selectbox("Find Pubs in Your Town!", authority_list)


for i in range(len(new_authority_list)):
    if selected_authority_bar_list == new_authority_list[i]:
        df_sub_sub = sub_df_list[i]
        df_sub_sub1 = df_sub_sub.reset_index()
        df_sub_sub1.index = df_sub_sub1.index + 1
        pd.set_option('max_colwidth', None)
        st.write("Pubs in", selected_authority_bar_list)
        st.write(df_sub_sub1[['name','address']])

st.sidebar.text("----------------------------------------")




st.sidebar.text("----------------------------------------")
st.sidebar.text("Most Common Pub Names")
number_names = st.sidebar.number_input("Choose how many names? ", 0,25)

names_list = []
repeated_names = {}
for c in df_pubs.name:
    names_list.append(c.strip())
for i in names_list:
    if names_list.count(i) >1:
        repeated_names[i] = names_list.count(i)

df_names = pd.DataFrame( list(repeated_names.items()),columns = ["Name",'Number of Pubs'])
df_sorted_names = df_names.sort_values('Number of Pubs',ascending=False)
print(df_sorted_names)

if number_names >0:
    st.text("Most Common Pub Names")
    display_name_table = df_sorted_names.head(n =number_names)
    display_name_table_1 = display_name_table.reset_index()
    display_name_table_1.index = display_name_table_1.index +1
    st.write(display_name_table_1[['Name', 'Number of Pubs']])





"""
def bar_count_chart():
    count_name = []
    count_value= []
    count_list = []
    if ascending_or_decending == "Most":
        display_table = df_bar_sort.head(n =number_authorities)
        display_table_1 = display_table.reset_index()
        display_table_1.index = display_table_1.index +1
        for i in display_table_1:
            count_list.append(display_table_1[i]['Local Authority', 'Number of Bars'])
        st.write(count_list)
            #count_name.append(display_table_1.Local_Authority_UK[i])
            #count_value.append(display_table_1.Bar_Count[i])
        #st.write(display_table_1[['Local Authority', 'Number of Bars']])
    else:
        display_table = df_bar_sort.head(n =number_authorities)
        display_table_1 = display_table.reset_index()
        display_table_1.index = display_table_1.index +1
        st.write(display_table_1[['Local Authority', 'Number of Bars']])


"""
