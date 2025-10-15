from flask import Flask, render_template, request

app = Flask(__name__)

# Un dictionnaire pour rendre les noms plus lisibles pour le client
# La clé est le 'name' de l'input HTML, la valeur est le texte à afficher
feature_names = {
    # Rôles
    "role_super_admin": "Rôle: Super-Admin (DG)",
    "role_comptable_central": "Rôle: Comptable Central",
    "role_chef_chantier": "Rôle: Chef de Chantier",
    "role_comptable_chantier": "Rôle: Comptable de Chantier",
    # Module 1
    "mod1_creer_chantier": "Module 1: Créer un nouveau chantier",
    "mod1_lister_chantiers": "Module 1: Lister tous les chantiers",
    "mod1_dashboard_chantier": "Module 1: Tableau de bord par chantier",
    "mod1_assigner_users": "Module 1: Assigner des utilisateurs à un chantier",
    "mod1_archiver_chantiers": "Module 1: Archiver les chantiers terminés",
    # Module 2
    "mod2_formulaire_depense": "Module 2: Formulaire simple pour ajouter une dépense",
    "mod2_gestion_categories": "Module 2: Gestion des catégories de dépenses",
    "mod2_cat_perso": "Module 2: Catégories de dépenses personnalisables",
    "mod2_photo_recu": "Module 2: Prise de photo du reçu obligatoire",
    "mod2_mode_hors_ligne": "Module 2: Mode HORS-LIGNE pour ajout de dépenses",
    "mod2_circuit_validation": "Module 2: Circuit de validation pour grosses dépenses",
    "mod2_transfert_fonds": "Module 2: Enregistrer un transfert de fonds",
    "mod2_confirmer_reception": "Module 2: Confirmer la réception des fonds",
    # Module 3
    "mod3_vue_ensemble_kpi": "Module 3: Vue d'ensemble des indicateurs clés (DG)",
    "mod3_graph_camembert": "Module 3: Graphique des dépenses par chantier (Camembert)",
    "mod3_graph_courbe": "Module 3: Graphique d'évolution des dépenses (Courbe)",
    "mod3_liste_top5": "Module 3: Liste des 5 chantiers les plus coûteux",
    "mod3_alertes_budget": "Module 3: Système d'alertes de budget",
    "mod3_generer_rapports_detailles": "Module 3: Générer des rapports détaillés",
    "mod3_export_excel": "Module 3: Exporter les rapports en format Excel",
    "mod3_export_pdf": "Module 3: Exporter les rapports en format PDF",
    "mod3_visualiser_recus": "Module 3: Visualiser les photos des reçus",
    # Module 4
    "mod4_ia_chat": "Module 4 (IA): Interface de chat en langage simple",
    # Spécifications Techniques
    "tech_app_web": "Plateforme: Application Web",
    "tech_app_mobile": "Plateforme: Application Mobile Android",
    "tech_app_bureau": "Plateforme: Application de Bureau (Optionnel)",
    "tech_hebergement_securise": "Sécurité: Hébergement sur serveur sécurisé",
    "tech_sauvegardes": "Sécurité: Sauvegardes quotidiennes automatiques",
    "tech_connexion_securisee": "Sécurité: Connexion sécurisée par mot de passe",
    # Permissions (optionnel, pour plus de détails)
}

@app.route('/')
def index():
    # Affiche simplement le formulaire HTML
    return render_template('index.html')

@app.route('/resultat', methods=['POST'])
def resultat():
    # Récupère toutes les données cochées du formulaire
    selections = request.form
    
    selected_features = []
    for key, value in selections.items():
        # On cherche la description lisible dans notre dictionnaire
        feature_text = feature_names.get(key, key) # Si non trouvé, on affiche la clé
        
        # Pour les radios, on affiche aussi la valeur (ex: Oui/Non)
        if key == "mod2_cat_perso":
             feature_text += f" : {value.capitalize()}"

        selected_features.append(feature_text)

    # On affiche une page de résultat simple avec la liste des sélections
    return f"""
    <html>
        <head>
            <title>Votre Sélection</title>
            <style>
                body {{ font-family: sans-serif; margin: 40px; }}
                h1 {{ color: #005a9c; }}
                ul {{ list-style-type: none; padding-left: 0; }}
                li {{ background-color: #f0f0f0; margin-bottom: 8px; padding: 12px; border-radius: 4px; }}
                .container {{ max-width: 800px; margin: auto; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Récapitulatif de votre sélection</h1>
                <p>Voici la liste des fonctionnalités que vous avez choisies pour le projet BTP-Pilot. Vous pouvez copier/coller ce résumé pour nous l'envoyer.</p>
                <ul>
                    {''.join([f'<li>✅ {feature}</li>' for feature in selected_features])}
                </ul>
            </div>
        </body>
    </html>
    """

if __name__ == '__main__':
    # Permet de lancer le serveur en local pour tester
    app.run(debug=True)