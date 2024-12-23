
--------------------- Création de la base de données logement.db ----------------------
-- Retire tout et recréer tout, à utiliser que pour réinitialiser la base de données


-- La commande sqlite3 pour lire un fichier est $ .read fichier.sql
-- sqlite3 logement.db
-- .read logement.sql

-- détruire toutes les tables existantes en respectant l'ordre des dépendances

DROP TABLE IF EXISTS mesures;
DROP TABLE IF EXISTS capteurs_actionneurs;
DROP TABLE IF EXISTS type_capteurs_actionneurs;
DROP TABLE IF EXISTS pieces;
DROP TABLE IF EXISTS factures;
DROP TABLE IF EXISTS logements;

-- Puis on recréer toutes les tables

-- ================= Tables et champs =================
-- Suivant mon diagramme de base de données

-- Table logements
CREATE TABLE IF NOT EXISTS logements (
    id_logement INTEGER PRIMARY KEY AUTOINCREMENT, -- adresse logement
    adresse TEXT,
    numero_tel TEXT,          -- numéro tel
    adresse_IP TEXT,          -- IP
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- date d'ajout d'après le sujet
);

-- Table pieces
CREATE TABLE IF NOT EXISTS pieces (
    id_piece INTEGER PRIMARY KEY AUTOINCREMENT, -- Identifiant unique de la pièce auto
    x INTEGER,                            -- coo pou localiser en 3d un logements
    y INTEGER,                            
    z INTEGER,
    adresse_logement TEXT                     -- adresse du logement referen                         
);

-- Table capteurs/actionneurs
CREATE TABLE IF NOT EXISTS capteurs_actionneurs (
    id_capteur INTEGER PRIMARY KEY AUTOINCREMENT,      -- key unique
    ref_type TEXT,                                     -- type
    ref_commerciale TEXT,                              -- Référence commerciale ou modèle
    ref_piece INTEGER,                                 -- Référence à la pièce xyz
    port_com INTEGER,                                   -- num port de communication 
    etat INTEGER DEFAULT 1 CHECK (etat IN (0, 1)),    -- état 0 ou 1, par défaut 1                                             
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- date d'ajout
);

-- Table types
CREATE TABLE IF NOT EXISTS type_capteurs_actionneurs (
    id_type INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identifiant unique du type de capteur/actionneur
    nom TEXT,                          -- elec par exemple
    unite TEXT,                        -- %, °C ...
    plage_max INTEGER,                  -- plage max
    plage_min INTEGER                  -- plage min
);

-- Table des mesures
CREATE TABLE IF NOT EXISTS mesures (
    id_mesure INTEGER PRIMARY KEY AUTOINCREMENT, -- Identifiant unique de la mesure
    ref_capteur TEXT,                            -- Référence au capteur/actionneur
    valeur REAL,                                        -- Valeur mesurée
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- auto
);

-- Table des factures
CREATE TABLE IF NOT EXISTS factures (
    id_facture INTEGER PRIMARY KEY AUTOINCREMENT, 
    adresse_logement TEXT,                -- Adresse du logement
    type_facture TEXT,                    -- Type de facture (eau, électricité, déchets...)
    date_facture DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,                    -- Date de la facture
    montant REAL,                         -- prix
    valeur_conso REAL                    -- valeur de consommation
);


-- ================== Création de base ============================

-- Tout contenu ci-dessous sera créer de base

-- ================= Créer un logement 4 pièces =================

-- Insertion d'un logement
INSERT INTO logements (adresse, numero_tel, adresse_IP) VALUES ('32_rue_ei', '0112345678', '192.168.1.1');
INSERT INTO logements (adresse, numero_tel, adresse_IP) VALUES ('16_rue_rob', '0719845601', '198.288.0.1');


-- Insertion des 4 pièces pour le logement
INSERT INTO pieces (x, y, z, adresse_logement) VALUES (0, 0, 0, '32_rue_ei');
INSERT INTO pieces (x, y, z, adresse_logement) VALUES (1, 0, 0, '32_rue_ei');
INSERT INTO pieces (x, y, z, adresse_logement) VALUES (0, 1, 0, '32_rue_ei');
INSERT INTO pieces (x, y, z, adresse_logement) VALUES (0, 0, 1, '32_rue_ei');

