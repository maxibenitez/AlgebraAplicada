import numpy as np
import unidecode as ud
import re

# Define el score sentimental
def emotion_vector(word, vector_s):
    if word in keywords_positive:
        vector_s[0] += 1
    elif word in keywords_negative:
        vector_s[2] += 1
    elif word in keywords_neutral:
        vector_s[1] += 1

# Calcula el promedio del sentimiento de cada tweet
def avg_feeling(vector_s):
    avg = np.mean(vector_s)
    avg_rounded = round(avg, 2)
    return avg_rounded

# Calcula la calidad de los resultados
def quality_results(vector_s, number_keywords):
    quality = number_keywords / np.sum(vector_s) 
    quality_rounded = round(quality, 2)
    return quality_rounded

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

# Inicialización para hacer un seguimiento del tweet más positivo y negativo
tweet_more_positive = None
tweet_more_negative = None
max_score = float('-inf')
min_score = float('inf')
tweets_scores = []

for tweet in tweets:
    vector_s = [0, 0, 0]
    dictionary_copy = dictionary.copy()
        
    for word in clean_tweet(tweet):
        emotion_vector(word,vector_s)
        dictionary_word = dictionary_copy.get(word)
        if dictionary_word is not None:
            dictionary_copy[word] += 1
    #average = avg_feeling(vector_s)
    tweet_score = score(vector_s)
    tweets_scores.append(tweet_score)
    qlt_results = quality_results(vector_s, len(keywords))
    if tweet_score > max_score:
        max_score = tweet_score
        tweet_more_positive = tweet
    if tweet_score < min_score:
        min_score = tweet_score
        tweet_more_negative = tweet

    print("Tweet:", tweet)
    print("Vector s:", vector_s)
    print("Promedio del sentimiento:", tweet_score)
    print("Calidad de los resultados:", qlt_results)
    print("El score es:", tweet_score)
    print("---------------------------------------------\n")

print("El tweet más positivo es:", tweet_more_positive)
print("El tweet más negativo es:", tweet_more_negative)
print("La calidad promedio es de:", np.mean(tweets_scores)) #No estoy muy seguro de esto.
