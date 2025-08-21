# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!"""
)


name_of_order = st.text_input('Name of your smoothie')
st.write('Smoothie: ' + name_of_order)

cnx = st.connection("snowflake")
session = cnx.session()


my_dataframe = session.table("smoothies.public.fruit_options").select('FRUIT_NAME', 'SEARCH_ON')
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_datafarme.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
    'Choos up to 5', my_dataframe, max_selections=5
)
if ingredients_list:

    ingredients_string = ''

    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '
        st.subheader(fruit_choosen + " Nutrition Information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_choosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
  
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""  + name_of_order+ """')"""

    st.write(my_insert_stmt)

    
    time_to_insert = st.button('Submit order')

    if time_to_insert:
    
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")



            
