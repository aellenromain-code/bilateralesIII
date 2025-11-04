import streamlit as st
import re
import random

# === BASE DE CONNAISSANCES : 5 thèmes, plusieurs variantes par thème ===
REPONSES = {
    "immigration": {
        "mythes": [
            "immigr", "frontier", "libre circulation", "trop d’étrangers", "invasion", "migrants"
        ],
        "contre": [
            "FAUX ! Les Bilat III renforcent **14 mesures de protection des salaires** : contrôles accrus, priorité aux Suisses, clauses de sauvegarde. La libre circulation n’est pas un robinet ouvert : elle est **équilibrée et contrôlée**.",
            "ERREUR ! On ne parle pas d’ouverture totale. La Suisse garde **le contrôle total des flux** grâce aux mesures d’accompagnement renforcées. 55 % de nos exportations vont vers l’UE : sans ça, on perd des emplois suisses.",
            "NON ! Ce n’t pas une immigration de masse. C’est **l’accès à des compétences qualifiées** dont nos entreprises ont besoin. Résultat : + innovation, + croissance, + emplois stables."
        ],
        "avantages": [
            "Accès au marché de 450 millions de consommateurs",
            "Renforcement de l’innovation et de la compétitivité suisse",
            "Stabilité économique : 1,2 million d’emplois liés à l’UE"
        ],
        "slogans": [
            "OUI = Emplois + Innovation",
            "OUI = Suisse forte, marché ouvert",
            "OUI = Contrôle + Prospérité"
        ]
    },
    "soumission_ue": {
        "mythes": [
            "soumission", "bruxelles", "ue dict", "perte souverain", "cjue", "eee", "on perd le contrôle"
        ],
        "contre": [
            "ABSOLUMENT PAS ! Pas d’EEE, pas de CJUE, pas de soumission automatique. On reprend **seulement 95 lois ciblées** (sur 14 000 !), **avec veto suisse** et **participation aux décisions**.",
            "FAUX ! C’est du **sur-mesure helvétique**. On garde **notre souveraineté totale** : pas d’institutions supranationales, pas de juge étranger. Comme en 2000 : **67 % de OUI** pour les Bilat I.",
            "NON ! La Suisse n’est pas un vassal. Elle **négocie en position de force**, obtient des exceptions (asile, agriculture), et **décide elle-même** ce qu’elle accepte."
        ],
        "avantages": [
            "Sécurité juridique pour nos PME et industries",
            "Maintien de Schengen et Dublin",
            "Accès à Horizon Europe pour la recherche"
        ],
        "slogans": [
            "Suisse forte, Europe ouverte",
            "OUI = Souveraineté + Stabilité",
            "OUI = Contrôle total, partenariat gagnant"
        ]
    },
    "salaires": {
        "mythes": [
            "salaire", "travail", "emploi", "baisse", "dumping", "concurrence déloyale"
        ],
        "contre": [
            "ERREUR ! Les Bilat III **protègent mieux les salaires suisses** avec des **mesures 1G renforcées** : contrôles sur place, sanctions, priorités locales.",
            "FAUX ! Des études fédérales montrent : **+0,5 % de PIB par an** grâce à l’accès au marché UE. Sans ça, ce sont **nos salaires qui baisseraient** à cause des barrières douanières.",
            "NON ! Les entreprises suisses ont besoin de l’UE pour exporter. Swissmem le dit : *'Vital pour l’emploi qualifié'*. Les Bilat III = **protection + croissance**."
        ],
        "avantages": [
            "Compétitivité renforcée",
            "Accès à la recherche (Horizon Europe)",
            "Croissance économique = + salaires réels"
        ],
        "slogans": [
            "OUI = Salaires protégés + Prospérité",
            "OUI = Emplois suisses + Innovation",
            "OUI = Protection + Croissance"
        ]
    },
    "couts": {
        "mythes": [
            "coût", "argent", "contribution", "trop cher", "milliards", "on paie pour l’ue"
        ],
        "contre": [
            "Faux : **~40 CHF par habitant et par an** (moins qu’un café par semaine). La Norvège paie 130 CHF. C’est un **investissement rentable** : retours via marchés, recherche, stabilité.",
            "NON ! On ne donne pas, on **investit**. 71 % des Suisses voient **plus d’avantages que d’inconvénients** (gfs.bern 2024). Sans ça, on perd **des milliards en export**.",
            "ERREUR ! Le coût est minime comparé aux bénéfices : **accès à 55 % de notre marché d’export**, **sécurité énergétique**, **recherche financée**."
        ],
        "avantages": [
            "Investissement rentable pour l’avenir",
            "Stabilité de la voie bilatérale",
            "Retour économique x10"
        ],
        "slogans": [
            "OUI = Suisse gagnante",
            "OUI = 40 CHF pour des milliards de retour",
            "OUI = Investissement intelligent"
        ]
    },
    "general": {
        "mythes": [],
        "contre": [
            "Les Bilatérales III, c’est du **pragmatisme suisse pur** : on négocie fort, on gagne des exceptions, on protège nos intérêts. Sans ça ? Isolement, barrières, perte d’emplois.",
            "C’est **notre modèle gagnant depuis 25 ans**. On garde le contrôle, on ouvre des portes, on protège nos citoyens. Le OUI, c’est la Suisse qui gagne.",
            "Pourquoi risquer l’isolement ? Les Bilat III = **stabilité, prospérité, souveraineté**. Tout ce que la Suisse fait de mieux."
        ],
        "avantages": [
            "Pour une Suisse prospère en Europe",
            "Maintien de notre succès économique",
            "Modèle bilatéral renforcé"
        ],
        "slogans": [
            "OUI aux Bilatérales III !",
            "OUI = Suisse forte en Europe",
            "OUI = Pragmatisme + Prospérité"
        ]
    }
}

