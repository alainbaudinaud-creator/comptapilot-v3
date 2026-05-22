
BEGIN;
CREATE TABLE plan_comptable (
            id SERIAL PRIMARY KEY ,
            numero TEXT,
            libelle TEXT,
            type TEXT
        , societe_id INTEGER);
INSERT INTO plan_comptable VALUES(1,'601','achat','charge',NULL);
INSERT INTO plan_comptable VALUES(2,'512','Banque','Actif',NULL);
INSERT INTO plan_comptable VALUES(3,'701','ventes','Produit',2);
INSERT INTO plan_comptable VALUES(4,'101','Capital','Passif',2);
INSERT INTO plan_comptable VALUES(5,'401','Fournisseurs','Passif',2);
INSERT INTO plan_comptable VALUES(6,'411','Clients','Actif',2);
INSERT INTO plan_comptable VALUES(7,'512','Banque','Actif',2);
INSERT INTO plan_comptable VALUES(8,'601','Achats','Charge',2);
INSERT INTO plan_comptable VALUES(9,'606','Fournitures','Charge',2);
INSERT INTO plan_comptable VALUES(10,'706','Prestations','Produit',2);
INSERT INTO plan_comptable VALUES(11,'44566','TVA d├®ductible','Actif',2);
INSERT INTO plan_comptable VALUES(12,'44571','TVA collect├®e','Passif',2);
CREATE TABLE ecritures (
            id SERIAL PRIMARY KEY ,
            date_ecriture TEXT,
            piece TEXT,
            libelle TEXT,
            debit REAL DEFAULT 0,
            credit REAL DEFAULT 0,
            societe_id INTEGER,
            compte_id INTEGER, rapproche INTEGER DEFAULT 0, date_rapprochement TEXT, reference_banque TEXT, journal TEXT, lettrage TEXT, date_lettrage TEXT, rapproche_bancaire INTEGER DEFAULT 0, exercice TEXT,
            FOREIGN KEY (societe_id) REFERENCES societes(id),
            FOREIGN KEY (compte_id) REFERENCES plan_comptable(id)
        );
