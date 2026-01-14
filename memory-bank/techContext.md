# Tech Context — HelpMe!

## Tecnologie
- **Frontend**: HTML, CSS, JavaScript (SPA).
- **Backend**: Python **Flask** (REST API).
- **Database**: **MySQL** (hostato su **Aiven**).

## Vincoli e decisioni
- L’interfaccia FE/BE deve essere **REST** (JSON).
- Gestione **sessioni** richiesta (cookie + sessione server oppure token; scelta da definire in `activeContext.md`).
- Supporto **media** (immagini/video) per post e commenti: decidere se
  - memorizzare solo URL (consigliato) con upload gestito dall’app/hosting esterno, oppure
  - BLOB su DB (sconsigliato per MySQL + semplicità).

## Convenzioni suggerite (da confermare)
- API versioning: `/api/v1/...`
- Date/time: `DATETIME` MySQL in UTC.
- Password: hash robusto (es. `werkzeug.security`).
- CORS: necessario se FE servito da host diverso (in dev).


