#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


with open('DATA\Records.json', encoding='utf-8') as f:
    data = json.load(f)


# In[3]:



locations = pd.DataFrame(data['locations'])
locations['lat'] = locations['latitudeE7'] / 1e7
locations['lon'] = locations['longitudeE7'] / 1e7


# In[4]:


Historiquedepositions = locations[['timestamp', 'deviceTag', 'source', 'lat', 'lon', 'accuracy']].rename(columns={'deviceTag': 'dispositif'})
Historiquedepositions.to_csv('Historiquedepositions.csv', index=False)


# In[5]:


# Convertir la colonne "timestamp" en format de date/heure
locations['timestamp'] = pd.to_datetime(locations['timestamp'])

# Trouver la valeur minimale de la colonne "timestamp"
min_Time = locations['timestamp'].min().strftime('%d/%m/%Y %H:%M:%S')

# Trouver la valeur maximale de la colonne "timestamp"
max_Time = locations['timestamp'].max().strftime('%d/%m/%Y %H:%M:%S')


print("Valeur minimale de l'accuracy:", min_Time)
print("Valeur maximale de l'accuracy:", max_Time)


# In[6]:


source_counts = Historiquedepositions['source'].value_counts()

# Afficher le nombre d'itérations pour chaque valeur unique dans la console
print(source_counts)


# In[7]:


# Extraire la date à partir du timestamp
locations['date'] = pd.to_datetime(locations['timestamp']).dt.date

# Calculer le nombre de points par jour
points_par_jour = locations['date'].value_counts().sort_index(ascending=False)

# Afficher le nombre de points par jour dans l'ordre décroissant
print("Nombre de points par jour (tri décroissant):")
print(points_par_jour.sort_values(ascending=False))


# In[8]:



# Calculer la moyenne de la colonne "accuracy"
mean_accuracy = locations['accuracy'].mean()

# Calculer la médiane de la colonne "accuracy"
median_accuracy = locations['accuracy'].median()

# Trouver la valeur minimale de la colonne "accuracy"
min_accuracy = locations['accuracy'].min()

# Trouver la valeur maximale de la colonne "accuracy"
max_accuracy = locations['accuracy'].max()

# Afficher les résultats
print("Moyenne de l'accuracy:", mean_accuracy)
print("Médiane de l'accuracy:", median_accuracy)
print("Valeur minimale de l'accuracy:", min_accuracy)
print("Valeur maximale de l'accuracy:", max_accuracy)


# In[9]:



# Tracer le nuage de points de l'accuracy
plt.scatter(range(len(locations)), locations['accuracy'], label='Accuracy')

# Tracer la courbe de la moyenne
plt.axhline(mean_accuracy, color='red', linestyle='--', label='Moyenne')

# Tracer la courbe de la médiane
plt.axhline(median_accuracy, color='green', linestyle='--', label='Médiane')

plt.xlabel('Index')
plt.ylabel('Accuracy')
plt.legend()
plt.show()


# In[10]:


# Sélectionner les 20 valeurs les plus grandes de la colonne "accuracy"
top_20_values = locations.nlargest(20, 'accuracy')

# Afficher les 20 valeurs les plus grandes
print(top_20_values['accuracy'])


# In[22]:


# Convertir la colonne "timestamp" en format de date/heure
locations['timestamp'] = pd.to_datetime(locations['timestamp'])

# Extraire la date (année-mois-jour) à partir du timestamp
locations['date'] = locations['timestamp'].dt.date

# Calculer le temps moyen entre les points d'une même date
date_grouped = locations.groupby('date')

time_diffs_dict = {}

for date, group in date_grouped:
    if len(group) > 1:
        time_diffs = group['timestamp'].diff().mean()
        time_diffs_dict[date] = {'time_diffs': time_diffs, 'count': len(group)}

# Afficher les résultats dans l'ordre décroissant par rapport au temps entre les points
sorted_dates = sorted(time_diffs_dict, key=lambda x: time_diffs_dict[x]['time_diffs'], reverse=True)

all_time_diffs = []  # Liste pour stocker tous les temps entre les points

for date in sorted_dates:
    group = date_grouped.get_group(date)
    time_diffs = group['timestamp'].diff().mean()
    time_diffs_seconds = time_diffs.total_seconds()
    all_time_diffs.append(time_diffs_seconds)

    median_time_diffs = group['timestamp'].diff().median()
    max_time_diffs = group['timestamp'].diff().max()
    min_time_diffs = group['timestamp'].diff().min()
    count = time_diffs_dict[date]['count']
    print(f"Date: {date}")
    print(f"Nombre de points: {count}")
    print(f"Temps moyen entre les points: {time_diffs}")
    print(f"Médiane du temps entre les points: {median_time_diffs}")
    print(f"Valeur la plus haute du temps entre les points: {max_time_diffs}")
    print(f"Valeur la plus basse du temps entre les points: {min_time_diffs}")
    print()


# In[21]:


# Calcul de la moyenne globale
global_mean = sum(all_time_diffs) / len(all_time_diffs)
mean_time_diffs = pd.Timedelta(seconds=global_mean)
formatted_mean_time_diffs = str(mean_time_diffs).split(".")[0]

# Calcul de la médiane globale
global_median = statistics.median(all_time_diffs)
median_time_diffs = pd.Timedelta(seconds=global_median)
formatted_median_time_diffs = str(median_time_diffs).split(".")[0]

print(f"Moyenne globale du temps entre les points: {formatted_mean_time_diffs}")
print(f"Médiane globale du temps entre les points: {formatted_median_time_diffs}")


# In[23]:


# Trouver la date avec le temps le plus haut
date_with_max_time = max(time_diffs_dict, key=lambda x: time_diffs_dict[x]['time_diffs'])
max_time = time_diffs_dict[date_with_max_time]['time_diffs']
print(f"Date avec le temps le plus haut: {date_with_max_time} (Temps: {max_time})")

# Trouver la date avec le temps le plus bas
date_with_min_time = min(time_diffs_dict, key=lambda x: time_diffs_dict[x]['time_diffs'])
min_time = time_diffs_dict[date_with_min_time]['time_diffs']
print(f"Date avec le temps le plus bas: {date_with_min_time} (Temps: {min_time})")


# In[ ]:




