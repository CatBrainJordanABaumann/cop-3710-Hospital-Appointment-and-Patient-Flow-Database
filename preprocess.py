import pandas as pd
import random


DOCTOR_COUNT = 10000

def gen_random_doctor_id() -> int:
    return random.randrange(0, 1000) if random.random() > 0.25 else -1


input_data = pd.read_csv("InputData.csv")

line_count = 0

appointment_data = []
doctor_data = []
locker_data = []
patients_read = []
patient_data = []
patient_doctor_data = []

for i in range(DOCTOR_COUNT):
    has_locker = random.random() > 0.25
    doctor_data.append((i, len(locker_data) if has_locker else -1))
    if has_locker:
        locker_data.append((len(locker_data), i, "D"))

for (raw_patient_id, appointment_id, gender, scheduled_day, appointment_day, age,
    neighbourhood, scholarship, hypertension, diabetes, alcoholism, handicap,
    sms_received, no_show) in input_data.itertuples(index=False):
    patient_id = int(raw_patient_id)
    doctor_id = gen_random_doctor_id()
    
    appointment_data.append((int(appointment_id), patient_id,\
        scheduled_day, appointment_day, int(sms_received),\
        0 if no_show == "No" else 1, gen_random_doctor_id()))
    
    if patient_id not in patients_read:
        has_locker = random.random() > 0.25
        patient_data.append((patient_id, 0 if gender == "M" else 1,
            int(age), neighbourhood, int(scholarship), int(hypertension),\
            int(diabetes), int(alcoholism), int(handicap),\
            len(locker_data) if has_locker else -1))
        if has_locker:
            locker_data.append((len(locker_data), i, "P"))
        patients_read.append(patient_id)
    
    if doctor_id != -1 and (patient_id, doctor_id) not in patient_doctor_data:
        patient_doctor_data.append((patient_id, doctor_id))
    
    line_count += 1
    if line_count % 1000 == 0:
        print(line_count)
    
appointment_df = pd.DataFrame(appointment_data, columns= ["appointment_id",\
    "patient_id", "scheduled_day", "appointment_day",\
    "sms_received", "no_show", "doctor_id"])

doctor_df = pd.DataFrame(doctor_data, columns= ["doctor_id", "locker_id"])

locker_df = pd.DataFrame(locker_data, columns= ["locker_id", "user_id", "user_type"])

patient_df = pd.DataFrame(patient_data, columns= ["patient_id", "gender",\
    "age", "neighbourhood", "scholarship", "hypertension", "diabetes",\
    "alcoholism", "handicap", "locker_id"])

patient_doctor_df = pd.DataFrame(patient_doctor_data, columns= ["patient_id", "doctor_id"])

appointment_df.to_csv("data/appointment.csv", index=False)
doctor_df.to_csv("data/doctor.csv", index=False)
locker_df.to_csv("data/locker.csv", index=False)
patient_df.to_csv("data/patient.csv", index=False)
patient_doctor_df.to_csv("data/patient_doctor.csv", index=False)