-- ================= Créer des types capteurs/actionneurs =================

INSERT INTO type_capteurs_actionneurs (nom, unite, plage_max, plage_min) VALUES ('Temp', '°C', 60, -10);
INSERT INTO type_capteurs_actionneurs (nom, unite, plage_max, plage_min) VALUES ('Humi', '%', 100, 0);
INSERT INTO type_capteurs_actionneurs (nom, unite, plage_max, plage_min) VALUES ('Press', 'Pa', 1100, 900);
INSERT INTO type_capteurs_actionneurs (nom, unite, plage_max, plage_min) VALUES ('Lumi', 'Lux', 1000, 0);

-- ================= Créer des capteurs/actionneurs =================

INSERT INTO capteurs_actionneurs (ref_type, ref_commerciale, ref_piece, port_com, etat) VALUES ('Temp', 'T1', 1, 7012, 1);
INSERT INTO capteurs_actionneurs (ref_type, ref_commerciale, ref_piece, port_com, etat) VALUES ('Humi', 'H1', 1, 1207, 1);
INSERT INTO capteurs_actionneurs (ref_type, ref_commerciale, ref_piece, port_com, etat) VALUES ('Press', 'P1', 4, 7120, 1);
INSERT INTO capteurs_actionneurs (ref_type, ref_commerciale, ref_piece, port_com, etat) VALUES ('Lumi', 'L1', 2, 7100, 1);
INSERT INTO capteurs_actionneurs (ref_type, ref_commerciale, ref_piece, port_com, etat) VALUES ('Temp', 'T2', 3, 2071, 1);
INSERT INTO capteurs_actionneurs (ref_type, ref_commerciale, ref_piece, port_com, etat) VALUES ('Lumi', 'L2', 4, 2171, 1);


-- ================= Créer des mesures =================

INSERT INTO mesures (ref_capteur, valeur) VALUES ('H1', 67);
INSERT INTO mesures (ref_capteur, valeur) VALUES ('H1', 60);
INSERT INTO mesures (ref_capteur, valeur) VALUES ('H1', 62);
INSERT INTO mesures (ref_capteur, valeur) VALUES ('H1', 55);

INSERT INTO mesures (ref_capteur, valeur) VALUES ('T1', 23);
INSERT INTO mesures (ref_capteur, valeur) VALUES ('T1', 25);
INSERT INTO mesures (ref_capteur, valeur) VALUES ('T1', 29);

-- ================== Créer des factures ==================

INSERT INTO factures (adresse_logement, type_facture, date_facture, montant, valeur_conso) VALUES ('32_rue_ei', 'Eau', '2020-01-01', 50, 300);
INSERT INTO factures (adresse_logement, type_facture, date_facture, montant, valeur_conso) VALUES ('32_rue_ei', 'Electricité', '2020-01-01', 100, 500);
INSERT INTO factures (adresse_logement, type_facture, date_facture, montant, valeur_conso) VALUES ('32_rue_ei', 'Déchets', '2020-01-01', 20, 100);

INSERT INTO factures (adresse_logement, type_facture, date_facture, montant, valeur_conso) VALUES ('32_rue_ei', 'Eau', '2020-02-01', 55, 360);
INSERT INTO factures (adresse_logement, type_facture, date_facture, montant, valeur_conso) VALUES ('32_rue_ei', 'Electricité', '2020-02-01', 80, 400);
INSERT INTO factures (adresse_logement, type_facture, date_facture, montant, valeur_conso) VALUES ('32_rue_ei', 'Déchets', '2020-02-01', 26, 150);

INSERT INTO factures (adresse_logement, type_facture, date_facture, montant, valeur_conso) VALUES ('32_rue_ei', 'Eau', '2020-03-01', 40, 200);
INSERT INTO factures (adresse_logement, type_facture, date_facture, montant, valeur_conso) VALUES ('32_rue_ei', 'Electricité', '2020-03-01', 70, 300);
INSERT INTO factures (adresse_logement, type_facture, date_facture, montant, valeur_conso) VALUES ('32_rue_ei', 'Déchets', '2020-03-01', 22, 120);





