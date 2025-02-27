import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
                   
                   
                     # ESTE PROYECTO ESTA VISUALIZADO PASO A PASO EN EL ARCHIVO explore.es.ipynb

resource_url = "https://companies-market-cap-copy.vercel.app/index.html"

response = requests.get(resource_url) # Hago la solicitud GET para obtener el contenido HTML.

html_content = response.text # Almaceno el contenido en una variable.


soup = BeautifulSoup(html_content, "html.parser") # Transformar la información en un objeto soup estructurado

soup_find_table = soup.find('div', class_ = 'profile-container pt-3').find('div', style = 'overflow-y: scroll;') # Busco dentro del objeto soup a travez de los div que encuentro tras utilizar las herramientas de desarrollador de nuestro navegador.

soup_table = soup_find_table.find('table') # Vuelvo a buscar de la misma manera pero ahora solo me quedo con la tabla. 

cells_of_table = soup_table.find_all('td') # vuelvo a buscar y me quedo con todas las celdas de la tabla.

# Obtengo el texto de cada celda.
cell_text = [cell.text.strip() for cell in cells_of_table]


# Organizo los datos en grupos de 3 (Año, Ganancia, Porcentaje de cambio).
data = []

for i in range(0, len(cell_text), 3):
    year = cell_text[i]
    revenue = cell_text[i + 1]
    change = cell_text[i + 2]
    data.append([year, revenue, change])

# Creo un DataFrame con los datos organizados.
df = pd.DataFrame(data, columns=['Year', 'Revenue', 'Change'])

# Limpieza del df y cenvertirlo a float. 
df = df.replace(r"[^0-9.]", "", regex=True).apply(pd.to_numeric)
df_final = df.dropna()




# Lo hago con with para asegurarme de que se cierre la concección y no se bloquee. 
with sqlite3.connect('DB_tesla') as con: # Creo, doy nombre y me conecto a la base de datos sqlite.
    df.to_sql('Tesla_table', con, if_exists='replace', index=False)  # Inserto o convierto el dataframe en sql.


# Muestro los resultados para verificar que he insertado bien los datos en la base de datos sql.
with sqlite3.connect('DB_tesla') as con:
    
    cursor = con.cursor() # Creo el cursor para ejecutar la consulta.
    
    cursor.execute('SELECT * FROM Tesla_table') # Ejecuto la consulta SELECT para obtener todos los datos de la tabla.
     
    data_rows = cursor.fetchall() # Obtener todos los resultados.
    
    # for row in data_rows: # Mostrar los resultados.
    #     print(row)



# Primera forma de visualizar los datos (Scatter Plot)
year = df_final['Year']
revenue = df_final['Revenue']
change = df_final['Change']

plt.figure(figsize = (10, 5))
scatter = plt.scatter(year, revenue, c = change, label = "Relationship between year and revenue", edgecolors='k', alpha=0.6) # Agrego (c = change) para agregar la columna extra al gráfico y poder hacer la barra lateral de colores. y lo meto todo en una variable que me pedira el codigo luego.
plt.title("Scatter plot: Year vs Revenue")
plt.xlabel("Year")
plt.ylabel("Revenue (Billions)")
plt.legend()
plt.grid(linestyle='--', alpha=0.7)
# plt.gca().invert_xaxis() # Con esto invierto el eje del gráfico porque estan los datos al revés para mi gusto. 
plt.colorbar(scatter, label='Change (%)') # Esta es la funcion de plt que hace la barra lateral y me pide la variable que inicializamos antes. 
plt.show()


# Segunda forma de visualizar los datos (Bars Plot)
year = df_final['Year']
revenue = df_final['Revenue']
change = df_final['Change']

plt.figure(figsize = (8, 5))
colors = ['blue' if x < 20 else 'green' if x < 50 else 'red' for x in change] # Defino los colores de los valores de la columna change en una variable.
plt.bar(year, revenue, color=colors) # Sumo los colores de la variable a la función.
plt.title("Bars plot: Year vs Revenue")
plt.xlabel("Year")
plt.ylabel("Revenue (Billions)")

plt.scatter([], [], color='blue', label='Change < 20%')
plt.scatter([], [], color='green', label='20 <= Change < 50%') # Creo los scatters para mostrar los colores en la legenda
plt.scatter([], [], color='red', label='Change >= 50%')
plt.legend(title='Change Categories')

plt.grid(linestyle='--', alpha=0.7)
# plt.gca().invert_xaxis() # Con esto invierto el eje del gráfico porque estan los datos al revés para mi gusto. 
plt.show()


year = df_final['Year']
revenue = df_final['Revenue']

plt.figure(figsize = (10, 5))
plt.plot(year, revenue)
plt.title("Line plot: Year vs Revenue")
plt.xlabel("Year")
plt.ylabel("Revenue (Billions)")
plt.grid(linestyle='--', alpha=0.7)
# plt.gca().invert_xaxis() # Con esto invierto el eje del gráfico porque estan los datos al revés para mi gusto. 
plt.show()