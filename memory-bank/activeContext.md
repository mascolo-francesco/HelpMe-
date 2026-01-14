# Active Context — HelpMe!

## Stato attuale
È disponibile solo la traccia dei requisiti (`productToBuild.md`). La memory bank viene creata ora come base per:
- modello E/R e logico,
- script SQL richiesti,
- implementazione backend Flask + frontend SPA (HTML/CSS/JS).

## Decisioni aperte (da chiudere prima dell’implementazione)
- **Votazione**:
  - nel testo compaiono sia “upvote/downvote” sia “voto 1–5”.
  - proposta: mantenere **upvote/downvote** come voto “rapido” e aggiungere una **valutazione 1–5** opzionale solo per l’autore del post sul commento (una sola valutazione per commento), oppure semplificare a uno solo (da confermare).
- **Media**: salvare solo URL (consigliato) e gestire upload separato (o fase 2).
- **Notifiche**: implementazione come notifiche “in-app” (tabella `notifications`) con stato letto/non letto.
- **Sessioni**: cookie + sessione server (Flask) vs token (JWT). Per progetto scolastico, cookie/sessione è spesso più semplice.

## Prossimi passi (ordinati)
- Finalizzare **modello E/R** e **modello logico**.
- Scrivere **DDL/DML** richiesti (sequenza di ALTER/RENAME ecc.).
- Scrivere le **query SQL** richieste.
- Definire API REST (endpoints + payload) coerenti con lo schema.
- Implementare backend Flask:
  - auth + ruoli (admin),
  - CRUD post/commenti,
  - chiusura post + soluzione,
  - voti + esperti,
  - categorie + iscrizioni + notifiche,
  - moderazione / ban.
- Implementare SPA HTML/CSS/JS:
  - pagine: feed, dettaglio post, login/register, profilo, admin,
  - stati UI: loading/error/success.

## Riferimenti interni
- Modelli: `memory-bank/dataModel.md`
- Checklist step: `memory-bank/nextSteps.md`


