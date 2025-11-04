import streamlit as st
import re
import io
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Base de connaissances
FAITS = {
    "immigration": {
        "mythe": "Trop d'immigrés vont arriver !",
        "contre": "FAUX ! Les Bilat III renforcent 14 mesures de protection des salaires (contrôles, priorités aux Suisses). La libre circulation est équilibrée : 55 % de nos exportations dépendent de l'UE. Résultat : + emplois qualifiés, + croissance.",
        "avantage": "Accès au marché de 450 millions de consommateurs",
        "slogan": "OUI = Emplois + Innovation",
        "couleur": "#0066CC"
    },
    "soumission_ue": {
        "mythe": "On se soumet à Bruxelles !",
        "contre": "NON ! Pas d'EEE, pas de CJUE. Seulement 95 lois UE ciblées (sur 14 000), avec veto suisse et participation. On garde le contrôle total, comme en 2000 (67 % de OUI).",
        "avantage": "Sécurité juridique pour nos PME",
        "slogan": "Suisse forte, Europe ouverte",
        "couleur": "#FFCC00"
    },
    "salaires": {
        "mythe": "Les salaires vont baisser !",
        "contre": "ERREUR ! Les accords protègent les salaires avec des mesures 1G renforcées. Études fédérales : +0,5 % de PIB/an grâce à l'accès UE. Swissmem : 'Vital pour l'export'.",
        "avantage": "Compétitivité + Recherche (Horizon Europe)",
        "slogan": "OUI = Salaires protégés + Prospérité",
        "couleur": "#009933"
    },
    "couts": {
        "mythe": "C'est trop cher !",
        "contre": "Faux : ~40 CHF/habitant/an (vs 130 pour la Norvège). Retour : marchés ouverts, recherche, stabilité. 71 % des Suisses y voient plus d'avantages (gfs.bern 2024).",
        "avantage": "Investissement rentable pour notre avenir",
        "slogan": "OUI = Suisse gagnante",
        "couleur": "#CC0000"
    },
    "general": {
        "mythe": "Pourquoi voter OUI ?",
        "contre": "Parce que c'est du pragmatisme suisse : on négocie fort, on gagne des exceptions (asile, agriculture), on évite l'isolement. Sans ça : adieu Schengen, + barrières, - jobs.",
        "avantage": "Pour une Suisse prospère en Europe",
        "slogan": "OUI aux Bilatérales III !",
        "couleur": "#1E90FF"
    }
}

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

def generer_image(theme):
    faits = FAITS[theme]
    img = Image.new('RGB', (800, 600), color=faits["couleur"])
    draw = ImageDraw.Draw(img)
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        text_font = ImageFont.truetype("arial.ttf", 40)
        slogan_font = ImageFont.truetype("arial.ttf", 70)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        slogan_font = ImageFont.load_default()
    draw.text((50, 50), "MYTHE DÉTRUIT !", fill="white", font=title_font)
    lines = textwrap.wrap(faits["contre"], width=35)
    y = 150
    for line in lines:
        draw.text((50, y), line, fill="white", font=text_font)
        y += 50
    draw.text((50, y + 30), faits["avantage"], fill="white", font=text_font)
    y += 80
    draw.text((50, 450), faits["slogan"], fill="white", font=slogan_font)
    draw.text((500, 500), "🇨🇭🇪🇺", fill="white", font=slogan_font)
    draw.text((50, 550), "#VotezOuiBilatIII", fill="white", font=text_font)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

st.title("🤖 IA Pro-Bilatérales III : Convaincs-toi du OUI !")
st.write("Tape ton doute sur les Bilatérales III, je te contredis avec des faits + une affiche choc !")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], caption="Affiche de campagne")

if prompt := st.chat_input("Ton argument anti-Bilat III ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    theme = detecter_theme(prompt)
    faits = FAITS[theme]
    reponse = (
        f"⚠️ {faits['mythe']}\n\n"
        f"❌ FAUX ! {faits['contre']}\n\n"
        f"✅ {faits['avantage']}\n\n"
        f"🇨🇭 VOTEZ OUI AUX BILATÉRALES III !\n"
        f"💪 {faits['slogan']}\n"
        f"#VotezOuiBilatIII"
    )
    img_bytes = generer_image(theme)
    with st.chat_message("assistant"):
        st.markdown(reponse)
        st.image(img_bytes, caption="Affiche de campagne", use_column_width=True)
    st.session_state.messages.append({"role": "assistant", "content": reponse, "image": img_bytes})
