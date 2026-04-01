import oracledb
import pandas as pd
import pyarrow


def fetch_data(table_name: str):
    return pyarrow.table(conn.fetch_df_all(
        "SELECT * FROM " + table_name)).to_pandas()



LIB_DIR = r"C:\oracle\instantclient_11_2"
DB_USER = "system"
DB_PASS = "GoofyGoober25"
DB_DSN = "localhost:1521/xe"

if LIB_DIR:
    oracledb.init_oracle_client(lib_dir=LIB_DIR)
else:
    oracledb.enable_thin_mode()

try:
    conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
except:
    print("Failed to initialize connection!")

try:
    cursor = conn.cursor()
except:
    print("Failed to initialize cursor!")


appointment_data = pd.read_csv("data/appointment.csv")
doctor_data = pd.read_csv("data/doctor.csv")
locker_data = pd.read_csv("data/locker.csv")
patient_data = pd.read_csv("data/patient.csv")
patient_doctor_data = pd.read_csv("data/patient_doctor.csv")


appointment_sql = "INSERT INTO Appointment\
(appointment_id, patient_id, scheduled_day, appointment_day,\
sms_received, no_show, doctor_id) VALUES \
(:1, :2, :3, :4, :5, :6, :7)"

doctor_sql = "INSERT INTO Doctor\
(doctor_id, locker_id) VALUES (:1, :2)"

locker_sql = "INSERT INTO Locker\
(locker_id, user_id, user_type) VALUES (:1, :2, :3)"

patient_sql = "INSERT INTO Patient\
(patient_id, gender, age, neighbourhood, scholarship, hypertension,\
diabetes, alcoholism, handicap, locker_id) VALUES \
(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)"

patient_doctor_sql = "INSERT INTO Patient_Doctor\
(patient_id, doctor_id) VALUES (:1, :2)"


for (locker_id, user_id, user_type) in locker_data.itertuples(index=False):
    cursor.execute(locker_sql, [locker_id, user_id, user_type])

for (doctor_id, locker_id) in doctor_data.itertuples(index=False):
    cursor.execute(doctor_sql, [doctor_id, None if locker_id == -1 else locker_id])

for (patient_id, gender, age, neighbourhood, scholarship, hypertension,\
    diabetes, alcoholism, handicap, locker_id) in patient_data.itertuples(index=False):
    cursor.execute(patient_sql, [patient_id, gender, age, neighbourhood,\
        scholarship, hypertension, diabetes, alcoholism, handicap,\
        None if locker_id == -1 else locker_id])

for (appointment_id, patient_id, scheduled_day, appointment_day,\
    sms_received, no_show, doctor_id) in appointment_data.itertuples(index=False):
    cursor.execute(appointment_sql, [appointment_id, patient_id,\
        scheduled_day, appointment_day, sms_received, no_show,\
        None if doctor_id == -1 else doctor_id])

for (patient_id, doctor_id) in patient_doctor_data.itertuples(index=False):
    cursor.execute(patient_doctor_sql, [patient_id, doctor_id])



SAVE_RESULTS = True
if SAVE_RESULTS:
    appointment_data = fetch_data("Appointment")
    doctor_data = fetch_data("Doctor")
    locker_data = fetch_data("Locker")
    patient_data = fetch_data("Patient")
    patient_doctor_data = fetch_data("Patient_Doctor")

    appointment_data.to_csv("results/appointment.csv", index=False)
    doctor_data.to_csv("results/doctor.csv", index=False)
    locker_data.to_csv("results/locker.csv", index=False)
    patient_data.to_csv("results/patient.csv", index=False)
    patient_doctor_data.to_csv("results/patient_doctor.csv", index=False)


cursor.close()
conn.close()
print("Oracle connection closed.")