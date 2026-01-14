-- HelpMe! — Full Database Schema for Web Application
-- This schema extends the basic schema to support all features

-- =========================
-- Utenti (extended)
-- =========================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nickname VARCHAR(50) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('USER', 'ADMIN') NOT NULL DEFAULT 'USER',
    status ENUM('ACTIVE', 'BANNED') NOT NULL DEFAULT 'ACTIVE',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- Categorie (extended)
-- =========================
CREATE TABLE IF NOT EXISTS categorie (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(60) NOT NULL UNIQUE,
    descrizione TEXT NULL,
    icona VARCHAR(10) NULL,  -- For emoji icon
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- Posts (extended from 'problema')
-- =========================
CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titolo_post VARCHAR(200) NOT NULL,
    descrizione TEXT NOT NULL,
    autore_id INT NOT NULL,
    data_inserimento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('OPEN', 'CLOSED') NOT NULL DEFAULT 'OPEN',
    data_chiusura DATETIME NULL,
    solution_comment_id INT NULL,
    final_solution_text TEXT NULL,
    deleted_at DATETIME NULL,
    CONSTRAINT fk_posts_autore FOREIGN KEY (autore_id) REFERENCES users(id)
);

-- =========================
-- Post-Categoria (N-N)
-- =========================
CREATE TABLE IF NOT EXISTS post_categorie (
    post_id INT NOT NULL,
    categoria_id INT NOT NULL,
    PRIMARY KEY (post_id, categoria_id),
    CONSTRAINT fk_pc_post FOREIGN KEY (post_id) REFERENCES posts(id),
    CONSTRAINT fk_pc_categoria FOREIGN KEY (categoria_id) REFERENCES categorie(id)
);

-- =========================
-- Post Media
-- =========================
CREATE TABLE IF NOT EXISTS post_media (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    tipo ENUM('IMAGE', 'VIDEO') NOT NULL DEFAULT 'IMAGE',
    url VARCHAR(500) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pm_post FOREIGN KEY (post_id) REFERENCES posts(id)
);

-- =========================
-- Commenti (extended)
-- =========================
CREATE TABLE IF NOT EXISTS commenti (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    autore_id INT NOT NULL,
    parent_comment_id INT NULL,
    testo TEXT NOT NULL,
    data_inserimento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME NULL,
    CONSTRAINT fk_commenti_post FOREIGN KEY (post_id) REFERENCES posts(id),
    CONSTRAINT fk_commenti_autore FOREIGN KEY (autore_id) REFERENCES users(id),
    CONSTRAINT fk_commenti_parent FOREIGN KEY (parent_comment_id) REFERENCES commenti(id)
);

-- =========================
-- Comment Media
-- =========================
CREATE TABLE IF NOT EXISTS comment_media (
    id INT AUTO_INCREMENT PRIMARY KEY,
    comment_id INT NOT NULL,
    tipo ENUM('IMAGE', 'VIDEO') NOT NULL DEFAULT 'IMAGE',
    url VARCHAR(500) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cm_comment FOREIGN KEY (comment_id) REFERENCES commenti(id)
);

-- =========================
-- Comment Votes
-- =========================
CREATE TABLE IF NOT EXISTS comment_votes (
    comment_id INT NOT NULL,
    voter_id INT NOT NULL,
    value TINYINT NOT NULL,  -- 1 for upvote, -1 for downvote
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (comment_id, voter_id),
    CONSTRAINT fk_cv_comment FOREIGN KEY (comment_id) REFERENCES commenti(id),
    CONSTRAINT fk_cv_voter FOREIGN KEY (voter_id) REFERENCES users(id)
);

-- =========================
-- User Category Stats (per expert tracking)
-- =========================
CREATE TABLE IF NOT EXISTS user_category_stats (
    user_id INT NOT NULL,
    categoria_id INT NOT NULL,
    score INT NOT NULL DEFAULT 0,
    is_expert BOOLEAN NOT NULL DEFAULT 0,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, categoria_id),
    CONSTRAINT fk_ucs_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_ucs_categoria FOREIGN KEY (categoria_id) REFERENCES categorie(id)
);

-- =========================
-- Category Subscriptions
-- =========================
CREATE TABLE IF NOT EXISTS category_subscriptions (
    user_id INT NOT NULL,
    categoria_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, categoria_id),
    CONSTRAINT fk_cs_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_cs_categoria FOREIGN KEY (categoria_id) REFERENCES categorie(id)
);

-- =========================
-- Notifications
-- =========================
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    tipo ENUM('NEW_POST_IN_CATEGORY', 'SYSTEM', 'MODERATION') NOT NULL DEFAULT 'SYSTEM',
    messaggio TEXT NOT NULL,
    post_id INT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    read_at DATETIME NULL,
    CONSTRAINT fk_notif_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_notif_post FOREIGN KEY (post_id) REFERENCES posts(id)
);

-- =========================
-- User Bans (storico)
-- =========================
CREATE TABLE IF NOT EXISTS user_bans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    admin_id INT NOT NULL,
    reason TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    revoked_at DATETIME NULL,
    CONSTRAINT fk_ub_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_ub_admin FOREIGN KEY (admin_id) REFERENCES users(id)
);

-- =========================
-- Add FK for solution_comment_id (after commenti table exists)
-- =========================
ALTER TABLE posts 
ADD CONSTRAINT fk_posts_solution_comment 
FOREIGN KEY (solution_comment_id) REFERENCES commenti(id);

