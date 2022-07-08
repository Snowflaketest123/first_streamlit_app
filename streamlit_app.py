import streamlit
import pandas
import requests



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

#New Section for requests
streamlit.header('Frutyvice Fruit Advise')
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityjuice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#json output for fruityjuice respons
#streamlit.text(fruityjuice_response.json())

#normalize the json
fruityvice_normalized=pandas.json_normalize(fruityjuice_response.json())
#-> output
streamlit.dataframe(fruityjuice_response)

# display csv file with pandas
streamlit.dataframe(my_fruit_list)
