Voici le README complet pour ton projet `FIRND_BI`, intégrant toutes les sections et détails que nous avons discutés :

---

# FIRND_BI

## Description

`FIRND_BI` est une solution innovante conçue pour garantir la protection et la pérennité de vos diplômes et certificats professionnels. En luttant contre la falsification et la perte de ces documents, `FIRND_BI` vous assure qu'ils seront toujours disponibles, sécurisés et transparents. Grâce à sa plateforme, vous pouvez être certain que vos qualifications sont protégées pour l'avenir.

## Prérequis

- Python 3.12
- Django 5.1
- PostgreSQL
- `python-dotenv` pour la gestion des variables d'environnement

## Installation

Suivez ces étapes pour installer et configurer `FIRND_BI` localement :

1. **Cloner le dépôt :**

   ```bash
   git clone <URL-du-dépôt>
   cd FIRND_BI
   ```

2. **Créer un environnement virtuel :**

   ```bash
   python -m venv env
   source env/bin/activate  # Sur Windows : env\Scripts\activate
   ```

3. **Installer les dépendances :**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données et autres paramètres :**

   a. **Installer PostgreSQL :**
   
      Téléchargez et installez PostgreSQL depuis [le site officiel](https://www.postgresql.org/download/).

   b. **Créer une base de données PostgreSQL :**

      Créez une base de données pour votre application :

      ```bash
      sudo -u postgres createdb firnd_bi_db
      ```

   c. **Configurer `settings.py` :**

      Ouvrez `settings.py` et configurez les paramètres de la base de données pour utiliser PostgreSQL :

      ```python
      import os
      from dotenv import load_dotenv

      # Charger les variables d'environnement depuis le fichier .env
      load_dotenv()

      DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.postgresql',
              'NAME': os.getenv('DATABASE_NAME'),
              'USER': os.getenv('DATABASE_USER'),
              'PASSWORD': os.getenv('DATABASE_PASSWORD'),
              'HOST': os.getenv('DATABASE_HOST', 'localhost'),
              'PORT': os.getenv('DATABASE_PORT', '5432'),
          }
      }
      ```

   d. **Configurer les variables d'environnement :**

      Créez un fichier `.env` à la racine du projet avec le contenu suivant :

      ```
      DATABASE_NAME=firnd_bi_db
      DATABASE_USER=votre_utilisateur_postgres
      DATABASE_PASSWORD=votre_mot_de_passe
      DATABASE_HOST=localhost
      DATABASE_PORT=5432
      ```

      Assurez-vous que `.env` est ajouté à `.gitignore`.

   e. **Installer `python-dotenv` :**

      Ajoutez `python-dotenv` à `requirements.txt` si ce n'est pas déjà fait et installez-le :

      ```bash
      pip install python-dotenv
      ```

5. **Effectuer les migrations de la base de données :**

   ```bash
   python manage.py migrate
   ```

6. **Lancer le serveur de développement :**

   ```bash
   python manage.py runserver
   ```

7. **Accéder à l'application :**

   Ouvrez un navigateur web et accédez à `http://127.0.0.1:8000/` pour voir l'application en action.

## Utilisation

Voici un aperçu des principales fonctionnalités de l'application `FIRND_BI` et de la façon dont elles sont organisées :

### Authentification et Sécurité

- **Authentification par token :** Gestion des rôles, autorisations et activation des comptes utilisateurs sont gérés dans l'application `authentification`.
- **Mise en place d'un OTP (One-Time Password) :** Génération de codes OTP envoyés par e-mail ou SMS pour la vérification et la sécurité des utilisateurs.

### Gestion des Diplômes et Certificats

- **Utilisation d'OCR (Reconnaissance Optique de Caractères) :** Extraction de données textuelles à partir d’images ou de fichiers PDF.

### Traitement des Documents

- **Traitement des fichiers PDF :** Développement d’un endpoint pour récupérer un fichier PDF à partir d'une URL fournie, appliquer un filigrane au document et le retourner à l'utilisateur. Cette fonctionnalité est gérée dans l'application `documents`.
- **Signature et Vérification d'Authenticité :** Fonctionnalité pour signer les diplômes et vérifier leur authenticité afin de garantir qu'ils n'ont pas été altérés.

### Gestion des Utilisateurs

- **Gestion des utilisateurs, rôles, etc. :** Ces fonctionnalités sont gérées dans l'application `accounts`.
