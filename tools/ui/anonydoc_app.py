# ====== Code Summary ======
# This script defines the AnonyDocApp class, which provides a Streamlit-based user interface for document
# anonymization, pseudonymization, and depseudonymization. It utilizes a text entity processor to identify
# and transform sensitive information based on user-defined rules or automatic entity detection.
# The app supports uploading various document types, visualizes the results, and allows downloading processed outputs.

# ====== Standard Library Imports ======
import os
import json
import tempfile

# ====== Third-Party Library Imports ======
import streamlit as st
import pandas as pd

# ====== Internal Project Imports ======
from config_loader import CONFIG
from entipy import TextEntityProcessor
from extractor import ExtractorFactory

# ====== Streamlit App Configuration ======
st.set_page_config(
    page_title="Anonydoc",
    layout="wide",
    initial_sidebar_state="expanded",

)


# ===== AnonyDocApp Class ======
class AnonyDocApp:
    """
    AnonyDoc Streamlit Application for document anonymization, pseudonymization, and depseudonymization.

    Attributes:
        processor (TextEntityProcessor): The text entity processor used for transformations.
        mode (str): Current operation mode selected by the user.
    """

    def __init__(self, text_entity_processor: TextEntityProcessor):
        """Initializes the app, configures the UI, and sets up session state."""
        self.processor = text_entity_processor
        self.mode = st.sidebar.selectbox(
            "Mode", ["Accueil", "Anonymisation", "Pseudonymisation", "Dépseudonymisation"],
            key="mode_selector"
        )
        self.init_session_state()

    def init_session_state(self):
        """Initializes or resets session state variables based on selected mode."""
        if 'last_mode' not in st.session_state or st.session_state['last_mode'] != self.mode:
            st.session_state['anonymization_result'] = None
            st.session_state['pseudonymization_result'] = None
            st.session_state['last_mode'] = self.mode

        if self.mode == "Anonymisation" and 'label_mapping_entries' not in st.session_state:
            st.session_state['label_mapping_entries'] = [("", "")]

        if self.mode == "Pseudonymisation" and 'custom_entities_entries' not in st.session_state:
            st.session_state['custom_entities_entries'] = [""]

    def run(self):
        """Main entry point to render the appropriate UI and handle actions based on selected mode."""
        mode_dispatch = {
            "Accueil": self.show_home,
            "Anonymisation": self.show_anonymisation,
            "Pseudonymisation": self.show_pseudonymisation,
            "Dépseudonymisation": self.show_depseudonymisation
        }

        mode_dispatch.get(self.mode, self.show_home)()

        if self.mode in ["Anonymisation", "Pseudonymisation"]:
            self.handle_processing()

    @staticmethod
    def show_home():
        """Displays the home page with app information."""
        st.markdown("""
        # 🔐 Anonydoc
        ### Outils d'anonymisation et de pseudonymisation de documents
        Anonydoc est un outil destiné aux métiers pour :
        - 🕵️ **Anonymisation** : remplacer des informations sensibles (noms, lieux…) par des étiquettes fixes.
        - 🔑 **Pseudonymisation** : générer des pseudonymes uniques tout en préservant la traçabilité.
        - 🔄 **Dépseudonymisation** : restaurer le texte original à partir du texte pseudonymisé et du fichier de mapping.

        Utilisez le menu de gauche pour choisir votre action.
        """, unsafe_allow_html=True)
        st.stop()

    @staticmethod
    def show_anonymisation():
        """Displays the anonymization UI and mapping entry controls."""
        st.header("🔒 Anonymisation")
        st.markdown(
            "> 💡 **Conseil** : un terme générique (mot-valise) comme « Personne » couvre tous les noms (Mathieu, Antoine…)."
        )
        to_remove = []
        for idx, (key, val) in enumerate(st.session_state['label_mapping_entries']):
            c1, c2, c3 = st.columns([4, 3, 1])
            new_key = c1.text_input("📝 Texte à remplacer", value=key, key=f"am_key_{idx}")
            new_val = c2.text_input("🏷️ Étiquette", value=val, key=f"am_val_{idx}")
            if c3.button("❌", key=f"am_del_{idx}"):
                to_remove.append(idx)
            st.session_state['label_mapping_entries'][idx] = (new_key, new_val)
        for idx in reversed(to_remove):
            st.session_state['label_mapping_entries'].pop(idx)
        if st.button("➕ Ajouter une règle"):
            st.session_state['label_mapping_entries'].append(("", ""))

    @staticmethod
    def show_pseudonymisation():
        """Displays the pseudonymization UI and custom entity controls."""
        st.header("🛡️ Pseudonymisation")
        st.markdown(
            "> 💡 **Note** : chaque entité listée recevra un pseudonyme unique (e.g. Personne_1, Personne_2)."
        )
        to_remove = []
        for idx, ent in enumerate(st.session_state['custom_entities_entries']):
            c1, c2 = st.columns([8, 1])
            new_ent = c1.text_input("📝 Entité à pseudonymiser", value=ent, key=f"ps_ent_{idx}")
            if c2.button("❌", key=f"ps_del_{idx}"):
                to_remove.append(idx)
            st.session_state['custom_entities_entries'][idx] = new_ent
        for idx in reversed(to_remove):
            st.session_state['custom_entities_entries'].pop(idx)
        if st.button("➕ Ajouter une entité"):
            st.session_state['custom_entities_entries'].append("")

    @staticmethod
    def show_depseudonymisation():
        """Displays the depseudonymization interface allowing file upload and text restoration."""
        st.header("🔄 Dépseudonymisation")
        st.markdown(
            "> 💡 Importez le texte pseudonymisé et le fichier JSON de mapping pour restaurer le texte."
        )
        f_text = st.file_uploader("📄 Texte pseudonymisé", type=["txt"])
        f_map = st.file_uploader("📁 Mapping JSON", type=["json"])
        if f_text and f_map:
            content = f_text.read().decode('utf-8')
            mapping = json.load(f_map)
            for pseudo, orig in mapping.items():
                content = content.replace(pseudo, orig)

            st.subheader("✅ Texte restauré")
            st.text_area("Texte original", content, height=300)

            tmpf = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")
            tmpf.write(content)
            tmpf.close()
            with open(tmpf.name, 'rb') as f:
                st.download_button("📥 Télécharger le texte restauré", data=f, file_name="texte_restaure.txt")
        st.stop()

    def handle_processing(self):
        """Handles document upload, content extraction, and triggers entity processing."""
        uploaded = st.file_uploader("📁 Importer un document (txt, pdf, docx, xlsx)")
        content = None

        if uploaded:
            ext = os.path.splitext(uploaded.name)[1]
            tmpf = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
            tmpf.write(uploaded.read())
            tmpf.close()

            try:
                content = ExtractorFactory.auto_extract(tmpf.name)
                st.subheader("📖 Contenu extrait")
                st.text_area("", content, height=200)
            except Exception as e:
                st.error(f"❌ Erreur d'extraction : {e}")

        result_key = 'anonymization_result' if self.mode == 'Anonymisation' else 'pseudonymization_result'
        if content and st.button("🚀 Traiter"):
            mapping = self.build_mapping()
            if self.mode == 'Anonymisation':
                st.session_state[result_key] = self.processor.anonymize(content, mapping)
            else:
                st.session_state[result_key] = self.processor.pseudonymize(content, mapping)

        self.display_results(st.session_state.get(result_key))

    def build_mapping(self):
        """Builds the entity mapping based on the current mode and user input."""
        if self.mode == 'Anonymisation':
            return {k: v for k, v in st.session_state['label_mapping_entries'] if k and v}
        return [e for e in st.session_state['custom_entities_entries'] if e]

    def display_results(self, res):
        """Displays processed results including statistics, mappings, and downloadable files."""
        if not res:
            return

        st.subheader("🎯 Résultat")
        st.text_area("", res.processed_text, height=300)

        st.subheader("📊 Statistiques")
        labels = list(self.build_mapping().keys()) if self.mode == 'Anonymisation' else self.build_mapping()
        stats = res.get_stats(labels)
        st.metric("🔢 Entités détectées", stats['entity_count'])
        st.metric("📈 Densité (%)", f"{stats['density'] * 100:.1f}")

        if stats['label_distribution']:
            df = pd.DataFrame({'count': stats['label_distribution'].values()},
                              index=stats['label_distribution'].keys())
            st.bar_chart(df)

        st.subheader("🗺️ Mappings" if self.mode == 'Anonymisation' else "🧬 Pseudonymes")
        if self.mode == 'Anonymisation':
            st.json(res.replacement_map())
        else:
            dfm = pd.DataFrame(res.pseudonym_table.items(), columns=["Original", "Pseudonyme"])
            st.dataframe(dfm)
            data = json.dumps(res.pseudonym_table, ensure_ascii=False).encode('utf-8')
            st.download_button("📥 Télécharger le mapping", data=data, file_name="mapping.json", mime="application/json")

        st.subheader("🔍 Contexte")
        for sn in res.contexts:
            ent = sn.entity
            if ent.label not in (
                    list(self.build_mapping().keys()) if self.mode == 'Anonymisation' else self.build_mapping()):
                continue
            with st.expander(
                    f"🔖 {ent.text} → {ent.replacement_text} ({ent.label}, confiance: {ent.detection_confidence:.2f})"):
                st.markdown(
                    f"Mots {ent.word_position.start}–{ent.word_position.end}, Caractères {ent.char_position.start}–{ent.char_position.end}")
                st.markdown(f"... {sn.left} <mark>{ent.text}</mark> {sn.right} ...", unsafe_allow_html=True)

        tmpf = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")
        tmpf.write(res.processed_text)
        tmpf.close()
        with open(tmpf.name, 'rb') as f:
            filename = "texte_anonyme.txt" if self.mode == 'Anonymisation' else "texte_pseudo.txt"
            st.download_button("📥 Télécharger le texte transformé", data=f, file_name=filename)
