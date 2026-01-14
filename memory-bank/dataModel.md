# Modello Dati — HelpMe! (E/R + Logico Relazionale)

> Nota: questo documento deriva da `productToBuild.md` e introduce alcune scelte implementative “ragionevoli” (soft delete, voti per utente, notifiche in-app). Le ambiguità sono evidenziate e vanno confermate.

## 1) Modello E/R (testuale)

### Entità

#### Utente
- **Attributi**: `id`, `nickname` (univoco), `nome`, `email` (univoca), `password_hash`, `ruolo` (USER/ADMIN), `stato` (ATTIVO/BANNATO), `created_at`

#### Categoria
- **Attributi**: `id`, `nome` (univoco), `descrizione`, `created_at`

#### Post / Problema
- **Attributi**: `id`, `titolo`, `descrizione`, `data_inserimento`, `stato` (APERTO/CHIUSO), `data_chiusura` (opzionale), `final_solution_text` (opzionale), `deleted_at` (opzionale)

#### Commento
- **Attributi**: `id`, `testo`, `data_inserimento`, `deleted_at` (opzionale)

#### Media (per Post o Commento)
- **Attributi**: `id`, `tipo` (IMMAGINE/VIDEO), `url`, `created_at`

#### Notifica
- **Attributi**: `id`, `tipo`, `testo`, `created_at`, `read_at` (opzionale)

#### Voto (up/down) su Commento
- **Attributi**: `valore` (+1/-1), `created_at`

#### Statistiche Utente per Categoria (punteggio/esperto)
- **Attributi**: `score`, `is_expert`, `updated_at`

### Relazioni (cardinalità)

#### Autore Post
- **Utente (1)** —scrive→ **Post (N)**

#### Post–Categoria (appartenenza)
- **Post (N)** —appartiene→ **Categoria (N)**
  - Vincolo: ogni Post deve appartenere ad **almeno 1** Categoria.

#### Iscrizione a Categoria
- **Utente (N)** —segue→ **Categoria (N)**
  - Da questa relazione derivano le notifiche “nuovo post in categoria seguita”.

#### Commenti
- **Utente (1)** —scrive→ **Commento (N)**
- **Post (1)** —ha→ **Commento (N)**
- **Commento (0..1)** —risponde a→ **Commento (0..N)** (thread tramite parent)

#### Media
- **Post (1)** —ha→ **MediaPost (0..N)**
- **Commento (1)** —ha→ **MediaCommento (0..N)**

#### Soluzione di un Post chiuso
- **Post (0..1)** —ha commento risolutivo→ **Commento (0..1)**
  - Vincolo: se `stato=CHIUSO` allora deve valere:
    - `commento_risolutivo` presente **oppure**
    - `final_solution_text` presente.

#### Votazione commenti
- **Utente (N)** —vota→ **Commento (N)** con attributo `valore` (+1/-1)
  - Vincolo: un utente può votare **al massimo una volta** lo stesso commento (unique).

#### Notifiche
- **Utente (1)** —riceve→ **Notifica (N)**
- (Opzionale) **Post (0..1)** —genera→ **Notifica (0..N)** (per tracciare “nuovo post”)

#### Punteggio/Esperti per categoria
- **Utente (N)** —ha stats→ **Categoria (N)** con `score` e `is_expert`
  - Lo score può essere calcolato dai voti ricevuti sui commenti nei post di quella categoria, ma per semplicità si può materializzare.

### Ambiguità da chiarire (impatta E/R)
- Nel testo compaiono sia “**upvote/downvote**” sia “**voto 1–5**”.
  - Proposta: implementare **upvote/downvote** e (opzionale) una **valutazione 1–5** assegnabile solo dall’autore del post al commento (tabella `comment_ratings`).

---

## 2) Modello logico relazionale (MySQL)

> Convenzione: `created_at`/`updated_at` `DATETIME` (UTC). Soft delete con `deleted_at` `DATETIME NULL`.

### Tabelle principali

#### `users`
- `id` PK
- `nickname` UNIQUE NOT NULL
- `name` NOT NULL
- `email` UNIQUE NOT NULL
- `password_hash` NOT NULL
- `role` ENUM('USER','ADMIN') NOT NULL
- `status` ENUM('ACTIVE','BANNED') NOT NULL DEFAULT 'ACTIVE'
- `created_at` NOT NULL

