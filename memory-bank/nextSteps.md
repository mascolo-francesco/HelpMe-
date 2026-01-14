# Next Steps Operativi - HelpMe!

## A) Consegna "prime quattro ore" (DB + SQL)

### A1) Diagramma E/R
- [x] Completare il diagramma partendo da `memory-bank/dataModel.md`:
  - entita e attributi
  - relazioni e cardinalita
  - vincoli: post >=1 categoria; post chiuso con soluzione; voto unico per commento/utente

### A2) Modello logico relazionale
- [x] Produrre lo schema relazionale definitivo (tabelle/PK/FK/index).
- [x] Definire naming coerente con le richieste SQL (tabella `post` che poi diventa `problema`).

### A3) Script SQL richiesti (DDL/DML)
- [x] Implementato in `deliverables/sql/02_required_operations.sql`.

### A4) Query SQL richieste
- [x] Implementato in `deliverables/sql/03_queries.sql`.

## B) Consegna "altre quattro ore" (SPA + Flask)

### B1) API REST (contratto)
- [x] Auth: register/login/logout/session, profilo.
- [x] Post: CRUD, chiusura + soluzione, media (URL).
- [x] Commenti: create/list/thread, media, delete (soft).
- [x] Voti: up/down.
- [x] Categorie: list (user), CRUD (admin).
- [x] Iscrizioni: follow/unfollow categorie.
- [x] Notifiche: list/mark-as-read.
- [x] Admin: ban/unban, moderazione.

### B2) Backend Flask
- [x] Struttura progetto, config MySQL, migration strategy (manuale o tool).
- [x] Implementazione endpoint + controlli permessi.
- [x] Aggiornamento punteggio/esperti (aggiornamento incrementale).

### B3) Frontend SPA (HTML/CSS/JS)
- [x] Routing client-side (semplice) + chiamate fetch API.
- [x] UI principali:
  - [x] feed / filtri per categoria
  - [x] dettaglio post (commenti, voti, evidenziazione soluzione)
  - [x] crea/modifica post
  - [x] login/register
  - [x] notifiche
  - [x] admin panel
- [x] Stati UI: loading/error/success, focus accessibile, validazioni.

## C) Prossimi Step

### C1) Test con Database
- [ ] Configurare connessione MySQL su Aiven
- [ ] Eseguire `init_db.sql` per creare schema e dati demo
- [ ] Testare tutti gli endpoint API
- [ ] Testare il flusso completo utente

### C2) Deployment (opzionale)
- [ ] Configurare WSGI server (Gunicorn)
- [ ] Configurare hosting (Render, Railway, o simile)
- [ ] Configurare dominio

### C3) Documentazione finale
- [ ] Generare diagramma E/R grafico (se richiesto)
- [ ] Screenshot dell'applicazione funzionante
- [ ] Video demo (opzionale)
