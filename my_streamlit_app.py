import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Titre de l'application
st.title('Analyse des voitures par région')

# Description
st.write("""
    Cette application permet d'explorer des données sur les voitures, avec une analyse de corrélation et des distributions.
    Vous pouvez filtrer les données par région (US, Europe, Japon) grâce aux boutons ci-dessous.
""")

# Charger les données
link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
df = pd.read_csv(link)

# Nettoyage des données : suppression des espaces et des points dans la colonne 'continent'
df['continent'] = df['continent'].str.strip().str.replace('.', '', regex=False)

# Afficher les premières lignes des données pour vérifier
st.write("Voici un aperçu des données :")
st.write(df.head())

# Liste des régions disponibles
regions = df['continent'].unique()

# Sélection de la région via un bouton radio
region_filter = st.radio("Sélectionner une région", regions)

# Filtrer les données en fonction de la région sélectionnée
df_filtered = df[df['continent'] == region_filter]

# Afficher les données filtrées
st.write(f"Voici les données pour la région {region_filter} :")
st.write(df_filtered)

# Affichage de la distribution des MPG pour la région sélectionnée
st.write("Distribution des MPG pour la région sélectionnée :")
plt.figure(figsize=(10,6))
sns.histplot(df_filtered['mpg'], kde=True, color='blue')
plt.title(f'Distribution des MPG pour la région {region_filter}')
st.pyplot()

# Affichage de la corrélation entre les différentes caractéristiques
st.write("Corrélation entre les différentes caractéristiques :")
plt.figure(figsize=(10,6))

# Nettoyer les colonnes numériques (assurer que ce sont des types numériques)
df_filtered['mpg'] = pd.to_numeric(df_filtered['mpg'], errors='coerce')
df_filtered['hp'] = pd.to_numeric(df_filtered['hp'], errors='coerce')
df_filtered['weightlbs'] = pd.to_numeric(df_filtered['weightlbs'], errors='coerce')
df_filtered['time-to-60'] = pd.to_numeric(df_filtered['time-to-60'], errors='coerce')
df_filtered['cylinders'] = pd.to_numeric(df_filtered['cylinders'], errors='coerce')
df_filtered['cubicinches'] = pd.to_numeric(df_filtered['cubicinches'], errors='coerce')

# Calculer la matrice de corrélation pour les colonnes numériques uniquement
corr_matrix = df_filtered[['mpg', 'hp', 'weightlbs', 'time-to-60', 'cylinders', 'cubicinches']].corr()

sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
plt.title(f'Corrélation des caractéristiques pour la région {region_filter}')
st.pyplot()

# Commentaires expliquant les résultats
st.write("""
    - **Distribution des MPG** : Cette courbe montre la distribution des MPG (miles par gallon) des voitures dans la région sélectionnée.
    - **Corrélation** : La carte de chaleur affiche les corrélations entre les différentes caractéristiques des voitures. Par exemple, on peut observer une forte corrélation entre la cylindrée du moteur et la puissance (hp).
""")
