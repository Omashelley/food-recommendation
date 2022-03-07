import random
import pandas as pd
import matplotlib.pyplot as plt

def read_file():
    df = pd.read_csv('nutrition.csv')
    df = df.iloc[: , 1:]
    df = df.reset_index()
    df = df.rename(columns={"index":"id"})
    df['id'] = df.index + 1
    return df

def find_bmi_range(value):
    result = None
    if value < 18.5:
        result = 'Underweight'
    elif 18.5 <= value <= 24.9:
        result = 'Normal weight'
    elif 25.0 <= value <= 29.9:
        result = 'Pre-obesity'
    elif 30.0 <= value <= 34.9:
        result = 'Obesity class I'
    elif 35.0 <= value <= 39.9:
        result = 'Obesity class II'
    elif value > 40:
        result = 'Obesity class III'
    return result

def food_recommender_helper(df, calories, weight_class):
    random.seed(weight_class)
    df = df.dropna()
    df = df[df.calories > (calories/100)]
    food_list = list(df['name'].values)
    selected_food = random.sample(food_list, 10)
    df = df.loc[df['name'].isin(selected_food)]
    df = df[['name', 'calories', 'fat', 'carbohydrate', 'protein']]
    return df

def set_bg_hack_url(st):
    st.markdown(
        f"""
            <style>
            .stApp {{
                background: url("https://source.unsplash.com/5PgY6Q5q5qs/1024x764");
                background-size: cover
            }}
            </style>
         """,unsafe_allow_html=True)

def format_dataframe_column(df, *args):
    for column in args:
        df[column] = df[column].map(lambda x: x.rstrip(' g')).astype(float)
    return df

def daily_calorie_burn(gender, weight, height, age):
    bmr_by_gender = {
        'male': 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age),
        'female': 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    }
    return bmr_by_gender[gender]

def formatted_dataframe(data):
    df = format_dataframe_column(data, 'protein', 'carbohydrate', 'fat', 'water', 'sugars')
    df = df.dropna()
    df = df[['name','fat', 'carbohydrate', 'protein', 'sugars']]
    df = df.head(20)
    return df

def plot_bar_chart(data, st, hist=False):
    with st.container():
        message = 'Food Recipe Distribution (Bar chart)'
        if hist:
            message = 'Food Recipe Histogram'
        description = f"<p style='font-family:Courier; color:Black; font-size: 15px;'> {message}.</p>"
        st.markdown(description, unsafe_allow_html=True)
        df = formatted_dataframe(data)
        labels = list(df['name'].values)
        protein = list(df['protein'].values)
        plt.bar(labels, protein)
        plt.xticks(rotation=45)
        if hist:
            df.hist()

def plot_stack_bar_chart(data, st):
    with st.container():
        description = '<p style="font-family:Courier; color:Black; font-size: 15px;"> Food Recipe Distribution (Stack Bar chart).</p>'
        st.markdown(description, unsafe_allow_html=True)
        df = formatted_dataframe(data)
        df = pd.DataFrame(df).set_index('name').rename_axis('Food Recipe', axis=1)
        ax = df.plot(kind='bar', stacked=True, figsize=(10, 6))
        ax.set_ylabel('Quantity (grams)')
        ax.set_xlabel('Food Recipe')
        plt.legend(title='labels', bbox_to_anchor=(1.0, 1), loc='upper left')
        plt.xticks(rotation=45)

def scatter_plot(data, st):
    with st.container():
        description = '<p style="font-family:Courier; color:Black; font-size: 15px;"> Food Recipe Scatter Plots.</p>'
        st.markdown(description, unsafe_allow_html=True)
        df = formatted_dataframe(data)
        fig, ax = plt.subplots(4, figsize=(10, 6))
        ax[0].scatter(x = df['fat'], y = df['carbohydrate'])
        ax[0].set_xlabel('fat')
        ax[0].set_ylabel('carbohydrate')

        ax[1].scatter(x=df['fat'], y=df['protein'])
        ax[1].set_xlabel("fat")
        ax[1].set_ylabel('protein')

        ax[2].scatter(x=df['fat'], y=df['sugars'])
        ax[2].set_xlabel("fat")
        ax[2].set_ylabel('sugars')

        ax[3].scatter(x=df['fat'], y=df['protein'])
        ax[3].set_xlabel("fat")
        ax[3].set_ylabel('protein')
