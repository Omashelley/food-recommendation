import streamlit as st
import matplotlib.pyplot as plt

from food_recommender import FoodRecommender
from utils import (plot_stack_bar_chart, read_file, find_bmi_range, 
                   set_bg_hack_url, daily_calorie_burn,
                   plot_bar_chart,scatter_plot)


check_bmi = None
data = read_file()

sidebar_menu = st.sidebar.selectbox(
'What Operation would you like to perform?',
[' ', 'Food Recommendation', 'Data Visualisation'])
if sidebar_menu == ' ':
    welcome_text = '<h1 style="font-family:sans-serif; color:White;">Food Recommendation System for Diabetic Patients </h1>'
    app_description = '<p style="font-family:Courier; color:White; font-size: 20px;">This data science project recommends food for diabetic patients. This product is intended for diabetic patients and it is assumed that the handler or the user is aware.</p>'
    st.markdown(welcome_text, unsafe_allow_html=True)
    st.markdown(app_description, unsafe_allow_html=True)
    set_bg_hack_url(st)

if sidebar_menu == 'Food Recommendation':
    st.markdown(f'<h3 style="font-family:sans-serif; color:Black;">Welcome </h3>', unsafe_allow_html=True)
    st.markdown(f'<h5 style="font-family:Courier; color:Black;">Please, fill the form to get information about your diet recommendation</h3>', unsafe_allow_html=True)
    food_recommender = FoodRecommender(st, data)
    with st.form(key='my_form'):
        age = st.number_input('Age')
        height = st.number_input('Height in cm')
        weight = st.number_input('Weight in kg')
        blood_sugar = st.number_input('Blood Sugar level')
        gender = st.selectbox('Gender', ['male', 'female'], key='gender')
        submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        bmi = weight/(height/100)**2
        check_bmi = find_bmi_range(bmi)
        bmr = daily_calorie_burn(gender,weight,height,age)
        with st.spinner('Loading...'):
            recommended = food_recommender.KNN_recommender_algo(data, 1000, bmr)
        st.markdown(f'<h6 style="font-family:Courier; color:Black;">BMI Status: {check_bmi}</h6>', unsafe_allow_html=True)
        st.markdown(f'<h6 style="font-family:Courier; color:Black;">Food and Nutrient Recommendation</h6>', unsafe_allow_html=True)
        st.table(recommended)
elif sidebar_menu == 'Data Visualisation':
    st.header('This section displays visualized data from the Food Recipe dataset used for this study')
    with st.container():
        description = '<p style="font-family:Courier; color:Black; font-size: 15px;"> A snippet of the structure of the dataset.</p>'
        st.markdown(description, unsafe_allow_html=True)
        st.write(data.dropna().head(5))
        st.markdown('##')
    
    plots = st.radio(
        "Choose Plots",
        ('Data Distribution (Bar Chart)', 'Data Distribution (Stacked Bar chart)', 'Histogram', 'Scatter Plot'))
    if plots == 'Data Distribution (Bar Chart)':
        plot_bar_chart(data, st)
    if plots == 'Data Distribution (Stacked Bar chart)':
        plot_stack_bar_chart(data, st)
    if plots == 'Histogram':
        plot_bar_chart(data, st, hist=True)
    if plots == 'Scatter Plot':
        scatter_plot(data, st)
    st.pyplot(plt)
