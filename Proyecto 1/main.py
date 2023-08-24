import numpy as np
import unidecode as ud
import re

tweets = [
    "No puedo creer la triste noticia de su fallecimiento. Una pérdida inmensa para todos nosotros.",
    "¡Excelente trabajo en la presentación! Tu dedicación y esfuerzo son inspiradores!",
    "¡Increíble concierto esta noche! La energía y la música me hicieron olvidar todos mis problemas...",
    "Mi día fue un desastre total. Nada salió como lo planeé.",
]

keywords_positive = ["excelente", "inspiradores", "increible"]
keywords_negative = ["triste", "fallecimiento", "perdida", "problemas", "desastre"]
keywords_neutral = ["noticia", "creer", "presentacion", "noche", "musica"]
keywords = keywords_negative + keywords_neutral + keywords_positive

# Inicializamos el diccionario con todas las palabras en 0
dictionary = {keywords[i]: 0 for i in range(len(keywords))}

# Define el score sentimental
def suma_entradas(word):
    if word in keywords_positive:
        vector_s[0] += 1
    elif word in keywords_negative:
        vector_s[2] += 1
    elif word in keywords_neutral:
        vector_s[1] += 1

# Calcula el promedio del sentimiento de cada tweet
def avg_feeling():
    avg = np.mean(vector_s)
    avg_rounded = round(avg, 2)
    return avg_rounded
    
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

# Inicialización para hacer un seguimiento del tweet más positivo y negativo
tweet_more_positive = None
tweet_more_negative = None
max_score = float('-inf')
min_score = float('inf')

for tweet in tweets:
    vector_s = [0, 0, 0]
    dictionary_copy = dictionary.copy()
    for word in clean_tweet(tweet):
        suma_entradas(word)
        matias = dictionary_copy.get(word)
        if matias is not None:
            dictionary_copy[word] += 1
    average = avg_feeling()
    tweet_score = score(vector_s)

    if tweet_score > max_score:
        max_score = tweet_score
        tweet_more_positive = tweet
    if tweet_score < min_score:
        min_score = tweet_score
        tweet_more_negative = tweet

    print("Tweet:", tweet)
    print("Vector s:", vector_s)
    print("Promedio del sentimiento:", average)
    print("El score es:", tweet_score)
    print("---------------------------------------------")

print("El tweet más positivo es:", tweet_more_positive)
print("El tweet más negativo es:", tweet_more_negative)