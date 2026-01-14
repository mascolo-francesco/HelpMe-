# HelpMe! — Project Brief

## Obiettivo
Realizzare **HelpMe!**, una web application (tipo piccolo social network tematico) per la **richiesta e l’offerta di aiuto**: gli utenti pubblicano problemi (post) e ricevono risposte (commenti) da altri utenti.

## Ruoli utente
- **Non registrato**: consulta post e commenti.
- **Registrato**: crea/modifica/rimuove/chiude post, commenta post e commenti, vota commenti, gestisce i propri contenuti, si iscrive alle categorie.
- **Amministratore**: crea/gestisce categorie, modera contenuti, banna utenti.

## Requisiti funzionali principali
- **Post (problemi)**: titolo, descrizione, data inserimento, ≥1 categoria, media (immagini/video) opzionali.
- **Commenti (risposte)**: autore, testo, data inserimento, media opzionali; commenti annidati (commenti ai commenti).
- **Chiusura post**: quando risolto, non si possono più aggiungere commenti; soluzione evidenziata tramite:
  - selezione di un commento “risolutivo”, oppure
  - risposta finale dell’autore del post.
- **Votazione**: upvote/downvote sui commenti (e tracciamento punteggio). Inoltre valutazione “1–5” delle risposte (da chiarire, vedi `activeContext.md`).
- **Categorie e iscrizioni**: post multi-categoria; iscrizione utente alle categorie; notifica quando nuovo post in categoria seguita.
- **Esperti**: punteggio per categoria; al superamento soglia utente diventa “esperto” della categoria.
- **Moderazione**: facoltativo modulo IA per filtrare commenti offensivi.

## Requisiti di consegna (scuola)
- Diagramma **E/R**.
- Modello **logico relazionale**.
- Script SQL richiesti (DDL/DML/query).
- Link GitHub web app.

## Stack richiesto
- **Backend**: Flask (REST API).
- **Frontend**: **HTML, CSS, JavaScript** (SPA).
- **DB**: MySQL su Aiven.


