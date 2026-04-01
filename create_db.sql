CREATE TABLE Patient (
    patient_id NUMBER NOT NULL PRIMARY KEY,
    gender NUMBER,
    age NUMBER,
    neighbourhood VARCHAR2(50),
    scholarship NUMBER,
    hypertension NUMBER,
    diabetes NUMBER,
    alcoholism NUMBER,
    handicap NUMBER,
    locker_id NUMBER
);


CREATE TABLE Locker (
    locker_id NUMBER NOT NULL PRIMARY KEY,
    user_id NUMBER,
    user_type VARCHAR2(1)
);


ALTER TABLE Patient ADD (
    CONSTRAINT FK_Patient_Locker
    FOREIGN KEY (locker_id)
    REFERENCES Locker(locker_id)
);


CREATE TABLE Doctor (
    doctor_id NUMBER NOT NULL PRIMARY KEY,
    locker_id NUMBER,
    CONSTRAINT FK_Doctor_Locker
        FOREIGN KEY (locker_id)
        REFERENCES Locker(locker_id)
);


CREATE TABLE Patient_Doctor (
    patient_id NUMBER NOT NULL,
    doctor_id NUMBER NOT NULL,
    CONSTRAINT PK_Patient_Doctor
        PRIMARY KEY (patient_id, doctor_id),
    CONSTRAINT FK_PD_Patient
        FOREIGN KEY (patient_id)
        REFERENCES Patient(patient_id),
    CONSTRAINT FK_PD_Doctor
        FOREIGN KEY (doctor_id)
        REFERENCES Doctor(doctor_id)
);


CREATE TABLE Appointment (
    appointment_id NUMBER NOT NULL,
    patient_id NUMBER NOT NULL,
    scheduled_day VARCHAR2(20) NOT NULL,
    appointment_day VARCHAR2(20) NOT NULL,
    no_show NUMBER,
    sms_received NUMBER,
    doctor_id NUMBER,
    CONSTRAINT PK_Appointment
        PRIMARY KEY (appointment_id, patient_id),
    CONSTRAINT FK_Appointment_Patient
        FOREIGN KEY (patient_id)
        REFERENCES Patient(patient_id),
    CONSTRAINT FK_Appointment_Doctor
        FOREIGN KEY (doctor_id)
        REFERENCES Doctor(doctor_id)
    -- Oracle doesn't seem to allow NULL values for optional foreign keys
    -- so I had to comment out that constraint
);