#### `categories`
- `id` PK
- `name` UNIQUE NOT NULL
- `description` NULL
- `created_at` NOT NULL

#### `posts`
- `id` PK
- `author_id` FK → `users.id` NOT NULL
- `title` NOT NULL  *(in SQL richiesto verrà rinominato/alterato; vedi step SQL)*
- `description` NOT NULL
- `created_at` NOT NULL
- `status` ENUM('OPEN','CLOSED') NOT NULL DEFAULT 'OPEN'
- `closed_at` NULL
- `solution_comment_id` NULL FK → `comments.id` *(deferrabile logicamente: in MySQL richiede che `comments` esista; gestire con ordine creazione o FK dopo)*
- `final_solution_text` NULL
- `deleted_at` NULL

#### `post_categories` (N–N)
- `post_id` FK → `posts.id`
- `category_id` FK → `categories.id`
- PK(`post_id`,`category_id`)

#### `post_media`
- `id` PK
- `post_id` FK → `posts.id` NOT NULL
- `type` ENUM('IMAGE','VIDEO') NOT NULL
- `url` NOT NULL
- `created_at` NOT NULL

#### `comments`
- `id` PK
- `post_id` FK → `posts.id` NOT NULL
- `author_id` FK → `users.id` NOT NULL
- `parent_comment_id` NULL FK → `comments.id`
- `text` NOT NULL
- `created_at` NOT NULL
- `deleted_at` NULL

#### `comment_media`
- `id` PK
- `comment_id` FK → `comments.id` NOT NULL
- `type` ENUM('IMAGE','VIDEO') NOT NULL
- `url` NOT NULL
- `created_at` NOT NULL

### Voti / reputazione

#### `comment_votes`
- `comment_id` FK → `comments.id` NOT NULL
- `voter_id` FK → `users.id` NOT NULL
- `value` TINYINT NOT NULL  *(vincolo applicativo: solo -1 o +1)*
- `created_at` NOT NULL
- PK(`comment_id`,`voter_id`)  *(1 voto per utente per commento)*

#### `user_category_stats`
- `user_id` FK → `users.id` NOT NULL
- `category_id` FK → `categories.id` NOT NULL
- `score` INT NOT NULL DEFAULT 0
- `is_expert` BOOLEAN NOT NULL DEFAULT 0
- `updated_at` NOT NULL
- PK(`user_id`,`category_id`)

> Nota: per coerenza, lo `score` per categoria può derivare dai voti ricevuti su commenti appartenenti a post della categoria. Se un post è multi-categoria, la politica di attribuzione (split o pieno) va definita.

### Notifiche

#### `category_subscriptions`
- `user_id` FK → `users.id` NOT NULL
- `category_id` FK → `categories.id` NOT NULL
- `created_at` NOT NULL
- PK(`user_id`,`category_id`)

#### `notifications`
- `id` PK
- `user_id` FK → `users.id` NOT NULL
- `type` ENUM('NEW_POST_IN_CATEGORY','SYSTEM','MODERATION') NOT NULL
- `message` NOT NULL
- `post_id` NULL FK → `posts.id`
- `created_at` NOT NULL
- `read_at` NULL

### Admin / moderazione (minimo)

#### `user_bans` (storico ban)
- `id` PK
- `user_id` FK → `users.id` NOT NULL
- `admin_id` FK → `users.id` NOT NULL
- `reason` NULL
- `created_at` NOT NULL
- `revoked_at` NULL

---

## 3) Vincoli applicativi (da implementare in API + DB dove possibile)
- Un post **deve** avere ≥1 categoria (verifica in API; in DB non è banale senza trigger).
- Se `posts.status='CLOSED'`:
  - `closed_at` NOT NULL
  - (`solution_comment_id` NOT NULL) XOR (`final_solution_text` NOT NULL) (vincolo applicativo o trigger).
- Non permettere inserimento commenti su post chiusi.
- Soft delete: filtrare `deleted_at IS NULL` su post/commenti nelle query pubbliche.
- Voti: impedire più voti dello stesso utente sullo stesso commento (PK composto).


