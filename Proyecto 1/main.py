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
def emotion_vector_2(vector_s, keywords, vector):
    for i in range(len(keywords)):
        word = keywords[i]
        if word in keywords_positive:
            vector_s[0] += vector[i]
        elif word in keywords_negative:
            vector_s[2] += vector[i]
        elif word in keywords_neutral:
            vector_s[1] += vector[i]

# Calcula el promedio del sentimiento de cada tweet
def avg_vector(vector):
    return np.array([round(i / len(vector), 2) for i in vector])

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

def key_words_mapper(word, keywords, vector):
    for i in range(len(keywords)):
        if word == keywords[i]:
            vector[i] += 1
            return

tweets = [
    "No puedo creer la triste noticia de su fallecimiento. Una pérdida inmensa para todos nosotros.",
    "¡Excelente trabajo en la presentación! Tu dedicación y esfuerzo son inspiradores!",
    "¡Increíble concierto esta noche! La energía y la música me hicieron olvidar todos mis problemas...",
    "Mi día fue un desastre total. Nada salió como lo planeé.",
]

#Sacarrrr
tweets = [
    "Que desprecio que me genera el gobierno de Fernandez! Es impresionante la inflacion que se genero. Es un muerto! Aun con trabajo no podes vivir!",
    "Estoy muy feliz, al fin me recibi de Ingeniero en Informatica, que orgullo!",
    "Ayer me estaba comiendo un sanguche de bondiola, no saben lo orgulloso que estoy del buen trabajo del de la fiambreria. Este sanguche es un exito.",
    "Mi día fue un desastre total. Nada salió como lo planeé.",
]

keywords_positive = ["excelente", "inspiradores", "increible"]
keywords_negative = ["triste", "fallecimiento", "perdida", "problemas", "desastre"]
keywords_neutral = ["noticia", "creer", "presentacion", "noche", "musica"]

#sacarrr
keywords_positive = ["feliz", "orgullo", "exito"]
keywords_negative = ["muerto", "desprecio", "inflacion"]
keywords_neutral = ["trabajo", "bondiola", "sanguche"]

keywords = keywords_positive + keywords_neutral + keywords_negative

# Inicialización para hacer un seguimiento del tweet más positivo y negativo
tweet_more_positive = None
tweet_more_negative = None
max_score = float('-inf')
min_score = float('inf')
result_mean_quality = []

for tweet in tweets:
    vector = np.array([0 for i in range(len(keywords))])
    vector_s = np.array([0, 0, 0])
    for word in clean_tweet(tweet):
        key_words_mapper(word, keywords, vector)
    emotion_vector_2(vector_s, keywords, vector)
    avereged_vector = avg_vector(vector)
    avereged_feelings_vector = avg_vector(vector_s)
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
#print("La calidad promedio es de:", np.mean(result_mean_quality)) #No estoy muy seguro de esto.
