Verifica — Progettazione e sviluppo della web application “HelpMe!”
Si vuole progettare e realizzare una web application chiamata HelpMe!, che funziona come un piccolo social network tematico finalizzato all’aiuto reciproco tra le persone.
Gli utenti utilizzano HelpMe! per pubblicare problemi di qualunque tipo (ad esempio problemi di cucina, informatica, giardinaggio, scuola, meccanica, orologi, automobile, ecc.) e ricevere suggerimenti da altri utenti che hanno competenze in quell’ambito.
Ogni problema pubblicato è rappresentato da un post, che contiene almeno:
un titolo sintetico,
una descrizione dettagliata del problema,
la data di inserimento,
una o più categorie tematiche di appartenenza,
eventualmente uno o più contenuti multimediali (immagini o video) utili a chiarire meglio il problema.
Ogni risposta a un post è un commento, che contiene:
l’utente che ha scritto il commento,
il testo della risposta,
la data di inserimento,
eventualmente immagini o video di supporto.
Utenti e ruoli
Nel sistema esistono tre tipologie di utenti:
gli utenti non registrati, che possono solo consultare i post e leggere i commenti;
gli utenti registrati, che possono pubblicare nuovi post, rispondere ai post degli altri utenti (commento), votare le risposte ricevute e gestire i propri contenuti. Gli utenti registrati possono anche commentare altri commenti e “upvotare” o “downvotare” un commento
gli amministratori, che gestiscono il funzionamento generale del sistema, creano le categorie tematiche, moderano i contenuti e possono intervenire in caso di violazioni delle regole. Possono anche bannare gli utenti che non rispettano le regole.
Categorie, gruppi di interesse e notifiche
Gli amministratori definiscono un insieme di categorie tematiche (ad esempio “Cucina”, “Orologi”, “Informatica”, “Giardinaggio”, ecc.).
Ogni post deve essere obbligatoriamente associato ad almeno una categoria, e può appartenere anche a più categorie contemporaneamente.
Gli utenti registrati possono scegliere di iscriversi a una o più categorie che rappresentano i loro interessi principali. In questo modo, quando viene pubblicato un nuovo post in una categoria a cui un utente è iscritto, l’utente riceve una notifica.
Gestione dei post e delle soluzioni
Un utente che ha pubblicato un post può in qualsiasi momento:
modificare il contenuto del post,
rimuovere il post (se non è più rilevante) e tutti i commenti relativi. Il post così non sarà più visibile ma resterà comunque memorizzato nel database
chiudere il post quando ha trovato una soluzione soddisfacente. In questo caso il post resta comunque visibile ma non si possono più aggiungere commenti.
Quando un post viene chiuso, l’utente deve indicare chiaramente qual è stata la soluzione al problema. Questo può avvenire in due modi:
selezionando uno dei commenti ricevuti come “commento risolutivo”;
oppure inserendo direttamente una propria risposta finale che descrive la soluzione.
Il sistema deve permettere di individuare immediatamente il commento che contiene la soluzione, senza dover scorrere tutti i commenti del post.
Valutazione delle risposte ed esperti
Gli utenti che ricevono risposte ai propri post possono assegnare un voto alle risposte ricevute (ad esempio su una scala da 1 a 5). I voti contribuiscono a determinare il punteggio degli utenti che rispondono.
Il punteggio viene tracciato anche per categoria: un utente può quindi essere particolarmente competente in una categoria e meno in un’altra.
Quando un utente raggiunge una certa soglia di punteggio in una determinata categoria, viene automaticamente considerato esperto di quella categoria, e il sistema lo segnala come tale agli altri utenti.
Moderazione dei contenuti
Facoltativamente, il sistema può integrare un modulo di Intelligenza Artificiale che analizza automaticamente i commenti per verificare che siano educati, rispettosi e costruttivi, bloccando o segnalando contenuti offensivi o inappropriati.

