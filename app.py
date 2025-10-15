import os
import requests  # N'oubliez pas d'installer requests: pip install requests
from flask import Flask, render_template, request

app = Flask(__name__)

# --- NOUVELLE Configuration pour l'API Brevo (plus de Flask-Mail) ---
BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
BREVO_API_KEY = os.environ.get('BREVO_API_KEY')       # La clé API SMTP de Brevo
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')      # Votre email validé comme expéditeur sur Brevo
SENDER_NAME = "Serveur Cahier de Charges BTP"        # Nom de l'expéditeur qui apparaîtra dans l'email
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')  # Votre email où recevoir les notifications
# ---------------------------------------------------------------------

# Le dictionnaire reste identique
feature_names = {
    # Rôles
    "role_super_admin": "Rôle: Super-Admin (DG)",
    "role_comptable_central": "Rôle: Comptable Central",
    "role_chef_chantier": "Rôle: Chef de Chantier",
    "role_comptable_chantier": "Rôle: Comptable de Chantier",
    # Permissions
    "perm_sa_voir_chantiers": "Permission (SA): Voir tous les chantiers",
    "perm_sa_gerer_users": "Permission (SA): Gérer les utilisateurs",
    "perm_sa_valider_budgets": "Permission (SA): Valider les budgets",
    "perm_sa_tous_rapports": "Permission (SA): Accéder à tous les rapports",
    "perm_cc_voir_chantiers": "Permission (CC): Voir tous les chantiers",
    "perm_cc_transferts": "Permission (CC): Gérer les transferts de fonds",
    "perm_cc_valider_depenses": "Permission (CC): Valider les dépenses importantes",
    "perm_cc_generer_rapports": "Permission (CC): Générer les rapports comptables",
    "perm_cdc_voir_son_chantier": "Permission (CdC): Voir uniquement son chantier",
    "perm_cdc_consulter_budget": "Permission (CdC): Consulter le budget",
    "perm_cdc_approuver_petites_depenses": "Permission (CdC): Approuver les petites dépenses",
    "perm_cc2_acces_son_chantier": "Permission (ComptaC): Accéder uniquement à son chantier",
    "perm_cc2_enregistrer_depense": "Permission (ComptaC): Enregistrer une dépense",
    "perm_cc2_consulter_depenses": "Permission (ComptaC): Consulter les dépenses",
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
}

# NOUVELLE fonction pour envoyer l'email via l'API HTTP de Brevo
def send_brevo_email(subject, html_content):
    # Vérifie que les variables d'environnement sont bien présentes
    if not all([BREVO_API_KEY, SENDER_EMAIL, RECIPIENT_EMAIL]):
        print("Erreur critique: Une ou plusieurs variables d'environnement pour l'email sont manquantes.")
        return False

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }
    payload = {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"email": RECIPIENT_EMAIL}],
        "subject": subject,
        "htmlContent": html_content
    }
    try:
        response = requests.post(BREVO_API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Lève une exception si le statut est une erreur (4xx ou 5xx)
        print("Email envoyé avec succès via l'API Brevo!")
        return True
    except requests.exceptions.RequestException as e:
        # Affiche des logs détaillés en cas d'échec
        print(f"Erreur lors de la requête à l'API Brevo: {e}")
        if 'response' in locals():
            print(f"Statut de la réponse: {response.status_code}")
            print(f"Détails de la réponse: {response.text}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultat', methods=['POST'])
def resultat():
    selections = request.form
    
    selected_features = []
    for key, value in selections.items():
        feature_text = feature_names.get(key, key.replace("_", " ").capitalize())
        if key == "mod2_cat_perso":
             feature_text += f" : {value.capitalize()}"
        selected_features.append(feature_text)

    # Création du corps de l'email en format HTML pour un joli rendu
    email_subject = "Nouvelle sélection de fonctionnalités - BTP-Pilot"
    html_body = "<h1>Nouvelle soumission du cahier des charges BTP-Pilot</h1>"
    html_body += "<p>Un client a soumis la sélection de fonctionnalités suivante :</p><ul>"
    for feature in selected_features:
        html_body += f"<li>✅ {feature}</li>"
    html_body += "</ul>"
    
    # Appel de notre nouvelle fonction d'envoi d'email
    send_brevo_email(email_subject, html_body)

    # Affichage de la page de confirmation au client (ne change pas)
    return f"""
    <html>
        <head><title>Votre Sélection</title>
        <style>
            body {{ font-family: sans-serif; margin: 20px; }}
            .container {{ max-width: 800px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9; }}
            h1 {{ color: #005a9c; }}
            ul {{ list-style-type: none; padding-left: 0; }}
            li {{ background-color: #e9f5e9; margin-bottom: 8px; padding: 12px; border-radius: 4px; border-left: 5px solid #28a745; }}
        </style>
        </head>
        <body>
            <div class="container">
                <h1>Récapitulatif de votre sélection</h1>
                <p>Merci ! Votre sélection a bien été enregistrée et nous a été transmise. Voici le récapitulatif :</p>
                <ul>
                    {''.join([f'<li>✅ {feature}</li>' for feature in selected_features])}
                </ul>
            </div>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)