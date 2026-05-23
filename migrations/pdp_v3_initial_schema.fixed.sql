CREATE TABLE IF NOT EXISTS pdp_v3_workflows (
    id INTEGER NOT NULL,
    facture_id INTEGER,
    numero VARCHAR(255) NOT NULL,
    sens VARCHAR(50) NOT NULL,
    statut VARCHAR(100) NOT NULL,
    canal VARCHAR(100) NOT NULL,
    accuse_reception VARCHAR(255),
    date_action VARCHAR(255),
    detail VARCHAR(2000),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS pdp_v3_archives (
    id INTEGER NOT NULL,
    nom_archive VARCHAR(255) NOT NULL,
    empreinte_sha256 VARCHAR(255) NOT NULL,
    date_archive VARCHAR(255),
    detail VARCHAR(2000),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS pdp_v3_journal_technique (
    id INTEGER NOT NULL,
    type_evenement VARCHAR(255) NOT NULL,
    reference VARCHAR(255),
    message VARCHAR(2000) NOT NULL,
    empreinte_sha256 VARCHAR(255),
    date_evenement VARCHAR(255),
    PRIMARY KEY (id)
);
