CREATE TABLE IF NOT EXISTS utilisateur (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    prenom TEXT,
    nom TEXT,
    nom_utilisateur TEXT UNIQUE NOT NULL,
    mot_passe TEXT NOT NULL,
    tel TEXT
);

CREATE TABLE IF NOT EXISTS entreprise (
    id_utilisateur INTEGER PRIMARY KEY,
    nom_entreprise TEXT,
    adresse TEXT,
    mail TEXT,
    telephone TEXT,
    nb_ser TEXT,
    logo TEXT,
    FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(ID)
);

CREATE TABLE IF NOT EXISTS client (
    num TEXT,
    nom TEXT,
    prenom TEXT,
    adresse TEXT,
    tel_fax TEXT,
    mobil TEXT,
    coment TEXT,
    id_utilisateur INTEGER,
    PRIMARY KEY (num, id_utilisateur),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(ID)
);

CREATE TABLE IF NOT EXISTS facture (
    num TEXT,
    date_fac TEXT,
    intervens TEXT,
    remarque TEXT,
    solde_du REAL,
    info_pay TEXT,
    infos_banque TEXT,
    signatur INTEGER,
    id_utilisateur INTEGER,
    ref_client TEXT,
    PRIMARY KEY (num, id_utilisateur),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(ID),
    FOREIGN KEY (ref_client, id_utilisateur) REFERENCES client(num, id_utilisateur)
);

CREATE TABLE IF NOT EXISTS devis (
    num TEXT,
    date_devis TEXT,
    intervens TEXT,
    montant REAL,
    remarque TEXT,
    signatur INTEGER,
    id_utilisateur INTEGER,
    ref_client TEXT,
    PRIMARY KEY (num, id_utilisateur),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(ID),
    FOREIGN KEY (ref_client, id_utilisateur) REFERENCES client(num, id_utilisateur)
);
