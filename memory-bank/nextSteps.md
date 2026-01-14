# Next Steps Operativi — HelpMe!

## A) Consegna “prime quattro ore” (DB + SQL)

### A1) Diagramma E/R
- Completare il diagramma partendo da `memory-bank/dataModel.md`:
  - entità e attributi
  - relazioni e cardinalità
  - vincoli: post ≥1 categoria; post chiuso con soluzione; voto unico per commento/utente

### A2) Modello logico relazionale
- Produrre lo schema relazionale definitivo (tabelle/PK/FK/index).
- Definire naming coerente con le richieste SQL (tabella `post` che poi diventa `problema`).

### A3) Script SQL richiesti (DDL/DML)
Da traccia:
- `CREATE TABLE post`
- `ALTER TABLE post ADD telefono NOT NULL`
- `ALTER TABLE post RENAME COLUMN titolo → titolo_post`
- `ALTER TABLE post MODIFY titolo_post VARCHAR(100)`
- `ALTER TABLE post DROP COLUMN telefono`
- `RENAME TABLE post → problema`
- `INSERT` id=1 ...
- `INSERT` due righe in un’unica istruzione
- `ALTER TABLE post ADD data_chiusura DATETIME` *(attenzione: dopo rename tabella si chiamerà `problema`)*
- `UPDATE` voto commento id=7 +1
- `UPDATE` titolo post id=2
- `DELETE` post con `data_chiusura IS NULL` e `data_inserimento` più vecchia di 1 anno
- ✅ Implementato in `deliverables/sql/02_required_operations.sql`.

### A4) Query SQL richieste
Da traccia (select/join/group by, ecc.) incluse:
- post con autore
- post per nickname
- ricerca titolo “forno”
- commenti per post
- post con categorie
- conteggio commenti per post, >3 commenti, max commenti
- post non chiusi / chiusi ordinati
- esperti per categoria
- utenti senza post
- ✅ Implementato in `deliverables/sql/03_queries.sql`.

## B) Consegna “altre quattro ore” (SPA + Flask)

### B1) API REST (contratto)
- Auth: register/login/logout/session, profilo.
- Post: CRUD, chiusura + soluzione, media (URL).
- Commenti: create/list/thread, media, delete (soft).
- Voti: up/down.
- Categorie: list (user), CRUD (admin).
- Iscrizioni: follow/unfollow categorie.
- Notifiche: list/mark-as-read.
- Admin: ban/unban, moderazione.

### B2) Backend Flask
- Struttura progetto, config MySQL, migration strategy (manuale o tool).
- Implementazione endpoint + controlli permessi.
- Aggiornamento punteggio/esperti (job o aggiornamento incrementale).

### B3) Frontend SPA (HTML/CSS/JS)
- Routing client-side (semplice) + chiamate fetch API.
- UI principali:
  - feed / filtri per categoria
  - dettaglio post (commenti, voti, evidenziazione soluzione)
  - crea/modifica post
  - login/register
  - notifiche
  - admin panel
- Stati UI: loading/error/success, focus accessibile, validazioni.

