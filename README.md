# 📚 Anonydoc

**Anonydoc** est une application interactive développée avec **Streamlit** permettant de traiter des documents textuels
sensibles à l’aide de techniques avancées d’**anonymisation**, de **pseudonymisation**, et de **dépseudonymisation**.  
Elle s’appuie sur le modèle NLP **GLiNER** pour la détection des entités nommées.

---

## 🚀 Fonctionnalités

- 🕵️ **Anonymisation** : Remplacement des entités détectées (noms, lieux, etc.) par des étiquettes fixes définies par
  l'utilisateur.
- 🛡️ **Pseudonymisation** : Substitution des entités par des pseudonymes uniques et réversibles pour assurer la
  traçabilité.
- 🔄 **Dépseudonymisation** : Restauration des textes originaux à partir d’un texte pseudonymisé et d’un fichier de
  correspondance (mapping JSON).
- 📊 **Analyse et Visualisation** : Calcul de statistiques sur les entités détectées, génération de graphiques
  interactifs et consultation des contextes de remplacement.

---

## 📦 Structure du Projet

```
📦 anonydoc\_env
┣ 📂 .venv/                # Environnement virtuel Python
┣ 📂 config/               # Fichiers de configuration applicative
┣ 📂 logs/                 # Fichiers de logs de l'application
┣ 📂 tools/                # Code source principal
┃ ┣ 📂 entipy/             # Gestion des entités
┃ ┣ 📂 extractor/          # Extraction de contenu depuis divers formats de documents
┃ ┣ 📂 ui/                  # Interface utilisateur basée sur Streamlit
┃ ┣ 📄 **init**.py
┣ 📄 config\_loader.py      # Chargement des paramètres de configuration
┣ 📄 main.py                # Point d'entrée de l'application
┣ 📄 .gitignore             # Exclusions Git
┗ 📄 README.md              # Documentation du projet
```

---

## 🛠️ Installation

1. Cloner le dépôt :

```bash
git clone https://github.com/Florian-BARRE/Anonydoc.git
cd anonydoc
```

2. Créer et activer un environnement virtuel :

```bash
python -m venv .venv
source .venv/bin/activate   # Sous Windows : .venv\\Scripts\\activate
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. Lancer l’application :

```bash
streamlit run main.py
```

---

## 📖 Exemple d’Utilisation

1. Lancer l’application avec la commande `streamlit run main.py`.
2. Depuis l’interface, sélectionner le mode souhaité :

    * **Anonymisation** : Définir des règles de remplacement.
    * **Pseudonymisation** : Spécifier les entités à pseudonymiser.
    * **Dépseudonymisation** : Fournir un fichier de mapping pour restaurer le texte original.
3. Consulter les résultats, analyser les statistiques et télécharger les fichiers transformés.

## Auteur

Projet créé et maintenu par **Florian BARRE**.  
Pour toute question ou contribution, n'hésitez pas à me contacter.
[Mon Site](https://florianbarre.fr/) | [Mon LinkedIn](www.linkedin.com/in/barre-florian) | [Mon GitHub](https://github.com/Florian-BARRE)