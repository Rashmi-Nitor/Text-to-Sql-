import sqlite3
from pathlib import Path

database_path = Path(__file__).resolve().parent / "healthcare.db"
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Patients
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT,
    age INTEGER,
    city TEXT,
    registration_date DATE
);
""")

# Doctors
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INTEGER PRIMARY KEY,
    doctor_name TEXT NOT NULL,
    specialization TEXT,
    experience_years INTEGER
);
""")

# Diagnoses
cursor.execute("""
CREATE TABLE IF NOT EXISTS diagnoses (
    diagnosis_id INTEGER PRIMARY KEY,
    diagnosis_name TEXT NOT NULL,
    severity TEXT
);
""")

# Appointments
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    diagnosis_id INTEGER,
    appointment_date DATE,
    appointment_status TEXT,

    FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id),

    FOREIGN KEY (doctor_id)
        REFERENCES doctors(doctor_id),

    FOREIGN KEY (diagnosis_id)
        REFERENCES diagnoses(diagnosis_id)
);
""")

# Medications
cursor.execute("""
CREATE TABLE IF NOT EXISTS medications (
    medication_id INTEGER PRIMARY KEY,
    medication_name TEXT NOT NULL,
    medication_type TEXT,
    manufacturer TEXT
);
""")

# Prescriptions
cursor.execute("""
CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_id INTEGER PRIMARY KEY,
    appointment_id INTEGER NOT NULL,
    medication_id INTEGER NOT NULL,
    dosage TEXT,
    duration_days INTEGER,

    FOREIGN KEY (appointment_id)
        REFERENCES appointments(appointment_id),

    FOREIGN KEY (medication_id)
        REFERENCES medications(medication_id)
);
""")

conn.commit()
conn.close()

print("Healthcare database and tables created successfully!")