import random
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


class FoodRecommender:

    def __init__(self, st, df):
        self.st = st
        self.df = df
        self.store = []

    def KNN_recommender_algo(self, nutrition_df, number_of_recommendations, calorie):
        nutrition_df = nutrition_df.drop_duplicates(['id', 'name'])
        nutrition_df_pivot = nutrition_df.pivot(index='id', columns='name', values='calories').fillna(0)
        nutrition_df_matrix = csr_matrix(nutrition_df_pivot.values)
        model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        model_knn.fit(nutrition_df_matrix)

        nutrition_df_pivot = nutrition_df_pivot.sample(n=number_of_recommendations+1)

        distances, indices = model_knn.kneighbors(
            nutrition_df_pivot.iloc[number_of_recommendations, :].values.reshape(1, -1), n_neighbors=10)
        
        for i in range(1, len(distances.flatten())):
            self.store.append(nutrition_df_pivot.columns[indices.flatten()[i]])
        

        df = self.df.loc[self.df['name'].isin(self.store)]
        df = df[df.calories > (calorie/100)]
        df = df[['name', 'calories', 'fat', 'carbohydrate', 'protein']]
        return df
