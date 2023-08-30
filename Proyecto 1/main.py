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
        
# Define el score sentimental (Version 2)
def emotion_vector_2(vector_s, dic_words):
    for word in dic_words:
        if word in keywords_positive:
            vector_s[0] += dic_words[word]
        elif word in keywords_negative:
            vector_s[2] += dic_words[word]
        elif word in keywords_neutral:
            vector_s[1] += dic_words[word]

# Calcula el promedio del sentimiento de cada tweet
def avg_vector(vector_s):
    avg = np.mean(vector_s)
    #avg_rounded = round(avg, 2)
    return avg
    
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
result_mean_quality = []

for tweet in tweets:
    vector_s = [0, 0, 0]
    dictionary_copy = dictionary.copy()
    for word in clean_tweet(tweet):
        #emotion_vector(word,vector_s)
        dictionary_word = dictionary_copy.get(word)
        if dictionary_word is not None:
            dictionary_copy[word] += 1
    emotion_vector_2(vector_s, dictionary_copy)
    result_quality = avg_vector(list(dictionary_copy.values()))
    result_mean_quality.append(result_quality)
    feelings_mean = avg_vector(vector_s)
    tweet_score = score(vector_s)

    if tweet_score > max_score:
        max_score = tweet_score
        tweet_more_positive = tweet
    if tweet_score < min_score:
        min_score = tweet_score
        tweet_more_negative = tweet

    print("Tweet:", tweet)
    print("Vector s:", vector_s)
    print("Promedio del sentimiento:", tweet_score)
    print("El score es:", tweet_score)
    print("---------------------------------------------\n")

print("El tweet más positivo es:", tweet_more_positive)
print("El tweet más negativo es:", tweet_more_negative)
print("La calidad promedio es de:", np.mean(result_mean_quality)) #No estoy muy seguro de esto.
