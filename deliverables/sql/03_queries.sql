-- HelpMe! — Query SQL richieste (sezioni Select/Join/Aggregate)
-- Eseguire dopo aver applicato 01_schema.sql e 02_required_operations.sql (tabella `post` rinominata in `problema`).

-- 1) Post con autore (id, titolo, descrizione, data inserimento, nome autore)
SELECT p.id,
       p.titolo_post AS titolo,
       p.descrizione,
       p.data_inserimento,
       u.nome AS autore
FROM problema p
JOIN users u ON u.id = p.autore_id;

-- 2) Titolo e data dei post dell'utente con nickname "Omega123"
SELECT p.titolo_post AS titolo,
       p.data_inserimento
FROM problema p
JOIN users u ON u.id = p.autore_id
WHERE u.nickname = 'Omega123';

-- 3) Post con titolo che contiene "forno" (case-insensitive)
SELECT p.id,
       p.titolo_post AS titolo,
       p.descrizione,
       p.data_inserimento,
       u.nickname AS autore
FROM problema p
JOIN users u ON u.id = p.autore_id
WHERE p.titolo_post LIKE '%forno%';

-- 4) Commenti per il post con id=1 (id commento, testo, data, nome autore)
SELECT c.id AS id_commento,
       c.testo,
       c.data_inserimento,
       u.nome AS autore
FROM commenti c
JOIN users u ON u.id = c.autore_id
WHERE c.post_id = 1;

-- 5) Post con relative categorie (id post, titolo, nome categoria)
SELECT p.id AS post_id,
       p.titolo_post AS titolo,
       c.nome AS categoria
FROM problema p
JOIN post_categorie pc ON pc.post_id = p.id
JOIN categorie c ON c.id = pc.categoria_id;

-- 6) Conteggio commenti per ciascun post
SELECT p.id AS post_id,
       p.titolo_post AS titolo,
       COUNT(c.id) AS numero_commenti
FROM problema p
LEFT JOIN commenti c ON c.post_id = p.id
GROUP BY p.id, p.titolo_post;

-- 7) Post con più di 3 commenti
SELECT p.id AS post_id,
       p.titolo_post AS titolo,
       COUNT(c.id) AS numero_commenti
FROM problema p
LEFT JOIN commenti c ON c.post_id = p.id
GROUP BY p.id, p.titolo_post
HAVING COUNT(c.id) > 3;

-- 8) Post con il numero massimo di commenti (tutti quelli a pari merito)
WITH comment_counts AS (
  SELECT p.id AS post_id,
         p.titolo_post AS titolo,
         COUNT(c.id) AS numero_commenti,
         DENSE_RANK() OVER (ORDER BY COUNT(c.id) DESC) AS rnk
  FROM problema p
  LEFT JOIN commenti c ON c.post_id = p.id
  GROUP BY p.id, p.titolo_post
)
SELECT post_id,
       titolo,
       numero_commenti
FROM comment_counts
WHERE rnk = 1;

-- 9) Post non chiusi (data_chiusura NULL), ordinati per data di inserimento crescente
SELECT p.id,
       p.titolo_post AS titolo,
       p.descrizione,
       p.data_inserimento,
       u.nome AS autore
FROM problema p
JOIN users u ON u.id = p.autore_id
WHERE p.data_chiusura IS NULL
ORDER BY p.data_inserimento ASC;

-- 10) Post chiusi (data_chiusura valorizzata), ordinati per data di chiusura decrescente
SELECT p.id,
       p.titolo_post AS titolo,
       p.data_chiusura,
       u.nome AS autore
FROM problema p
JOIN users u ON u.id = p.autore_id
WHERE p.data_chiusura IS NOT NULL
ORDER BY p.data_chiusura DESC;

-- 11) Maggiori esperti per categoria (categoria, nickname esperto, score)
SELECT c.nome AS categoria,
       u.nickname AS esperto,
       ucs.score
FROM user_category_stats ucs
JOIN categorie c ON c.id = ucs.categoria_id
JOIN users u ON u.id = ucs.user_id
WHERE ucs.score = (
  SELECT MAX(ucs2.score)
  FROM user_category_stats ucs2
  WHERE ucs2.categoria_id = ucs.categoria_id
);

-- 12) Utenti che non hanno mai scritto un post
SELECT u.id,
       u.nome
FROM users u
LEFT JOIN problema p ON p.autore_id = u.id
WHERE p.id IS NULL;
