from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

regions_mapping = {
    '01': 'Auvergne-Rhône-Alpes', '02': 'Hauts-de-France', '03': 'Auvergne-Rhône-Alpes',
    '04': 'Provence-Alpes-Côte d\'Azur', '05': 'Provence-Alpes-Côte d\'Azur', '06': 'Provence-Alpes-Côte d\'Azur',
    '07': 'Auvergne-Rhône-Alpes', '08': 'Grand Est', '09': 'Occitanie',
    '10': 'Grand Est', '11': 'Occitanie', '12': 'Occitanie',
    '13': 'Provence-Alpes-Côte d\'Azur', '14': 'Normandie', '15': 'Auvergne-Rhône-Alpes',
    '16': 'Nouvelle-Aquitaine', '17': 'Nouvelle-Aquitaine', '18': 'Centre-Val de Loire',
    '19': 'Nouvelle-Aquitaine', '21': 'Bourgogne-Franche-Comté', '22': 'Bretagne',
    '23': 'Nouvelle-Aquitaine', '24': 'Nouvelle-Aquitaine', '25': 'Bourgogne-Franche-Comté',
    '26': 'Auvergne-Rhône-Alpes', '27': 'Normandie', '28': 'Centre-Val de Loire',
    '29': 'Bretagne', '2A': 'Corse', '2B': 'Corse',
    '30': 'Occitanie', '31': 'Occitanie', '32': 'Occitanie',
    '33': 'Nouvelle-Aquitaine', '34': 'Occitanie', '35': 'Bretagne',
    '36': 'Centre-Val de Loire', '37': 'Centre-Val de Loire', '38': 'Auvergne-Rhône-Alpes',
    '39': 'Bourgogne-Franche-Comté', '40': 'Nouvelle-Aquitaine', '41': 'Centre-Val de Loire',
    '42': 'Auvergne-Rhône-Alpes', '43': 'Auvergne-Rhône-Alpes', '44': 'Pays de la Loire',
    '45': 'Centre-Val de Loire', '46': 'Occitanie', '47': 'Nouvelle-Aquitaine',
    '48': 'Occitanie', '49': 'Pays de la Loire', '50': 'Normandie',
    '49': 'Pays de la Loire', '50': 'Normandie', '51': 'Grand Est', '52': 'Grand Est',
    '53': 'Pays de la Loire', '54': 'Grand Est', '55': 'Grand Est', '56': 'Bretagne',
    '57': 'Grand Est', '58': 'Bourgogne-Franche-Comté', '59': 'Hauts-de-France',
    '60': 'Hauts-de-France', '61': 'Normandie', '62': 'Hauts-de-France',
    '63': 'Auvergne-Rhône-Alpes', '64': 'Nouvelle-Aquitaine', '65': 'Occitanie',
    '66': 'Occitanie', '67': 'Grand Est', '68': 'Grand Est',
    '69': 'Auvergne-Rhône-Alpes', '70': 'Bourgogne-Franche-Comté', '71': 'Bourgogne-Franche-Comté',
    '72': 'Pays de la Loire', '73': 'Auvergne-Rhône-Alpes', '74': 'Auvergne-Rhône-Alpes',
    '75': 'Île-de-France', '76': 'Normandie', '77': 'Île-de-France',
    '78': 'Île-de-France', '79': 'Nouvelle-Aquitaine', '80': 'Hauts-de-France',
    '81': 'Occitanie', '82': 'Occitanie', '83': 'Provence-Alpes-Côte d\'Azur',
    '84': 'Provence-Alpes-Côte d\'Azur', '85': 'Pays de la Loire', '86': 'Nouvelle-Aquitaine',
    '87': 'Nouvelle-Aquitaine', '88': 'Grand Est', '89': 'Bourgogne-Franche-Comté',
    '90': 'Bourgogne-Franche-Comté', '91': 'Île-de-France', '92': 'Île-de-France',
    '93': 'Île-de-France', '94': 'Île-de-France',
    '95': 'Île-de-France',
    '971': 'Guadeloupe', '972': 'Martinique', '973': 'Guyane',
    '974': 'La Réunion', '976': 'Mayotte'
}

def map_graph(df):

    # Filter out NaN values for the 'diplome' column
    private_public_counts = df[df['diplome'].notna()]['diplome'].value_counts().reset_index()
    private_public_counts.columns = ['Diplome', 'Count']

    # Create the first pie chart
    fig1 = px.pie(private_public_counts, values='Count', names='Diplome', title='Répartition des lycées privés et publics')
    fig1.update_layout(font=dict(family="Arial", size=15, color="black"))

    # Extract the department number and map to regions, handling NaN values
    df['Departement'] = df['adresse'].str.extract(r'(\d{2})')
    df['Region'] = df['Departement'].map(regions_mapping)

    # Filter out NaN values for the 'Region' column
    region_counts = df[df['Region'].notna()]['Region'].value_counts().reset_index()
    region_counts.columns = ['Region', 'Count']

    # Create the second pie chart
    fig2 = px.pie(region_counts, values='Count', names='Region', title='Nombre de lycées par région')
    fig2.update_layout(showlegend=False, font=dict(family="Arial", size=15, color="black"))

    fig2.update_layout(showlegend=False,font=dict(
            family="Arial",
            size=15,
            color="black"
        ))
    
    return fig1,fig2

def layout_maps(df):

    fig1,fig2 = map_graph(df)

    return html.Div([
        html.Div(id='page-map', children=[
            html.Div(children=[
                html.Iframe(id='map', src='/assets/cities_map.html', style={'width': '100%', 'height': '100%'})
            ], id='container-map'),
            html.Div(id='piechart-container', children=[
                dcc.Graph(id='pie-chart-1', figure=fig1, className='pie-chart'),  # Ajouter le premier graphique en secteurs avec une classe
                dcc.Graph(id='pie-chart-2', figure=fig2, className='pie-chart')   # Ajouter le deuxième graphique en secteurs avec une classe
            ]),
        ]),
    ], className='conteneur-page')