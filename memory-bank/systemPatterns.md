# System Patterns — HelpMe!

## Architettura (macro)
- **SPA** (HTML/CSS/JS) servita da web server (può essere lo stesso Flask in produzione).
- **REST API** Flask per autenticazione, gestione post/commenti/categorie/voti/notifiche/admin.
- **MySQL** come persistenza.

## Pattern di dominio

### Post (“Problema”)
- Stato: **aperto** / **chiuso**.
- Se chiuso:
  - non si possono aggiungere commenti,
  - deve esistere una soluzione: **commento risolutivo** *oppure* **risposta finale** dell’autore.

### Commenti (thread)
- Un commento può rispondere a un post oppure a un altro commento (albero con `parent_comment_id`).
- Voti: supportare **upvote/downvote** (conteggio +1/-1 o tabella voti per utente).

### Categorie e iscrizioni
- Post multi-categoria: relazione N–N.
- Iscrizioni utente–categoria: relazione N–N.
- Notifiche “nuovo post in categoria seguita”: create al momento dell’inserimento post.

### Punteggio per categoria / esperti
- Punteggio aggregabile da voti ricevuti sui commenti per categoria dei post.
- “Esperto” quando supera una soglia per categoria (soglia configurabile).

## Autorizzazioni (pattern)
- **Guest**: sola lettura.
- **User**:
  - CRUD sui propri post (con vincoli: se chiuso non modifica contenuti critici? da definire),
  - commenta post aperti,
  - commenta commenti,
  - vota commenti (una volta per commento).
- **Admin**:
  - CRUD categorie,
  - ban/unban utenti,
  - moderazione (rimozione/oscura contenuti).

## Soft delete / storico
- Requisito: rimuovere post e relativi commenti “non visibili ma memorizzati”.
  - Pattern: `deleted_at` (soft delete) su `posts` e `comments` (e filtri in query).


