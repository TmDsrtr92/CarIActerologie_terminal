# CarIActerologie Terminal

## Vue d'ensemble

Système de caractérologie intelligent utilisant l'IA et la recherche vectorielle pour analyser et répondre aux questions sur les traits de caractère basés sur le traité de caractérologie.

## Architecture du Système

### Structure des Composants

```
CarIActerologie_terminal/
├── app.py                          # Point d'entrée principal
├── agents.py                       # Système d'agents IA
├── tools/
│   └── vector_search.py           # Outil de recherche vectorielle
├── data/
│   └── source/
│       ├── traite_caracterologie.pdf
│       └── vector_stores/         # Base de données vectorielle ChromaDB
├── vector_store_creation.py       # Script de création de la base
└── requirements.txt               # Dépendances
```

### Composants Principaux

1. **Agents IA** (`agents.py`)
   - `caracteriologue_agent`: Expert en caractérologie avec accès à la base de connaissances
   - `psychologue_agent`: Expert en psychologie générale
   - `trieur_agent`: Agent de routage qui détermine quel expert utiliser

2. **Recherche Vectorielle** (`tools/vector_search.py`)
   - Fonction `search_caracterologie_knowledge()` pour interroger la base de connaissances
   - Interface avec ChromaDB et embeddings OpenAI

3. **Base de Données Vectorielle** (`data/source/vector_stores/`)
   - ChromaDB persistant
   - Chunks du traité de caractérologie avec embeddings `text-embedding-3-large`

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
```

### 3. Vector Search Process

```
Query: "caractérologie"
     ↓
OpenAI Embeddings: text-embedding-3-large
     ↓
ChromaDB: Similarity Search (k=5)
     ↓
Retrieved Documents: Top 5 chunks pertinents
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
2. **Routage intelligent** par le `trieur_agent`
3. **Sélection de l'agent expert** approprié
4. **Recherche vectorielle** si nécessaire :
   - Connexion à ChromaDB
   - Embedding de la query
   - Recherche par similarité
   - Récupération des chunks pertinents
5. **Génération de réponse** par l'agent expert
6. **Affichage formaté** dans le terminal

### Phase de Sortie
- Réponse contextuelle basée sur la base de connaissances
- Format lisible avec sources (pages) si applicable
- Boucle continue jusqu'à commande de sortie

## Configuration et Utilisation

### Installation
```bash
pip install -r requirements.txt
```

### Variables d'environnement
```env
OPENAI_API_KEY=your_openai_api_key
```

### Création de la base vectorielle
```bash
python vector_store_creation.py
```

### Lancement de l'application
```bash
python app.py
```

## Technologies Utilisées

- **LangChain** : Framework pour applications IA
- **ChromaDB** : Base de données vectorielle
- **OpenAI** : API pour embeddings (text-embedding-3-large) et LLM (gpt-4o-mini)
- **PyPDF** : Extraction de texte des documents PDF
- **Python asyncio** : Gestion asynchrone des agents

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