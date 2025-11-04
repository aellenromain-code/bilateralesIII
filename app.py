import streamlit as st
import re
import random

# === MÉGA BASE DE CONNAISSANCES : 100+ ARGUMENTS ANTI + 1000+ RÉPONSES ===
ARGUMENTS_ANTI = {
    "immigration": [
        "trop d'immigrés", "invasion", "frontières ouvertes", "libre circulation = chaos", "migrants partout",
        "on va être submergés", "plus de place", "étrangers prennent nos jobs", "immigration de masse",
        "pas de contrôle", "Schengen = danger", "asile abusé", "frontaliers ruinent salaires",
        "trop de permis B", "on n'arrive plus à loger tout le monde", "écoles surchargées", "hôpitaux pleins"
    ],
    "soumission_ue": [
        "soumission à Bruxelles", "perte de souveraineté", "on devient une province UE", "CJUE décide pour nous",
        "on perd notre démocratie directe", "référendum inutile", "Bruxelles nous impose tout", "pas d'EEE mais pire",
        "on signe sans lire", "dictature européenne", "Suisse vassale", "on perd notre neutralité",
        "on va payer des amendes", "on n'a plus le choix", "l'UE nous manipule", "on est des suiveurs"
    ],
    "salaires": [
        "salaires vont baisser", "dumping salarial", "travailleurs détachés", "concurrence déloyale",
        "patrons préfèrent embaucher pas cher", "fin des conventions collectives", "SMIC européen",
        "plus de protection", "jeunes sans formation", "chômage va exploser", "précarité généralisée",
        "on travaille plus pour moins", "inflation des loyers", "pouvoir d'achat en chute"
    ],
    "couts": [
        "coûte des milliards", "contribution trop chère", "on paie pour les autres", "argent jeté par les fenêtres",
        "Norvège paie moins", "on finance l'UE", "retour sur investissement nul", "impôts en hausse",
        "dette publique explose", "on donne sans rien recevoir", "40 CHF ? Mensonge !", "c'est 100 CHF en vrai"
    ],
    "general": [
        "c'est un piège", "on nous ment", "gouvernement vend la Suisse", "économie va s'effondrer",
        "PME en danger", "agriculture sacrifiée", "énergie plus chère", "recherche bloquée",
        "jeunes sans avenir", "vieux perdent leur rente", "Suisse isolée mais libre", "mieux vaut le non",
        "on a survécu sans", "bilatérales I/II suffisent", "c'est la fin de la Suisse", "vote populaire ignoré"
    ]
}

# === MÉGA RÉPONSES : 5 à 8 variantes par type d'argument ===
REPONSES_VARIANTS = {
    "immigration": [
        "FAUX ! Les Bilat III renforcent **14 mesures de protection** : contrôles, priorités aux Suisses, clauses de sauvegarde. La libre circulation = **accès à des compétences**, pas ouverture totale.",
        "ERREUR ! 55 % de nos exportations vont vers l’UE. Sans ça, **on perd des emplois suisses**, pas l’inverse. Les frontaliers ? Ils **paient des impôts en Suisse**.",
        "NON ! La Suisse garde **le contrôle total des flux**. Les permis B sont limités, les abus sanctionnés. C’est **l’innovation qui entre**, pas le chaos.",
        "Faux mythe ! Les études montrent : **+0,3 % de croissance par an** grâce à la main-d’œuvre qualifiée. Sans Bilat III, **c’est l’isolement qui submerge**.",
        "Absurde ! Schengen = **moins de criminalité transfrontalière** (statistiques fédérales). Les Bilat III = **sécurité + prospérité**."
    ],
    "soumission_ue": [
        "ABSOLUMENT PAS ! **Pas d’EEE, pas de CJUE**. Seulement **95 lois ciblées sur 14 000**, **avec veto suisse** et **participation**. C’est du **sur-mesure**.",
        "FAUX ! En 2000, **67 % de OUI** pour Bilat I. On a **gardé notre souveraineté** et gagné des marchés. Les Bilat III = **même recette, renforcée**.",
        "NON ! La Suisse **négocie en position de force** : exceptions asile, agriculture, neutralité. Bruxelles **ne décide pas pour nous**.",
        "Mythe ! On **ne signe rien sans référendum**. La démocratie directe reste **intacte**. Les Bilat III = **partenariat, pas soumission**.",
        "Faux ! L’UE a **besoin de la Suisse** (pharma, machines, finance). On est **partenaire stratégique**, pas vassal."
    ],
    "salaires": [
        "ERREUR ! Les Bilat III **renforcent les mesures d’accompagnement** : contrôles sur chantier, sanctions, salaires minimums. **Dumping = interdit**.",
        "FAUX ! Études fédérales : **+0,5 % de PIB/an** grâce à l’accès UE. Sans ça, **nos salaires baissent** à cause des barrières douanières.",
        "NON ! Swissmem : *'Vital pour l’emploi qualifié'*. Les Bilat III = **protection + croissance**. Les patrons suisses **embauchent local d’abord**.",
        "Mythe ! Les conventions collectives sont **renforcées**, pas affaiblies. Les Bilat III = **plus de jobs stables**, pas précarité.",
        "Faux ! Les frontaliers **paient impôts et cotisations en Suisse**. Ils **financent nos retraites**, pas l’inverse."
    ],
    "couts": [
        "Faux : **~40 CHF/habitant/an** (moins qu’un café/semaine). Norvège = 130 CHF. Retour : **marchés ouverts, recherche, stabilité**.",
        "NON ! On **investit**, pas on donne. 71 % des Suisses voient **plus d’avantages** (gfs.bern 2024). Sans ça, **-10 milliards d’export/an**.",
        "ERREUR ! Le coût est **x10 inférieur aux bénéfices**. Accès à **Horizon Europe, électricité, PME protégées**.",
        "Mythe ! Les contributions = **investissement rentable**. Sans Bilat III, **barrières douanières = +100 CHF par ménage** en produits chers.",
        "Faux ! L’argent reste **en Suisse** : fonds de cohésion pour nos régions, recherche, formation."
    ],
    "general": [
        "Les Bilat III = **pragmatisme suisse** : on négocie, on gagne, on protège. Sans ça ? **Isolement = perte d’emplois, d’innovation, de prospérité**.",
        "C’est **notre modèle gagnant depuis 25 ans**. On garde **le contrôle**, on ouvre **des portes**. Le OUI = **Suisse forte**.",
        "Pourquoi risquer l’inconnu ? Les Bilat III = **stabilité, croissance, souveraineté**. Tout ce que la Suisse fait de mieux.",
        "Faux ! Les PME **dépendent à 60 % de l’UE**. Sans Bilat III, **fermetures, licenciements, chute du franc**.",
        "Mythe ! L’agriculture est **protégée par des exceptions**. Les Bilat III = **sécurité alimentaire + export**."
    ]
}

