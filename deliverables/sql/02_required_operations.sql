-- HelpMe! — Operazioni SQL richieste (DDL/DML)
-- Eseguire dopo `01_schema.sql`

-- 1) Modificare la tabella post aggiungendo il campo telefono non nullo.
ALTER TABLE post
  ADD telefono VARCHAR(20) NOT NULL;

-- 2) Modificare la tabella post rinominando il campo titolo in titolo_post.
ALTER TABLE post
  RENAME COLUMN titolo TO titolo_post;

-- 3) Modificare la tabella post cambiando il tipo del campo titolo_post da VARCHAR(50) a VARCHAR(100).
ALTER TABLE post
  MODIFY titolo_post VARCHAR(100) NOT NULL;

-- 4) Modificare la tabella post eliminando il campo telefono.
ALTER TABLE post
  DROP COLUMN telefono;

-- 5) Rinominare la tabella post in problema
RENAME TABLE post TO problema;

-- Nota: dopo il rename, anche le FK che puntano a `post` ora puntano a `problema` (MySQL le aggiorna).

-- 6) Inserire un nuovo post: id=1, titolo_post="Forno che non scalda", descrizione="Il forno si accende ma resta freddo",
--    autore_id=3, data_inserimento="2026-01-10 15:30:00".
INSERT INTO problema (id, titolo_post, descrizione, autore_id, data_inserimento)
VALUES (1, 'Forno che non scalda', 'Il forno si accende ma resta freddo', 3, '2026-01-10 15:30:00');

-- 7) Inserire due nuovi post in un’unica istruzione
INSERT INTO problema (id, titolo_post, descrizione, autore_id, data_inserimento)
VALUES
  (2, 'Lavastoviglie rumorosa', 'Fa un rumore metallico durante il lavaggio', 4, '2026-01-11 10:00:00'),
  (3, 'PC molto lento', 'Il computer impiega 10 minuti ad avviarsi', 5, '2026-01-12 09:15:00');

-- 8) Modificare la tabella post aggiungendo un campo data_chiusura di tipo DATETIME.
--    Nota: la tabella è stata rinominata in `problema`, quindi l'ALTER si applica a `problema`.
ALTER TABLE problema
  ADD data_chiusura DATETIME NULL;

-- 9) Aggiornare il voto di un commento con id=7 aumentandolo di 1.
UPDATE commenti
SET voto = voto + 1
WHERE id = 7;

-- 10) Aggiornare il titolo del post con id=2 sostituendo "Lavastoviglie rumorosa" con "Lavastoviglie molto rumorosa".
UPDATE problema
SET titolo_post = 'Lavastoviglie molto rumorosa'
WHERE id = 2;

-- 11) Cancellare dalla tabella post tutti i post la cui data_chiusura è NULL e la cui data_inserimento è più vecchia di un anno.
--     Nota: tabella rinominata → `problema`.
DELETE FROM problema
WHERE data_chiusura IS NULL
  AND data_inserimento < (NOW() - INTERVAL 1 YEAR);


