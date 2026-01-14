-- HelpMe! — Schema minimo (MySQL) per consegna SQL
-- Nota: questo schema è pensato per supportare le query richieste e le operazioni su `post`/`problema`.

-- Facoltativo: crea e usa un database dedicato
-- CREATE DATABASE helpme CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
-- USE helpme;

-- =========================
-- Utenti
-- =========================
CREATE TABLE users (
  id INT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  nickname VARCHAR(50) NOT NULL UNIQUE
);

-- =========================
-- Tabella "post" (verrà rinominata in "problema" nello script operazioni)
-- =========================
CREATE TABLE post (
  id INT PRIMARY KEY,
  titolo VARCHAR(50) NOT NULL,
  descrizione TEXT NOT NULL,
  autore_id INT NOT NULL,
  data_inserimento DATETIME NOT NULL,
  CONSTRAINT fk_post_autore
    FOREIGN KEY (autore_id) REFERENCES users(id)
);

-- =========================
-- Commenti (con campo voto per l’operazione "aumenta voto di 1")
-- =========================
CREATE TABLE commenti (
  id INT PRIMARY KEY,
  post_id INT NOT NULL,
  autore_id INT NOT NULL,
  testo TEXT NOT NULL,
  data_inserimento DATETIME NOT NULL,
  voto INT NOT NULL DEFAULT 0,
  CONSTRAINT fk_commenti_post
    FOREIGN KEY (post_id) REFERENCES post(id),
  CONSTRAINT fk_commenti_autore
    FOREIGN KEY (autore_id) REFERENCES users(id)
);

-- =========================
-- Categorie e appartenenza Post–Categoria (N–N)
-- =========================
CREATE TABLE categorie (
  id INT PRIMARY KEY,
  nome VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE post_categorie (
  post_id INT NOT NULL,
  categoria_id INT NOT NULL,
  PRIMARY KEY (post_id, categoria_id),
  CONSTRAINT fk_pc_post
    FOREIGN KEY (post_id) REFERENCES post(id),
  CONSTRAINT fk_pc_categoria
    FOREIGN KEY (categoria_id) REFERENCES categorie(id)
);

-- =========================
-- Punteggi per esperti (minimo per la query "maggiori esperti per categoria")
-- =========================
CREATE TABLE user_category_stats (
  user_id INT NOT NULL,
  categoria_id INT NOT NULL,
  score INT NOT NULL DEFAULT 0,
  PRIMARY KEY (user_id, categoria_id),
  CONSTRAINT fk_ucs_user
    FOREIGN KEY (user_id) REFERENCES users(id),
  CONSTRAINT fk_ucs_cat
    FOREIGN KEY (categoria_id) REFERENCES categorie(id)
);


