import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError



#load Data from txt into Variable my_fruit_list
my_fruit_list =pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#set selection to column Fruit
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#create a pick list and add some preselected fruits
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

#put selcted fruits into a variable
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]

#display only selected fruits
streamlit.dataframe(fruits_to_show)




#create the repeatable code block (called a function=def)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    #normalize the json
    fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#New Section for requests
streamlit.header('Frutyvice Fruit Advise')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
  else:
       back_from_function = get_fruityvice_data(fruit_choice)
       streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()
        
streamlit.write('The user entered ', fruit_choice)


streamlit.header("The fruit load list contains:")
#Snoflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("Select * from fruit_load_list")
        return my_cur.fetchall()
    
#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

# display csv file with pandas
#streamlit.dataframe(my_fruit_list)

#don´t run anything past here while we troubleshoot
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("Select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.text("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#add fruit to list
add_my_fruit = streamlit.text_input('What fruit do you like to add?','Jackfruit')
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
streamlit.write('Thanks for adding ',add_my_fruit)
