# HelpMe! 🤝

Una web application (SPA) per l'aiuto reciproco tra persone. Gli utenti pubblicano problemi e ricevono suggerimenti da altri utenti esperti in vari ambiti.

## Funzionalità

- **Utenti non registrati**: Consultano post e commenti
- **Utenti registrati**: Creano/modificano/rimuovono/chiudono post, commentano, votano, si iscrivono alle categorie
- **Amministratori**: Gestiscono categorie, moderano contenuti, bannano utenti

### Caratteristiche principali

- Post multi-categoria con titolo, descrizione e media
- Commenti con thread (risposte ai commenti)
- Sistema di voti (upvote/downvote)
- Sistema di esperti per categoria (basato sul punteggio)
- Notifiche per nuovi post nelle categorie seguite
- Chiusura post con soluzione evidenziata
- Pannello amministrazione

## Stack Tecnologico

- **Frontend**: HTML, CSS, JavaScript (SPA)
- **Backend**: Python Flask (REST API)
- **Database**: MySQL (compatibile con Aiven)

## Installazione

### Prerequisiti

- Python 3.10+
- MySQL 8.0+
- Node.js (opzionale, per sviluppo)

### Setup Backend

```bash
# Entra nella directory backend
cd backend

# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure: venv\Scripts\activate  # Windows

# Installa dipendenze
pip install -r requirements.txt

# Configura variabili ambiente
cp .env.example .env
# Modifica .env con le tue credenziali database

# Inizializza database
mysql -u root -p < init_db.sql

# Avvia server
python app.py
```

### Setup Database (Aiven)

1. Crea un servizio MySQL su [Aiven](https://aiven.io/)
2. Copia le credenziali nel file `.env`
3. Esegui lo script `init_db.sql` per creare le tabelle

### Avvio

```bash
cd backend
python app.py
```

L'applicazione sarà disponibile su `http://localhost:5000`

## Struttura Progetto

```
HelpMe-/
├── backend/
│   ├── app.py              # Applicazione Flask principale
│   ├── config.py           # Configurazione
│   ├── database.py         # Connessione database
│   ├── init_db.sql         # Script inizializzazione DB
│   ├── requirements.txt    # Dipendenze Python
│   └── routes/             # API endpoints
│       ├── auth.py         # Autenticazione
│       ├── users.py        # Gestione utenti
│       ├── posts.py        # CRUD post
│       ├── comments.py     # Gestione commenti
│       ├── categories.py   # Categorie e iscrizioni
│       ├── votes.py        # Sistema voti
│       ├── notifications.py # Notifiche
│       └── admin.py        # Pannello admin
├── frontend/
│   ├── index.html          # SPA principale
│   ├── css/styles.css      # Stili (Design System)
│   └── js/
│       ├── api.js          # Client API
│       └── app.js          # Logica applicazione
├── deliverables/
│   └── sql/                # Script SQL richiesti
│       ├── 01_schema.sql
│       ├── 02_required_operations.sql
│       └── 03_queries.sql
├── memory-bank/            # Documentazione progetto
│   ├── dataModel.md        # Modello E/R e logico
│   ├── designSystem.md     # Design system UI
│   └── ...
├── demo-design.html        # Demo design statico
└── productToBuild.md       # Requisiti progetto
```

## API Endpoints

### Autenticazione
- `POST /api/v1/auth/register` - Registrazione
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/logout` - Logout
- `GET /api/v1/auth/session` - Verifica sessione

### Post
- `GET /api/v1/posts` - Lista post (con filtri)
- `GET /api/v1/posts/:id` - Dettaglio post
- `POST /api/v1/posts` - Crea post
- `PUT /api/v1/posts/:id` - Modifica post
- `DELETE /api/v1/posts/:id` - Elimina post
- `POST /api/v1/posts/:id/close` - Chiudi post

### Commenti
- `GET /api/v1/comments/post/:postId` - Lista commenti
- `POST /api/v1/comments/post/:postId` - Aggiungi commento
- `DELETE /api/v1/comments/:id` - Elimina commento

### Voti
- `POST /api/v1/votes/comment/:id` - Vota commento

### Categorie
- `GET /api/v1/categories` - Lista categorie
- `POST /api/v1/categories` - Crea categoria (admin)
- `POST /api/v1/categories/:id/subscribe` - Iscriviti
- `POST /api/v1/categories/:id/unsubscribe` - Annulla iscrizione

### Notifiche
- `GET /api/v1/notifications` - Lista notifiche
- `POST /api/v1/notifications/read-all` - Segna tutte come lette

### Admin
- `GET /api/v1/admin/users` - Lista utenti
- `POST /api/v1/admin/users/:id/ban` - Banna utente
- `POST /api/v1/admin/users/:id/unban` - Sbanna utente
- `GET /api/v1/admin/stats` - Statistiche

## Design System

Il design segue il sistema documentato in `memory-bank/designSystem.md`:

- **Font**: Fraunces (titoli), Work Sans (body)
- **Colori**: Palette terrosa con arancio bruciato (#D85A3C) e verde salvia (#4A6B5C)
- **Componenti**: Card con bordi arrotondati, badge esperti, status badges

## Credenziali Demo

- **Admin**: admin@helpme.it / admin123
- **Utente**: mario@example.com / password123

## Autore

Progetto scolastico - HelpMe! Web Application
