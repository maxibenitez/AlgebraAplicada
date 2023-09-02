import numpy as np
import unidecode as ud
import re

# Define el vector de sentimientos
def emotion_vector(vector_s, keywords, vector_w):
    for i in range(len(keywords)):
        word = keywords[i]
        if word in keywords_positive:
            vector_s[0] += vector_w[i]
        elif word in keywords_negative:
            vector_s[2] += vector_w[i]
        elif word in keywords_neutral:
            vector_s[1] += vector_w[i]

# Dibide cada entrada del vector entre el largo del mismo (1/n * vector)
def avg_vector(vector):
    return np.array([round(i / len(vector), 2) for i in vector])

# Obtiene el promedio general de un vector de vectores
def vector_averages(result_mean_quality):
    vector = np.sum(np.array(result_mean_quality), axis=0)
    return avg_vector(vector)

# Limpia el tweet, sacando tildes, signos y mayúsculas
def clean_tweet(tweet):
    cleaned_tweet = ud.unidecode(tweet.lower())
    parsed_tweet = re.findall(r'\b\w+\b', cleaned_tweet)
    return parsed_tweet

# Calcula el score sentimental de cada tweet
def score(vector_s):
    vector_1 = np.array([1, 0, -1])
    vector_2 = np.array(vector_s)

    score = np.dot(vector_1, vector_2)
    return score

# Inicializa el vector que contiene la informacion de las palabras que tiene l tweet (vector w)
def key_words_mapper(word, keywords, vector):
    for i in range(len(keywords)):
        if word == keywords[i]:
            vector[i] += 1
            return

tweets = [
    "No puedo creer la triste noticia de su fallecimiento. Una pérdida inmensa para todos nosotros.",
    "¡Excelente trabajo en la presentación! Tu dedicación y esfuerzo son inspiradores y excelente!",
    "¡Increíble concierto esta noche! La energía y la música me hicieron olvidar todos mis problemas...",
    "Mi día fue un desastre total. Nada salió como lo planeé.",
]

keywords_positive = ["excelente", "inspiradores", "increible", "sublime"]
keywords_negative = ["triste", "fallecimiento", "perdida", "problemas", "desastre"]
keywords_neutral = ["noticia", "creer", "presentacion", "noche", "musica", "total"]

keywords = keywords_positive + keywords_neutral + keywords_negative

# Inicialización para hacer un seguimiento del tweet más positivo y negativo
tweet_more_positive = None
tweet_more_negative = None
max_score = float('-inf')
min_score = float('inf')
result_mean_quality = []

for tweet in tweets:
    vector_w = np.array([0 for i in range(len(keywords))])
    vector_s = np.array([0, 0, 0])
    for word in clean_tweet(tweet):
        key_words_mapper(word, keywords, vector_w)
    emotion_vector(vector_s, keywords, vector_w)
    avereged_vector = avg_vector(vector_w)
    avereged_feelings_vector = avg_vector(vector_s)
    result_mean_quality.append(vector_w)
    tweet_score = score(vector_s)

    if tweet_score > max_score:
        max_score = tweet_score
        tweet_more_positive = tweet
    if tweet_score < min_score:
        min_score = tweet_score
        tweet_more_negative = tweet

    print("Tweet:", tweet)
    print("Vector s:", vector_s)
    print("Promedio del sentimiento:", avereged_feelings_vector)
    print("La calidad del tweet:", avereged_vector)
    print("El score es:", tweet_score)
    print("---------------------------------------------\n")

print("El tweet más positivo es:", tweet_more_positive)
print("El tweet más negativo es:", tweet_more_negative)
print("La calidad promedio es de:", vector_averages(result_mean_quality))
