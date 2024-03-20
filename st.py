# Import python packages
import streamlit as st
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """)

from snowflake.snowpark.functions import col

Name_on_order = st.text_input('Name on smoothie:')
st.write('Name on your smoothie will be:',Name_on_order )
cnx = st.connection("snowflake")
session = cnx.session()
st.my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')),col('SEARCH_ON')
st.stop()
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
    )
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen+'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_chosen)
        fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
            values ('""" + ingredients_string + """','""" + Name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered,{Name_on_order}!', icon="✅")


