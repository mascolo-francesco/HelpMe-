# Progress - HelpMe!

## Fatto
- Creata struttura iniziale memory bank (brief/contesti/pattern).
- Consegna SQL (schema minimo + operazioni + query): `deliverables/sql/01_schema.sql`, `02_required_operations.sql`, `03_queries.sql`.
- **Backend Flask completato**:
  - Struttura progetto con Flask + Flask-CORS + PyMySQL
  - API REST completa:
    - Auth: register/login/logout/session
    - Users: profile, experts
    - Posts: CRUD, close with solution
    - Comments: create, list, delete
    - Categories: CRUD (admin), subscribe/unsubscribe
    - Votes: upvote/downvote sui commenti
    - Notifications: list, mark as read
    - Admin: users management, ban/unban, moderation, stats
  - Database schema completo: `backend/init_db.sql`
  - Configurazione ambiente: `backend/.env.example`
- **Frontend SPA completato**:
  - Design system applicato (Fraunces + Work Sans, palette terrosa)
  - Homepage con hero, categorie, post recenti, sidebar esperti
  - Modali: login, registrazione, nuovo post
  - Pagine: categorie, esperti, dettaglio post, profilo, attivita utente
  - Pannello admin: gestione utenti, categorie, statistiche
  - Sistema notifiche in-app
  - Toast per feedback utente
  - Responsive design
- **Documentazione**:
  - README.md aggiornato con istruzioni complete

## In corso
- Test con database MySQL connesso (Aiven)

## Da fare (high level)
- [x] Progettazione API REST
- [x] Backend Flask
- [x] Frontend SPA
- [ ] Collegare a database MySQL su Aiven per test completo
- [ ] Documentazione consegna (ER grafico, se richiesto)

## Problemi noti / rischi
- Implementato upvote/downvote invece di voto 1-5 (piu semplice e comune)
- Database non ancora connesso (richiede credenziali Aiven)

## Documenti chiave
- `memory-bank/dataModel.md` (E/R testuale + modello logico)
- `memory-bank/nextSteps.md` (tutti gli step richiesti dalla consegna)
- `memory-bank/designSystem.md` (design system UI)
- `backend/init_db.sql` (schema database completo)