# === DÉTECTION DU THÈME ===
def detecter_theme(message):
    message_lower = message.lower()
    for theme, data in REPONSES.items():
        if theme == "general":
            continue
        for mot in data["mythes"]:
            if mot in message_lower:
                return theme
    return "general"

# === GÉNÉRER RÉPONSE PERSONNALISÉE ===
def generer_reponse_personnalisee(message, theme):
    data = REPONSES[theme]
    
    # Choisir une variante aléatoire
    contre = random.choice(data["contre"])
    avantage = random.choice(data["avantages"])
    slogan = random.choice(data["slogans"])
    
    # Personnaliser avec l'argument de l'utilisateur
    if "souveraineté" in message.lower():
        contre = contre.replace("souveraineté totale", "**souveraineté pleine et entière**")
    if "salaires" in message.lower():
        contre = contre.replace("protègent", "**garantissent**")
    
    # Réponse finale
    reponse = (
        f"**Ton doute :** *\"{message.strip()}\"*\n\n"
        f"**FAUX !** {contre}\n\n"
        f"**En réalité :** {avantage}\n\n"
        f"**VOTE OUI AUX BILATÉRALES III !**\n"
        f"**{slogan}**\n"
        f"#VotezOuiBilatIII"
    )
    return reponse

# === INTERFACE STREAMLIT ===
st.title("IA Pro-Bilat III – Réponses 100% Personnalisées")
st.markdown("### Tape ton doute → ")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input utilisateur
if prompt := st.chat_input("Ex: 'Les Bilatérales III vont ruiner notre souveraineté !'"):
    # Ajouter message user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Générer réponse personnalisée
    theme = detecter_theme(prompt)
    reponse = generer_reponse_personnalisee(prompt, theme)

    # Afficher réponse IA
    with st.chat_message("assistant"):
        st.markdown(reponse)
    
    st.session_state.messages.append({"role": "assistant", "content": reponse})
