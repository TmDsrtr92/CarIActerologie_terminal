# CarIActerologie Terminal 🧠✨

## Vue d'ensemble

Système de caractérologie intelligent avec **interface Rich** utilisant l'IA et la recherche vectorielle pour analyser et répondre aux questions sur les traits de caractère basés sur le traité de caractérologie.

## 🎨 Interface Utilisateur

### Interface Rich Terminal
- **Interface colorée et interactive** avec Rich Python
- **Panneaux formatés** avec bordures et styles personnalisés
- **Agent branding** : chaque agent a sa couleur et son emoji
- **Commandes interactives** : help, clear, agents, quit
- **Indicateurs visuels** : spinners et messages de statut
- **Formatage Markdown** pour les réponses

### 👤 Configuration Utilisateur
- **ID utilisateur personnalisable** : Choix de l'identifiant au démarrage
- **Support multi-format** : Accepte nombres et texte (ex: "123" ou "john_doe")
- **Valeur par défaut** : Nombre aléatoire proposé automatiquement
- **Confirmation visuelle** : Affichage de l'ID sélectionné avec validation

### 🧠 Gestion de la Mémoire Conversationnelle

#### 📝 Architecture Mémoire Duale
Le système implémente deux niveaux de mémoire complémentaires :

**🔄 Mémoire Court Terme (Session)**
- **Méthode** : `to_input_list()` pour maintenir l'historique conversationnel
- **Portée** : Limitée à la session courante
- **Données** : Échanges utilisateur/agent dans l'ordre chronologique
- **Reset** : Effacée à la fermeture de l'application
- **Usage** : Contexte immédiat pour les agents

**💾 Mémoire Long Terme (Persistante)**
- **Méthode** : Outils `save_memory` et `search_memory` via Mem0
- **Portée** : Persistante entre sessions via user_id
- **Données** : Informations importantes sur l'utilisateur et ses caractéristiques
- **Reset** : Conservée indéfiniment, liée à l'identifiant utilisateur
- **Usage** : Profil utilisateur et apprentissage personnalisé

#### 🔄 Implémentation Technique (app.py)
**Mémoire Court Terme :**
- **Initialisation** : `convo: list[TResponseInputItem] = []` (ligne 84)
- **Ajout input utilisateur** : `convo.append({"content": user_input, "role": "user"})` (ligne 93)
- **Debug historique** : `print("Historique de conversation: ", convo)` (ligne 94)
- **Transmission aux agents** : `result = await Runner.run(last_agent, convo)` (ligne 120)
- **Mise à jour post-réponse** : `convo = result.to_input_list()` (ligne 150)
- **Persistance agent** : `last_agent = result.last_agent` pour continuité inter-tours

**Mémoire Long Terme :**
- **Sauvegarde** : Les agents utilisent `save_memory(content, user_id)` pour enregistrer des informations importantes
- **Récupération** : Les agents utilisent `search_memory(query, user_id)` pour accéder aux souvenirs passés
- **Liaison utilisateur** : Toutes les mémoires sont liées au `user_id` configuré au démarrage
- **Continuité** : L'utilisateur retrouve ses informations en utilisant le même identifiant

## Architecture du Système

### Structure des Composants

```
CarIActerologie_terminal/
├── app.py                          # Point d'entrée principal (minimal)
├── agent_config.py                 # Configuration et création des agents
├── agent/                          # Dossier des agents spécialisés
│   ├── trieur.py                   # Agent de routage intelligent
│   ├── caracteriologue.py          # Expert en caractérologie
│   ├── interrogateur.py            # Spécialiste questionnaire
│   └── profiler.py                 # Générateur de profils
├── ui.py                          # Interface utilisateur Rich
├── tools/
│   └── vector_search.py           # Outil de recherche vectorielle
├── data/
│   └── source/
│       ├── traite_caracterologie.pdf
│       └── vector_stores/         # Base de données vectorielle ChromaDB
├── vector_store_creation.py       # Script de création de la base
└── requirements.txt               # Dépendances
```

### 🏗️ Architecture Modulaire

**Séparation des responsabilités :**

1. **`app.py`** - Point d'entrée minimaliste
   - Gestion de la boucle conversationnelle principale
   - Orchestration des agents et de l'interface
   - ~100 lignes de code clean

2. **`agent_config.py`** - Configuration et création des agents
   - **Architecture modulaire** : Import des agents depuis le dossier `agent/`
   - **Fonction centralisée** : `create_agents()` crée tous les agents et configure les handoffs
   - **Gestion des handoffs** : Configuration des transferts entre agents
   - **Agent retrieval** : Fonction `get_agent_by_name()` pour récupération d'agent

