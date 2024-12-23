// Faire un "node serveur.js" pour démarrer la connexion au serveur
// nodemon pour mettre toujours à jour

const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors'); // Importer cors

const app = express();
const port = 3000;

// pour permettre les requêtes depuis d'autres domaines
app.use(cors());

// connex à la base de données avec le chemin absolu
const db = new sqlite3.Database('C:/Users/theot/Desktop/Inge/S7/base_donnees_TP1/logement.db', (err) => {
  if (err) {
    console.error('Erreur de connexion à la base de données', err.message);
  } else {
    console.log('Connexion réussie à la base de données SQLite.');
  }
});


// récupérer les logements
app.get('/logements', (req, res) => {
  db.all('SELECT id_logement, adresse FROM logements', [], (err, rows) => {
    // plein debugs
    if (err) {
      console.error('Erreur SQL lors de la récupération des logements:', err.message);
      res.status(500).send({
        error: true,
        message: 'Erreur lors de la récupération des logements',
        details: err.message 
      });
    } else {
      if (rows.length === 0) {
        console.warn('Aucun logement trouvé dans la base de données.');
        res.status(404).send({
          error: false,
          message: 'Aucun logement trouvé'
        });
      } else {
        console.log('Logements récupérés avec succès:', rows);
        res.json(rows); // donne les logements avec l'id et l'adresse
      }
    }
  });
});

// page consommation

// récup les factures d'un logement spécifique
app.get('/factures/:logementId', (req, res) => {
  const logementId = req.params.logementId;
  const mois = req.query.mois; // Format attendu : 'YYYY-MM'

  let query = 'SELECT type_facture, montant FROM factures WHERE adresse_logement = ?';
  const params = [logementId];

  if (mois) {
      query += ' AND strftime("%Y-%m", date_facture) = ?';
      params.push(mois);
  }

  db.all(query, params, (err, rows) => {
      if (err) {
          res.status(500).send({ error: 'Erreur interne du serveur' });
      } else {
          res.json(rows);
      }
  });
});

// Nouvelle route pour récupérer les factures pour deux mois différents
app.get('/factures/comparaison/:logementId', (req, res) => {
  const logementId = req.params.logementId;
  const mois1 = req.query.mois1; // attendu 'YYYY-MM'
  const mois2 = req.query.mois2; // attendu : 'YYYY-MM'

  if (!mois1 || !mois2) {
    return res.status(400).send({ error: 'Les deux mois (mois1 et mois2) sont requis' });
  }

  let query = 'SELECT type_facture, montant, strftime("%Y-%m", date_facture) AS mois FROM factures WHERE adresse_logement = ?';
  const params = [logementId];

  query += ' AND (strftime("%Y-%m", date_facture) = ? OR strftime("%Y-%m", date_facture) = ?)';
  params.push(mois1, mois2);

  db.all(query, params, (err, rows) => {
    if (err) {
      res.status(500).send({ error: 'Erreur interne du serveur' });
    } else {
      res.json(rows);
    }
  });
});


// Page capteurs

// récupérer les capteurs d'un logement spécifique
app.get('/capteurs/:adresse', (req, res) => {
  const adresseLogement = req.params.adresse; // adresse logement récupérée dans URL

  // requête SQL pr récup capteurs associés à adresse logement
  db.all(`
    SELECT ca.id_capteur, ca.ref_type, ca.ref_commerciale, ca.port_com, ca.etat, ca.date_insertion
    FROM capteurs_actionneurs ca
    JOIN pieces p ON ca.ref_piece = p.id_piece
    JOIN logements l ON p.adresse_logement = l.adresse
    WHERE l.adresse = ?
  `, [adresseLogement], (err, rows) => {
    if (err) {
      console.error('Erreur SQL lors de la récupération des capteurs:', err.message);
      res.status(500).send({
        error: true,
        message: 'Erreur lors de la récupération des capteurs',
        details: err.message
      });
    } else {
      if (rows.length === 0) {
        console.warn(`Aucun capteur trouvé pour le logement avec l'adresse ${adresseLogement}`);
        res.status(404).send({
          error: false,
          message: `Aucun capteur trouvé pour le logement avec l'adresse ${adresseLogement}`
        });
      } else {
        console.log('Capteurs récupérés avec succès:', rows);
        res.json(rows); // donne les capteurs sous forme de JSON
      }
    }
  });
});


