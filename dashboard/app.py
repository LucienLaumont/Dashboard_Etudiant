# Importation des bibliothèques nécessaires
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from data import get_data_from_mongodb
from time import sleep 

from homes_pages import layout_home
from users_pages import layout_users, callback_user  # Importez la fonction de callback
from stats_pages import layout_stats
from maps_pages import layout_maps

print("Avant Boucle")

# Vérification de la présence de données dans la base de données
df = None
while df is None or df.empty:
    df = get_data_from_mongodb()
    print(1)
    print(df)
    if df is None or df.empty:
        print("Aucune donnée trouvée dans la base de données. Attente de 20 secondes...")
        sleep(20)  # Attendez 60 secondes avant de vérifier à nouveau


print("Après Boucle")

# Initialisation de l'application Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Layout principal de l'application
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    layout_home(),
    html.Div(id='page-content')
])

# Callback pour le routage
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname in ['/', '/page_user']:
        return layout_users(df)
    elif pathname == '/page_stat':
        return layout_stats(df)
    elif pathname == '/page_map':
        return layout_maps(df)
    else:
        return layout_home()  # Retour à la page d'accueil pour les chemins non reconnus

# Enregistrez la fonction de callback définie dans users_pages.py avec l'objet app
callback_user(df,app)

# Lancement de l'application
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')

#CCECEC
#638487
#4E6166
#357A8D
#162220