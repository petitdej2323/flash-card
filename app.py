import streamlit as st
import json
from datetime import datetime
from fpdf import FPDF
import os

DATA_FILE = "flashcards.json"

def load_cards():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_cards(cards):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

def add_card(question, answer, category):
    cards = load_cards()
    cards.append({
        "question": question,
        "answer": answer,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d")
    })
    save_cards(cards)

def export_pdf(cards, filename="cartes_revision.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Cartes de Révision", ln=True, align="C")
    pdf.ln(10)
    for card in cards:
        pdf.multi_cell(0, 10, f"Catégorie : {card['category']}
Question : {card['question']}
Réponse : {card['answer']}
Date : {card['date']}")
        pdf.ln(5)
    pdf.output(filename)

st.title("🧠 Cartes de Révision TOEIC")

menu = st.sidebar.selectbox("Menu", ["Créer une carte", "Afficher les cartes", "Exporter en PDF"])

if menu == "Créer une carte":
    st.subheader("Créer une nouvelle carte")
    question = st.text_input("Question")
    answer = st.text_input("Réponse")
    category = st.text_input("Catégorie")
    if st.button("Ajouter la carte"):
        if question and answer and category:
            add_card(question, answer, category)
            st.success("Carte ajoutée avec succès.")
        else:
            st.warning("Veuillez remplir tous les champs.")

elif menu == "Afficher les cartes":
    st.subheader("Liste des cartes")
    cards = load_cards()
    if cards:
        for card in cards:
            st.markdown(f"**Catégorie :** {card['category']}")
            st.markdown(f"**Question :** {card['question']}")
            st.markdown(f"**Réponse :** {card['answer']}")
            st.markdown(f"**Date :** {card['date']}")
            st.markdown("---")
    else:
        st.info("Aucune carte enregistrée.")

elif menu == "Exporter en PDF":
    st.subheader("Exporter les cartes en PDF")
    cards = load_cards()
    if st.button("Exporter maintenant"):
        if cards:
            export_pdf(cards)
            with open("cartes_revision.pdf", "rb") as f:
                st.download_button("Télécharger le PDF", f, file_name="cartes_revision.pdf")
        else:
            st.warning("Aucune carte à exporter.")
