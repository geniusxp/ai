import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

recommendations_df = pd.read_excel('./model/geniusxp-database-next-projects.xlsx')

vectorizer = CountVectorizer(tokenizer=lambda x: x.split(';'))
segment_matrix = vectorizer.fit_transform(recommendations_df['segmentos'])

def recommend_projects(interests):
    user_interests_vec = vectorizer.transform([interests])
    similarity = cosine_similarity(user_interests_vec, segment_matrix)
    recommended_projects_indexes = similarity.argsort()[0][::-1]

    return recommendations_df.iloc[recommended_projects_indexes]
