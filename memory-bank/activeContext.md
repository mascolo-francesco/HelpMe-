# Active Context - HelpMe!

## Stato attuale
L'applicazione HelpMe! e stata completamente sviluppata con:
- **Backend Flask** con API REST complete
- **Frontend SPA** (HTML/CSS/JS) con design system applicato
- **Database schema** pronto per MySQL/Aiven

## Decisioni prese
- **Votazione**: implementato **upvote/downvote** come sistema di voto sui commenti
- **Media**: salvato solo URL (non upload diretto)
- **Notifiche**: implementate come notifiche "in-app" con stato letto/non letto
- **Sessioni**: cookie + sessione server Flask

## Stack implementato
- **Frontend**: HTML, CSS, JavaScript (SPA senza framework)
- **Backend**: Python Flask con Flask-CORS, PyMySQL
- **Database**: MySQL (schema in `backend/init_db.sql`)

## Struttura progetto
```
backend/
  app.py              # Flask app principale
  config.py           # Configurazione
  database.py         # Connessione DB
  init_db.sql         # Schema + dati demo
  routes/
    auth.py           # Autenticazione
    users.py          # Gestione utenti
    posts.py          # CRUD post
    comments.py       # Commenti
    categories.py     # Categorie
    votes.py          # Voti
    notifications.py  # Notifiche
    admin.py          # Admin panel

frontend/
  index.html          # SPA principale
  css/styles.css      # Design system
  js/
    api.js            # Client API
    app.js            # Logica applicazione
```

## Per testare
1. Configurare `.env` con credenziali database
2. Eseguire `init_db.sql` su MySQL
3. Avviare: `cd backend && python app.py`
4. Aprire: http://localhost:5000

## Credenziali demo
- Admin: admin@helpme.it / admin123
- Utente: mario@example.com / password123

## Riferimenti interni
- Modelli: `memory-bank/dataModel.md`
- Checklist step: `memory-bank/nextSteps.md`
- Design system: `memory-bank/designSystem.md`
