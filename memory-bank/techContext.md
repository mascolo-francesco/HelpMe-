# Tech Context — HelpMe!

## Tecnologie
- **Frontend**: HTML, CSS, JavaScript (SPA).
- **Backend**: Python **Flask** (REST API).
- **Database**: **MySQL 8.0+** (hostato su **Aiven**).

## Database Aiven (configurato)
- **Host**: mysql-chatdb-chatwithdb.h.aivencloud.com
- **Port**: 19515
- **Database**: defaultdb
- **SSL**: Abilitato per connessioni sicure
- **Schema**: 16 tabelle (users, posts, commenti, categorie, votes, notifications, ecc.)
- **Credenziali**: configurate in `backend/.env`

## Vincoli e decisioni
- L’interfaccia FE/BE deve essere **REST** (JSON).
- Gestione **sessioni** richiesta (cookie + sessione server oppure token; scelta da definire in `activeContext.md`).
- Supporto **media** (immagini/video) per post e commenti: decidere se
  - memorizzare solo URL (consigliato) con upload gestito dall’app/hosting esterno, oppure
  - BLOB su DB (sconsigliato per MySQL + semplicità).

## Convenzioni implementate
- **API versioning**: `/api/v1/...` ✅
- **Date/time**: `DATETIME` MySQL con `DEFAULT CURRENT_TIMESTAMP` ✅
- **Password**: hash con `werkzeug.security.generate_password_hash` (scrypt) ✅
- **CORS**: abilitato con Flask-CORS per sviluppo ✅
- **Media**: salvato solo URL (no BLOB) ✅
- **Sessioni**: Cookie-based con Flask sessions ✅
- **Soft delete**: campo `deleted_at` per post e commenti ✅


