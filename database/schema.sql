PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date_of_birth TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS drugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    generic_name TEXT NOT NULL,
    brand_name TEXT,
    active_ingredient TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS prescriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    drug_id INTEGER NOT NULL,
    dosage TEXT,
    frequency TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (drug_id) REFERENCES drugs(id)
);


CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drug_a_id INTEGER NOT NULL,
    drug_b_id INTEGER NOT NULL,
    severity TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (drug_a_id) REFERENCES drugs(id),
    FOREIGN KEY (drug_b_id) REFERENCES drugs(id)
);


CREATE TABLE IF NOT EXISTS allergies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    allergen TEXT NOT NULL,
    reaction TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);