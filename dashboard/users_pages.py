
from dash import Input, Output,html,dcc,dash_table
import pandas as pd

# Colonnes spécifiques qu'on souhaite afficher
selected_columns = ['nom', 'diplome', 'statut', 'ville','taux_reussite_bac','taux_mentions_bac','effectifs_terminale']


def user_component(df):

    # Colonnes spécifiques que vous souhaitez afficher
    selected_columns = ['nom', 'diplome', 'statut', 'ville','taux_reussite_bac','taux_mentions_bac','effectifs_terminale']

    # Filtrer le DataFrame pour sélectionner les colonnes spécifiques
    filtered_df = df[selected_columns]

    statuts_uniques = df['statut'].dropna().unique()
    diplomes_uniques = df['diplome'].dropna().unique()
    villes_uniques = df['ville'].dropna().unique()

    return statuts_uniques,diplomes_uniques,villes_uniques,filtered_df

# Définissez votre layout pour la page des utilisateurs
def layout_users(df):

    statuts_uniques,diplomes_uniques,villes_uniques,filtered_df = user_component(df)

    return html.Div([
        html.Div(id='page-user', children=[
            # Sélecteur pour choisir une ville
            html.Div(id='selecteur-box', children=[
                html.Div(id='selecteur-ville', children=[
                    html.H3('VILLE : ', className='selecteur-titre'),  # Titre
                    dcc.Dropdown(
                        id='ville-dropdown',
                        options=[{'label': ville, 'value': ville} for ville in villes_uniques],
                        value=villes_uniques[0],  # Valeur initiale
                        multi=True,
                        placeholder="Sélectionnez une ville"
                    ),
                ]),
                # Sélecteur de statut avec des boutons à cocher
                html.Div(id='selecteur-status', children=[
                    html.H3('STATUT : ', className='selecteur-titre'),
                    dcc.Checklist(
                        id='statut-checklist-statut',
                        options=[{'label': statut, 'value': statut} for statut in statuts_uniques],
                        value=statuts_uniques,  # Valeur initiale
                        inline=True  # Aligner les boutons horizontalement
                    ),
                ]),
                html.Div(id='selecteur-diplome', children=[
                    html.H3('DIPLOME : ', className='selecteur-titre'),
                    dcc.Checklist(
                        id='statut-checklist-diplome',
                        options=[{'label': diplome, 'value': diplome} for diplome in diplomes_uniques],
                        value=diplomes_uniques,  # Valeur initiale
                        inline=True  # Aligner les boutons horizontalement
                    ),
                ]),
            ]),
            # Espace pour afficher les résultats
            html.Div(id='user-results-container', children=[
                dash_table.DataTable(
                    id='table',
                    columns=[{'name': col, 'id': col} for col in filtered_df.columns],
                    data=filtered_df.to_dict('records'),
                    style_table={'overflowX': 'scroll'},
                    style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
                    style_data={'whiteSpace': 'normal'},
                    page_size=15,
                )
            ]),
            html.Div([
                html.P("Créateurs de ce dashboard : Emmanuelle Lepage & Lucien Laumont", className='creators-text')
            ])
        ], className='conteneur-page')
    ])


def callback_user(df,app):
    # Callback pour mettre à jour la table en fonction des sélections dans les sélecteurs
    @app.callback(
        Output('table', 'data'),
        Input('ville-dropdown', 'value'),
        Input('statut-checklist-statut', 'value'),
        Input('statut-checklist-diplome', 'value')
    )
    def update_table(selected_villes, selected_statuts, selected_diplomes):

        # Assurez-vous que les variables sont des listes
        if not isinstance(selected_villes, list):
            selected_villes = [selected_villes]
        if not isinstance(selected_statuts, list):
            selected_statuts = [selected_statuts]
        if not isinstance(selected_diplomes, list):
            selected_diplomes = [selected_diplomes]

        # Filtrer le DataFrame en fonction des sélections
        filtered_data = df[
            (df['ville'].isin(selected_villes)) &
            (df['statut'].isin(selected_statuts)) &
            (df['diplome'].isin(selected_diplomes))
        ]

        # Sélectionner les colonnes spécifiques
        filtered_data = filtered_data[selected_columns]

        return filtered_data.to_dict('records')