-- =========================
-- Indexes for performance
-- =========================
CREATE INDEX idx_posts_autore ON posts(autore_id);
CREATE INDEX idx_posts_status ON posts(status);
CREATE INDEX idx_posts_deleted ON posts(deleted_at);
CREATE INDEX idx_commenti_post ON commenti(post_id);
CREATE INDEX idx_commenti_autore ON commenti(autore_id);
CREATE INDEX idx_commenti_deleted ON commenti(deleted_at);
CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(read_at);

-- =========================
-- Default Categories
-- =========================
INSERT INTO categorie (nome, descrizione, icona) VALUES
('Cucina', 'Problemi e consigli culinari', '👨‍🍳'),
('Informatica', 'Computer, software e tecnologia', '💻'),
('Giardinaggio', 'Piante, fiori e spazi verdi', '🌱'),
('Meccanica', 'Auto, moto e riparazioni', '🔧'),
('Scuola', 'Studio, compiti e formazione', '📚'),
('Elettronica', 'Dispositivi elettronici e circuiti', '⚡'),
('Casa', 'Manutenzione domestica', '🏠'),
('Salute', 'Benessere e consigli medici', '💊'),
('Sport', 'Attività fisica e fitness', '⚽'),
('Finanza', 'Investimenti e gestione denaro', '💰');

-- =========================
-- Create Admin User (password: admin123)
-- =========================
INSERT INTO users (nickname, nome, email, password_hash, role, status) VALUES
('admin', 'Amministratore', 'admin@helpme.it', 'scrypt:32768:8:1$VqXpZhN8nSsM4hYz$c5d5e8f8e5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2', 'ADMIN', 'ACTIVE');

-- =========================
-- Demo Users (password: password123)
-- =========================
INSERT INTO users (nickname, nome, email, password_hash, role, status) VALUES
('marioconti', 'Mario Conti', 'mario@example.com', 'scrypt:32768:8:1$VqXpZhN8nSsM4hYz$c5d5e8f8e5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2', 'USER', 'ACTIVE'),
('giulialenzi', 'Giulia Lenzi', 'giulia@example.com', 'scrypt:32768:8:1$VqXpZhN8nSsM4hYz$c5d5e8f8e5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2', 'USER', 'ACTIVE'),
('andrearossi', 'Andrea Rossi', 'andrea@example.com', 'scrypt:32768:8:1$VqXpZhN8nSsM4hYz$c5d5e8f8e5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2', 'USER', 'ACTIVE'),
('omega123', 'Omega Utente', 'omega@example.com', 'scrypt:32768:8:1$VqXpZhN8nSsM4hYz$c5d5e8f8e5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2', 'USER', 'ACTIVE');

-- Make some users experts
INSERT INTO user_category_stats (user_id, categoria_id, score, is_expert) VALUES
(2, 1, 150, 1),  -- Mario expert in Cucina
(4, 3, 120, 1),  -- Andrea expert in Giardinaggio
(3, 2, 200, 1);  -- Giulia expert in Informatica

-- Demo Posts
INSERT INTO posts (titolo_post, descrizione, autore_id, status) VALUES
('Forno elettrico che non scalda uniformemente', 'Ho un forno elettrico da incasso e da qualche settimana noto che cuoce in modo non uniforme: la parte superiore rimane cruda mentre quella inferiore si brucia. Ho già controllato le resistenze e sembrano funzionare. Qualcuno ha avuto un problema simile?', 2, 'OPEN'),
('MacBook che si surriscalda durante le videochiamate', 'Il mio MacBook Pro 2020 si surriscalda tantissimo quando uso Zoom o Meet, soprattutto se condivido lo schermo. La ventola va a massima velocità e la batteria si scarica velocemente. Ho già provato a resettare la SMC. Cosa posso fare?', 3, 'OPEN'),
('Pianta di basilico con foglie gialle', 'Il mio basilico in vaso sul balcone ha iniziato a fare foglie gialle dalla base. L\'innaffio ogni giorno la mattina presto, è esposto a sud e riceve sole diretto dalle 10 alle 16. Drenaggio buono. Qualche consiglio?', 4, 'CLOSED');

-- Link posts to categories
INSERT INTO post_categorie (post_id, categoria_id) VALUES
(1, 1), (1, 7),  -- Post 1: Cucina, Casa
(2, 2),          -- Post 2: Informatica
(3, 3);          -- Post 3: Giardinaggio

-- Demo Comments
INSERT INTO commenti (post_id, autore_id, testo) VALUES
(1, 3, 'Potrebbe essere un problema con la ventola del forno. Hai controllato se gira correttamente?'),
(1, 4, 'Secondo me è la sonda di temperatura. È un problema comune nei forni da incasso.'),
(2, 4, 'Prova a chiudere tutte le app in background durante le videochiamate. Chrome in particolare consuma molte risorse.'),
(3, 2, 'Probabilmente stai innaffiando troppo! Il basilico preferisce terreno leggermente asciutto tra un\'innaffiatura e l\'altra.');

-- Set solution for closed post
UPDATE posts SET solution_comment_id = 4, data_chiusura = NOW() WHERE id = 3;

-- Add some votes
INSERT INTO comment_votes (comment_id, voter_id, value) VALUES
(1, 2, 1),
(2, 2, 1),
(2, 3, 1),
(4, 4, 1),
(4, 3, 1);