Richieste
Progettare e realizzare l’intero sistema.
In particolare:
progettare il modello concettuale (ER) del database che rappresenta tutte le informazioni descritte nel testo.
progettare il modello logico relazionale corrispondente.
scrivere una serie di operazioni SQL che permettano di:
Creare la tabella post.
Modificare la tabella post aggiungendo il campo telefono non nullo.
Modificare la tabella post rinominando il campo titolo in titolo_post.
Modificare la tabella post cambiando il tipo del campo titolo_post da VARCHAR(50) a VARCHAR(100).
Modificare la tabella post eliminando il campo telefono.
Rinominare la tabella post in problema
Inserire un nuovo post: id=1, titolo_post="Forno che non scalda", descrizione="Il forno si accende ma resta freddo", autore_id=3, data_inserimento="2026-01-10 15:30:00".
Inserire due nuovi post in un’unica istruzione: id=2, titolo_post="Lavastoviglie rumorosa", descrizione="Fa un rumore metallico durante il lavaggio", autore_id=4, data_inserimento="2026-01-11 10:00:00"; id=3, titolo_post="PC molto lento", descrizione="Il computer impiega 10 minuti ad avviarsi", autore_id=5, data_inserimento="2026-01-12 09:15:00".
Modificare la tabella post aggiungendo un campo data_chiusura di tipo DATETIME.
Aggiornare il voto di un commento con id=7 aumentandolo di 1.
Aggiornare il titolo del post con id=2 sostituendo "Lavastoviglie rumorosa" con "Lavastoviglie molto rumorosa".
Cancellare dalla tabella post tutti i post la cui data_chiusura è NULL e la cui data_inserimento è più vecchia di un anno.
scrivere le istruzioni SQL che permettano di:
Selezionare tutti i post mostrando id, titolo, descrizione, data di inserimento e nome dell’autore.
Selezionare titolo e data di inserimento di tutti i post scritti dall’utente con nickname Omega123
Selezionare tutti i post il cui titolo contiene la parola “forno”, mostrando id, titolo, descrizione, data di inserimento e nickname dell’autore.
Selezionare tutti i commenti associati al post con id=1, mostrando id commento, testo, data di inserimento e nome dell’autore.
Selezionare i post insieme alle categorie a cui appartengono, mostrando id post, titolo e nome categoria.
Contare quanti commenti ci sono per ciascun post, mostrando id post, titolo e numero di commenti.
Visualizzare tutti i post che hanno più di 3 commenti, mostrando id post, titolo e numero di commenti.
Visualizzare il post che ha più commenti.
Trovare i post non ancora chiusi, mostrando id post, titolo, descrizione, data di inserimento e nome autore, ordinati per data di inserimento crescente.
Visualizzare tutti i post chiusi, mostrando id post, titolo, data di chiusura e nome autore, ordinati per data di chiusura decrescente.
Visualizzare il/i maggior/i esperto/i di ogni categoria. Visualizzare la categoria e il nickname dell’esperto.
Selezionare tutti gli utenti che non hanno mai scritto un post, mostrando id utente e nome.
(fine prime quattro ore)
Sviluppo della web application (SPA)
Sviluppare una Single Page Application (SPA) completa, che includa sia un frontend che un backend:
Il frontend può essere sviluppato con il framework o la libreria che si preferisce (ad esempio Angular, React o Vue.js ma anche con html/css/js) e deve permettere di interagire con tutte le funzionalità della piattaforma.
Il backend deve essere sviluppato utilizzando Flask e deve gestire tutte le operazioni legate ai dati e alle logiche applicative.
Deve essere presente un server web che fornisce la SPA e un server API attraverso il quale il frontend accede al database.
L’interfaccia tra frontend e backend deve seguire il formato REST.
Il database deve essere hostato su Aiven e deve utilizzare MySQL.
Funzionalità della SPA:
registrazione e autenticazione degli utenti;
gestione delle sessioni;
inserimento, modifica, cancellazione e chiusura dei post;
inserimento dei commenti;
votazione dei commenti;
evidenziazione delle soluzioni;
gestione delle categorie, delle iscrizioni e degli esperti;
pannello di amministrazione.
(fine ulteriori quattro ore)
Consegnare su Classroom:
il diagramma ER,
il modello logico relazionale,
gli script SQL,
il link GitHub della web app
