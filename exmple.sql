SELECT
    p.first_name,
    d.doctor_name,
    a.appointment_date
FROM patients p
JOIN appointments a
    ON p.patient_id = a.patient_id
JOIN doctors d
    ON a.doctor_id = d.doctor_id;