3. **Dossier `agent/`** - Agents spécialisés modulaires
   - **`trieur.py`** : Agent de routage avec logique de redirection
   - **`caracteriologue.py`** : Expert en caractérologie avec recherche vectorielle
   - **`interrogateur.py`** : Questionnaire en 3 étapes (Activité, Émotivité, Retentissement)
   - **`profiler.py`** : Générateur de profils caractérologiques
   - **Architecture propre** : Chaque agent dans son propre fichier avec fonction `create_*_agent()`
   - **Instructions structurées** : Rôle, méthodologie, style définis par agent
   - **Séparation claire** : Instructions et logique métier isolées par responsabilité

4. **`ui.py`** - Interface utilisateur Rich
   - Toutes les fonctions d'affichage
   - Formatage et stylisme
   - Panneaux, tableaux, headers

### 🤖 Agents IA Spécialisés (Architecture Modulaire)

Chaque agent est maintenant dans son propre fichier dans le dossier `agent/`:

1. **🧑‍🔬 Caractériologue** (`agent/caracteriologue.py`)
   - **Rôle** : Expert en analyse et théorie de la caractérologie
   - **Outils** : Recherche vectorielle dans le traité de caractérologie
   - **Capacités** : Analyse détaillée, identification des 8 types de caractères
   - **Modèle** : `gpt-4.1-mini`
   - **Méthodologie** : Pédagogique et scientifique
   - **Fonction** : `create_caracteriologue_agent()`

2. **❓ Interrogateur** (`agent/interrogateur.py`)
   - **Rôle** : Évaluation personnalisée par questionnaire en 3 étapes
   - **Processus** : Activité → Émotivité → Retentissement
   - **Questions clés** : Obstacles, émotions, poids du passé
   - **Modèle** : `gpt-4.1-mini`
   - **Handoff** : Transfère vers Caractériologue pour analyse finale
   - **Fonction** : `create_interrogateur_agent()`

3. **🎯 Trieur** (`agent/trieur.py`)
   - **Rôle** : Agent de routage intelligent
   - **Logique** : Questions théoriques → Caractériologue, Évaluation → Interrogateur
   - **Style** : Concis et orienté solution
   - **Modèle** : `gpt-4o-mini`
   - **Fonction** : `create_trieur_agent()`

4. **📊 Profiler** (`agent/profiler.py`)
   - **Rôle** : Générateur de profils caractérologiques structurés
   - **Output** : Profil UserProfile avec émotivité, activité, retentissement
   - **Analyse** : Basée sur l'historique de conversation
   - **Modèle** : `gpt-4o-mini`
   - **Fonction** : `create_profiler_agent()`

### 🔍 Recherche Vectorielle (`tools/vector_search.py`)
- **Fonction `search_caracterologie_knowledge()`** : Interrogation de la base de connaissances du traité de caractérologie
- **Fonction `search_timidite_knowledge()`** : Recherche dans la base de connaissances sur la timidité
- **Interface unifiée** avec ChromaDB et embeddings OpenAI
- **Collections multiples** : Support de plusieurs bases de connaissances spécialisées

### 💾 Base de Données Vectorielle (`data/source/vector_stores/`)
- **ChromaDB persistant** avec collections multiples :
  - **`traite_de_caracterologie_large_v1`** : Traité de caractérologie complet
  - **`la_timidite_v3`** : Base de connaissances spécialisée sur la timidité
- **Embeddings** : `text-embedding-3-large` pour toutes les collections
- **Architecture modulaire** : Chaque collection accessible via son propre outil de recherche

## Workflow Global

### 1. User Input → Agent Routing

```
User Input: "Qu'est-ce que la caractérologie ?"
     ↓
Trieur Agent: Analyse la question
     ↓
Routing Decision: → Caractériologue Agent
```

### 2. Agent Processing → Tool Usage

```
Caractériologue Agent
     ↓
Décision: Utiliser l'outil de recherche
     ↓
search_caracterologie_knowledge("caractérologie")
ou
search_timidite_knowledge("timidité")
```

### 3. Vector Search Process

```
Query: "caractérologie" ou "timidité"
     ↓
OpenAI Embeddings: text-embedding-3-large
     ↓
ChromaDB: Similarity Search dans la collection appropriée (k=5)
     ↓
Retrieved Documents: Top 5 chunks pertinents de la base spécialisée
```

### 4. Response Generation

```
Retrieved Chunks + Query
     ↓
Caractériologue Agent: Synthèse avec GPT-4o-mini
     ↓
Formatted Response: Réponse contextuelle en français
     ↓
Terminal Output: Affichage à l'utilisateur
```

## Flux de Données Détaillé

### Phase d'Initialisation
1. **Chargement des variables d'environnement** (OpenAI API Key)
2. **Initialisation des agents** avec leurs instructions spécifiques
3. **Démarrage de la boucle interactive** terminal

### Phase de Traitement
1. **Capture input utilisateur** via terminal
2. **Ajout à l'historique** : `convo.append({"content": user_input, "role": "user"})`
3. **Continuation intelligente** : Utilisation de `last_agent` pour maintenir la continuité
4. **Workflow des agents** :
   - **Trieur** → Analyse la demande et route vers l'expert approprié
   - **Interrogateur** → Pose 3 questions (Activité, Émotivité, Retentissement) puis transfère vers Caractériologue
   - **Caractériologue** → Analyse finale et identification du type de caractère