INSERT INTO ecritures VALUES(2,'2026-05-05','fac2','fournitures',0.0,100.0,1,2,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(3,'2026-05-05','AUTO1','Achat fournitures',120.0,0.0,2,9,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(4,'2026-05-05','AUTO1','Achat fournitures',0.0,120.0,2,7,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(5,'2026-05-05','AUTO-TVA','Achat fournitures',100.0,0.0,2,9,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(6,'2026-05-05','AUTO-TVA','TVA d├®ductible - Achat fournitures',20.0,0.0,2,11,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(7,'2026-05-05','AUTO-TVA','Achat fournitures',0.0,120.0,2,7,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(8,'2026-05-05','F001','Facture client - Dupont',120.0,0.0,2,7,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(9,'2026-05-05','F001','Facture client - Dupont',0.0,100.0,2,10,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(10,'2026-05-05','F001','TVA collect├®e - Facture client - Dupont',0.0,20.0,2,12,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(11,'2026-05-05','F001','Facture client - durand',100.0,0.0,2,7,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(12,'2026-05-05','F001','Facture client - durand',0.0,83.33,2,10,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(13,'2026-05-05','F001','TVA collect├®e - Facture client - durand',0.0,16.67,2,12,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(14,'2026-05-05','F001','Facture client - durand',100.0,0.0,2,7,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(15,'2026-05-05','F001','Facture client - durand',0.0,83.33,2,10,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(16,'2026-05-05','F001','TVA collect├®e - Facture client - durand',0.0,16.67,2,12,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(17,'2026-05-05','F001','Facture F001 - durand - Prestation de services',250.0,0.0,2,7,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(18,'2026-05-05','F001','Facture F001 - durand - Prestation de services',0.0,208.33,2,10,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(19,'2026-05-05','F001','TVA collect├®e - Facture F001 - durand - Prestation de services',0.0,41.67,2,12,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(20,'2026-05-05','F001','Facture F001 - Dupont',624.0,0.0,2,7,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(21,'2026-05-05','F001','Facture F001 - Dupont',0.0,520.0,2,10,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(22,'2026-05-05','F001','TVA collect├®e - Facture F001 - Dupont',0.0,104.0,2,12,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(23,'2026-05-05','F001','Facture F001 - durand',705.6,0.0,2,7,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(24,'2026-05-05','F001','Facture F001 - durand',0.0,588.0,2,10,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(25,'2026-05-05','F001','TVA collect├®e - Facture F001 - durand',0.0,117.6,2,12,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(26,'2026-05-05','F001','Facture F001 - durand',1086.0,0.0,2,7,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(27,'2026-05-05','F001','Facture F001 - durand',0.0,905.0,2,10,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(28,'2026-05-05','F001','TVA collect├®e - Facture F001 - durand',0.0,181.0,2,12,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(29,'2026-05-05','F2026-0001','Facture F2026-0001 - durand',616.8,0.0,2,7,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(30,'2026-05-05','F2026-0001','Facture F2026-0001 - durand',0.0,512.0,2,10,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(31,'2026-05-05','F2026-0001','TVA collect├®e - Facture F2026-0001 - durand',0.0,102.8,2,12,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(32,'2026-05-05','F2026-0002','Facture F2026-0002 - durand',1058.4,0.0,2,7,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(34,'2026-05-05','F2026-0004','Facture F2026-0004 - durand',950.4,0.0,2,7,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(36,'2026-05-05','F2026-0004','TVA collect├®e - Facture F2026-0004 - durand',0.0,158.4,2,12,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(39,'2026-05-03','FA002','Conseil ',0.0,800.0,1,7,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(40,'2026-05-06','FAC20260506124025','Fournisseurs',158.0,0.0,1,2,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(41,'2026-05-06','FAC20260506124025','Fournisseurs',0.0,126.4,1,6,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(42,'2026-05-06','FAC20260506124025','TVA collect├®e',0.0,31.6,1,8,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(43,'2026-05-06','FAC20260506132838','Test facture automatique',120.0,0.0,1,2,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(44,'2026-05-06','FAC20260506132838','Test facture automatique',0.0,96.0,1,6,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(45,'2026-05-06','FAC20260506132838','TVA collect├®e',0.0,24.0,1,8,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(46,'2026-05-06','FAC20260506145815','ventes',99.0,0.0,1,2,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(47,'2026-05-06','FAC20260506145815','ventes',0.0,79.2,1,6,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
INSERT INTO ecritures VALUES(48,'2026-05-06','FAC20260506145815','TVA collect├®e',0.0,19.8,1,8,0,NULL,NULL,NULL,'ZHOD','2026-05-07',0,NULL);
CREATE TABLE users (
            id SERIAL PRIMARY KEY ,
            username TEXT UNIQUE,
            password TEXT
        );
INSERT INTO users VALUES(1,'Alain BAUDINAUD','scrypt:32768:8:1$EPd06r6mL3smNGJA$d9261287e8f202009efb951852661a73d57820a74d7b422b37cb509c4568395d46f669a988b71a9586572fe096207863db165f0b038e5c8138d624be5442b61a');
INSERT INTO users VALUES(2,'test','scrypt:32768:8:1$UUxAxRllk6bAKpQs$2197fd5015b299ac463931bb0709c1f65b24f58cebdfe2c3656688fb03e6899c66f757cc8a51ec0729c971fbc6a8a419b0cf5e3bda7669c9b540a29a9d61fb23');
CREATE TABLE clotures (
            id SERIAL PRIMARY KEY ,
            societe_id INTEGER UNIQUE,
            date_cloture TEXT DEFAULT CURRENT_TIMESTAMP
        );
INSERT INTO clotures VALUES(1,1,'2026-05-07');
CREATE TABLE factures (
    id SERIAL PRIMARY KEY ,
    numero TEXT,
    client TEXT,
    date_facture TEXT,
    montant_ht REAL,
    tva REAL,
    montant_ttc REAL
, client_id INTEGER, statut TEXT DEFAULT 'Impay├®e', date_echeance TEXT, nombre_relances INTEGER DEFAULT 0, date_derniere_relance TEXT);
INSERT INTO factures VALUES(1,'FAC20260506132838','Client','2026-05-06',96.0,24.0,120.0,NULL,'payee','2026-06-05',0,NULL);
INSERT INTO factures VALUES(2,'FAC20260506145815','Client','2026-05-06',79.2,19.8,99.0,1,'en_attente','2026-06-05',0,NULL);
CREATE TABLE clients (
    id SERIAL PRIMARY KEY ,
    nom TEXT NOT NULL,
    email TEXT,
    telephone TEXT,
    adresse TEXT,
    siret TEXT,
    tva_intra TEXT
);
INSERT INTO clients VALUES(1,'Alain BAUDINAUD','alain.baudinaud@orange.fr','0678567831','124 Chemin du Bouchaud','','');
CREATE TABLE societes (
    id SERIAL PRIMARY KEY ,
    nom TEXT,
    siret TEXT,
    adresse TEXT
);
CREATE TABLE audit_log (
            id SERIAL PRIMARY KEY ,
            action TEXT,
            detail TEXT,
            date_action TEXT
        );
INSERT INTO audit_log VALUES(1,'TRANSMISSION_FACTURE','Facture FD-2026-00001 transmise au client murielle','2026-05-07 16:21:25');
INSERT INTO audit_log VALUES(2,'SIGNATURE','Acc├¿s au module transmission factures','2026-05-08 23:30:15');
INSERT INTO audit_log VALUES(3,'SIGNATURE','Acc├¿s au module transmission factures','2026-05-08 23:33:53');
INSERT INTO audit_log VALUES(4,'SIGNATURE','Acc├¿s au module transmission factures','2026-05-08 23:36:28');
INSERT INTO audit_log VALUES(5,'SIGNATURE','Acc├¿s au module transmission factures','2026-05-08 23:53:50');
INSERT INTO audit_log VALUES(6,'TRANSMISSION_FACTURE','Acc├¿s au module transmission factures','2026-05-09 00:47:36');
INSERT INTO audit_log VALUES(7,'TRANSMISSION_FACTURE','Acc├¿s au module transmission factures','2026-05-09 00:59:18');
INSERT INTO audit_log VALUES(8,'TRANSMISSION_FACTURE','Acc├¿s au module transmission factures','2026-05-09 01:36:01');
INSERT INTO audit_log VALUES(9,'TEST_SERVICE','Test audit service OK','2026-05-09 01:41:57');
INSERT INTO audit_log VALUES(10,'SIGNATURE','Document sign├® : TEST_DOC par ALAIN','2026-05-09 01:45:31');
INSERT INTO audit_log VALUES(11,'TRANSMISSION_FACTURE','Acc├¿s au module transmission factures','2026-05-09 01:54:25');
INSERT INTO audit_log VALUES(12,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 02:11:45');
INSERT INTO audit_log VALUES(13,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 02:15:09');
INSERT INTO audit_log VALUES(14,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 02:20:23');
INSERT INTO audit_log VALUES(15,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 02:22:11');
INSERT INTO audit_log VALUES(16,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 02:23:52');
INSERT INTO audit_log VALUES(17,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 02:23:52');
INSERT INTO audit_log VALUES(18,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 13:58:20');
INSERT INTO audit_log VALUES(19,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 13:58:20');
INSERT INTO audit_log VALUES(20,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 13:58:20');
INSERT INTO audit_log VALUES(21,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 14:44:17');
INSERT INTO audit_log VALUES(22,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 14:44:17');
INSERT INTO audit_log VALUES(23,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 14:44:17');
INSERT INTO audit_log VALUES(24,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 14:44:17');
INSERT INTO audit_log VALUES(25,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 14:44:17');
INSERT INTO audit_log VALUES(26,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 14:50:41');
INSERT INTO audit_log VALUES(27,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 14:50:41');
INSERT INTO audit_log VALUES(28,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 14:50:41');
INSERT INTO audit_log VALUES(29,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 14:50:41');
INSERT INTO audit_log VALUES(30,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 14:50:41');
INSERT INTO audit_log VALUES(31,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 14:56:34');
INSERT INTO audit_log VALUES(32,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 14:56:34');
INSERT INTO audit_log VALUES(33,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 14:56:34');
INSERT INTO audit_log VALUES(34,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 14:56:34');
INSERT INTO audit_log VALUES(35,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 14:56:34');
INSERT INTO audit_log VALUES(36,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 15:01:34');
INSERT INTO audit_log VALUES(37,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 15:01:34');
INSERT INTO audit_log VALUES(38,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 15:01:34');
INSERT INTO audit_log VALUES(39,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 15:01:34');
INSERT INTO audit_log VALUES(40,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 15:01:34');
INSERT INTO audit_log VALUES(41,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 15:06:34');
INSERT INTO audit_log VALUES(42,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 15:06:34');
INSERT INTO audit_log VALUES(43,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 15:06:34');
INSERT INTO audit_log VALUES(44,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 15:06:34');
INSERT INTO audit_log VALUES(45,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 15:06:34');
INSERT INTO audit_log VALUES(46,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 15:11:34');
INSERT INTO audit_log VALUES(47,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 15:11:34');
INSERT INTO audit_log VALUES(48,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 15:11:34');
INSERT INTO audit_log VALUES(49,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 15:11:34');
INSERT INTO audit_log VALUES(50,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 15:11:34');
INSERT INTO audit_log VALUES(51,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 15:16:34');
INSERT INTO audit_log VALUES(52,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 15:16:34');
INSERT INTO audit_log VALUES(53,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 15:16:34');
INSERT INTO audit_log VALUES(54,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 15:16:34');
INSERT INTO audit_log VALUES(55,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 15:16:34');
INSERT INTO audit_log VALUES(56,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 15:21:34');
INSERT INTO audit_log VALUES(57,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 15:21:34');
INSERT INTO audit_log VALUES(58,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 15:21:34');
INSERT INTO audit_log VALUES(59,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 15:21:34');
INSERT INTO audit_log VALUES(60,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 15:21:34');
INSERT INTO audit_log VALUES(61,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 15:23:57');
INSERT INTO audit_log VALUES(62,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 15:23:57');
INSERT INTO audit_log VALUES(63,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 15:23:58');
INSERT INTO audit_log VALUES(64,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 15:23:58');
INSERT INTO audit_log VALUES(65,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 15:23:58');
INSERT INTO audit_log VALUES(66,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 15:28:58');
INSERT INTO audit_log VALUES(67,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 15:28:58');
INSERT INTO audit_log VALUES(68,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 15:28:58');
INSERT INTO audit_log VALUES(69,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 15:28:58');
INSERT INTO audit_log VALUES(70,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 15:28:58');
INSERT INTO audit_log VALUES(71,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 15:33:58');
INSERT INTO audit_log VALUES(72,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 15:33:58');
INSERT INTO audit_log VALUES(73,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 15:33:58');
INSERT INTO audit_log VALUES(74,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 15:33:58');
INSERT INTO audit_log VALUES(75,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 15:33:58');
INSERT INTO audit_log VALUES(76,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 15:38:58');
INSERT INTO audit_log VALUES(77,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 15:38:58');
INSERT INTO audit_log VALUES(78,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 15:38:58');
INSERT INTO audit_log VALUES(79,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 15:38:58');
INSERT INTO audit_log VALUES(80,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 15:38:58');
INSERT INTO audit_log VALUES(81,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 15:43:58');
INSERT INTO audit_log VALUES(82,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 15:43:58');
INSERT INTO audit_log VALUES(83,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 15:43:58');
INSERT INTO audit_log VALUES(84,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 15:43:58');
INSERT INTO audit_log VALUES(85,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 15:43:58');
INSERT INTO audit_log VALUES(86,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 15:48:58');
INSERT INTO audit_log VALUES(87,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 15:48:58');
INSERT INTO audit_log VALUES(88,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 15:48:58');
INSERT INTO audit_log VALUES(89,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 15:48:58');
INSERT INTO audit_log VALUES(90,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 15:48:58');
INSERT INTO audit_log VALUES(91,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 15:53:58');
INSERT INTO audit_log VALUES(92,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 15:53:58');
INSERT INTO audit_log VALUES(93,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 15:53:58');
INSERT INTO audit_log VALUES(94,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 15:53:58');
INSERT INTO audit_log VALUES(95,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 15:53:58');
INSERT INTO audit_log VALUES(96,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 15:58:58');
INSERT INTO audit_log VALUES(97,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 15:58:58');
INSERT INTO audit_log VALUES(98,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 15:58:58');
INSERT INTO audit_log VALUES(99,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 15:58:58');
INSERT INTO audit_log VALUES(100,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 15:58:58');
INSERT INTO audit_log VALUES(101,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 16:03:58');
INSERT INTO audit_log VALUES(102,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 16:03:58');
INSERT INTO audit_log VALUES(103,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 16:03:58');
INSERT INTO audit_log VALUES(104,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 16:03:58');
INSERT INTO audit_log VALUES(105,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 16:03:58');
INSERT INTO audit_log VALUES(106,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 16:08:58');
INSERT INTO audit_log VALUES(107,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 16:08:58');
INSERT INTO audit_log VALUES(108,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 16:08:58');
INSERT INTO audit_log VALUES(109,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 16:08:58');
INSERT INTO audit_log VALUES(110,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 16:08:58');
INSERT INTO audit_log VALUES(111,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 16:13:58');
INSERT INTO audit_log VALUES(112,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 16:13:58');
INSERT INTO audit_log VALUES(113,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 16:13:58');
INSERT INTO audit_log VALUES(114,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 16:13:58');
INSERT INTO audit_log VALUES(115,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 16:13:58');
INSERT INTO audit_log VALUES(116,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 16:18:58');
INSERT INTO audit_log VALUES(117,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 16:18:58');
INSERT INTO audit_log VALUES(118,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 16:18:58');
INSERT INTO audit_log VALUES(119,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 16:18:58');
INSERT INTO audit_log VALUES(120,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 16:18:58');
INSERT INTO audit_log VALUES(121,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 16:23:58');
INSERT INTO audit_log VALUES(122,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 16:23:58');
INSERT INTO audit_log VALUES(123,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 16:23:58');
INSERT INTO audit_log VALUES(124,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 16:23:58');
INSERT INTO audit_log VALUES(125,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 16:23:58');
INSERT INTO audit_log VALUES(126,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 16:28:58');
INSERT INTO audit_log VALUES(127,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 16:28:58');
INSERT INTO audit_log VALUES(128,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 16:28:58');
INSERT INTO audit_log VALUES(129,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 16:28:58');
INSERT INTO audit_log VALUES(130,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 16:28:58');
INSERT INTO audit_log VALUES(131,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 16:33:58');
INSERT INTO audit_log VALUES(132,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 16:33:58');
INSERT INTO audit_log VALUES(133,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 16:33:58');
INSERT INTO audit_log VALUES(134,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 16:33:58');
INSERT INTO audit_log VALUES(135,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 16:33:58');
INSERT INTO audit_log VALUES(136,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 16:38:58');
INSERT INTO audit_log VALUES(137,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 16:38:58');
INSERT INTO audit_log VALUES(138,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 16:38:58');
INSERT INTO audit_log VALUES(139,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 16:38:58');
INSERT INTO audit_log VALUES(140,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 16:38:58');
INSERT INTO audit_log VALUES(141,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 16:43:58');
INSERT INTO audit_log VALUES(142,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 16:43:58');
INSERT INTO audit_log VALUES(143,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 16:43:58');
INSERT INTO audit_log VALUES(144,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 16:43:58');
INSERT INTO audit_log VALUES(145,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 16:43:58');
INSERT INTO audit_log VALUES(146,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 16:48:58');
INSERT INTO audit_log VALUES(147,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 16:48:58');
INSERT INTO audit_log VALUES(148,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 16:48:58');
INSERT INTO audit_log VALUES(149,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 16:48:58');
INSERT INTO audit_log VALUES(150,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 16:48:58');
INSERT INTO audit_log VALUES(151,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 16:53:58');
INSERT INTO audit_log VALUES(152,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 16:53:58');
INSERT INTO audit_log VALUES(153,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 16:53:58');
INSERT INTO audit_log VALUES(154,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 16:53:58');
INSERT INTO audit_log VALUES(155,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 16:53:58');
INSERT INTO audit_log VALUES(156,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 16:58:58');
INSERT INTO audit_log VALUES(157,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 16:58:58');
INSERT INTO audit_log VALUES(158,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 16:58:58');
INSERT INTO audit_log VALUES(159,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 16:58:58');
INSERT INTO audit_log VALUES(160,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 16:58:58');
INSERT INTO audit_log VALUES(161,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 17:03:58');
INSERT INTO audit_log VALUES(162,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 17:03:58');
INSERT INTO audit_log VALUES(163,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 17:03:58');
INSERT INTO audit_log VALUES(164,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 17:03:58');
INSERT INTO audit_log VALUES(165,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 17:03:58');
INSERT INTO audit_log VALUES(166,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 17:08:58');
INSERT INTO audit_log VALUES(167,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 17:08:58');
INSERT INTO audit_log VALUES(168,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 17:08:58');
INSERT INTO audit_log VALUES(169,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 17:08:58');
INSERT INTO audit_log VALUES(170,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 17:08:58');
INSERT INTO audit_log VALUES(171,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 17:13:58');
INSERT INTO audit_log VALUES(172,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 17:13:58');
INSERT INTO audit_log VALUES(173,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 17:13:58');
INSERT INTO audit_log VALUES(174,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 17:13:58');
INSERT INTO audit_log VALUES(175,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 17:13:58');
INSERT INTO audit_log VALUES(176,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 17:18:58');
INSERT INTO audit_log VALUES(177,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 17:18:58');
INSERT INTO audit_log VALUES(178,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 17:18:58');
INSERT INTO audit_log VALUES(179,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 17:18:58');
INSERT INTO audit_log VALUES(180,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 17:18:58');
INSERT INTO audit_log VALUES(181,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 17:23:58');
INSERT INTO audit_log VALUES(182,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 17:23:58');
INSERT INTO audit_log VALUES(183,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 17:23:58');
INSERT INTO audit_log VALUES(184,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 17:23:58');
INSERT INTO audit_log VALUES(185,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 17:23:58');
INSERT INTO audit_log VALUES(186,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 17:28:58');
INSERT INTO audit_log VALUES(187,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 17:28:58');
INSERT INTO audit_log VALUES(188,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 17:28:58');
INSERT INTO audit_log VALUES(189,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 17:28:58');
INSERT INTO audit_log VALUES(190,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 17:28:58');
INSERT INTO audit_log VALUES(191,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 17:33:58');
INSERT INTO audit_log VALUES(192,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 17:33:58');
INSERT INTO audit_log VALUES(193,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 17:33:58');
INSERT INTO audit_log VALUES(194,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 17:33:58');
INSERT INTO audit_log VALUES(195,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 17:33:58');
INSERT INTO audit_log VALUES(196,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 17:38:58');
INSERT INTO audit_log VALUES(197,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 17:38:58');
INSERT INTO audit_log VALUES(198,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 17:38:58');
INSERT INTO audit_log VALUES(199,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 17:38:58');
INSERT INTO audit_log VALUES(200,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 17:38:58');
INSERT INTO audit_log VALUES(201,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 17:43:58');
INSERT INTO audit_log VALUES(202,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 17:43:58');
INSERT INTO audit_log VALUES(203,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 17:43:58');
INSERT INTO audit_log VALUES(204,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 17:43:58');
INSERT INTO audit_log VALUES(205,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 17:43:58');
INSERT INTO audit_log VALUES(206,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 17:48:58');
INSERT INTO audit_log VALUES(207,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 17:48:58');
INSERT INTO audit_log VALUES(208,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 17:48:58');
INSERT INTO audit_log VALUES(209,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 17:48:58');
INSERT INTO audit_log VALUES(210,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 17:48:59');
INSERT INTO audit_log VALUES(211,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 17:53:59');
INSERT INTO audit_log VALUES(212,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 17:53:59');
INSERT INTO audit_log VALUES(213,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 17:53:59');
INSERT INTO audit_log VALUES(214,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 17:53:59');
INSERT INTO audit_log VALUES(215,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 17:53:59');
INSERT INTO audit_log VALUES(216,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 17:58:59');
INSERT INTO audit_log VALUES(217,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 17:58:59');
INSERT INTO audit_log VALUES(218,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 17:58:59');
INSERT INTO audit_log VALUES(219,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 17:58:59');
INSERT INTO audit_log VALUES(220,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 17:58:59');
INSERT INTO audit_log VALUES(221,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 18:03:59');
INSERT INTO audit_log VALUES(222,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 18:03:59');
INSERT INTO audit_log VALUES(223,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 18:03:59');
INSERT INTO audit_log VALUES(224,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 18:03:59');
INSERT INTO audit_log VALUES(225,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 18:03:59');
INSERT INTO audit_log VALUES(226,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 18:08:59');
INSERT INTO audit_log VALUES(227,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 18:08:59');
INSERT INTO audit_log VALUES(228,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 18:08:59');
INSERT INTO audit_log VALUES(229,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 18:08:59');
INSERT INTO audit_log VALUES(230,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 18:08:59');
INSERT INTO audit_log VALUES(231,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 18:13:59');
INSERT INTO audit_log VALUES(232,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 18:13:59');
INSERT INTO audit_log VALUES(233,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 18:13:59');
INSERT INTO audit_log VALUES(234,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 18:13:59');
INSERT INTO audit_log VALUES(235,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 18:13:59');
INSERT INTO audit_log VALUES(236,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 18:18:59');
INSERT INTO audit_log VALUES(237,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 18:18:59');
INSERT INTO audit_log VALUES(238,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 18:18:59');
INSERT INTO audit_log VALUES(239,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 18:18:59');
INSERT INTO audit_log VALUES(240,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 18:18:59');
INSERT INTO audit_log VALUES(241,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 18:23:59');
INSERT INTO audit_log VALUES(242,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 18:23:59');
INSERT INTO audit_log VALUES(243,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 18:23:59');
INSERT INTO audit_log VALUES(244,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 18:23:59');
INSERT INTO audit_log VALUES(245,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 18:23:59');
INSERT INTO audit_log VALUES(246,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 18:28:59');
INSERT INTO audit_log VALUES(247,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 18:28:59');
INSERT INTO audit_log VALUES(248,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 18:28:59');
INSERT INTO audit_log VALUES(249,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 18:28:59');
INSERT INTO audit_log VALUES(250,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 18:28:59');
INSERT INTO audit_log VALUES(251,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 18:33:59');
INSERT INTO audit_log VALUES(252,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 18:33:59');
INSERT INTO audit_log VALUES(253,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 18:33:59');
INSERT INTO audit_log VALUES(254,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 18:33:59');
INSERT INTO audit_log VALUES(255,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 18:33:59');
INSERT INTO audit_log VALUES(256,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 18:38:59');
INSERT INTO audit_log VALUES(257,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 18:38:59');
INSERT INTO audit_log VALUES(258,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 18:38:59');
INSERT INTO audit_log VALUES(259,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 18:38:59');
INSERT INTO audit_log VALUES(260,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 18:38:59');
INSERT INTO audit_log VALUES(261,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 18:43:59');
INSERT INTO audit_log VALUES(262,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 18:43:59');
INSERT INTO audit_log VALUES(263,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 18:43:59');
INSERT INTO audit_log VALUES(264,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 18:43:59');
INSERT INTO audit_log VALUES(265,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 18:43:59');
INSERT INTO audit_log VALUES(266,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 18:48:59');
INSERT INTO audit_log VALUES(267,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 18:48:59');
INSERT INTO audit_log VALUES(268,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 18:48:59');
INSERT INTO audit_log VALUES(269,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 18:48:59');
INSERT INTO audit_log VALUES(270,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 18:48:59');
INSERT INTO audit_log VALUES(271,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 18:53:59');
INSERT INTO audit_log VALUES(272,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 18:53:59');
INSERT INTO audit_log VALUES(273,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 18:53:59');
INSERT INTO audit_log VALUES(274,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 18:53:59');
INSERT INTO audit_log VALUES(275,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 18:53:59');
INSERT INTO audit_log VALUES(276,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 18:58:59');
INSERT INTO audit_log VALUES(277,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 18:58:59');
INSERT INTO audit_log VALUES(278,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 18:58:59');
INSERT INTO audit_log VALUES(279,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 18:58:59');
INSERT INTO audit_log VALUES(280,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 18:58:59');
INSERT INTO audit_log VALUES(281,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 19:03:59');
INSERT INTO audit_log VALUES(282,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 19:03:59');
INSERT INTO audit_log VALUES(283,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 19:03:59');
INSERT INTO audit_log VALUES(284,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 19:03:59');
INSERT INTO audit_log VALUES(285,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 19:03:59');
INSERT INTO audit_log VALUES(286,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 19:08:59');
INSERT INTO audit_log VALUES(287,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 19:08:59');
INSERT INTO audit_log VALUES(288,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 19:08:59');
INSERT INTO audit_log VALUES(289,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 19:08:59');
INSERT INTO audit_log VALUES(290,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 19:08:59');
INSERT INTO audit_log VALUES(291,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 19:13:59');
INSERT INTO audit_log VALUES(292,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 19:13:59');
INSERT INTO audit_log VALUES(293,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 19:13:59');
INSERT INTO audit_log VALUES(294,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 19:13:59');
INSERT INTO audit_log VALUES(295,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 19:13:59');
INSERT INTO audit_log VALUES(296,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 19:18:59');
INSERT INTO audit_log VALUES(297,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 19:18:59');
INSERT INTO audit_log VALUES(298,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 19:18:59');
INSERT INTO audit_log VALUES(299,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 19:18:59');
INSERT INTO audit_log VALUES(300,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 19:18:59');
INSERT INTO audit_log VALUES(301,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 19:23:59');
INSERT INTO audit_log VALUES(302,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 19:23:59');
INSERT INTO audit_log VALUES(303,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 19:23:59');
INSERT INTO audit_log VALUES(304,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 19:23:59');
INSERT INTO audit_log VALUES(305,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 19:23:59');
INSERT INTO audit_log VALUES(306,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 19:28:59');
INSERT INTO audit_log VALUES(307,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 19:28:59');
INSERT INTO audit_log VALUES(308,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 19:28:59');
INSERT INTO audit_log VALUES(309,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 19:28:59');
INSERT INTO audit_log VALUES(310,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 19:28:59');
INSERT INTO audit_log VALUES(311,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 19:33:59');
INSERT INTO audit_log VALUES(312,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 19:33:59');
INSERT INTO audit_log VALUES(313,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 19:33:59');
INSERT INTO audit_log VALUES(314,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 19:33:59');
INSERT INTO audit_log VALUES(315,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 19:33:59');
INSERT INTO audit_log VALUES(316,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 19:38:59');
INSERT INTO audit_log VALUES(317,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 19:38:59');
INSERT INTO audit_log VALUES(318,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 19:38:59');
INSERT INTO audit_log VALUES(319,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 19:38:59');
INSERT INTO audit_log VALUES(320,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 19:38:59');
INSERT INTO audit_log VALUES(321,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 19:43:59');
INSERT INTO audit_log VALUES(322,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 19:43:59');
INSERT INTO audit_log VALUES(323,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 19:43:59');
INSERT INTO audit_log VALUES(324,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 19:43:59');
INSERT INTO audit_log VALUES(325,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 19:43:59');
INSERT INTO audit_log VALUES(326,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 19:48:59');
INSERT INTO audit_log VALUES(327,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 19:48:59');
INSERT INTO audit_log VALUES(328,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 19:48:59');
INSERT INTO audit_log VALUES(329,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 19:48:59');
INSERT INTO audit_log VALUES(330,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 19:48:59');
INSERT INTO audit_log VALUES(331,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 19:53:59');
INSERT INTO audit_log VALUES(332,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 19:53:59');
INSERT INTO audit_log VALUES(333,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 19:53:59');
INSERT INTO audit_log VALUES(334,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 19:53:59');
INSERT INTO audit_log VALUES(335,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 19:53:59');
INSERT INTO audit_log VALUES(336,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 19:58:59');
INSERT INTO audit_log VALUES(337,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 19:58:59');
INSERT INTO audit_log VALUES(338,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 19:58:59');
INSERT INTO audit_log VALUES(339,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 19:58:59');
INSERT INTO audit_log VALUES(340,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 19:58:59');
INSERT INTO audit_log VALUES(341,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 20:03:59');
INSERT INTO audit_log VALUES(342,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 20:03:59');
INSERT INTO audit_log VALUES(343,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 20:03:59');
INSERT INTO audit_log VALUES(344,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 20:03:59');
INSERT INTO audit_log VALUES(345,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 20:03:59');
INSERT INTO audit_log VALUES(346,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 20:08:59');
INSERT INTO audit_log VALUES(347,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 20:08:59');
INSERT INTO audit_log VALUES(348,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 20:08:59');
INSERT INTO audit_log VALUES(349,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 20:08:59');
INSERT INTO audit_log VALUES(350,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 20:08:59');
INSERT INTO audit_log VALUES(351,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 20:13:59');
INSERT INTO audit_log VALUES(352,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 20:13:59');
INSERT INTO audit_log VALUES(353,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 20:13:59');
INSERT INTO audit_log VALUES(354,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 20:13:59');
INSERT INTO audit_log VALUES(355,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 20:13:59');
INSERT INTO audit_log VALUES(356,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 20:18:59');
INSERT INTO audit_log VALUES(357,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 20:19:00');
INSERT INTO audit_log VALUES(358,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 20:19:00');
INSERT INTO audit_log VALUES(359,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 20:19:00');
INSERT INTO audit_log VALUES(360,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 20:19:00');
INSERT INTO audit_log VALUES(361,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 20:24:00');
INSERT INTO audit_log VALUES(362,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 20:24:00');
INSERT INTO audit_log VALUES(363,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 20:24:00');
INSERT INTO audit_log VALUES(364,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 20:24:00');
INSERT INTO audit_log VALUES(365,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 20:24:00');
INSERT INTO audit_log VALUES(366,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 20:29:00');
INSERT INTO audit_log VALUES(367,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 20:29:00');
INSERT INTO audit_log VALUES(368,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 20:29:00');
INSERT INTO audit_log VALUES(369,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 20:29:00');
INSERT INTO audit_log VALUES(370,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 20:29:00');
INSERT INTO audit_log VALUES(371,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 20:34:00');
INSERT INTO audit_log VALUES(372,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 20:34:00');
INSERT INTO audit_log VALUES(373,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 20:34:00');
INSERT INTO audit_log VALUES(374,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 20:34:00');
INSERT INTO audit_log VALUES(375,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 20:34:00');
INSERT INTO audit_log VALUES(376,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 20:39:00');
INSERT INTO audit_log VALUES(377,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 20:39:00');
INSERT INTO audit_log VALUES(378,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 20:39:00');
INSERT INTO audit_log VALUES(379,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 20:39:00');
INSERT INTO audit_log VALUES(380,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 20:39:00');
INSERT INTO audit_log VALUES(381,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 20:44:00');
INSERT INTO audit_log VALUES(382,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 20:44:00');
INSERT INTO audit_log VALUES(383,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 20:44:00');
INSERT INTO audit_log VALUES(384,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 20:44:00');
INSERT INTO audit_log VALUES(385,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 20:44:00');
INSERT INTO audit_log VALUES(386,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 20:49:00');
INSERT INTO audit_log VALUES(387,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 20:49:00');
INSERT INTO audit_log VALUES(388,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 20:49:00');
INSERT INTO audit_log VALUES(389,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 20:49:00');
INSERT INTO audit_log VALUES(390,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 20:49:00');
INSERT INTO audit_log VALUES(391,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 20:54:00');
INSERT INTO audit_log VALUES(392,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 20:54:00');
INSERT INTO audit_log VALUES(393,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 20:54:00');
INSERT INTO audit_log VALUES(394,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 20:54:00');
INSERT INTO audit_log VALUES(395,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 20:54:00');
INSERT INTO audit_log VALUES(396,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 20:59:09');
INSERT INTO audit_log VALUES(397,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 20:59:09');
INSERT INTO audit_log VALUES(398,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 20:59:09');
INSERT INTO audit_log VALUES(399,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 20:59:09');
INSERT INTO audit_log VALUES(400,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 20:59:09');
INSERT INTO audit_log VALUES(401,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 21:01:55');
INSERT INTO audit_log VALUES(402,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 21:01:55');
INSERT INTO audit_log VALUES(403,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 21:01:55');
INSERT INTO audit_log VALUES(404,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 21:01:55');
INSERT INTO audit_log VALUES(405,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 21:01:55');
INSERT INTO audit_log VALUES(406,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 21:06:55');
INSERT INTO audit_log VALUES(407,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 21:06:55');
INSERT INTO audit_log VALUES(408,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 21:06:55');
INSERT INTO audit_log VALUES(409,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 21:06:55');
INSERT INTO audit_log VALUES(410,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 21:06:55');
INSERT INTO audit_log VALUES(411,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 21:11:55');
INSERT INTO audit_log VALUES(412,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 21:11:55');
INSERT INTO audit_log VALUES(413,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 21:11:55');
INSERT INTO audit_log VALUES(414,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 21:11:55');
INSERT INTO audit_log VALUES(415,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 21:11:55');
INSERT INTO audit_log VALUES(416,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 21:16:55');
INSERT INTO audit_log VALUES(417,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 21:16:55');
INSERT INTO audit_log VALUES(418,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 21:16:55');
INSERT INTO audit_log VALUES(419,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 21:16:55');
INSERT INTO audit_log VALUES(420,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 21:16:55');
INSERT INTO audit_log VALUES(421,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 21:21:55');
INSERT INTO audit_log VALUES(422,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 21:21:55');
INSERT INTO audit_log VALUES(423,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 21:21:55');
INSERT INTO audit_log VALUES(424,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 21:21:55');
INSERT INTO audit_log VALUES(425,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 21:21:55');
INSERT INTO audit_log VALUES(426,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 21:26:55');
INSERT INTO audit_log VALUES(427,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 21:26:55');
INSERT INTO audit_log VALUES(428,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 21:26:55');
INSERT INTO audit_log VALUES(429,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 21:26:55');
INSERT INTO audit_log VALUES(430,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 21:26:55');
INSERT INTO audit_log VALUES(431,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 21:31:55');
INSERT INTO audit_log VALUES(432,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 21:31:55');
INSERT INTO audit_log VALUES(433,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 21:31:55');
INSERT INTO audit_log VALUES(434,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 21:31:55');
INSERT INTO audit_log VALUES(435,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 21:31:55');
INSERT INTO audit_log VALUES(436,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 21:36:55');
INSERT INTO audit_log VALUES(437,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 21:36:55');
INSERT INTO audit_log VALUES(438,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 21:36:55');
INSERT INTO audit_log VALUES(439,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 21:36:55');
INSERT INTO audit_log VALUES(440,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 21:36:55');
INSERT INTO audit_log VALUES(441,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 21:41:55');
INSERT INTO audit_log VALUES(442,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 21:41:55');
INSERT INTO audit_log VALUES(443,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 21:41:55');
INSERT INTO audit_log VALUES(444,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 21:41:55');
INSERT INTO audit_log VALUES(445,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 21:41:55');
INSERT INTO audit_log VALUES(446,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 21:46:55');
INSERT INTO audit_log VALUES(447,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 21:46:55');
INSERT INTO audit_log VALUES(448,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 21:46:55');
INSERT INTO audit_log VALUES(449,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 21:46:55');
INSERT INTO audit_log VALUES(450,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 21:46:55');
INSERT INTO audit_log VALUES(451,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 21:51:55');
INSERT INTO audit_log VALUES(452,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 21:51:55');
INSERT INTO audit_log VALUES(453,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 21:51:55');
INSERT INTO audit_log VALUES(454,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 21:51:55');
INSERT INTO audit_log VALUES(455,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 21:51:55');
INSERT INTO audit_log VALUES(456,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 21:56:55');
INSERT INTO audit_log VALUES(457,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 21:56:55');
INSERT INTO audit_log VALUES(458,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 21:56:55');
INSERT INTO audit_log VALUES(459,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 21:56:55');
INSERT INTO audit_log VALUES(460,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 21:56:55');
INSERT INTO audit_log VALUES(461,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 22:01:55');
INSERT INTO audit_log VALUES(462,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 22:01:55');
INSERT INTO audit_log VALUES(463,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 22:01:55');
INSERT INTO audit_log VALUES(464,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 22:01:55');
INSERT INTO audit_log VALUES(465,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 22:01:55');
INSERT INTO audit_log VALUES(466,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 22:06:55');
INSERT INTO audit_log VALUES(467,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 22:06:55');
INSERT INTO audit_log VALUES(468,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 22:06:55');
INSERT INTO audit_log VALUES(469,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 22:06:55');
INSERT INTO audit_log VALUES(470,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 22:06:55');
INSERT INTO audit_log VALUES(471,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 22:11:55');
INSERT INTO audit_log VALUES(472,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 22:11:55');
INSERT INTO audit_log VALUES(473,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 22:11:55');
INSERT INTO audit_log VALUES(474,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 22:11:55');
INSERT INTO audit_log VALUES(475,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 22:11:55');
INSERT INTO audit_log VALUES(476,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 22:16:55');
INSERT INTO audit_log VALUES(477,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 22:16:55');
INSERT INTO audit_log VALUES(478,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 22:16:55');
INSERT INTO audit_log VALUES(479,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 22:16:55');
INSERT INTO audit_log VALUES(480,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 22:16:55');
INSERT INTO audit_log VALUES(481,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 22:21:55');
INSERT INTO audit_log VALUES(482,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 22:21:55');
INSERT INTO audit_log VALUES(483,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 22:21:55');
INSERT INTO audit_log VALUES(484,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 22:21:55');
INSERT INTO audit_log VALUES(485,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 22:21:55');
INSERT INTO audit_log VALUES(486,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 22:26:55');
INSERT INTO audit_log VALUES(487,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 22:26:55');
INSERT INTO audit_log VALUES(488,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 22:26:55');
INSERT INTO audit_log VALUES(489,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 22:26:55');
INSERT INTO audit_log VALUES(490,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 22:26:55');
INSERT INTO audit_log VALUES(491,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 22:31:55');
INSERT INTO audit_log VALUES(492,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 22:31:55');
INSERT INTO audit_log VALUES(493,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 22:31:55');
INSERT INTO audit_log VALUES(494,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 22:31:55');
INSERT INTO audit_log VALUES(495,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 22:31:55');
INSERT INTO audit_log VALUES(496,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 22:36:55');
INSERT INTO audit_log VALUES(497,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 22:36:55');
INSERT INTO audit_log VALUES(498,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 22:36:55');
INSERT INTO audit_log VALUES(499,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 22:36:55');
INSERT INTO audit_log VALUES(500,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 22:36:55');
INSERT INTO audit_log VALUES(501,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 22:41:55');
INSERT INTO audit_log VALUES(502,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 22:41:55');
INSERT INTO audit_log VALUES(503,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 22:41:55');
INSERT INTO audit_log VALUES(504,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 22:41:55');
INSERT INTO audit_log VALUES(505,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 22:41:55');
INSERT INTO audit_log VALUES(506,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 22:46:55');
INSERT INTO audit_log VALUES(507,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 22:46:55');
INSERT INTO audit_log VALUES(508,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 22:46:55');
INSERT INTO audit_log VALUES(509,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 22:46:55');
INSERT INTO audit_log VALUES(510,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 22:46:55');
INSERT INTO audit_log VALUES(511,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 22:51:55');
INSERT INTO audit_log VALUES(512,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 22:51:55');
INSERT INTO audit_log VALUES(513,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 22:51:55');
INSERT INTO audit_log VALUES(514,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 22:51:55');
INSERT INTO audit_log VALUES(515,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 22:51:55');
INSERT INTO audit_log VALUES(516,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 22:56:55');
INSERT INTO audit_log VALUES(517,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 22:56:55');
INSERT INTO audit_log VALUES(518,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 22:56:55');
INSERT INTO audit_log VALUES(519,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 22:56:55');
INSERT INTO audit_log VALUES(520,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 22:56:55');
INSERT INTO audit_log VALUES(521,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 23:01:55');
INSERT INTO audit_log VALUES(522,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 23:01:55');
INSERT INTO audit_log VALUES(523,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 23:01:55');
INSERT INTO audit_log VALUES(524,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 23:01:55');
INSERT INTO audit_log VALUES(525,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 23:01:55');
INSERT INTO audit_log VALUES(526,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 23:06:55');
INSERT INTO audit_log VALUES(527,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 23:06:55');
INSERT INTO audit_log VALUES(528,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 23:06:55');
INSERT INTO audit_log VALUES(529,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 23:06:55');
INSERT INTO audit_log VALUES(530,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 23:06:55');
INSERT INTO audit_log VALUES(531,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 23:11:55');
INSERT INTO audit_log VALUES(532,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 23:11:55');
INSERT INTO audit_log VALUES(533,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 23:11:55');
INSERT INTO audit_log VALUES(534,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 23:11:55');
INSERT INTO audit_log VALUES(535,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 23:11:55');
INSERT INTO audit_log VALUES(536,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 23:16:55');
INSERT INTO audit_log VALUES(537,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 23:16:55');
INSERT INTO audit_log VALUES(538,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 23:16:55');
INSERT INTO audit_log VALUES(539,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 23:16:55');
INSERT INTO audit_log VALUES(540,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 23:16:55');
INSERT INTO audit_log VALUES(541,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 23:18:36');
INSERT INTO audit_log VALUES(542,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 23:18:36');
INSERT INTO audit_log VALUES(543,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 23:18:36');
INSERT INTO audit_log VALUES(544,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 23:18:36');
INSERT INTO audit_log VALUES(545,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 23:18:36');
INSERT INTO audit_log VALUES(546,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 23:22:31');
INSERT INTO audit_log VALUES(547,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 23:22:31');
INSERT INTO audit_log VALUES(548,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 23:22:31');
INSERT INTO audit_log VALUES(549,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 23:22:31');
INSERT INTO audit_log VALUES(550,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 23:22:31');
INSERT INTO audit_log VALUES(551,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 23:28:34');
INSERT INTO audit_log VALUES(552,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 23:28:34');
INSERT INTO audit_log VALUES(553,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 23:28:34');
INSERT INTO audit_log VALUES(554,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 23:28:34');
INSERT INTO audit_log VALUES(555,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 23:28:34');
INSERT INTO audit_log VALUES(556,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 23:37:36');
INSERT INTO audit_log VALUES(557,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 23:37:36');
INSERT INTO audit_log VALUES(558,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 23:37:36');
INSERT INTO audit_log VALUES(559,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-09 23:37:36');
INSERT INTO audit_log VALUES(560,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 23:37:36');
INSERT INTO audit_log VALUES(561,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 23:37:36');
INSERT INTO audit_log VALUES(562,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 23:42:15');
INSERT INTO audit_log VALUES(563,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 23:42:15');
INSERT INTO audit_log VALUES(564,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 23:42:15');
INSERT INTO audit_log VALUES(565,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-09 23:42:15');
INSERT INTO audit_log VALUES(566,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 23:42:15');
INSERT INTO audit_log VALUES(567,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 23:42:15');
INSERT INTO audit_log VALUES(568,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-09 23:55:57');
INSERT INTO audit_log VALUES(569,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-09 23:55:57');
INSERT INTO audit_log VALUES(570,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-09 23:55:57');
INSERT INTO audit_log VALUES(571,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-09 23:55:57');
INSERT INTO audit_log VALUES(572,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-09 23:55:57');
INSERT INTO audit_log VALUES(573,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-09 23:55:57');
INSERT INTO audit_log VALUES(574,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:00:57');
INSERT INTO audit_log VALUES(575,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:00:57');
INSERT INTO audit_log VALUES(576,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:00:58');
INSERT INTO audit_log VALUES(577,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:00:58');
INSERT INTO audit_log VALUES(578,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:00:58');
INSERT INTO audit_log VALUES(579,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:00:58');
INSERT INTO audit_log VALUES(580,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:05:58');
INSERT INTO audit_log VALUES(581,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:05:58');
INSERT INTO audit_log VALUES(582,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:05:58');
INSERT INTO audit_log VALUES(583,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:05:58');
INSERT INTO audit_log VALUES(584,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:05:58');
INSERT INTO audit_log VALUES(585,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:05:58');
INSERT INTO audit_log VALUES(586,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:09:57');
INSERT INTO audit_log VALUES(587,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:09:57');
INSERT INTO audit_log VALUES(588,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:09:57');
INSERT INTO audit_log VALUES(589,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:09:57');
INSERT INTO audit_log VALUES(590,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:09:57');
INSERT INTO audit_log VALUES(591,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:09:57');
INSERT INTO audit_log VALUES(592,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:12:13');
INSERT INTO audit_log VALUES(593,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:12:13');
INSERT INTO audit_log VALUES(594,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:12:13');
INSERT INTO audit_log VALUES(595,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:12:13');
INSERT INTO audit_log VALUES(596,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:12:13');
INSERT INTO audit_log VALUES(597,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:12:13');
INSERT INTO audit_log VALUES(598,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:14:47');
INSERT INTO audit_log VALUES(599,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:14:47');
INSERT INTO audit_log VALUES(600,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:14:47');
INSERT INTO audit_log VALUES(601,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:14:47');
INSERT INTO audit_log VALUES(602,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:14:47');
INSERT INTO audit_log VALUES(603,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:14:47');
INSERT INTO audit_log VALUES(604,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:16:35');
INSERT INTO audit_log VALUES(605,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:16:35');
INSERT INTO audit_log VALUES(606,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:16:35');
INSERT INTO audit_log VALUES(607,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:16:35');
INSERT INTO audit_log VALUES(608,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:16:35');
INSERT INTO audit_log VALUES(609,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:16:35');
INSERT INTO audit_log VALUES(610,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:17:44');
INSERT INTO audit_log VALUES(611,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:17:44');
INSERT INTO audit_log VALUES(612,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:17:44');
INSERT INTO audit_log VALUES(613,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:17:44');
INSERT INTO audit_log VALUES(614,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:17:44');
INSERT INTO audit_log VALUES(615,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:17:44');
INSERT INTO audit_log VALUES(616,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:20:12');
INSERT INTO audit_log VALUES(617,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:20:12');
INSERT INTO audit_log VALUES(618,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:20:12');
INSERT INTO audit_log VALUES(619,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:20:12');
INSERT INTO audit_log VALUES(620,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:20:12');
INSERT INTO audit_log VALUES(621,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:20:12');
INSERT INTO audit_log VALUES(622,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:23:30');
INSERT INTO audit_log VALUES(623,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:23:30');
INSERT INTO audit_log VALUES(624,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:23:30');
INSERT INTO audit_log VALUES(625,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:23:30');
INSERT INTO audit_log VALUES(626,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:23:30');
INSERT INTO audit_log VALUES(627,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:23:30');
INSERT INTO audit_log VALUES(628,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:28:30');
INSERT INTO audit_log VALUES(629,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:28:30');
INSERT INTO audit_log VALUES(630,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:28:30');
INSERT INTO audit_log VALUES(631,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:28:30');
INSERT INTO audit_log VALUES(632,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:28:30');
INSERT INTO audit_log VALUES(633,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:28:30');
INSERT INTO audit_log VALUES(634,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:31:03');
INSERT INTO audit_log VALUES(635,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:31:03');
INSERT INTO audit_log VALUES(636,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:31:03');
INSERT INTO audit_log VALUES(637,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:31:03');
INSERT INTO audit_log VALUES(638,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:31:03');
INSERT INTO audit_log VALUES(639,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:31:03');
INSERT INTO audit_log VALUES(640,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:33:30');
INSERT INTO audit_log VALUES(641,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:33:30');
INSERT INTO audit_log VALUES(642,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:33:30');
INSERT INTO audit_log VALUES(643,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:33:30');
INSERT INTO audit_log VALUES(644,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:33:30');
INSERT INTO audit_log VALUES(645,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:33:30');
INSERT INTO audit_log VALUES(646,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:34:53');
INSERT INTO audit_log VALUES(647,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:34:53');
INSERT INTO audit_log VALUES(648,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:34:53');
INSERT INTO audit_log VALUES(649,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:34:53');
INSERT INTO audit_log VALUES(650,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:34:53');
INSERT INTO audit_log VALUES(651,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:34:53');
INSERT INTO audit_log VALUES(652,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:35:32');
INSERT INTO audit_log VALUES(653,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:35:32');
INSERT INTO audit_log VALUES(654,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:35:32');
INSERT INTO audit_log VALUES(655,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:35:32');
INSERT INTO audit_log VALUES(656,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:35:32');
INSERT INTO audit_log VALUES(657,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:35:32');
INSERT INTO audit_log VALUES(658,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:38:30');
INSERT INTO audit_log VALUES(659,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:38:30');
INSERT INTO audit_log VALUES(660,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:38:30');
INSERT INTO audit_log VALUES(661,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:38:30');
INSERT INTO audit_log VALUES(662,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:38:30');
INSERT INTO audit_log VALUES(663,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:38:30');
INSERT INTO audit_log VALUES(664,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:43:10');
INSERT INTO audit_log VALUES(665,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:43:10');
INSERT INTO audit_log VALUES(666,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:43:10');
INSERT INTO audit_log VALUES(667,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:43:10');
INSERT INTO audit_log VALUES(668,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:43:10');
INSERT INTO audit_log VALUES(669,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:43:10');
INSERT INTO audit_log VALUES(670,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:46:56');
INSERT INTO audit_log VALUES(671,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:46:56');
INSERT INTO audit_log VALUES(672,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:46:56');
INSERT INTO audit_log VALUES(673,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:46:56');
INSERT INTO audit_log VALUES(674,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:46:56');
INSERT INTO audit_log VALUES(675,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:46:56');
INSERT INTO audit_log VALUES(676,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:51:42');
INSERT INTO audit_log VALUES(677,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:51:42');
INSERT INTO audit_log VALUES(678,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:51:42');
INSERT INTO audit_log VALUES(679,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:51:42');
INSERT INTO audit_log VALUES(680,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:51:42');
INSERT INTO audit_log VALUES(681,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:51:42');
INSERT INTO audit_log VALUES(682,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:54:43');
INSERT INTO audit_log VALUES(683,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:54:43');
INSERT INTO audit_log VALUES(684,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:54:43');
INSERT INTO audit_log VALUES(685,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:54:43');
INSERT INTO audit_log VALUES(686,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:54:43');
INSERT INTO audit_log VALUES(687,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:54:43');
INSERT INTO audit_log VALUES(688,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:56:35');
INSERT INTO audit_log VALUES(689,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:56:35');
INSERT INTO audit_log VALUES(690,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:56:36');
INSERT INTO audit_log VALUES(691,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:56:36');
INSERT INTO audit_log VALUES(692,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:56:36');
INSERT INTO audit_log VALUES(693,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:56:36');
INSERT INTO audit_log VALUES(694,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 00:58:59');
INSERT INTO audit_log VALUES(695,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 00:58:59');
INSERT INTO audit_log VALUES(696,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 00:58:59');
INSERT INTO audit_log VALUES(697,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 00:58:59');
INSERT INTO audit_log VALUES(698,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 00:58:59');
INSERT INTO audit_log VALUES(699,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 00:58:59');
INSERT INTO audit_log VALUES(700,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 01:03:03');
INSERT INTO audit_log VALUES(701,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 01:03:03');
INSERT INTO audit_log VALUES(702,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 01:03:03');
INSERT INTO audit_log VALUES(703,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 01:03:03');
INSERT INTO audit_log VALUES(704,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 01:03:03');
INSERT INTO audit_log VALUES(705,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 01:03:03');
INSERT INTO audit_log VALUES(706,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 01:08:33');
INSERT INTO audit_log VALUES(707,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 01:08:33');
INSERT INTO audit_log VALUES(708,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 01:08:33');
INSERT INTO audit_log VALUES(709,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 01:08:33');
INSERT INTO audit_log VALUES(710,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 01:08:33');
INSERT INTO audit_log VALUES(711,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 01:08:33');
INSERT INTO audit_log VALUES(712,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 01:15:16');
INSERT INTO audit_log VALUES(713,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 01:15:16');
INSERT INTO audit_log VALUES(714,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 01:15:16');
INSERT INTO audit_log VALUES(715,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 01:15:16');
INSERT INTO audit_log VALUES(716,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 01:15:16');
INSERT INTO audit_log VALUES(717,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 01:15:16');
INSERT INTO audit_log VALUES(718,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 01:20:50');
INSERT INTO audit_log VALUES(719,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 01:20:50');
INSERT INTO audit_log VALUES(720,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 01:20:50');
INSERT INTO audit_log VALUES(721,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 01:20:50');
INSERT INTO audit_log VALUES(722,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 01:20:50');
INSERT INTO audit_log VALUES(723,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 01:20:50');
INSERT INTO audit_log VALUES(724,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 01:22:07');
INSERT INTO audit_log VALUES(725,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 01:22:07');
INSERT INTO audit_log VALUES(726,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 01:22:07');
INSERT INTO audit_log VALUES(727,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 01:22:07');
INSERT INTO audit_log VALUES(728,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 01:22:07');
INSERT INTO audit_log VALUES(729,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 01:22:07');
INSERT INTO audit_log VALUES(730,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 01:32:05');
INSERT INTO audit_log VALUES(731,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 01:32:05');
INSERT INTO audit_log VALUES(732,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 01:32:05');
INSERT INTO audit_log VALUES(733,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 01:32:05');
INSERT INTO audit_log VALUES(734,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 01:32:05');
INSERT INTO audit_log VALUES(735,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 01:32:05');
INSERT INTO audit_log VALUES(736,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 01:37:05');
INSERT INTO audit_log VALUES(737,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 01:37:05');
INSERT INTO audit_log VALUES(738,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 01:37:05');
INSERT INTO audit_log VALUES(739,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 01:37:05');
INSERT INTO audit_log VALUES(740,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 01:37:05');
INSERT INTO audit_log VALUES(741,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 01:37:05');
INSERT INTO audit_log VALUES(742,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 01:41:03');
INSERT INTO audit_log VALUES(743,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 01:41:03');
INSERT INTO audit_log VALUES(744,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 01:41:03');
INSERT INTO audit_log VALUES(745,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 01:41:03');
INSERT INTO audit_log VALUES(746,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 01:41:03');
INSERT INTO audit_log VALUES(747,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 01:41:03');
INSERT INTO audit_log VALUES(748,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 01:43:20');
INSERT INTO audit_log VALUES(749,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 01:43:20');
INSERT INTO audit_log VALUES(750,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 01:43:20');
INSERT INTO audit_log VALUES(751,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 01:43:20');
INSERT INTO audit_log VALUES(752,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 01:43:20');
INSERT INTO audit_log VALUES(753,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 01:43:20');
INSERT INTO audit_log VALUES(754,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 01:57:06');
INSERT INTO audit_log VALUES(755,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 01:57:06');
INSERT INTO audit_log VALUES(756,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 01:57:06');
INSERT INTO audit_log VALUES(757,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 01:57:06');
INSERT INTO audit_log VALUES(758,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 01:57:06');
INSERT INTO audit_log VALUES(759,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 01:57:06');
INSERT INTO audit_log VALUES(760,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 01:58:02');
INSERT INTO audit_log VALUES(761,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 01:58:02');
INSERT INTO audit_log VALUES(762,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 01:58:02');
INSERT INTO audit_log VALUES(763,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 01:58:02');
INSERT INTO audit_log VALUES(764,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 01:58:02');
INSERT INTO audit_log VALUES(765,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 01:58:02');
INSERT INTO audit_log VALUES(766,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 02:03:25');
INSERT INTO audit_log VALUES(767,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 02:03:25');
INSERT INTO audit_log VALUES(768,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 02:03:25');
INSERT INTO audit_log VALUES(769,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 02:03:25');
INSERT INTO audit_log VALUES(770,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 02:03:25');
INSERT INTO audit_log VALUES(771,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 02:03:25');
INSERT INTO audit_log VALUES(772,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 02:10:54');
INSERT INTO audit_log VALUES(773,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 02:10:54');
INSERT INTO audit_log VALUES(774,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 02:10:54');
INSERT INTO audit_log VALUES(775,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 02:10:54');
INSERT INTO audit_log VALUES(776,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 02:10:54');
INSERT INTO audit_log VALUES(777,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 02:10:54');
INSERT INTO audit_log VALUES(778,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 02:14:27');
INSERT INTO audit_log VALUES(779,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 02:14:27');
INSERT INTO audit_log VALUES(780,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 02:14:27');
INSERT INTO audit_log VALUES(781,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 02:14:27');
INSERT INTO audit_log VALUES(782,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 02:14:27');
INSERT INTO audit_log VALUES(783,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 02:14:27');
INSERT INTO audit_log VALUES(784,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 02:18:22');
INSERT INTO audit_log VALUES(785,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 02:18:22');
INSERT INTO audit_log VALUES(786,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 02:18:22');
INSERT INTO audit_log VALUES(787,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 02:18:22');
INSERT INTO audit_log VALUES(788,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 02:18:22');
INSERT INTO audit_log VALUES(789,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 02:18:22');
INSERT INTO audit_log VALUES(790,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 02:27:40');
INSERT INTO audit_log VALUES(791,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 02:27:40');
INSERT INTO audit_log VALUES(792,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 02:27:40');
INSERT INTO audit_log VALUES(793,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 02:27:40');
INSERT INTO audit_log VALUES(794,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 02:27:40');
INSERT INTO audit_log VALUES(795,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 02:27:40');
INSERT INTO audit_log VALUES(796,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 02:32:40');
INSERT INTO audit_log VALUES(797,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 02:32:40');
INSERT INTO audit_log VALUES(798,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 02:32:40');
INSERT INTO audit_log VALUES(799,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 02:32:40');
INSERT INTO audit_log VALUES(800,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 02:32:40');
INSERT INTO audit_log VALUES(801,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 02:32:40');
INSERT INTO audit_log VALUES(802,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 02:37:40');
INSERT INTO audit_log VALUES(803,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 02:37:40');
INSERT INTO audit_log VALUES(804,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 02:37:40');
INSERT INTO audit_log VALUES(805,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 02:37:40');
INSERT INTO audit_log VALUES(806,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 02:37:40');
INSERT INTO audit_log VALUES(807,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 02:37:40');
INSERT INTO audit_log VALUES(808,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 02:42:40');
INSERT INTO audit_log VALUES(809,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 02:42:40');
INSERT INTO audit_log VALUES(810,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 02:42:40');
INSERT INTO audit_log VALUES(811,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 02:42:40');
INSERT INTO audit_log VALUES(812,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 02:42:40');
INSERT INTO audit_log VALUES(813,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 02:42:40');
INSERT INTO audit_log VALUES(814,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 02:47:40');
INSERT INTO audit_log VALUES(815,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 02:47:40');
INSERT INTO audit_log VALUES(816,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 02:47:40');
INSERT INTO audit_log VALUES(817,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 02:47:40');
INSERT INTO audit_log VALUES(818,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 02:47:40');
INSERT INTO audit_log VALUES(819,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 02:47:40');
INSERT INTO audit_log VALUES(820,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 02:52:40');
INSERT INTO audit_log VALUES(821,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 02:52:40');
INSERT INTO audit_log VALUES(822,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 02:52:40');
INSERT INTO audit_log VALUES(823,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 02:52:40');
INSERT INTO audit_log VALUES(824,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 02:52:40');
INSERT INTO audit_log VALUES(825,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 02:52:40');
INSERT INTO audit_log VALUES(826,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 02:57:40');
INSERT INTO audit_log VALUES(827,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 02:57:40');
INSERT INTO audit_log VALUES(828,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 02:57:40');
INSERT INTO audit_log VALUES(829,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 02:57:40');
INSERT INTO audit_log VALUES(830,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 02:57:40');
INSERT INTO audit_log VALUES(831,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 02:57:40');
INSERT INTO audit_log VALUES(832,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 03:02:40');
INSERT INTO audit_log VALUES(833,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 03:02:40');
INSERT INTO audit_log VALUES(834,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 03:02:40');
INSERT INTO audit_log VALUES(835,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 03:02:40');
INSERT INTO audit_log VALUES(836,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 03:02:40');
INSERT INTO audit_log VALUES(837,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 03:02:40');
INSERT INTO audit_log VALUES(838,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 03:07:40');
INSERT INTO audit_log VALUES(839,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 03:07:40');
INSERT INTO audit_log VALUES(840,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 03:07:40');
INSERT INTO audit_log VALUES(841,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 03:07:40');
INSERT INTO audit_log VALUES(842,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 03:07:40');
INSERT INTO audit_log VALUES(843,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 03:07:40');
INSERT INTO audit_log VALUES(844,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 03:12:40');
INSERT INTO audit_log VALUES(845,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 03:12:40');
INSERT INTO audit_log VALUES(846,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 03:12:40');
INSERT INTO audit_log VALUES(847,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 03:12:40');
INSERT INTO audit_log VALUES(848,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 03:12:40');
INSERT INTO audit_log VALUES(849,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 03:12:40');
INSERT INTO audit_log VALUES(850,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 03:17:40');
INSERT INTO audit_log VALUES(851,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 03:17:40');
INSERT INTO audit_log VALUES(852,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 03:17:40');
INSERT INTO audit_log VALUES(853,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 03:17:40');
INSERT INTO audit_log VALUES(854,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 03:17:40');
INSERT INTO audit_log VALUES(855,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 03:17:40');
INSERT INTO audit_log VALUES(856,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 03:22:40');
INSERT INTO audit_log VALUES(857,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 03:22:40');
INSERT INTO audit_log VALUES(858,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 03:22:40');
INSERT INTO audit_log VALUES(859,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 03:22:40');
INSERT INTO audit_log VALUES(860,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 03:22:40');
INSERT INTO audit_log VALUES(861,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 03:22:40');
INSERT INTO audit_log VALUES(862,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 03:27:40');
INSERT INTO audit_log VALUES(863,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 03:27:40');
INSERT INTO audit_log VALUES(864,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 03:27:40');
INSERT INTO audit_log VALUES(865,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 03:27:40');
INSERT INTO audit_log VALUES(866,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 03:27:40');
INSERT INTO audit_log VALUES(867,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 03:27:40');
INSERT INTO audit_log VALUES(868,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 03:32:40');
INSERT INTO audit_log VALUES(869,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 03:32:40');
INSERT INTO audit_log VALUES(870,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 03:32:40');
INSERT INTO audit_log VALUES(871,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 03:32:40');
INSERT INTO audit_log VALUES(872,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 03:32:40');
INSERT INTO audit_log VALUES(873,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 03:32:40');
INSERT INTO audit_log VALUES(874,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 03:37:40');
INSERT INTO audit_log VALUES(875,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 03:37:40');
INSERT INTO audit_log VALUES(876,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 03:37:40');
INSERT INTO audit_log VALUES(877,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 03:37:40');
INSERT INTO audit_log VALUES(878,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 03:37:40');
INSERT INTO audit_log VALUES(879,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 03:37:40');
INSERT INTO audit_log VALUES(880,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 03:42:40');
INSERT INTO audit_log VALUES(881,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 03:42:40');
INSERT INTO audit_log VALUES(882,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 03:42:40');
INSERT INTO audit_log VALUES(883,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 03:42:40');
INSERT INTO audit_log VALUES(884,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 03:42:40');
INSERT INTO audit_log VALUES(885,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 03:42:40');
INSERT INTO audit_log VALUES(886,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 03:47:40');
INSERT INTO audit_log VALUES(887,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 03:47:40');
INSERT INTO audit_log VALUES(888,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 03:47:40');
INSERT INTO audit_log VALUES(889,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 03:47:40');
INSERT INTO audit_log VALUES(890,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 03:47:40');
INSERT INTO audit_log VALUES(891,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 03:47:40');
INSERT INTO audit_log VALUES(892,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 03:52:40');
INSERT INTO audit_log VALUES(893,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 03:52:40');
INSERT INTO audit_log VALUES(894,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 03:52:40');
INSERT INTO audit_log VALUES(895,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 03:52:40');
INSERT INTO audit_log VALUES(896,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 03:52:40');
INSERT INTO audit_log VALUES(897,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 03:52:40');
INSERT INTO audit_log VALUES(898,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 03:57:40');
INSERT INTO audit_log VALUES(899,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 03:57:40');
INSERT INTO audit_log VALUES(900,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 03:57:40');
INSERT INTO audit_log VALUES(901,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 03:57:41');
INSERT INTO audit_log VALUES(902,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 03:57:41');
INSERT INTO audit_log VALUES(903,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 03:57:41');
INSERT INTO audit_log VALUES(904,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 04:02:41');
INSERT INTO audit_log VALUES(905,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 04:02:41');
INSERT INTO audit_log VALUES(906,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 04:02:41');
INSERT INTO audit_log VALUES(907,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 04:02:41');
INSERT INTO audit_log VALUES(908,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 04:02:41');
INSERT INTO audit_log VALUES(909,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 04:02:41');
INSERT INTO audit_log VALUES(910,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 04:07:41');
INSERT INTO audit_log VALUES(911,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 04:07:41');
INSERT INTO audit_log VALUES(912,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 04:07:41');
INSERT INTO audit_log VALUES(913,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 04:07:41');
INSERT INTO audit_log VALUES(914,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 04:07:41');
INSERT INTO audit_log VALUES(915,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 04:07:41');
INSERT INTO audit_log VALUES(916,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 04:12:41');
INSERT INTO audit_log VALUES(917,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 04:12:41');
INSERT INTO audit_log VALUES(918,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 04:12:41');
INSERT INTO audit_log VALUES(919,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 04:12:41');
INSERT INTO audit_log VALUES(920,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 04:12:41');
INSERT INTO audit_log VALUES(921,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 04:12:41');
INSERT INTO audit_log VALUES(922,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 04:17:41');
INSERT INTO audit_log VALUES(923,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 04:17:41');
INSERT INTO audit_log VALUES(924,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 04:17:41');
INSERT INTO audit_log VALUES(925,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 04:17:41');
INSERT INTO audit_log VALUES(926,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 04:17:41');
INSERT INTO audit_log VALUES(927,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 04:17:41');
INSERT INTO audit_log VALUES(928,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 04:22:41');
INSERT INTO audit_log VALUES(929,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 04:22:41');
INSERT INTO audit_log VALUES(930,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 04:22:41');
INSERT INTO audit_log VALUES(931,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 04:22:41');
INSERT INTO audit_log VALUES(932,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 04:22:41');
INSERT INTO audit_log VALUES(933,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 04:22:41');
INSERT INTO audit_log VALUES(934,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 04:27:41');
INSERT INTO audit_log VALUES(935,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 04:27:41');
INSERT INTO audit_log VALUES(936,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 04:27:41');
INSERT INTO audit_log VALUES(937,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 04:27:41');
INSERT INTO audit_log VALUES(938,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 04:27:41');
INSERT INTO audit_log VALUES(939,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 04:27:41');
INSERT INTO audit_log VALUES(940,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 04:32:41');
INSERT INTO audit_log VALUES(941,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 04:32:41');
INSERT INTO audit_log VALUES(942,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 04:32:41');
INSERT INTO audit_log VALUES(943,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 04:32:41');
INSERT INTO audit_log VALUES(944,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 04:32:41');
INSERT INTO audit_log VALUES(945,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 04:32:41');
INSERT INTO audit_log VALUES(946,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 04:37:41');
INSERT INTO audit_log VALUES(947,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 04:37:41');
INSERT INTO audit_log VALUES(948,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 04:37:41');
INSERT INTO audit_log VALUES(949,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 04:37:41');
INSERT INTO audit_log VALUES(950,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 04:37:41');
INSERT INTO audit_log VALUES(951,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 04:37:41');
INSERT INTO audit_log VALUES(952,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 04:42:41');
INSERT INTO audit_log VALUES(953,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 04:42:41');
INSERT INTO audit_log VALUES(954,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 04:42:41');
INSERT INTO audit_log VALUES(955,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 04:42:41');
INSERT INTO audit_log VALUES(956,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 04:42:41');
INSERT INTO audit_log VALUES(957,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 04:42:41');
INSERT INTO audit_log VALUES(958,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 04:47:41');
INSERT INTO audit_log VALUES(959,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 04:47:41');
INSERT INTO audit_log VALUES(960,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 04:47:41');
INSERT INTO audit_log VALUES(961,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 04:47:41');
INSERT INTO audit_log VALUES(962,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 04:47:41');
INSERT INTO audit_log VALUES(963,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 04:47:41');
INSERT INTO audit_log VALUES(964,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 04:52:41');
INSERT INTO audit_log VALUES(965,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 04:52:41');
INSERT INTO audit_log VALUES(966,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 04:52:41');
INSERT INTO audit_log VALUES(967,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 04:52:41');
INSERT INTO audit_log VALUES(968,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 04:52:41');
INSERT INTO audit_log VALUES(969,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 04:52:41');
INSERT INTO audit_log VALUES(970,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 04:57:41');
INSERT INTO audit_log VALUES(971,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 04:57:41');
INSERT INTO audit_log VALUES(972,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 04:57:41');
INSERT INTO audit_log VALUES(973,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 04:57:41');
INSERT INTO audit_log VALUES(974,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 04:57:41');
INSERT INTO audit_log VALUES(975,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 04:57:41');
INSERT INTO audit_log VALUES(976,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 05:02:41');
INSERT INTO audit_log VALUES(977,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 05:02:41');
INSERT INTO audit_log VALUES(978,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 05:02:41');
INSERT INTO audit_log VALUES(979,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 05:02:41');
INSERT INTO audit_log VALUES(980,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 05:02:41');
INSERT INTO audit_log VALUES(981,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 05:02:41');
INSERT INTO audit_log VALUES(982,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 05:07:41');
INSERT INTO audit_log VALUES(983,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 05:07:41');
INSERT INTO audit_log VALUES(984,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 05:07:41');
INSERT INTO audit_log VALUES(985,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 05:07:41');
INSERT INTO audit_log VALUES(986,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 05:07:41');
INSERT INTO audit_log VALUES(987,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 05:07:41');
INSERT INTO audit_log VALUES(988,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 05:12:41');
INSERT INTO audit_log VALUES(989,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 05:12:41');
INSERT INTO audit_log VALUES(990,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 05:12:41');
INSERT INTO audit_log VALUES(991,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 05:12:41');
INSERT INTO audit_log VALUES(992,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 05:12:41');
INSERT INTO audit_log VALUES(993,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 05:12:41');
INSERT INTO audit_log VALUES(994,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 05:17:41');
INSERT INTO audit_log VALUES(995,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 05:17:41');
INSERT INTO audit_log VALUES(996,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 05:17:41');
INSERT INTO audit_log VALUES(997,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 05:17:41');
INSERT INTO audit_log VALUES(998,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 05:17:41');
INSERT INTO audit_log VALUES(999,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 05:17:41');
INSERT INTO audit_log VALUES(1000,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 05:22:41');
INSERT INTO audit_log VALUES(1001,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 05:22:41');
INSERT INTO audit_log VALUES(1002,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 05:22:41');
INSERT INTO audit_log VALUES(1003,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 05:22:41');
INSERT INTO audit_log VALUES(1004,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 05:22:41');
INSERT INTO audit_log VALUES(1005,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 05:22:41');
INSERT INTO audit_log VALUES(1006,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 05:27:41');
INSERT INTO audit_log VALUES(1007,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 05:27:41');
INSERT INTO audit_log VALUES(1008,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 05:27:41');
INSERT INTO audit_log VALUES(1009,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 05:27:41');
INSERT INTO audit_log VALUES(1010,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 05:27:41');
INSERT INTO audit_log VALUES(1011,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 05:27:41');
INSERT INTO audit_log VALUES(1012,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 05:32:41');
INSERT INTO audit_log VALUES(1013,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 05:32:41');
INSERT INTO audit_log VALUES(1014,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 05:32:41');
INSERT INTO audit_log VALUES(1015,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 05:32:41');
INSERT INTO audit_log VALUES(1016,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 05:32:41');
INSERT INTO audit_log VALUES(1017,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 05:32:41');
INSERT INTO audit_log VALUES(1018,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 05:37:41');
INSERT INTO audit_log VALUES(1019,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 05:37:41');
INSERT INTO audit_log VALUES(1020,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 05:37:41');
INSERT INTO audit_log VALUES(1021,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 05:37:41');
INSERT INTO audit_log VALUES(1022,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 05:37:41');
INSERT INTO audit_log VALUES(1023,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 05:37:41');
INSERT INTO audit_log VALUES(1024,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 05:42:41');
INSERT INTO audit_log VALUES(1025,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 05:42:41');
INSERT INTO audit_log VALUES(1026,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 05:42:41');
INSERT INTO audit_log VALUES(1027,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 05:42:41');
INSERT INTO audit_log VALUES(1028,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 05:42:41');
INSERT INTO audit_log VALUES(1029,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 05:42:41');
INSERT INTO audit_log VALUES(1030,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 05:47:41');
INSERT INTO audit_log VALUES(1031,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 05:47:41');
INSERT INTO audit_log VALUES(1032,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 05:47:41');
INSERT INTO audit_log VALUES(1033,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 05:47:41');
INSERT INTO audit_log VALUES(1034,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 05:47:41');
INSERT INTO audit_log VALUES(1035,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 05:47:41');
INSERT INTO audit_log VALUES(1036,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 05:52:41');
INSERT INTO audit_log VALUES(1037,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 05:52:41');
INSERT INTO audit_log VALUES(1038,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 05:52:41');
INSERT INTO audit_log VALUES(1039,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 05:52:41');
INSERT INTO audit_log VALUES(1040,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 05:52:41');
INSERT INTO audit_log VALUES(1041,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 05:52:41');
INSERT INTO audit_log VALUES(1042,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 05:57:41');
INSERT INTO audit_log VALUES(1043,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 05:57:41');
INSERT INTO audit_log VALUES(1044,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 05:57:41');
INSERT INTO audit_log VALUES(1045,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 05:57:41');
INSERT INTO audit_log VALUES(1046,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 05:57:41');
INSERT INTO audit_log VALUES(1047,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 05:57:41');
INSERT INTO audit_log VALUES(1048,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 06:02:41');
INSERT INTO audit_log VALUES(1049,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 06:02:41');
INSERT INTO audit_log VALUES(1050,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 06:02:41');
INSERT INTO audit_log VALUES(1051,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 06:02:41');
INSERT INTO audit_log VALUES(1052,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 06:02:41');
INSERT INTO audit_log VALUES(1053,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 06:02:42');
INSERT INTO audit_log VALUES(1054,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 06:07:42');
INSERT INTO audit_log VALUES(1055,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 06:07:42');
INSERT INTO audit_log VALUES(1056,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 06:07:42');
INSERT INTO audit_log VALUES(1057,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 06:07:42');
INSERT INTO audit_log VALUES(1058,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 06:07:42');
INSERT INTO audit_log VALUES(1059,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 06:07:42');
INSERT INTO audit_log VALUES(1060,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 06:12:42');
INSERT INTO audit_log VALUES(1061,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 06:12:42');
INSERT INTO audit_log VALUES(1062,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 06:12:42');
INSERT INTO audit_log VALUES(1063,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 06:12:42');
INSERT INTO audit_log VALUES(1064,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 06:12:42');
INSERT INTO audit_log VALUES(1065,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 06:12:42');
INSERT INTO audit_log VALUES(1066,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 06:17:42');
INSERT INTO audit_log VALUES(1067,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 06:17:42');
INSERT INTO audit_log VALUES(1068,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 06:17:42');
INSERT INTO audit_log VALUES(1069,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 06:17:42');
INSERT INTO audit_log VALUES(1070,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 06:17:42');
INSERT INTO audit_log VALUES(1071,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 06:17:42');
INSERT INTO audit_log VALUES(1072,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 06:22:42');
INSERT INTO audit_log VALUES(1073,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 06:22:42');
INSERT INTO audit_log VALUES(1074,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 06:22:42');
INSERT INTO audit_log VALUES(1075,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 06:22:42');
INSERT INTO audit_log VALUES(1076,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 06:22:42');
INSERT INTO audit_log VALUES(1077,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 06:22:42');
INSERT INTO audit_log VALUES(1078,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 06:27:42');
INSERT INTO audit_log VALUES(1079,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 06:27:42');
INSERT INTO audit_log VALUES(1080,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 06:27:42');
INSERT INTO audit_log VALUES(1081,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 06:27:42');
INSERT INTO audit_log VALUES(1082,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 06:27:42');
INSERT INTO audit_log VALUES(1083,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 06:27:42');
INSERT INTO audit_log VALUES(1084,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 06:32:42');
INSERT INTO audit_log VALUES(1085,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 06:32:42');
INSERT INTO audit_log VALUES(1086,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 06:32:42');
INSERT INTO audit_log VALUES(1087,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 06:32:42');
INSERT INTO audit_log VALUES(1088,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 06:32:42');
INSERT INTO audit_log VALUES(1089,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 06:32:42');
INSERT INTO audit_log VALUES(1090,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 06:37:42');
INSERT INTO audit_log VALUES(1091,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 06:37:42');
INSERT INTO audit_log VALUES(1092,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 06:37:42');
INSERT INTO audit_log VALUES(1093,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 06:37:42');
INSERT INTO audit_log VALUES(1094,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 06:37:42');
INSERT INTO audit_log VALUES(1095,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 06:37:42');
INSERT INTO audit_log VALUES(1096,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 06:42:42');
INSERT INTO audit_log VALUES(1097,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 06:42:42');
INSERT INTO audit_log VALUES(1098,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 06:42:42');
INSERT INTO audit_log VALUES(1099,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 06:42:42');
INSERT INTO audit_log VALUES(1100,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 06:42:42');
INSERT INTO audit_log VALUES(1101,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 06:42:42');
INSERT INTO audit_log VALUES(1102,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 06:47:42');
INSERT INTO audit_log VALUES(1103,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 06:47:42');
INSERT INTO audit_log VALUES(1104,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 06:47:42');
INSERT INTO audit_log VALUES(1105,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 06:47:42');
INSERT INTO audit_log VALUES(1106,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 06:47:42');
INSERT INTO audit_log VALUES(1107,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 06:47:42');
INSERT INTO audit_log VALUES(1108,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 06:52:42');
INSERT INTO audit_log VALUES(1109,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 06:52:42');
INSERT INTO audit_log VALUES(1110,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 06:52:42');
INSERT INTO audit_log VALUES(1111,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 06:52:42');
INSERT INTO audit_log VALUES(1112,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 06:52:42');
INSERT INTO audit_log VALUES(1113,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 06:52:42');
INSERT INTO audit_log VALUES(1114,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 06:57:42');
INSERT INTO audit_log VALUES(1115,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 06:57:42');
INSERT INTO audit_log VALUES(1116,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 06:57:42');
INSERT INTO audit_log VALUES(1117,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 06:57:42');
INSERT INTO audit_log VALUES(1118,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 06:57:42');
INSERT INTO audit_log VALUES(1119,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 06:57:42');
INSERT INTO audit_log VALUES(1120,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 07:02:42');
INSERT INTO audit_log VALUES(1121,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 07:02:42');
INSERT INTO audit_log VALUES(1122,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 07:02:42');
INSERT INTO audit_log VALUES(1123,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 07:02:42');
INSERT INTO audit_log VALUES(1124,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 07:02:42');
INSERT INTO audit_log VALUES(1125,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 07:02:42');
INSERT INTO audit_log VALUES(1126,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 07:07:42');
INSERT INTO audit_log VALUES(1127,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 07:07:42');
INSERT INTO audit_log VALUES(1128,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 07:07:42');
INSERT INTO audit_log VALUES(1129,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 07:07:42');
INSERT INTO audit_log VALUES(1130,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 07:07:42');
INSERT INTO audit_log VALUES(1131,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 07:07:42');
INSERT INTO audit_log VALUES(1132,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 07:12:42');
INSERT INTO audit_log VALUES(1133,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 07:12:42');
INSERT INTO audit_log VALUES(1134,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 07:12:42');
INSERT INTO audit_log VALUES(1135,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 07:12:42');
INSERT INTO audit_log VALUES(1136,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 07:12:42');
INSERT INTO audit_log VALUES(1137,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 07:12:42');
INSERT INTO audit_log VALUES(1138,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 07:17:42');
INSERT INTO audit_log VALUES(1139,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 07:17:42');
INSERT INTO audit_log VALUES(1140,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 07:17:42');
INSERT INTO audit_log VALUES(1141,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 07:17:42');
INSERT INTO audit_log VALUES(1142,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 07:17:42');
INSERT INTO audit_log VALUES(1143,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 07:17:42');
INSERT INTO audit_log VALUES(1144,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 07:22:42');
INSERT INTO audit_log VALUES(1145,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 07:22:42');
INSERT INTO audit_log VALUES(1146,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 07:22:42');
INSERT INTO audit_log VALUES(1147,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 07:22:42');
INSERT INTO audit_log VALUES(1148,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 07:22:42');
INSERT INTO audit_log VALUES(1149,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 07:22:42');
INSERT INTO audit_log VALUES(1150,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 07:27:42');
INSERT INTO audit_log VALUES(1151,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 07:27:42');
INSERT INTO audit_log VALUES(1152,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 07:27:42');
INSERT INTO audit_log VALUES(1153,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 07:27:42');
INSERT INTO audit_log VALUES(1154,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 07:27:42');
INSERT INTO audit_log VALUES(1155,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 07:27:42');
INSERT INTO audit_log VALUES(1156,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 07:32:42');
INSERT INTO audit_log VALUES(1157,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 07:32:42');
INSERT INTO audit_log VALUES(1158,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 07:32:42');
INSERT INTO audit_log VALUES(1159,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 07:32:42');
INSERT INTO audit_log VALUES(1160,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 07:32:42');
INSERT INTO audit_log VALUES(1161,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 07:32:42');
INSERT INTO audit_log VALUES(1162,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 07:37:42');
INSERT INTO audit_log VALUES(1163,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 07:37:42');
INSERT INTO audit_log VALUES(1164,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 07:37:42');
INSERT INTO audit_log VALUES(1165,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 07:37:42');
INSERT INTO audit_log VALUES(1166,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 07:37:42');
INSERT INTO audit_log VALUES(1167,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 07:37:42');
INSERT INTO audit_log VALUES(1168,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 07:42:42');
INSERT INTO audit_log VALUES(1169,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 07:42:42');
INSERT INTO audit_log VALUES(1170,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 07:42:42');
INSERT INTO audit_log VALUES(1171,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 07:42:42');
INSERT INTO audit_log VALUES(1172,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 07:42:42');
INSERT INTO audit_log VALUES(1173,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 07:42:42');
INSERT INTO audit_log VALUES(1174,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 07:47:42');
INSERT INTO audit_log VALUES(1175,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 07:47:42');
INSERT INTO audit_log VALUES(1176,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 07:47:42');
INSERT INTO audit_log VALUES(1177,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 07:47:42');
INSERT INTO audit_log VALUES(1178,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 07:47:42');
INSERT INTO audit_log VALUES(1179,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 07:47:42');
INSERT INTO audit_log VALUES(1180,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 07:52:42');
INSERT INTO audit_log VALUES(1181,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 07:52:42');
INSERT INTO audit_log VALUES(1182,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 07:52:42');
INSERT INTO audit_log VALUES(1183,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 07:52:42');
INSERT INTO audit_log VALUES(1184,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 07:52:42');
INSERT INTO audit_log VALUES(1185,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 07:52:42');
INSERT INTO audit_log VALUES(1186,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 07:57:42');
INSERT INTO audit_log VALUES(1187,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 07:57:42');
INSERT INTO audit_log VALUES(1188,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 07:57:42');
INSERT INTO audit_log VALUES(1189,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 07:57:42');
INSERT INTO audit_log VALUES(1190,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 07:57:42');
INSERT INTO audit_log VALUES(1191,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 07:57:42');
INSERT INTO audit_log VALUES(1192,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 08:02:42');
INSERT INTO audit_log VALUES(1193,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 08:02:42');
INSERT INTO audit_log VALUES(1194,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 08:02:42');
INSERT INTO audit_log VALUES(1195,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 08:02:42');
INSERT INTO audit_log VALUES(1196,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 08:02:42');
INSERT INTO audit_log VALUES(1197,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 08:02:42');
INSERT INTO audit_log VALUES(1198,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 08:07:42');
INSERT INTO audit_log VALUES(1199,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 08:07:42');
INSERT INTO audit_log VALUES(1200,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 08:07:42');
INSERT INTO audit_log VALUES(1201,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 08:07:42');
INSERT INTO audit_log VALUES(1202,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 08:07:42');
INSERT INTO audit_log VALUES(1203,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 08:07:42');
INSERT INTO audit_log VALUES(1204,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 08:12:42');
INSERT INTO audit_log VALUES(1205,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 08:12:42');
INSERT INTO audit_log VALUES(1206,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 08:12:42');
INSERT INTO audit_log VALUES(1207,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 08:12:42');
INSERT INTO audit_log VALUES(1208,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 08:12:42');
INSERT INTO audit_log VALUES(1209,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 08:12:42');
INSERT INTO audit_log VALUES(1210,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 08:17:42');
INSERT INTO audit_log VALUES(1211,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 08:17:42');
INSERT INTO audit_log VALUES(1212,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 08:17:42');
INSERT INTO audit_log VALUES(1213,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 08:17:42');
INSERT INTO audit_log VALUES(1214,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 08:17:42');
INSERT INTO audit_log VALUES(1215,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 08:17:42');
INSERT INTO audit_log VALUES(1216,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 08:22:42');
INSERT INTO audit_log VALUES(1217,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 08:22:42');
INSERT INTO audit_log VALUES(1218,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 08:22:42');
INSERT INTO audit_log VALUES(1219,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 08:22:43');
INSERT INTO audit_log VALUES(1220,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 08:22:43');
INSERT INTO audit_log VALUES(1221,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 08:22:43');
INSERT INTO audit_log VALUES(1222,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 08:27:43');
INSERT INTO audit_log VALUES(1223,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 08:27:43');
INSERT INTO audit_log VALUES(1224,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 08:27:43');
INSERT INTO audit_log VALUES(1225,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 08:27:43');
INSERT INTO audit_log VALUES(1226,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 08:27:43');
INSERT INTO audit_log VALUES(1227,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 08:27:43');
INSERT INTO audit_log VALUES(1228,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 08:32:43');
INSERT INTO audit_log VALUES(1229,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 08:32:43');
INSERT INTO audit_log VALUES(1230,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 08:32:43');
INSERT INTO audit_log VALUES(1231,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 08:32:43');
INSERT INTO audit_log VALUES(1232,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 08:32:43');
INSERT INTO audit_log VALUES(1233,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 08:32:43');
INSERT INTO audit_log VALUES(1234,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 08:37:43');
INSERT INTO audit_log VALUES(1235,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 08:37:43');
INSERT INTO audit_log VALUES(1236,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 08:37:43');
INSERT INTO audit_log VALUES(1237,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 08:37:43');
INSERT INTO audit_log VALUES(1238,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 08:37:43');
INSERT INTO audit_log VALUES(1239,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 08:37:43');
INSERT INTO audit_log VALUES(1240,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 08:42:43');
INSERT INTO audit_log VALUES(1241,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 08:42:43');
INSERT INTO audit_log VALUES(1242,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 08:42:43');
INSERT INTO audit_log VALUES(1243,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 08:42:43');
INSERT INTO audit_log VALUES(1244,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 08:42:43');
INSERT INTO audit_log VALUES(1245,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 08:42:43');
INSERT INTO audit_log VALUES(1246,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 08:47:43');
INSERT INTO audit_log VALUES(1247,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 08:47:43');
INSERT INTO audit_log VALUES(1248,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 08:47:43');
INSERT INTO audit_log VALUES(1249,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 08:47:43');
INSERT INTO audit_log VALUES(1250,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 08:47:43');
INSERT INTO audit_log VALUES(1251,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 08:47:43');
INSERT INTO audit_log VALUES(1252,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 08:52:43');
INSERT INTO audit_log VALUES(1253,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 08:52:43');
INSERT INTO audit_log VALUES(1254,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 08:52:43');
INSERT INTO audit_log VALUES(1255,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 08:52:43');
INSERT INTO audit_log VALUES(1256,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 08:52:43');
INSERT INTO audit_log VALUES(1257,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 08:52:43');
INSERT INTO audit_log VALUES(1258,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 08:57:43');
INSERT INTO audit_log VALUES(1259,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 08:57:43');
INSERT INTO audit_log VALUES(1260,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 08:57:43');
INSERT INTO audit_log VALUES(1261,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 08:57:43');
INSERT INTO audit_log VALUES(1262,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 08:57:43');
INSERT INTO audit_log VALUES(1263,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 08:57:43');
INSERT INTO audit_log VALUES(1264,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 09:06:47');
INSERT INTO audit_log VALUES(1265,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 09:06:47');
INSERT INTO audit_log VALUES(1266,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 09:06:47');
INSERT INTO audit_log VALUES(1267,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 09:06:47');
INSERT INTO audit_log VALUES(1268,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 09:06:47');
INSERT INTO audit_log VALUES(1269,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 09:06:47');
INSERT INTO audit_log VALUES(1270,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 09:12:22');
INSERT INTO audit_log VALUES(1271,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 09:12:22');
INSERT INTO audit_log VALUES(1272,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 09:12:22');
INSERT INTO audit_log VALUES(1273,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 09:12:22');
INSERT INTO audit_log VALUES(1274,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 09:12:22');
INSERT INTO audit_log VALUES(1275,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 09:12:22');
INSERT INTO audit_log VALUES(1276,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 09:16:52');
INSERT INTO audit_log VALUES(1277,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 09:16:52');
INSERT INTO audit_log VALUES(1278,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 09:16:52');
INSERT INTO audit_log VALUES(1279,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 09:16:52');
INSERT INTO audit_log VALUES(1280,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 09:16:52');
INSERT INTO audit_log VALUES(1281,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 09:16:52');
INSERT INTO audit_log VALUES(1282,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 09:19:46');
INSERT INTO audit_log VALUES(1283,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 09:19:46');
INSERT INTO audit_log VALUES(1284,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 09:19:46');
INSERT INTO audit_log VALUES(1285,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 09:19:46');
INSERT INTO audit_log VALUES(1286,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 09:19:46');
INSERT INTO audit_log VALUES(1287,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 09:19:46');
INSERT INTO audit_log VALUES(1288,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 09:20:51');
INSERT INTO audit_log VALUES(1289,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 09:20:51');
INSERT INTO audit_log VALUES(1290,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 09:20:51');
INSERT INTO audit_log VALUES(1291,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 09:20:51');
INSERT INTO audit_log VALUES(1292,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 09:20:51');
INSERT INTO audit_log VALUES(1293,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 09:20:51');
INSERT INTO audit_log VALUES(1294,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 09:24:22');
INSERT INTO audit_log VALUES(1295,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 09:24:22');
INSERT INTO audit_log VALUES(1296,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 09:24:22');
INSERT INTO audit_log VALUES(1297,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 09:24:22');
INSERT INTO audit_log VALUES(1298,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 09:24:22');
INSERT INTO audit_log VALUES(1299,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 09:24:22');
INSERT INTO audit_log VALUES(1300,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 09:36:40');
INSERT INTO audit_log VALUES(1301,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 09:36:40');
INSERT INTO audit_log VALUES(1302,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 09:36:40');
INSERT INTO audit_log VALUES(1303,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 09:36:40');
INSERT INTO audit_log VALUES(1304,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 09:36:40');
INSERT INTO audit_log VALUES(1305,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 09:36:40');
INSERT INTO audit_log VALUES(1306,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 09:44:37');
INSERT INTO audit_log VALUES(1307,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 09:44:37');
INSERT INTO audit_log VALUES(1308,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 09:44:37');
INSERT INTO audit_log VALUES(1309,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 09:44:38');
INSERT INTO audit_log VALUES(1310,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 09:44:38');
INSERT INTO audit_log VALUES(1311,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 09:44:38');
INSERT INTO audit_log VALUES(1312,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 09:45:26');
INSERT INTO audit_log VALUES(1313,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 09:45:26');
INSERT INTO audit_log VALUES(1314,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 09:45:26');
INSERT INTO audit_log VALUES(1315,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 09:45:26');
INSERT INTO audit_log VALUES(1316,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 09:45:26');
INSERT INTO audit_log VALUES(1317,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 09:45:26');
INSERT INTO audit_log VALUES(1318,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 09:50:25');
INSERT INTO audit_log VALUES(1319,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 09:50:25');
INSERT INTO audit_log VALUES(1320,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 09:50:25');
INSERT INTO audit_log VALUES(1321,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 09:50:26');
INSERT INTO audit_log VALUES(1322,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 09:50:26');
INSERT INTO audit_log VALUES(1323,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 09:50:26');
INSERT INTO audit_log VALUES(1324,'CREATION_UTILISATEUR','Utilisateur cr├®├® : testaudit (CLIENT)','2026-05-10 09:51:30');
INSERT INTO audit_log VALUES(1325,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 09:55:26');
INSERT INTO audit_log VALUES(1326,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 09:55:26');
INSERT INTO audit_log VALUES(1327,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 09:55:26');
INSERT INTO audit_log VALUES(1328,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 09:55:26');
INSERT INTO audit_log VALUES(1329,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 09:55:26');
INSERT INTO audit_log VALUES(1330,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 09:55:26');
INSERT INTO audit_log VALUES(1331,'MODIFICATION_ROLE','Utilisateur ID 3 ÔåÆ r├┤le COMPTABLE','2026-05-10 09:57:54');
INSERT INTO audit_log VALUES(1332,'DESACTIVATION_UTILISATEUR','Utilisateur d├®sactiv├® : ID 3','2026-05-10 09:58:34');
INSERT INTO audit_log VALUES(1333,'SUPPRESSION_UTILISATEUR','Utilisateur supprim├® : ID 3','2026-05-10 09:59:42');
INSERT INTO audit_log VALUES(1334,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 10:00:26');
INSERT INTO audit_log VALUES(1335,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 10:00:26');
INSERT INTO audit_log VALUES(1336,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 10:00:26');
INSERT INTO audit_log VALUES(1337,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 10:00:26');
INSERT INTO audit_log VALUES(1338,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 10:00:26');
INSERT INTO audit_log VALUES(1339,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 10:00:26');
INSERT INTO audit_log VALUES(1340,'CREATION_UTILISATEUR','Utilisateur cr├®├® : testpassword (CLIENT)','2026-05-10 10:01:43');
INSERT INTO audit_log VALUES(1341,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 10:05:26');
INSERT INTO audit_log VALUES(1342,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 10:05:26');
INSERT INTO audit_log VALUES(1343,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 10:05:26');
INSERT INTO audit_log VALUES(1344,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 10:05:26');
INSERT INTO audit_log VALUES(1345,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 10:05:26');
INSERT INTO audit_log VALUES(1346,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 10:05:26');
INSERT INTO audit_log VALUES(1347,'RESET_PASSWORD','Mot de passe modifi├® pour utilisateur ID 4','2026-05-10 10:05:53');
INSERT INTO audit_log VALUES(1348,'RESET_PASSWORD','Mot de passe modifi├® pour utilisateur ID 4','2026-05-10 10:08:37');
INSERT INTO audit_log VALUES(1349,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 10:10:26');
INSERT INTO audit_log VALUES(1350,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 10:10:26');
INSERT INTO audit_log VALUES(1351,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 10:10:26');
INSERT INTO audit_log VALUES(1352,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 10:10:26');
INSERT INTO audit_log VALUES(1353,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 10:10:26');
INSERT INTO audit_log VALUES(1354,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 10:10:26');
INSERT INTO audit_log VALUES(1355,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 10:15:26');
INSERT INTO audit_log VALUES(1356,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 10:15:26');
INSERT INTO audit_log VALUES(1357,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 10:15:26');
INSERT INTO audit_log VALUES(1358,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 10:15:26');
INSERT INTO audit_log VALUES(1359,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 10:15:26');
INSERT INTO audit_log VALUES(1360,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 10:15:26');
INSERT INTO audit_log VALUES(1361,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 10:20:26');
INSERT INTO audit_log VALUES(1362,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 10:20:26');
INSERT INTO audit_log VALUES(1363,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 10:20:26');
INSERT INTO audit_log VALUES(1364,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 10:20:26');
INSERT INTO audit_log VALUES(1365,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 10:20:26');
INSERT INTO audit_log VALUES(1366,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 10:20:26');
INSERT INTO audit_log VALUES(1367,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 10:28:35');
INSERT INTO audit_log VALUES(1368,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 10:28:35');
INSERT INTO audit_log VALUES(1369,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 10:28:35');
INSERT INTO audit_log VALUES(1370,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 10:28:35');
INSERT INTO audit_log VALUES(1371,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 10:28:35');
INSERT INTO audit_log VALUES(1372,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 10:28:35');
INSERT INTO audit_log VALUES(1373,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 10:33:35');
INSERT INTO audit_log VALUES(1374,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 10:33:35');
INSERT INTO audit_log VALUES(1375,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 10:33:35');
INSERT INTO audit_log VALUES(1376,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 10:33:35');
INSERT INTO audit_log VALUES(1377,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 10:33:35');
INSERT INTO audit_log VALUES(1378,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 10:33:35');
INSERT INTO audit_log VALUES(1379,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 10:38:35');
INSERT INTO audit_log VALUES(1380,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 10:38:35');
INSERT INTO audit_log VALUES(1381,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 10:38:35');
INSERT INTO audit_log VALUES(1382,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 10:38:35');
INSERT INTO audit_log VALUES(1383,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 10:38:35');
INSERT INTO audit_log VALUES(1384,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 10:38:35');
INSERT INTO audit_log VALUES(1385,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 10:40:57');
INSERT INTO audit_log VALUES(1386,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 10:40:57');
INSERT INTO audit_log VALUES(1387,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 10:40:57');
INSERT INTO audit_log VALUES(1388,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 10:40:57');
INSERT INTO audit_log VALUES(1389,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 10:40:57');
INSERT INTO audit_log VALUES(1390,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 10:40:57');
INSERT INTO audit_log VALUES(1391,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 10:44:34');
INSERT INTO audit_log VALUES(1392,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 10:44:34');
INSERT INTO audit_log VALUES(1393,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 10:44:34');
INSERT INTO audit_log VALUES(1394,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 10:44:34');
INSERT INTO audit_log VALUES(1395,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 10:44:34');
INSERT INTO audit_log VALUES(1396,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 10:44:34');
INSERT INTO audit_log VALUES(1397,'MODIFICATION_ROLE','Utilisateur ID 4 ÔåÆ r├┤le COMPTABLE','2026-05-10 10:46:55');
INSERT INTO audit_log VALUES(1398,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 10:49:50');
INSERT INTO audit_log VALUES(1399,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 10:49:50');
INSERT INTO audit_log VALUES(1400,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 10:49:50');
INSERT INTO audit_log VALUES(1401,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 10:49:50');
INSERT INTO audit_log VALUES(1402,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 10:49:50');
INSERT INTO audit_log VALUES(1403,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 10:49:50');
INSERT INTO audit_log VALUES(1404,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 10:53:08');
INSERT INTO audit_log VALUES(1405,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 10:53:08');
INSERT INTO audit_log VALUES(1406,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 10:53:08');
INSERT INTO audit_log VALUES(1407,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 10:53:08');
INSERT INTO audit_log VALUES(1408,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 10:53:08');
INSERT INTO audit_log VALUES(1409,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 10:53:08');
INSERT INTO audit_log VALUES(1410,'MODIFICATION_ROLE','Utilisateur ID 4 ÔåÆ r├┤le CLIENT','2026-05-10 10:55:46');
INSERT INTO audit_log VALUES(1411,'MODIFICATION_ROLE','Utilisateur ID 4 ÔåÆ r├┤le CLIENT','2026-05-10 10:56:14');
INSERT INTO audit_log VALUES(1412,'MODIFICATION_ROLE','Utilisateur ID 4 ÔåÆ r├┤le COMPTABLE','2026-05-10 10:57:42');
INSERT INTO audit_log VALUES(1413,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 10:58:08');
INSERT INTO audit_log VALUES(1414,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 10:58:08');
INSERT INTO audit_log VALUES(1415,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 10:58:08');
INSERT INTO audit_log VALUES(1416,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 10:58:08');
INSERT INTO audit_log VALUES(1417,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 10:58:08');
INSERT INTO audit_log VALUES(1418,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 10:58:08');
INSERT INTO audit_log VALUES(1419,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 11:03:08');
INSERT INTO audit_log VALUES(1420,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 11:03:08');
INSERT INTO audit_log VALUES(1421,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 11:03:08');
INSERT INTO audit_log VALUES(1422,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 11:03:08');
INSERT INTO audit_log VALUES(1423,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 11:03:08');
INSERT INTO audit_log VALUES(1424,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 11:03:08');
INSERT INTO audit_log VALUES(1425,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 11:08:08');
INSERT INTO audit_log VALUES(1426,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 11:08:08');
INSERT INTO audit_log VALUES(1427,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 11:08:08');
INSERT INTO audit_log VALUES(1428,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 11:08:08');
INSERT INTO audit_log VALUES(1429,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 11:08:08');
INSERT INTO audit_log VALUES(1430,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 11:08:08');
INSERT INTO audit_log VALUES(1431,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 11:13:08');
INSERT INTO audit_log VALUES(1432,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 11:13:08');
INSERT INTO audit_log VALUES(1433,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 11:13:08');
INSERT INTO audit_log VALUES(1434,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 11:13:08');
INSERT INTO audit_log VALUES(1435,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 11:13:08');
INSERT INTO audit_log VALUES(1436,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 11:13:08');
INSERT INTO audit_log VALUES(1437,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 11:18:08');
INSERT INTO audit_log VALUES(1438,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 11:18:08');
INSERT INTO audit_log VALUES(1439,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 11:18:08');
INSERT INTO audit_log VALUES(1440,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 11:18:08');
INSERT INTO audit_log VALUES(1441,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 11:18:08');
INSERT INTO audit_log VALUES(1442,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 11:18:08');
INSERT INTO audit_log VALUES(1443,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 11:28:09');
INSERT INTO audit_log VALUES(1444,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 11:28:09');
INSERT INTO audit_log VALUES(1445,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 11:28:09');
INSERT INTO audit_log VALUES(1446,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 11:28:09');
INSERT INTO audit_log VALUES(1447,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 11:28:09');
INSERT INTO audit_log VALUES(1448,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 11:28:09');
INSERT INTO audit_log VALUES(1449,'MODIFICATION_ROLE','Utilisateur ID 4 ÔåÆ r├┤le CLIENT','2026-05-10 11:32:49');
INSERT INTO audit_log VALUES(1450,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 11:33:09');
INSERT INTO audit_log VALUES(1451,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 11:33:09');
INSERT INTO audit_log VALUES(1452,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 11:33:09');
INSERT INTO audit_log VALUES(1453,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 11:33:09');
INSERT INTO audit_log VALUES(1454,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 11:33:09');
INSERT INTO audit_log VALUES(1455,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 11:33:09');
INSERT INTO audit_log VALUES(1456,'ACCES_REFUSE','R├┤le CLIENT refus├®. R├┤les requis : [''ADMIN'', ''COMPTABLE'']','2026-05-10 11:33:16');
INSERT INTO audit_log VALUES(1457,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 11:37:46');
INSERT INTO audit_log VALUES(1458,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 11:37:46');
INSERT INTO audit_log VALUES(1459,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 11:37:46');
INSERT INTO audit_log VALUES(1460,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 11:37:46');
INSERT INTO audit_log VALUES(1461,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 11:37:46');
INSERT INTO audit_log VALUES(1462,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 11:37:46');
INSERT INTO audit_log VALUES(1463,'API_KEY_MANQUANTE','Tentative acc├¿s API sans cl├® API','2026-05-10 11:39:00');
INSERT INTO audit_log VALUES(1464,'API_KEY_INVALIDE','Tentative acc├¿s API avec cl├® API invalide','2026-05-10 11:39:32');
INSERT INTO audit_log VALUES(1465,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 11:44:44');
INSERT INTO audit_log VALUES(1466,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 11:44:44');
INSERT INTO audit_log VALUES(1467,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 11:44:44');
INSERT INTO audit_log VALUES(1468,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 11:44:44');
INSERT INTO audit_log VALUES(1469,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 11:44:44');
INSERT INTO audit_log VALUES(1470,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 11:44:44');
INSERT INTO audit_log VALUES(1471,'API_KEY_INVALIDE','Tentative acc├¿s API avec cl├® API invalide','2026-05-10 11:45:29');
INSERT INTO audit_log VALUES(1472,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 11:49:44');
INSERT INTO audit_log VALUES(1473,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 11:49:44');
INSERT INTO audit_log VALUES(1474,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 11:49:44');
INSERT INTO audit_log VALUES(1475,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 11:49:44');
INSERT INTO audit_log VALUES(1476,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 11:49:44');
INSERT INTO audit_log VALUES(1477,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 11:49:44');
INSERT INTO audit_log VALUES(1478,'ACCES_REFUSE','R├┤le CLIENT refus├®. R├┤les requis : [''ADMIN'', ''COMPTABLE'']','2026-05-10 11:52:18');
INSERT INTO audit_log VALUES(1479,'MODIFICATION_ROLE','Utilisateur ID 4 ÔåÆ r├┤le COMPTABLE','2026-05-10 11:53:37');
INSERT INTO audit_log VALUES(1480,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 11:54:44');
INSERT INTO audit_log VALUES(1481,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 11:54:44');
INSERT INTO audit_log VALUES(1482,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 11:54:44');
INSERT INTO audit_log VALUES(1483,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 11:54:44');
INSERT INTO audit_log VALUES(1484,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 11:54:44');
INSERT INTO audit_log VALUES(1485,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 11:54:44');
INSERT INTO audit_log VALUES(1486,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 12:05:21');
INSERT INTO audit_log VALUES(1487,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 12:05:21');
INSERT INTO audit_log VALUES(1488,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 12:05:21');
INSERT INTO audit_log VALUES(1489,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 12:05:21');
INSERT INTO audit_log VALUES(1490,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 12:05:21');
INSERT INTO audit_log VALUES(1491,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 12:05:21');
INSERT INTO audit_log VALUES(1492,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 12:10:32');
INSERT INTO audit_log VALUES(1493,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 12:10:33');
INSERT INTO audit_log VALUES(1494,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 12:10:33');
INSERT INTO audit_log VALUES(1495,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 12:10:33');
INSERT INTO audit_log VALUES(1496,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 12:10:33');
INSERT INTO audit_log VALUES(1497,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 12:10:33');
INSERT INTO audit_log VALUES(1498,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 12:12:41');
INSERT INTO audit_log VALUES(1499,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 12:12:41');
INSERT INTO audit_log VALUES(1500,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 12:12:41');
INSERT INTO audit_log VALUES(1501,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 12:12:41');
INSERT INTO audit_log VALUES(1502,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 12:12:41');
INSERT INTO audit_log VALUES(1503,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 12:12:41');
INSERT INTO audit_log VALUES(1504,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 12:19:40');
INSERT INTO audit_log VALUES(1505,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 12:19:40');
INSERT INTO audit_log VALUES(1506,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 12:19:40');
INSERT INTO audit_log VALUES(1507,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 12:19:40');
INSERT INTO audit_log VALUES(1508,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 12:19:40');
INSERT INTO audit_log VALUES(1509,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 12:19:40');
INSERT INTO audit_log VALUES(1510,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 12:22:26');
INSERT INTO audit_log VALUES(1511,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 12:22:26');
INSERT INTO audit_log VALUES(1512,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 12:22:26');
INSERT INTO audit_log VALUES(1513,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 12:22:26');
INSERT INTO audit_log VALUES(1514,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 12:22:26');
INSERT INTO audit_log VALUES(1515,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 12:22:26');
INSERT INTO audit_log VALUES(1516,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 12:27:26');
INSERT INTO audit_log VALUES(1517,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 12:27:26');
INSERT INTO audit_log VALUES(1518,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 12:27:26');
INSERT INTO audit_log VALUES(1519,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 12:27:26');
INSERT INTO audit_log VALUES(1520,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 12:27:26');
INSERT INTO audit_log VALUES(1521,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 12:27:26');
INSERT INTO audit_log VALUES(1522,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 12:32:26');
INSERT INTO audit_log VALUES(1523,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 12:32:26');
INSERT INTO audit_log VALUES(1524,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 12:32:26');
INSERT INTO audit_log VALUES(1525,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 12:32:26');
INSERT INTO audit_log VALUES(1526,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 12:32:26');
INSERT INTO audit_log VALUES(1527,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 12:32:26');
INSERT INTO audit_log VALUES(1528,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 12:34:40');
INSERT INTO audit_log VALUES(1529,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 12:34:40');
INSERT INTO audit_log VALUES(1530,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 12:34:40');
INSERT INTO audit_log VALUES(1531,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 12:34:40');
INSERT INTO audit_log VALUES(1532,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 12:34:40');
INSERT INTO audit_log VALUES(1533,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 12:34:40');
INSERT INTO audit_log VALUES(1534,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 12:35:03');
INSERT INTO audit_log VALUES(1535,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 12:35:03');
INSERT INTO audit_log VALUES(1536,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 12:35:03');
INSERT INTO audit_log VALUES(1537,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 12:35:03');
INSERT INTO audit_log VALUES(1538,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 12:35:03');
INSERT INTO audit_log VALUES(1539,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 12:35:03');
INSERT INTO audit_log VALUES(1540,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 12:37:26');
INSERT INTO audit_log VALUES(1541,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 12:37:26');
INSERT INTO audit_log VALUES(1542,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 12:37:26');
INSERT INTO audit_log VALUES(1543,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 12:37:26');
INSERT INTO audit_log VALUES(1544,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 12:37:26');
INSERT INTO audit_log VALUES(1545,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 12:37:26');
INSERT INTO audit_log VALUES(1546,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 12:38:30');
INSERT INTO audit_log VALUES(1547,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 12:38:30');
INSERT INTO audit_log VALUES(1548,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 12:38:30');
INSERT INTO audit_log VALUES(1549,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 12:38:30');
INSERT INTO audit_log VALUES(1550,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 12:38:30');
INSERT INTO audit_log VALUES(1551,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 12:38:30');
INSERT INTO audit_log VALUES(1552,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 12:43:30');
INSERT INTO audit_log VALUES(1553,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 12:43:30');
INSERT INTO audit_log VALUES(1554,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 12:43:30');
INSERT INTO audit_log VALUES(1555,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 12:43:30');
INSERT INTO audit_log VALUES(1556,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 12:43:30');
INSERT INTO audit_log VALUES(1557,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 12:43:30');
INSERT INTO audit_log VALUES(1558,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 12:45:53');
INSERT INTO audit_log VALUES(1559,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 12:45:53');
INSERT INTO audit_log VALUES(1560,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 12:45:53');
INSERT INTO audit_log VALUES(1561,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 12:45:53');
INSERT INTO audit_log VALUES(1562,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 12:45:53');
INSERT INTO audit_log VALUES(1563,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 12:45:53');
INSERT INTO audit_log VALUES(1564,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 12:50:53');
INSERT INTO audit_log VALUES(1565,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 12:50:53');
INSERT INTO audit_log VALUES(1566,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 12:50:53');
INSERT INTO audit_log VALUES(1567,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 12:50:53');
INSERT INTO audit_log VALUES(1568,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 12:50:53');
INSERT INTO audit_log VALUES(1569,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 12:50:53');
INSERT INTO audit_log VALUES(1570,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 12:55:53');
INSERT INTO audit_log VALUES(1571,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 12:55:53');
INSERT INTO audit_log VALUES(1572,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 12:55:53');
INSERT INTO audit_log VALUES(1573,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 12:55:53');
INSERT INTO audit_log VALUES(1574,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 12:55:53');
INSERT INTO audit_log VALUES(1575,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 12:55:53');
INSERT INTO audit_log VALUES(1576,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 13:00:53');
INSERT INTO audit_log VALUES(1577,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 13:00:53');
INSERT INTO audit_log VALUES(1578,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 13:00:53');
INSERT INTO audit_log VALUES(1579,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 13:00:53');
INSERT INTO audit_log VALUES(1580,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 13:00:53');
INSERT INTO audit_log VALUES(1581,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 13:00:53');
INSERT INTO audit_log VALUES(1582,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 13:05:53');
INSERT INTO audit_log VALUES(1583,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 13:05:53');
INSERT INTO audit_log VALUES(1584,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 13:05:53');
INSERT INTO audit_log VALUES(1585,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 13:05:53');
INSERT INTO audit_log VALUES(1586,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 13:05:53');
INSERT INTO audit_log VALUES(1587,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 13:05:53');
INSERT INTO audit_log VALUES(1588,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 13:10:53');
INSERT INTO audit_log VALUES(1589,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 13:10:53');
INSERT INTO audit_log VALUES(1590,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 13:10:53');
INSERT INTO audit_log VALUES(1591,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 13:10:53');
INSERT INTO audit_log VALUES(1592,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 13:10:53');
INSERT INTO audit_log VALUES(1593,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 13:10:53');
INSERT INTO audit_log VALUES(1594,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 13:15:53');
INSERT INTO audit_log VALUES(1595,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 13:15:53');
INSERT INTO audit_log VALUES(1596,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 13:15:53');
INSERT INTO audit_log VALUES(1597,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 13:15:53');
INSERT INTO audit_log VALUES(1598,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 13:15:53');
INSERT INTO audit_log VALUES(1599,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 13:15:53');
INSERT INTO audit_log VALUES(1600,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 13:20:53');
INSERT INTO audit_log VALUES(1601,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 13:20:53');
INSERT INTO audit_log VALUES(1602,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 13:20:53');
INSERT INTO audit_log VALUES(1603,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 13:20:53');
INSERT INTO audit_log VALUES(1604,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 13:20:53');
INSERT INTO audit_log VALUES(1605,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 13:20:53');
INSERT INTO audit_log VALUES(1606,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 13:25:53');
INSERT INTO audit_log VALUES(1607,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 13:25:53');
INSERT INTO audit_log VALUES(1608,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 13:25:53');
INSERT INTO audit_log VALUES(1609,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 13:25:53');
INSERT INTO audit_log VALUES(1610,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 13:25:53');
INSERT INTO audit_log VALUES(1611,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 13:25:53');
INSERT INTO audit_log VALUES(1612,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 13:30:53');
INSERT INTO audit_log VALUES(1613,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 13:30:53');
INSERT INTO audit_log VALUES(1614,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 13:30:53');
INSERT INTO audit_log VALUES(1615,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 13:30:53');
INSERT INTO audit_log VALUES(1616,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 13:30:54');
INSERT INTO audit_log VALUES(1617,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 13:30:54');
INSERT INTO audit_log VALUES(1618,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 13:35:54');
INSERT INTO audit_log VALUES(1619,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 13:35:54');
INSERT INTO audit_log VALUES(1620,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 13:35:54');
INSERT INTO audit_log VALUES(1621,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 13:35:54');
INSERT INTO audit_log VALUES(1622,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 13:35:54');
INSERT INTO audit_log VALUES(1623,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 13:35:54');
INSERT INTO audit_log VALUES(1624,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 13:40:54');
INSERT INTO audit_log VALUES(1625,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 13:40:54');
INSERT INTO audit_log VALUES(1626,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 13:40:54');
INSERT INTO audit_log VALUES(1627,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 13:40:54');
INSERT INTO audit_log VALUES(1628,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 13:40:54');
INSERT INTO audit_log VALUES(1629,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 13:40:54');
INSERT INTO audit_log VALUES(1630,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 13:45:54');
INSERT INTO audit_log VALUES(1631,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 13:45:54');
INSERT INTO audit_log VALUES(1632,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 13:45:54');
INSERT INTO audit_log VALUES(1633,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 13:45:54');
INSERT INTO audit_log VALUES(1634,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 13:45:54');
INSERT INTO audit_log VALUES(1635,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 13:45:54');
INSERT INTO audit_log VALUES(1636,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 13:50:54');
INSERT INTO audit_log VALUES(1637,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 13:50:54');
INSERT INTO audit_log VALUES(1638,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 13:50:54');
INSERT INTO audit_log VALUES(1639,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 13:50:54');
INSERT INTO audit_log VALUES(1640,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 13:50:54');
INSERT INTO audit_log VALUES(1641,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 13:50:54');
INSERT INTO audit_log VALUES(1642,'SCHEDULER','Ex├®cution p├®riodique du scheduler interne','2026-05-10 13:55:54');
INSERT INTO audit_log VALUES(1643,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #2 - Robot relances clients (RELANCES_CLIENTS)','2026-05-10 13:55:54');
INSERT INTO audit_log VALUES(1644,'ROBOT_RELANCES_CLIENTS','Robot relances clients ex├®cut├®','2026-05-10 13:55:54');
INSERT INTO audit_log VALUES(1645,'NOTIFICATION_AUTO','Relances clients : v├®rification automatique effectu├®e par le robot V7.','2026-05-10 13:55:54');
INSERT INTO audit_log VALUES(1646,'EXECUTION_TACHE_V7','Ex├®cution t├óche V7 #1 - Test scheduler (Test)','2026-05-10 13:55:54');
INSERT INTO audit_log VALUES(1647,'ROBOT_INCONNU','Type de robot inconnu : Test','2026-05-10 13:55:54');
CREATE TABLE factures_dematerialisees (
            id SERIAL PRIMARY KEY ,
            numero TEXT,
            client TEXT,
            montant_ht REAL,
            tva REAL,
            montant_ttc REAL,
            statut TEXT,
            canal TEXT,
            date_creation TEXT,
            date_transmission TEXT,
            preuve TEXT
        );
INSERT INTO factures_dematerialisees VALUES(1,'FD-2026-00001','murielle',250.0,50.0,300.0,'TRANSMISE','PLATEFORME_INTERNE','2026-05-07 16:21:19','2026-05-07 16:21:25','8644cc3453d804391dfadc5778ab7dd7f7df43d31b4c526030d2ab3f871aacd4');
INSERT INTO factures_dematerialisees VALUES(2,'FD-2026-00002','murielle',200.0,40.0,240.0,'BROUILLON','INTERNE','2026-05-07 16:22:12','','');
CREATE TABLE annuaire_clients_pdp (
            id SERIAL PRIMARY KEY ,
            nom TEXT,
            siret TEXT,
            tva_intracom TEXT,
            email TEXT
        );
CREATE TABLE workflow_factures_pdp_v2 (
            id SERIAL PRIMARY KEY ,
            facture_id INTEGER,
            numero TEXT,
            sens TEXT,
            statut TEXT,
            canal TEXT,
            accuse_reception TEXT,
            date_action TEXT,
            detail TEXT
        );
INSERT INTO workflow_factures_pdp_v2 VALUES(1,0,'REC-20260507185525','RECEPTION','RE├çUE','PDP_INTERNE','f6015c7f76319c1a15bef892c9bc6010e31da5b4a2fe0bac8a0b5991d6e14ca9','2026-05-07 18:55:25','Simulation de r├®ception automatique fournisseur');
INSERT INTO workflow_factures_pdp_v2 VALUES(2,0,'REC-20260507185527','RECEPTION','RE├çUE','PDP_INTERNE','07affd2bd1772fde6b4f9d61cc1b8bfc5e8b135bf5ad8631d9d0eb980c1050b6','2026-05-07 18:55:27','Simulation de r├®ception automatique fournisseur');
INSERT INTO workflow_factures_pdp_v2 VALUES(3,0,'REC-20260507185528','RECEPTION','RE├çUE','PDP_INTERNE','7d1bb788bf2a422b3fd49cb1bf92eb2f763996c62b8d20f347a818972888ffc0','2026-05-07 18:55:28','Simulation de r├®ception automatique fournisseur');
CREATE TABLE documents_comptables_importes (
            id SERIAL PRIMARY KEY ,
            nom_fichier TEXT,
            type_document TEXT,
            extension TEXT,
            chemin TEXT,
            taille_ko REAL,
            empreinte_sha256 TEXT,
            statut TEXT,
            date_import TEXT,
            commentaire TEXT
        );
INSERT INTO documents_comptables_importes VALUES(1,'Facture de prestation de d├®pot de capital.pdf','FACTURE_CLIENT','pdf','imports_documents_comptables\20260508_083644_Facture de prestation de d├®pot de capital.pdf',25.23,'c41b72743b1e6f1768460d16a593636cf123dd687956e8bd8013d191a5dedd78','A_TRAITER','2026-05-08 08:36:44','');
INSERT INTO documents_comptables_importes VALUES(2,'facture_Immatriculation_dossier_5785887.pdf','FACTURE_CLIENT','pdf','imports_documents_comptables\20260508_084252_facture_Immatriculation_dossier_5785887.pdf',24.92,'55b4598fa079f32e4d5a04a98f5defa15f5acc06400fb93efd4a27f82c200603','IMPORTE','2026-05-08 08:42:52','');
INSERT INTO documents_comptables_importes VALUES(3,'facture-abonnement-15_04_2026.pdf','FACTURE_CLIENT','pdf','imports_documents_comptables\20260508_093453_facture-abonnement-15_04_2026.pdf',54.51,'43b77058001b2237d469c6f636b292f48f222025f24ebe23974c0bf26fd35272','REJETE','2026-05-08 09:34:53','');
CREATE TABLE extractions_documents_comptables (
            id SERIAL PRIMARY KEY ,
            document_id INTEGER,
            fournisseur_client TEXT,
            numero_facture TEXT,
            date_document TEXT,
            montant_ttc TEXT,
            siret TEXT,
            tva_intracom TEXT,
            type_probable TEXT,
            texte_extrait TEXT
        );
INSERT INTO extractions_documents_comptables VALUES(1,1,'Qonto (Olinda SAS)','n','','522,49','','FR10819489626','FACTURE_CLIENT',unistr('Qonto (Olinda SAS)\u000a18 rue de Navarin\u000a75009 Paris - France\u000ahello@qonto.com\u000aPAY├ë\u000aFactur├® ├á\u000aSOCIETE INVESTISSEMENTS IMMOBILIERS\u000a124 Chemin du Bouchaud, 16430, Balzac, FR\u000aalain.baudinaud@orange.fr\u000aFacture n┬░ 01-08-23-partner-\u000apayment-2308\u000a├ëmise le : 01/08/23\u000aDue ├á : la date d''├®mission\u000aQuantit├®\u000aTotal HT\u000aTaux TVA\u000aTVA\u000aTotal TTC\u000aPack Qonto Basic\u000aVotre pack inclut : \u000a- Prestation d├®p├┤t de capital en ligne\u000a- 12 mois d''abonnement Qonto au forfait\u000aBasic (├á partir de la date de v├®rification\u000ar├®glementaire de votre nouvelle\u000aentreprise)\u000a1\u000a169,00 Ôé¼\u000a20.0%\u000a33,80 Ôé¼\u000a202,80 Ôé¼\u000aSous-total (HT)\u000a169,00 Ôé¼\u000aTVA\u000a33,80 Ôé¼\u000aMontant total (TTC)\u000a202,80 Ôé¼\u000aMontant pay├®\u000a(TTC)\u000a202,80 Ôé¼\u000aOlinda SAS, au capital de 296 522,49 Ôé¼\u000aSIREN : 819 489 626\u000aTVA intracommunautaire : FR10819489626\u000aPAGE \u000a1\u000a/\u000a1'));
INSERT INTO extractions_documents_comptables VALUES(2,1,'Qonto (Olinda SAS)','n','','522,49','','FR10819489626','FACTURE_CLIENT',unistr('Qonto (Olinda SAS)\u000a18 rue de Navarin\u000a75009 Paris - France\u000ahello@qonto.com\u000aPAY├ë\u000aFactur├® ├á\u000aSOCIETE INVESTISSEMENTS IMMOBILIERS\u000a124 Chemin du Bouchaud, 16430, Balzac, FR\u000aalain.baudinaud@orange.fr\u000aFacture n┬░ 01-08-23-partner-\u000apayment-2308\u000a├ëmise le : 01/08/23\u000aDue ├á : la date d''├®mission\u000aQuantit├®\u000aTotal HT\u000aTaux TVA\u000aTVA\u000aTotal TTC\u000aPack Qonto Basic\u000aVotre pack inclut : \u000a- Prestation d├®p├┤t de capital en ligne\u000a- 12 mois d''abonnement Qonto au forfait\u000aBasic (├á partir de la date de v├®rification\u000ar├®glementaire de votre nouvelle\u000aentreprise)\u000a1\u000a169,00 Ôé¼\u000a20.0%\u000a33,80 Ôé¼\u000a202,80 Ôé¼\u000aSous-total (HT)\u000a169,00 Ôé¼\u000aTVA\u000a33,80 Ôé¼\u000aMontant total (TTC)\u000a202,80 Ôé¼\u000aMontant pay├®\u000a(TTC)\u000a202,80 Ôé¼\u000aOlinda SAS, au capital de 296 522,49 Ôé¼\u000aSIREN : 819 489 626\u000aTVA intracommunautaire : FR10819489626\u000aPAGE \u000a1\u000a/\u000a1'));
INSERT INTO extractions_documents_comptables VALUES(3,3,'FACTURE2026-71763','2026-71763','','10,00','','FR43851036947','FACTURE_CLIENT',unistr('FACTURE2026-71763\u000aDate d''├®mission\u000a15 avr. 2026\u000aDate d''├®ch├®ance\u000a15 avr. 2026\u000aEmetteur\u000aLokki\u000a89 rue de Reaumur\u000a75002 Paris\u000aFrance\u000aFR43851036947\u000aClient\u000aRapidloc\u000a126 CHEMIN DES BOUCHAUDS\u000a16430  BALZAC\u000aFrance\u000aFR35978648657Lokki Facture 2026-71763 154,80┬áÔé¼ d├╗ le 15 avr. 2026\u000aD├ëTAILS\u000aProduit Quantit├® Prix unitaire HT Taux de TVA Total HT\u000aAbonnement Lokki\u000aAbonnement Lokki\u000a1 129,00┬áÔé¼ 20% 129,00┬áÔé¼\u000aSTATUT DE LA FACTURE Pay├®\u000aMoyen de paiement Date Montant\u000aPr├®l├¿vement SEPA 15 avr. 2026 154,80┬áÔé¼\u000aSous total 129,00┬áÔé¼\u000aTVA 20% 25,80┬áÔé¼\u000aTotal 154,80┬áÔé¼\u000aINFORMATIONS L├ëGALES\u000aSIRET Lokki: 851 036 947 00022\u000aINFORMATIONS COMPL├ëMENTAIRES\u000aEn cas de paiement par virement, merci d''indiquer le num├®ro de facture correspondant au paiement\u000aP├®nalit├®s de retard (taux annuel) : 10,00 %\u000aPas descompte en cas de paiement anticip├® \u000aIndemnit├® forfaitaire pour frais de recouvrement en cas de retard de paiement : 40 Ôé¼\u000aInvoice generated by Hyperline.co - The new standard for revenue management 1 / 199 / 99'));
CREATE TABLE precomptabilisation_documents (
            id SERIAL PRIMARY KEY ,
            document_id INTEGER,
            journal TEXT,
            compte_tiers TEXT,
            compte_charge TEXT,
            compte_tva TEXT,
            libelle TEXT,
            date_piece TEXT,
            montant_ht REAL,
            montant_tva REAL,
            montant_ttc REAL,
            statut TEXT
        );
INSERT INTO precomptabilisation_documents VALUES(1,1,'VEN','411','706','44566','VENTE Qonto (Olinda SAS) n','',435.41,87.08,522.49,'VALIDEE');
INSERT INTO precomptabilisation_documents VALUES(2,1,'VEN','411','706','44566','VENTE Qonto (Olinda SAS) n','',435.41,87.08,522.49,'A_VALIDER');
INSERT INTO precomptabilisation_documents VALUES(3,3,'VEN','411','706','44566','VENTE FACTURE2026-71763 2026-71763','',8.33,1.67,10.0,'A_VALIDER');
INSERT INTO precomptabilisation_documents VALUES(4,3,'VEN','411','706','44566','VENTE FACTURE2026-71763 2026-71763','',8.33,1.67,10.0,'VALIDEE');
INSERT INTO precomptabilisation_documents VALUES(5,3,'VEN','411','706','44566','VENTE FACTURE2026-71763 2026-71763','',8.33,1.67,10.0,'A_VALIDER');
CREATE TABLE ecritures_auto (
            id SERIAL PRIMARY KEY ,
            journal TEXT,
            date_ecriture TEXT,
            libelle TEXT,
            compte TEXT,
            debit REAL,
            credit REAL
        );
INSERT INTO ecritures_auto VALUES(1,'VEN','','VENTE Qonto (Olinda SAS) n','706',435.41,0.0);
INSERT INTO ecritures_auto VALUES(2,'VEN','','VENTE Qonto (Olinda SAS) n','44566',87.08,0.0);
INSERT INTO ecritures_auto VALUES(3,'VEN','','VENTE Qonto (Olinda SAS) n','411',0.0,522.49);
INSERT INTO ecritures_auto VALUES(4,'VEN','','VENTE FACTURE2026-71763 2026-71763','706',8.33,0.0);
INSERT INTO ecritures_auto VALUES(5,'VEN','','VENTE FACTURE2026-71763 2026-71763','44566',1.67,0.0);
INSERT INTO ecritures_auto VALUES(6,'VEN','','VENTE FACTURE2026-71763 2026-71763','411',0.0,10.0);
CREATE TABLE regles_comptables_ia (
            id SERIAL PRIMARY KEY ,
            mot_cle TEXT,
            compte_suggere TEXT,
            journal_suggere TEXT,
            type_document TEXT,
            commentaire TEXT
        );
INSERT INTO regles_comptables_ia VALUES(1,'qonto','627','ACH','FACTURE_FOURNISSEUR','Frais bancaires / service Qonto');
CREATE TABLE analyses_ia_documents (
            id SERIAL PRIMARY KEY ,
            document_id INTEGER,
            compte_suggere TEXT,
            journal_suggere TEXT,
            regle_trouvee TEXT,
            score_confiance INTEGER,
            doublon TEXT
        );
INSERT INTO analyses_ia_documents VALUES(1,3,'628','OD','Aucune r├¿gle trouv├®e',50,'NON');
INSERT INTO analyses_ia_documents VALUES(2,3,'628','OD','Aucune r├¿gle trouv├®e',50,'NON');
CREATE TABLE fournisseurs_ia_v2 (
            id SERIAL PRIMARY KEY ,
            nom TEXT,
            compte_pcg TEXT,
            compte_tva TEXT,
            journal TEXT,
            taux_tva REAL,
            nb_validations INTEGER DEFAULT 0,
            derniere_utilisation TEXT
        );
INSERT INTO fournisseurs_ia_v2 VALUES(1,'FACTURE2026-71763 2026-71763','706','44566','VEN',20.0,2,'2026-05-08 09:37:45');
CREATE TABLE historique_apprentissage_ia_v2 (
            id SERIAL PRIMARY KEY ,
            fournisseur TEXT,
            compte_pcg TEXT,
            compte_tva TEXT,
            journal TEXT,
            montant_ttc REAL,
            source TEXT,
            date_apprentissage TEXT
        );
INSERT INTO historique_apprentissage_ia_v2 VALUES(1,'FACTURE2026-71763 2026-71763','706','44566','VEN',10.0,'VALIDATION_PRECOMPTA','2026-05-08 09:36:57');
INSERT INTO historique_apprentissage_ia_v2 VALUES(2,'FACTURE2026-71763 2026-71763','706','44566','VEN',10.0,'VALIDATION_PRECOMPTA','2026-05-08 09:37:45');
CREATE TABLE workflow_expert_comptable_v2 (
            id SERIAL PRIMARY KEY ,
            document_id INTEGER,
            statut TEXT,
            validateur TEXT,
            commentaire TEXT,
            date_action TEXT
        );
INSERT INTO workflow_expert_comptable_v2 VALUES(1,3,'APPROUVE','expert_local','Validation expert-comptable simul├®e','2026-05-08 09:39:11');
INSERT INTO workflow_expert_comptable_v2 VALUES(2,3,'REJETE','expert_local','Validation expert-comptable simul├®e','2026-05-08 09:39:32');
CREATE TABLE clotures_comptables_v3 (
            id SERIAL PRIMARY KEY ,
            date_cloture TEXT,
            total_debit REAL,
            total_credit REAL,
            resultat REAL,
            empreinte_sha256 TEXT,
            statut TEXT
        );
INSERT INTO clotures_comptables_v3 VALUES(1,'2026-05-08 09:58:55',532.49,532.49,0.0,'1e682afa9a46870cc9a3a3aa9e4735479dab5529b66abe1491d158534750980f','CLOTURE_SIMULEE');
CREATE TABLE connecteurs_bancaires_dsp2_v3 (
            id SERIAL PRIMARY KEY ,
            banque TEXT,
            statut TEXT,
            derniere_synchro TEXT,
            commentaire TEXT
        );
INSERT INTO connecteurs_bancaires_dsp2_v3 VALUES(1,'BANQUE_DEMO_DSP2','SYNCHRONISE','2026-05-08 09:59:35','Simulation DSP2 locale. Pas encore de connexion bancaire r├®elle.');
CREATE TABLE lettrages_auto_v4 (
            id SERIAL PRIMARY KEY ,
            compte TEXT,
            libelle TEXT,
            montant REAL,
            statut TEXT,
            date_lettrage TEXT
        );
INSERT INTO lettrages_auto_v4 VALUES(1,'411','VENTE Qonto (Olinda SAS) n',522.49,'LETTRAGE_SUGGERE','2026-05-08 12:56:11');
INSERT INTO lettrages_auto_v4 VALUES(2,'411','VENTE FACTURE2026-71763 2026-71763',10.0,'LETTRAGE_SUGGERE','2026-05-08 12:56:11');
CREATE TABLE relances_clients_v4 (
            id SERIAL PRIMARY KEY ,
            client TEXT,
            facture TEXT,
            montant REAL,
            niveau TEXT,
            message TEXT,
            date_relance TEXT
        );
INSERT INTO relances_clients_v4 VALUES(1,'murielle','FD-2026-00001',300.0,'RELANCE_1','Relance automatique : facture FD-2026-00001 de 300.0 EUR en attente de paiement.','2026-05-08 12:56:17');
INSERT INTO relances_clients_v4 VALUES(2,'murielle','FD-2026-00002',240.0,'RELANCE_1','Relance automatique : facture FD-2026-00002 de 240.0 EUR en attente de paiement.','2026-05-08 12:56:17');
CREATE TABLE echeancier_fournisseurs_v4 (
            id SERIAL PRIMARY KEY ,
            fournisseur TEXT,
            facture TEXT,
            montant REAL,
            date_echeance TEXT,
            statut TEXT
        );
CREATE TABLE immobilisations_v4 (
            id SERIAL PRIMARY KEY ,
            nom TEXT,
            valeur REAL,
            duree INTEGER,
            date_acquisition TEXT,
            compte TEXT
        );
CREATE TABLE analytique_v4 (
            id SERIAL PRIMARY KEY ,
            axe TEXT,
            compte TEXT,
            montant REAL,
            commentaire TEXT
        );
CREATE TABLE budgets_v4 (
            id SERIAL PRIMARY KEY ,
            axe TEXT,
            budget REAL,
            realise REAL,
            ecart REAL
        );
CREATE TABLE roles_permissions_v4 (
            id SERIAL PRIMARY KEY ,
            utilisateur TEXT,
            role TEXT,
            permission TEXT,
            statut TEXT
        );
CREATE TABLE journal_legal_v4 (
            id SERIAL PRIMARY KEY ,
            evenement TEXT,
            detail TEXT,
            empreinte_sha256 TEXT,
            date_evenement TEXT
        );
INSERT INTO journal_legal_v4 VALUES(1,'CONTROLE_LEGAL','Journalisation l├®gale compl├¿te simul├®e','0347962947334025d2195df3536e0bd90f8550bce86e4443ed5fb7e1f2bf3cb0','2026-05-08 12:56:41');
CREATE TABLE coffre_fort_probatoire_v4 (
            id SERIAL PRIMARY KEY ,
            fichier TEXT,
            chemin TEXT,
            empreinte_sha256 TEXT,
            date_depot TEXT
        );
INSERT INTO coffre_fort_probatoire_v4 VALUES(1,'coffre_probatoire_20260508_125649.sqlite','C:/Users/alain/mon-projet-agent/coffre_fort_probatoire_v4\coffre_probatoire_20260508_125649.sqlite','3bb0ac74adb9a7693033b631ebb516315e9cc9e73336700cd3b3c9e3c8fc8842','2026-05-08 12:56:49');
CREATE TABLE parametres_societe_v5 (
            id SERIAL PRIMARY KEY ,
            raison_sociale TEXT,
            siret TEXT,
            tva_intracom TEXT,
            adresse TEXT,
            email TEXT,
            date_modification TEXT
        );
CREATE TABLE numerotation_officielle_v5 (
            id SERIAL PRIMARY KEY ,
            type_document TEXT,
            prefixe TEXT,
            prochain_numero INTEGER,
            date_modification TEXT
        );
CREATE TABLE exercices_comptables_v5 (
            id SERIAL PRIMARY KEY ,
            nom TEXT,
            date_debut TEXT,
            date_fin TEXT,
            statut TEXT,
            date_creation TEXT
        );
CREATE TABLE journal_actions_v5 (
            id SERIAL PRIMARY KEY ,
            action TEXT,
            detail TEXT,
            date_action TEXT
        );
INSERT INTO journal_actions_v5 VALUES(1,'SAUVEGARDE_AVANT_CLOTURE','Sauvegarde cr├®├®e : C:/Users/alain/mon-projet-agent/sauvegardes_avant_cloture_v5\sauvegarde_avant_cloture_20260508_143708.sqlite','2026-05-08 14:37:08');
CREATE TABLE sauvegardes_avant_cloture_v5 (
            id SERIAL PRIMARY KEY ,
            fichier TEXT,
            chemin TEXT,
            empreinte_sha256 TEXT,
            date_sauvegarde TEXT
        );
INSERT INTO sauvegardes_avant_cloture_v5 VALUES(1,'sauvegarde_avant_cloture_20260508_143708.sqlite','C:/Users/alain/mon-projet-agent/sauvegardes_avant_cloture_v5\sauvegarde_avant_cloture_20260508_143708.sqlite','5bb34a965c72a9e557e9fddf178bab5315bc38ef37142659a58766a32b0febdb','2026-05-08 14:37:08');
CREATE TABLE tenants_v6 (
            id SERIAL PRIMARY KEY ,
            nom TEXT,
            code TEXT,
            statut TEXT,
            date_creation TEXT
        );
CREATE TABLE abonnements_v6 (
            id SERIAL PRIMARY KEY ,
            tenant TEXT,
            plan TEXT,
            prix REAL,
            statut TEXT,
            date_creation TEXT
        );
CREATE TABLE droits_modules_v6 (
            id SERIAL PRIMARY KEY ,
            utilisateur TEXT,
            module TEXT,
            droit TEXT,
            date_creation TEXT
        );
CREATE TABLE journal_acces_v6 (
            id SERIAL PRIMARY KEY ,
            utilisateur TEXT,
            ip TEXT,
            page TEXT,
            date_acces TEXT
        );
INSERT INTO journal_acces_v6 VALUES(1,'utilisateur_local','127.0.0.1','/ecritures/journal-acces-v6','2026-05-08 15:17:48');
CREATE TABLE mode_application_v6 (
            id SERIAL PRIMARY KEY ,
            mode TEXT,
            date_activation TEXT
        );
INSERT INTO mode_application_v6 VALUES(1,'LECTURE_SEULE','2026-05-08 15:18:20');
INSERT INTO mode_application_v6 VALUES(2,'MAINTENANCE','2026-05-08 15:18:30');
CREATE TABLE erreurs_systeme_v6 (
            id SERIAL PRIMARY KEY ,
            type_erreur TEXT,
            message TEXT,
            date_erreur TEXT
        );
INSERT INTO erreurs_systeme_v6 VALUES(1,'SIMULATION','Erreur simul├®e pour tester le monitoring','2026-05-08 15:18:40');
CREATE TABLE taches_automatiques_v7 (
            id SERIAL PRIMARY KEY ,
            nom TEXT,
            type_tache TEXT,
            frequence TEXT,
            statut TEXT,
            derniere_execution TEXT,
            date_creation TEXT
        );
INSERT INTO taches_automatiques_v7 VALUES(1,'Test scheduler','Test','quotidienne','ACTIVE','','2026-05-09 02:23:17');
INSERT INTO taches_automatiques_v7 VALUES(2,'Robot relances clients','RELANCES_CLIENTS','quotidienne','ACTIVE','','2026-05-09 13:59:28');
CREATE TABLE scenarios_intelligents_v7 (
            id SERIAL PRIMARY KEY ,
            nom TEXT,
            condition_declenchement TEXT,
            action TEXT,
            statut TEXT,
            date_creation TEXT
        );
CREATE TABLE alertes_metier_v7 (
            id SERIAL PRIMARY KEY ,
            alerte TEXT,
            niveau TEXT,
            date_alerte TEXT
        );
INSERT INTO alertes_metier_v7 VALUES(1,'ALERTE : 2 facture(s) non pay├®e(s).','CRITIQUE','2026-05-08 22:44:41');
INSERT INTO alertes_metier_v7 VALUES(2,'ALERTE : 2 document(s) comptable(s) ├á traiter.','CRITIQUE','2026-05-08 22:44:41');
CREATE TABLE notifications_internes_v7 (
            id SERIAL PRIMARY KEY ,
            destinataire TEXT,
            message TEXT,
            statut TEXT,
            date_creation TEXT
        );
INSERT INTO notifications_internes_v7 VALUES(1,'Alain baudinaud','mmmmmmmmmmmm','NON_LUE','2026-05-09 14:51:31');
INSERT INTO notifications_internes_v7 VALUES(2,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-09 23:37:36');
INSERT INTO notifications_internes_v7 VALUES(3,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-09 23:42:15');
INSERT INTO notifications_internes_v7 VALUES(4,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-09 23:55:57');
INSERT INTO notifications_internes_v7 VALUES(5,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:00:58');
INSERT INTO notifications_internes_v7 VALUES(6,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:05:58');
INSERT INTO notifications_internes_v7 VALUES(7,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:09:57');
INSERT INTO notifications_internes_v7 VALUES(8,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:12:13');
INSERT INTO notifications_internes_v7 VALUES(9,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:14:47');
INSERT INTO notifications_internes_v7 VALUES(10,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:16:35');
INSERT INTO notifications_internes_v7 VALUES(11,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:17:44');
INSERT INTO notifications_internes_v7 VALUES(12,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:20:12');
INSERT INTO notifications_internes_v7 VALUES(13,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:23:30');
INSERT INTO notifications_internes_v7 VALUES(14,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:28:30');
INSERT INTO notifications_internes_v7 VALUES(15,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:31:03');
INSERT INTO notifications_internes_v7 VALUES(16,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:33:30');
INSERT INTO notifications_internes_v7 VALUES(17,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:34:53');
INSERT INTO notifications_internes_v7 VALUES(18,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:35:32');
INSERT INTO notifications_internes_v7 VALUES(19,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:38:30');
INSERT INTO notifications_internes_v7 VALUES(20,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:43:10');
INSERT INTO notifications_internes_v7 VALUES(21,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:46:56');
INSERT INTO notifications_internes_v7 VALUES(22,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:51:42');
INSERT INTO notifications_internes_v7 VALUES(23,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:54:43');
INSERT INTO notifications_internes_v7 VALUES(24,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:56:36');
INSERT INTO notifications_internes_v7 VALUES(25,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 00:58:59');
INSERT INTO notifications_internes_v7 VALUES(26,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 01:03:03');
INSERT INTO notifications_internes_v7 VALUES(27,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 01:08:33');
INSERT INTO notifications_internes_v7 VALUES(28,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 01:15:16');
INSERT INTO notifications_internes_v7 VALUES(29,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 01:20:50');
INSERT INTO notifications_internes_v7 VALUES(30,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 01:22:07');
INSERT INTO notifications_internes_v7 VALUES(31,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 01:32:05');
INSERT INTO notifications_internes_v7 VALUES(32,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 01:37:05');
INSERT INTO notifications_internes_v7 VALUES(33,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 01:41:03');
INSERT INTO notifications_internes_v7 VALUES(34,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 01:43:20');
INSERT INTO notifications_internes_v7 VALUES(35,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 01:57:06');
INSERT INTO notifications_internes_v7 VALUES(36,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 01:58:02');
INSERT INTO notifications_internes_v7 VALUES(37,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 02:03:25');
INSERT INTO notifications_internes_v7 VALUES(38,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 02:10:54');
INSERT INTO notifications_internes_v7 VALUES(39,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 02:14:27');
INSERT INTO notifications_internes_v7 VALUES(40,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 02:18:22');
INSERT INTO notifications_internes_v7 VALUES(41,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 02:27:40');
INSERT INTO notifications_internes_v7 VALUES(42,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 02:32:40');
INSERT INTO notifications_internes_v7 VALUES(43,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 02:37:40');
INSERT INTO notifications_internes_v7 VALUES(44,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 02:42:40');
INSERT INTO notifications_internes_v7 VALUES(45,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 02:47:40');
INSERT INTO notifications_internes_v7 VALUES(46,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 02:52:40');
INSERT INTO notifications_internes_v7 VALUES(47,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 02:57:40');
INSERT INTO notifications_internes_v7 VALUES(48,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 03:02:40');
INSERT INTO notifications_internes_v7 VALUES(49,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 03:07:40');
INSERT INTO notifications_internes_v7 VALUES(50,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 03:12:40');
INSERT INTO notifications_internes_v7 VALUES(51,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 03:17:40');
INSERT INTO notifications_internes_v7 VALUES(52,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 03:22:40');
INSERT INTO notifications_internes_v7 VALUES(53,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 03:27:40');
INSERT INTO notifications_internes_v7 VALUES(54,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 03:32:40');
INSERT INTO notifications_internes_v7 VALUES(55,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 03:37:40');
INSERT INTO notifications_internes_v7 VALUES(56,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 03:42:40');
INSERT INTO notifications_internes_v7 VALUES(57,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 03:47:40');
INSERT INTO notifications_internes_v7 VALUES(58,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 03:52:40');
INSERT INTO notifications_internes_v7 VALUES(59,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 03:57:41');
INSERT INTO notifications_internes_v7 VALUES(60,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 04:02:41');
INSERT INTO notifications_internes_v7 VALUES(61,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 04:07:41');
INSERT INTO notifications_internes_v7 VALUES(62,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 04:12:41');
INSERT INTO notifications_internes_v7 VALUES(63,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 04:17:41');
INSERT INTO notifications_internes_v7 VALUES(64,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 04:22:41');
INSERT INTO notifications_internes_v7 VALUES(65,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 04:27:41');
INSERT INTO notifications_internes_v7 VALUES(66,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 04:32:41');
INSERT INTO notifications_internes_v7 VALUES(67,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 04:37:41');
INSERT INTO notifications_internes_v7 VALUES(68,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 04:42:41');
INSERT INTO notifications_internes_v7 VALUES(69,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 04:47:41');
INSERT INTO notifications_internes_v7 VALUES(70,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 04:52:41');
INSERT INTO notifications_internes_v7 VALUES(71,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 04:57:41');
INSERT INTO notifications_internes_v7 VALUES(72,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 05:02:41');
INSERT INTO notifications_internes_v7 VALUES(73,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 05:07:41');
INSERT INTO notifications_internes_v7 VALUES(74,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 05:12:41');
INSERT INTO notifications_internes_v7 VALUES(75,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 05:17:41');
INSERT INTO notifications_internes_v7 VALUES(76,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 05:22:41');
INSERT INTO notifications_internes_v7 VALUES(77,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 05:27:41');
INSERT INTO notifications_internes_v7 VALUES(78,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 05:32:41');
INSERT INTO notifications_internes_v7 VALUES(79,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 05:37:41');
INSERT INTO notifications_internes_v7 VALUES(80,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 05:42:41');
INSERT INTO notifications_internes_v7 VALUES(81,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 05:47:41');
INSERT INTO notifications_internes_v7 VALUES(82,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 05:52:41');
INSERT INTO notifications_internes_v7 VALUES(83,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 05:57:41');
INSERT INTO notifications_internes_v7 VALUES(84,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 06:02:41');
INSERT INTO notifications_internes_v7 VALUES(85,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 06:07:42');
INSERT INTO notifications_internes_v7 VALUES(86,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 06:12:42');
INSERT INTO notifications_internes_v7 VALUES(87,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 06:17:42');
INSERT INTO notifications_internes_v7 VALUES(88,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 06:22:42');
INSERT INTO notifications_internes_v7 VALUES(89,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 06:27:42');
INSERT INTO notifications_internes_v7 VALUES(90,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 06:32:42');
INSERT INTO notifications_internes_v7 VALUES(91,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 06:37:42');
INSERT INTO notifications_internes_v7 VALUES(92,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 06:42:42');
INSERT INTO notifications_internes_v7 VALUES(93,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 06:47:42');
INSERT INTO notifications_internes_v7 VALUES(94,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 06:52:42');
INSERT INTO notifications_internes_v7 VALUES(95,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 06:57:42');
INSERT INTO notifications_internes_v7 VALUES(96,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 07:02:42');
INSERT INTO notifications_internes_v7 VALUES(97,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 07:07:42');
INSERT INTO notifications_internes_v7 VALUES(98,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 07:12:42');
INSERT INTO notifications_internes_v7 VALUES(99,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 07:17:42');
INSERT INTO notifications_internes_v7 VALUES(100,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 07:22:42');
INSERT INTO notifications_internes_v7 VALUES(101,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 07:27:42');
INSERT INTO notifications_internes_v7 VALUES(102,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 07:32:42');
INSERT INTO notifications_internes_v7 VALUES(103,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 07:37:42');
INSERT INTO notifications_internes_v7 VALUES(104,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 07:42:42');
INSERT INTO notifications_internes_v7 VALUES(105,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 07:47:42');
INSERT INTO notifications_internes_v7 VALUES(106,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 07:52:42');
INSERT INTO notifications_internes_v7 VALUES(107,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 07:57:42');
INSERT INTO notifications_internes_v7 VALUES(108,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 08:02:42');
INSERT INTO notifications_internes_v7 VALUES(109,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 08:07:42');
INSERT INTO notifications_internes_v7 VALUES(110,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 08:12:42');
INSERT INTO notifications_internes_v7 VALUES(111,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 08:17:42');
INSERT INTO notifications_internes_v7 VALUES(112,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 08:22:42');
INSERT INTO notifications_internes_v7 VALUES(113,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 08:27:43');
INSERT INTO notifications_internes_v7 VALUES(114,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 08:32:43');
INSERT INTO notifications_internes_v7 VALUES(115,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 08:37:43');
INSERT INTO notifications_internes_v7 VALUES(116,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 08:42:43');
INSERT INTO notifications_internes_v7 VALUES(117,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 08:47:43');
INSERT INTO notifications_internes_v7 VALUES(118,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 08:52:43');
INSERT INTO notifications_internes_v7 VALUES(119,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 08:57:43');
INSERT INTO notifications_internes_v7 VALUES(120,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 09:06:47');
INSERT INTO notifications_internes_v7 VALUES(121,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 09:12:22');
INSERT INTO notifications_internes_v7 VALUES(122,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 09:16:52');
INSERT INTO notifications_internes_v7 VALUES(123,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 09:19:46');
INSERT INTO notifications_internes_v7 VALUES(124,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 09:20:51');
INSERT INTO notifications_internes_v7 VALUES(125,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 09:24:22');
INSERT INTO notifications_internes_v7 VALUES(126,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 09:36:40');
INSERT INTO notifications_internes_v7 VALUES(127,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 09:44:38');
INSERT INTO notifications_internes_v7 VALUES(128,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 09:45:26');
INSERT INTO notifications_internes_v7 VALUES(129,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 09:50:25');
INSERT INTO notifications_internes_v7 VALUES(130,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 09:55:26');
INSERT INTO notifications_internes_v7 VALUES(131,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 10:00:26');
INSERT INTO notifications_internes_v7 VALUES(132,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 10:05:26');
INSERT INTO notifications_internes_v7 VALUES(133,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 10:10:26');
INSERT INTO notifications_internes_v7 VALUES(134,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 10:15:26');
INSERT INTO notifications_internes_v7 VALUES(135,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 10:20:26');
INSERT INTO notifications_internes_v7 VALUES(136,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 10:28:35');
INSERT INTO notifications_internes_v7 VALUES(137,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 10:33:35');
INSERT INTO notifications_internes_v7 VALUES(138,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 10:38:35');
INSERT INTO notifications_internes_v7 VALUES(139,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 10:40:57');
INSERT INTO notifications_internes_v7 VALUES(140,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 10:44:34');
INSERT INTO notifications_internes_v7 VALUES(141,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 10:49:50');
INSERT INTO notifications_internes_v7 VALUES(142,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 10:53:08');
INSERT INTO notifications_internes_v7 VALUES(143,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 10:58:08');
INSERT INTO notifications_internes_v7 VALUES(144,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 11:03:08');
INSERT INTO notifications_internes_v7 VALUES(145,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 11:08:08');
INSERT INTO notifications_internes_v7 VALUES(146,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 11:13:08');
INSERT INTO notifications_internes_v7 VALUES(147,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 11:18:08');
INSERT INTO notifications_internes_v7 VALUES(148,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 11:28:09');
INSERT INTO notifications_internes_v7 VALUES(149,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 11:33:09');
INSERT INTO notifications_internes_v7 VALUES(150,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 11:37:46');
INSERT INTO notifications_internes_v7 VALUES(151,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 11:44:44');
INSERT INTO notifications_internes_v7 VALUES(152,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 11:49:44');
INSERT INTO notifications_internes_v7 VALUES(153,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 11:54:44');
INSERT INTO notifications_internes_v7 VALUES(154,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 12:05:21');
INSERT INTO notifications_internes_v7 VALUES(155,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 12:10:33');
INSERT INTO notifications_internes_v7 VALUES(156,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 12:12:41');
INSERT INTO notifications_internes_v7 VALUES(157,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 12:19:40');
INSERT INTO notifications_internes_v7 VALUES(158,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 12:22:26');
INSERT INTO notifications_internes_v7 VALUES(159,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 12:27:26');
INSERT INTO notifications_internes_v7 VALUES(160,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 12:32:26');
INSERT INTO notifications_internes_v7 VALUES(161,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 12:34:40');
INSERT INTO notifications_internes_v7 VALUES(162,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 12:35:03');
INSERT INTO notifications_internes_v7 VALUES(163,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 12:37:26');
INSERT INTO notifications_internes_v7 VALUES(164,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 12:38:30');
INSERT INTO notifications_internes_v7 VALUES(165,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 12:43:30');
INSERT INTO notifications_internes_v7 VALUES(166,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 12:45:53');
INSERT INTO notifications_internes_v7 VALUES(167,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 12:50:53');
INSERT INTO notifications_internes_v7 VALUES(168,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 12:55:53');
INSERT INTO notifications_internes_v7 VALUES(169,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 13:00:53');
INSERT INTO notifications_internes_v7 VALUES(170,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 13:05:53');
INSERT INTO notifications_internes_v7 VALUES(171,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 13:10:53');
INSERT INTO notifications_internes_v7 VALUES(172,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 13:15:53');
INSERT INTO notifications_internes_v7 VALUES(173,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 13:20:53');
INSERT INTO notifications_internes_v7 VALUES(174,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 13:25:53');
INSERT INTO notifications_internes_v7 VALUES(175,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 13:30:53');
INSERT INTO notifications_internes_v7 VALUES(176,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 13:35:54');
INSERT INTO notifications_internes_v7 VALUES(177,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 13:40:54');
INSERT INTO notifications_internes_v7 VALUES(178,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 13:45:54');
INSERT INTO notifications_internes_v7 VALUES(179,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 13:50:54');
INSERT INTO notifications_internes_v7 VALUES(180,'admin','Relances clients : v├®rification automatique effectu├®e par le robot V7.','NON_LUE','2026-05-10 13:55:54');
CREATE TABLE emails_automatiques_v7 (
            id SERIAL PRIMARY KEY ,
            destinataire TEXT,
            sujet TEXT,
            message TEXT,
            statut TEXT,
            date_creation TEXT
        );
INSERT INTO emails_automatiques_v7 VALUES(1,'murielle','Relance facture FD-2026-00001','Relance automatique : facture FD-2026-00001 de 300.0 EUR en attente de paiement.','BROUILLON_EMAIL','2026-05-08 22:46:57');
INSERT INTO emails_automatiques_v7 VALUES(2,'murielle','Relance facture FD-2026-00002','Relance automatique : facture FD-2026-00002 de 240.0 EUR en attente de paiement.','BROUILLON_EMAIL','2026-05-08 22:46:57');
INSERT INTO emails_automatiques_v7 VALUES(3,'murielle','Relance facture FD-2026-00001','Relance automatique : facture FD-2026-00001 de 300.0 EUR en attente de paiement.','BROUILLON_EMAIL','2026-05-08 22:48:04');
INSERT INTO emails_automatiques_v7 VALUES(4,'murielle','Relance facture FD-2026-00002','Relance automatique : facture FD-2026-00002 de 240.0 EUR en attente de paiement.','BROUILLON_EMAIL','2026-05-08 22:48:04');
CREATE TABLE scheduler_automatique_v7 (
            id SERIAL PRIMARY KEY ,
            nom TEXT,
            prochaine_execution TEXT,
            statut TEXT
        );
INSERT INTO scheduler_automatique_v7 VALUES(1,'Scheduler quotidien ComptaPilot','2026-05-08 22:48:27','PLANIFIE');
CREATE TABLE journal_orchestration_v7 (
            id SERIAL PRIMARY KEY ,
            evenement TEXT,
            detail TEXT,
            date_evenement TEXT
        );
CREATE TABLE signatures (
            id SERIAL PRIMARY KEY ,
            document TEXT,
            signataire TEXT,
            date_signature TEXT,
            empreinte_sha256 TEXT
        );
INSERT INTO signatures VALUES(1,'TEST_DOC','ALAIN','2026-05-09 01:45:31','403655f4323f728364790d5bcb4e917eeab9ce97db922a46c1ea3e0c7171b3cc');
PRAGMA writable_schema=ON;
CREATE TABLE IF NOT EXISTS sqlite_sequence(name,seq);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('users',2);
INSERT INTO sqlite_sequence VALUES('plan_comptable',12);
INSERT INTO sqlite_sequence VALUES('ecritures',48);
INSERT INTO sqlite_sequence VALUES('factures',2);
INSERT INTO sqlite_sequence VALUES('clients',1);
INSERT INTO sqlite_sequence VALUES('clotures',1);
INSERT INTO sqlite_sequence VALUES('factures_dematerialisees',2);
INSERT INTO sqlite_sequence VALUES('audit_log',1647);
INSERT INTO sqlite_sequence VALUES('workflow_factures_pdp_v2',3);
INSERT INTO sqlite_sequence VALUES('documents_comptables_importes',3);
INSERT INTO sqlite_sequence VALUES('extractions_documents_comptables',3);
INSERT INTO sqlite_sequence VALUES('precomptabilisation_documents',5);
INSERT INTO sqlite_sequence VALUES('ecritures_auto',6);
INSERT INTO sqlite_sequence VALUES('regles_comptables_ia',1);
INSERT INTO sqlite_sequence VALUES('analyses_ia_documents',2);
INSERT INTO sqlite_sequence VALUES('fournisseurs_ia_v2',1);
INSERT INTO sqlite_sequence VALUES('historique_apprentissage_ia_v2',2);
INSERT INTO sqlite_sequence VALUES('workflow_expert_comptable_v2',2);
INSERT INTO sqlite_sequence VALUES('clotures_comptables_v3',1);
INSERT INTO sqlite_sequence VALUES('connecteurs_bancaires_dsp2_v3',1);
INSERT INTO sqlite_sequence VALUES('lettrages_auto_v4',2);
INSERT INTO sqlite_sequence VALUES('relances_clients_v4',2);
INSERT INTO sqlite_sequence VALUES('journal_legal_v4',1);
INSERT INTO sqlite_sequence VALUES('coffre_fort_probatoire_v4',1);
INSERT INTO sqlite_sequence VALUES('sauvegardes_avant_cloture_v5',1);
INSERT INTO sqlite_sequence VALUES('journal_actions_v5',1);
INSERT INTO sqlite_sequence VALUES('journal_acces_v6',1);
INSERT INTO sqlite_sequence VALUES('mode_application_v6',2);
INSERT INTO sqlite_sequence VALUES('erreurs_systeme_v6',1);
INSERT INTO sqlite_sequence VALUES('alertes_metier_v7',2);
INSERT INTO sqlite_sequence VALUES('emails_automatiques_v7',4);
INSERT INTO sqlite_sequence VALUES('scheduler_automatique_v7',1);
INSERT INTO sqlite_sequence VALUES('signatures',1);
INSERT INTO sqlite_sequence VALUES('taches_automatiques_v7',2);
INSERT INTO sqlite_sequence VALUES('notifications_internes_v7',180);
PRAGMA writable_schema=OFF;
COMMIT;
