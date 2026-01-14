# Active Context - HelpMe!

## Stato attuale
L'applicazione HelpMe! è stata completamente sviluppata e **funzionante**:
- **Backend Flask** con API REST complete
- **Frontend SPA** (HTML/CSS/JS) con design system applicato
- **Database MySQL su Aiven** inizializzato e funzionante
- **Dati di esempio** inseriti (10 categorie, 5 utenti, 3 post, 4 commenti)

## Ultimo problema risolto (14 gen 2026)
L'applicazione restituiva errori 500 perché:
- Il database Aiven remoto era configurato correttamente nel `.env`
- Ma lo script `init_db.sql` era stato eseguito solo su MySQL locale, non su Aiven
- Risultato: connessione OK, ma tabelle inesistenti sul database remoto

**Soluzione applicata**:
1. Eseguito `init_db.sql` sul database Aiven remoto tramite script Python
2. Create tutte le 16 tabelle del sistema
3. Inseriti dati demo: 10 categorie, 5 utenti (incluso admin), 3 post, 4 commenti, esperti, voti
4. Verificata connettività e integrità del database

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
1. ✅ `.env` già configurato con credenziali Aiven
2. ✅ Database Aiven già inizializzato con schema e dati
3. Avviare server: `cd backend && source venv/bin/activate && python app.py`
4. Aprire browser: http://localhost:5000

**Nota**: Il database è già pronto su Aiven. Non serve più eseguire `init_db.sql` manualmente a meno di reset completo.

## Credenziali demo
- Admin: admin@helpme.it / admin123
- Utente: mario@example.com / password123

## Riferimenti interni
- Modelli: `memory-bank/dataModel.md`
- Checklist step: `memory-bank/nextSteps.md`
- Design system: `memory-bank/designSystem.md`