# === AVANTAGES & SLOGANS ALÉATOIRES ===
AVANTAGES = [
    "Accès au marché de 450 millions de consommateurs",
    "Sécurité juridique pour nos PME",
    "Maintien de Schengen et Dublin",
    "Accès à Horizon Europe (recherche)",
    "Stabilité énergétique (accord électricité)",
    "1,2 million d’emplois liés à l’UE",
    "+0,5 % de croissance PIB/an",
    "Investissement rentable x10",
    "Suisse forte, Europe partenaire"
]

SLOGANS = [
    "OUI = Suisse forte en Europe",
    "OUI = Emplois + Innovation",
    "OUI = Souveraineté + Stabilité",
    "OUI = Protection + Prospérité",
    "OUI = Investissement gagnant",
    "OUI aux Bilatérales III !"
]

# === DÉTECTION FINE DU THÈME ===
def detecter_theme_et_argument(message):
    message_lower = message.lower()
    for theme, arguments in ARGUMENTS_ANTI.items():
        for arg in arguments:
            if arg in message_lower:
                return theme, arg
    # Sinon, thème général
    for theme in ["immigration", "soumission_ue", "salaires", "couts"]:
        if any(word in message_lower for word in theme.split("_")):
            return theme, message
    return "general", message

# === GÉNÉRER RÉPONSE MÉGA ===
def generer_reponse_mega(message):
    theme, argument_detecte = detecter_theme_et_argument(message)
    
    # Choisir réponse anti-mythe
    contre = random.choice(REPONSES_VARIANTS[theme])
    
    # Personnaliser légèrement
    if "souveraineté" in message.lower():
        contre = contre.replace("contrôle", "**pleine souveraineté**")
    if "salaires" in message.lower():
        contre = contre.replace("protection", "**garantie salariale**")
    
    avantage = random.choice(AVANTAGES)
    slogan = random.choice(SLOGANS)
    
    # Réponse finale
    reponse = (
        f"**Ton argument :** *\"{message.strip()}\"*\n\n"
        f"**FAUX !** {contre}\n\n"
        f"**En réalité :** {avantage}\n\n"
        f"**VOTE OUI AUX BILATÉRALES III !**\n"
        f"**{slogan}**\n"
        f"#VotezOuiBilatIII"
    )
    return reponse

# === INTERFACE STREAMLIT ===
st.title("IA Bilatérales III")
st.markdown("Donne moi ton argument contre les bilatérales III*")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ex: 'Les Bilatérales III = invasion d’immigrés !'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    reponse = generer_reponse_mega(prompt)

    with st.chat_message("assistant"):
        st.markdown(reponse)
    
    st.session_state.messages.append({"role": "assistant", "content": reponse})