5. **Recherche vectorielle** (Caractériologue uniquement) :
   - Connexion à ChromaDB
   - Embedding de la query avec contexte
   - Recherche par similarité dans le traité
   - Récupération des chunks pertinents
6. **Génération de réponse** par l'agent expert avec mémoire
7. **Mise à jour complète** :
   - `convo = result.to_input_list()` (historique complet)
   - `last_agent = result.last_agent` (agent actuel après handoff)
8. **Affichage formaté** avec couleurs spécifiques par agent

### Phase de Sortie
- **Réponse contextuelle** basée sur la base de connaissances ET l'historique
- **Format lisible** avec sources (pages) si applicable
- **Persistance mémoire** : L'historique complet est conservé pour les prochains échanges
- **Boucle continue** jusqu'à commande de sortie

## 🚀 Configuration et Utilisation

### Prérequis
- Python 3.8+
- Clé API OpenAI
- Terminal avec support des couleurs
- Environnement virtuel recommandé

### 💡 Guide d'Usage Rapide

**Pour une évaluation personnelle :**
- "Quel est mon caractère ?" → Déclenche le processus d'évaluation en 3 questions
- "Peux-tu m'évaluer ?" → L'Interrogateur vous guide dans le questionnaire
- "Je veux connaître ma personnalité" → Workflow complet d'évaluation

**Pour des questions théoriques :**
- "Qu'est-ce que la caractérologie ?" → Le Caractériologue explique la théorie
- "Quels sont les 8 types de caractères ?" → Accès à la base de connaissances
- "Explique-moi le type colérique" → Analyse détaillée d'un type spécifique

### Installation
```bash
# Cloner le projet
git clone <repository-url>
cd CarIActerologie_terminal

# Créer un environnement virtuel (recommandé)
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou source .venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt
```

### Variables d'environnement
Créer un fichier `.env` :
```env
OPENAI_API_KEY=your_openai_api_key
```

### Création de la base vectorielle
```bash
python vector_store_creation.py
```

### 🎯 Lancement de l'application
```bash
python app.py
```

## 📝 Commandes Disponibles

Une fois l'application lancée, vous disposez de ces commandes :

| Commande | Description | Exemple |
|----------|-------------|---------|
| `quit` / `exit` / `q` | Quitter l'application | `quit` |
| `clear` | Effacer l'écran et réafficher l'en-tête | `clear` |
| `help` | Afficher le guide d'utilisation | `help` |
| `agents` | Voir les agents disponibles | `agents` |

## 🎨 Fonctionnalités Interface

### Éléments Visuels
- **🧠 En-tête stylisé** avec gradient de couleurs
- **📋 Tableau des commandes** avec exemples
- **🌳 Arbre des agents** avec descriptions
- **💬 Compteur de conversations** pour le suivi
- **🔄 Indicateurs de traitement** avec animations

### Gestion des Erreurs et Debugging
- **Panneaux d'erreur colorés** avec conseils et solutions
- **Gestion des interruptions** (Ctrl+C) gracieuse avec message personnalisé
- **Messages d'aide contextuels** intégrés
- **Debug logging** : Messages détaillés pour diagnostic
- **Error handling robuste** : Capture et affichage user-friendly des exceptions
- **Fallbacks intelligents** : `get_agent_by_name()` avec agent par défaut
- **Validation des types** : Vérification des objets Agent vs strings

## 🛠️ Technologies Utilisées

- **Rich** : Interface terminal avancée avec couleurs et formatage
- **LangChain** : Framework pour applications IA
- **ChromaDB** : Base de données vectorielle
- **OpenAI** : API pour embeddings (text-embedding-3-large) et LLM (gpt-4o-mini)
- **PyPDF** : Extraction de texte des documents PDF
- **Python asyncio** : Gestion asynchrone des agents
- **openai-agents** : Système d'agents IA modulaires

## Monitoring et Debugging

### Heartbeat Monitoring
- Surveillance de la connexion ChromaDB pendant la création de la base
- Vérification périodique de l'état du serveur

### Logging
- Affichage du statut des opérations vectorielles
- Messages d'erreur détaillés
- Compteurs de chunks traités

## Architecture de Recherche

### Embeddings
- **Modèle**: `text-embedding-3-large` (3072 dimensions)
- **Chunks**: Texte découpé avec `RecursiveCharacterTextSplitter`
- **Taille**: 2171 caractères par chunk, pas de chevauchement

### Recherche
- **Méthode**: Similarité cosine dans l'espace vectoriel
- **Nombre de résultats**: Configurable (défaut: 5)
- **Métadonnées**: Page source, contenu truncated à 200 caractères

Cette architecture permet une recherche sémantique efficace dans le corpus de caractérologie tout en maintenant une interface conversationnelle naturelle.