// page finale qui rajoute des capteurs et modifie nuemro tel

// parser les données JSON
app.use(express.json());

// ajout capteur
app.post('/capteurs', (req, res) => {
  const { ref_type, ref_commerciale, ref_piece, port_com, etat } = req.body;

  if (!ref_type || !ref_commerciale || !ref_piece || !port_com || etat === undefined) {
    return res.status(400).send({ error: 'Tous les champs sont requis : ref_type, ref_commerciale, ref_piece, port_com, etat' });
  }

  const query = `
    INSERT INTO capteurs_actionneurs (ref_type, ref_commerciale, ref_piece, port_com, etat)
    VALUES (?, ?, ?, ?, ?)
  `;

  db.run(query, [ref_type, ref_commerciale, ref_piece, port_com, etat], function (err) {
    if (err) {
      console.error('Erreur lors de l\'ajout du capteur :', err.message);
      res.status(500).send({ error: 'Erreur lors de l\'ajout du capteur', details: err.message });
    } else {
      console.log('Capteur ajouté avec succès, ID:', this.lastID);
      res.status(201).send({ message: 'Capteur ajouté avec succès', id: this.lastID });
    }
  });
});

// Partie numero tel à modif et recup

// Récup un logement par son adresse
app.get('/logement/:id', (req, res) => {
  const logementId = req.params.id;

  const query = 'SELECT id_logement, adresse, numero_tel FROM logements WHERE adresse = ?';
  db.get(query, [logementId], (err, row) => {
    if (err) {
      console.error('Erreur SQL lors de la récupération du logement:', err.message);
      res.status(500).send({
        error: true,
        message: 'Erreur lors de la récupération du logement',
        details: err.message
      });
    } else if (!row) {
      res.status(404).send({ error: 'Logement non trouvé' });
    } else {
      console.log('Logement récupéré:', row);
      res.json(row); // l'objet logement avec numéro de téléphone
    }
  });
});

app.get('/logement/:adresse/numero_tel', (req, res) => {
  const logementAdresse = req.params.adresse;

  const query = 'SELECT numero_tel FROM logements WHERE adresse = ?';
  db.get(query, [logementAdresse], (err, row) => {
    if (err) {
      console.error('Erreur SQL:', err.message);
      return res.status(500).send({ error: 'Erreur lors de la récupération du numéro de téléphone' });
    }

    if (!row) {
      return res.status(404).send({ error: 'Logement non trouvé' });
    }

    res.json({ numero_tel: row.numero_tel }); // envoie num
  });
});



app.put('/logement/:adresse/numero_tel', (req, res) => {
  const logementAdresse = req.params.adresse;
  const nouveauTelephone = req.body.telephone; 

  console.log('Requête reçue pour adresse:', logementAdresse);
  console.log('Numéro reçu:', nouveauTelephone);

  if (!nouveauTelephone) {
    return res.status(400).send({ error: 'Le numéro de téléphone est requis' });
  }

  // check si l'adresse existe dans la base de données
  db.get('SELECT * FROM logements WHERE adresse = ?', [logementAdresse], (err, row) => {
    if (err) {
      console.error('Erreur SQL lors de la vérification de l\'adresse:', err.message);
      return res.status(500).send({ error: 'Erreur lors de la vérification de l\'adresse' });
    }
    if (!row) {
      console.warn('Adresse non trouvée:', logementAdresse);
      return res.status(404).send({ error: 'Logement non trouvé' });
    }

    // mise à jour du numéro de téléphone
    const query = 'UPDATE logements SET numero_tel = ? WHERE adresse = ?';
    db.run(query, [nouveauTelephone, logementAdresse], function (err) {
      if (err) {
        console.error('Erreur SQL lors de la mise à jour:', err.message);
        return res.status(500).send({ error: 'Erreur lors de la mise à jour du téléphone' });
      }

      console.log('Numéro de téléphone mis à jour avec succès');
      res.send({ success: 'Numéro de téléphone mis à jour avec succès' });
    });
  });
});

// ----------------------------------------------------

// start serveur
app.listen(port, () => {
  console.log(`Serveur démarré sur http://localhost:${port}`);
});
