import streamlit as st
import re

# === BASE DE CONNAISSANCES (faits sourcés) ===
FAITS = {
    "immigration": {
        "mythe": "Trop d'immigrés vont arriver !",
        "contre": "FAUX ! Les Bilat III renforcent **14 mesures de protection des salaires** (contrôles, priorités aux Suisses). La libre circulation est équilibrée : **55 % de nos exportations dépendent de l'UE**. Résultat : **+ emplois qualifiés, + croissance**.",
        "avantage": "Accès au marché de 450 millions de consommateurs",
        "slogan": "OUI = Emplois + Innovation"
    },
    "soumission_ue": {
        "mythe": "On se soumet à Bruxelles !",
        "contre": "NON ! **Pas d'EEE, pas de CJUE**. Seulement **95 lois UE ciblées** (sur 14 000), **avec veto suisse** et **participation**. On garde le contrôle total, comme en 2000 (**67 % de OUI**).",
        "avantage": "Sécurité juridique pour nos PME",
        "slogan": "Suisse forte, Europe ouverte"
    },
    "salaires": {
        "mythe": "Les salaires vont baisser !",
        "contre": "ERREUR ! Les accords protègent les salaires avec **mesures 1G renforcées**. Études fédérales : **+0,5 % de PIB/an** grâce à l'accès UE. Swissmem : *'Vital pour l'export'*. ",
        "avantage": "Compétitivité + Recherche (Horizon Europe)",
        "slogan": "OUI = Salaires protégés + Prospérité"
    },
    "couts": {
        "mythe": "C'est trop cher !",
        "contre": "Faux : **~40 CHF/habitant/an** (vs 130 pour la Norvège). Retour : marchés ouverts, recherche, stabilité. **71 % des Suisses y voient plus d'avantages** (gfs.bern 2024).",
        "avantage": "Investissement rentable pour notre avenir",
        "slogan": "OUI = Suisse gagnante"
    },
    "general": {
        "mythe": "Pourquoi voter OUI ?",
        "contre": "Parce que c'est du **pragmatisme suisse** : on négocie fort, on gagne des exceptions (asile, agriculture), on évite l'isolement. **Sans ça : adieu Schengen, + barrières, - jobs**.",
        "avantage": "Pour une Suisse prospère en Europe",
        "slogan": "OUI aux Bilatérales III !"
    }
}

# === DÉTECTION DU THÈME ===
def detecter_theme(message):
    message_lower = message.lower()
    if re.search(r'(immigr|frontier|libre circulation)', message_lower):
        return "immigration"
    elif re.search(r'(soumission|bruxelles|ue dict|perte souverain)', message_lower):
        return "soumission_ue"
    elif re.search(r'(salaire|travail|emploi)', message_lower):
        return "salaires"
    elif re.search(r'(coût|argent|contribution)', message_lower):
        return "couts"
    else:
        return "general"

# === INTERFACE STREAMLIT ===
st.title("IA Pro-Bilatérales III")
st.markdown("### *Tape ton doute, je te contredis avec des faits. Vote OUI !*")

# Historique du chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utilisateur
if prompt := st.chat_input("Ex: 'Les Bilatérales III ruinent la souveraineté !'"):
    # Ajouter message user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Générer réponse
    theme = detecter_theme(prompt)
    faits = FAITS[theme]
    
    reponse = (
        f"**{faits['mythe']}**\n\n"
        f"**FAUX !** {faits['contre']}\n\n"
        f"**{faits['avantage']}**\n\n"
        f"**VOTEZ OUI AUX BILATÉRALES III !**\n"
        f"**{faits['slogan']}**\n"
        f"#VotezOuiBilatIII"
    )

    # Afficher réponse IA
    with st.chat_message("assistant"):
        st.markdown(reponse)
    
    st.session_state.messages.append({"role": "assistant", "content": reponse})
