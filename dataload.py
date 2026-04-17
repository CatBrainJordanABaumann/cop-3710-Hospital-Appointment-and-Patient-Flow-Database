import oracledb
import pandas as pd
import pyarrow


def fetch_data(table_name: str, conn: oracledb.Connection):
    return pyarrow.table(conn.fetch_df_all(
        "SELECT * FROM " + table_name)).to_pandas()



LIB_DIR = r"C:\oracle\instantclient_11_2"
DB_USER = input("Username: ")
DB_PASS = input("Password:")
DB_DSN = "localhost:1521/xe"


def open_connection() -> tuple[oracledb.Connection, oracledb.Cursor]:
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
    return conn, cursor


def close_connection(conn, cursor):
    cursor.close()
    conn.close()
    print("Oracle connection closed.")


def load_lockers(cursor):
    data = pd.read_csv("data/locker.csv")

    sql = "INSERT INTO Locker "\
        "(locker_id, user_id, user_type) VALUES (:1, :2, :3)"

    for (locker_id, user_id, user_type) in data.itertuples(index=False):
        cursor.execute(sql, [locker_id, user_id, user_type])


def load_doctors(cursor):
    data = pd.read_csv("data/doctor.csv")

    sql = "INSERT INTO Doctor "\
        "(doctor_id, locker_id) VALUES (:1, :2)"

    for (doctor_id, locker_id) in data.itertuples(index=False):
        cursor.execute(sql, [doctor_id, None if locker_id == -1 else locker_id])
        

def load_appointments(cursor):
    data = pd.read_csv("data/appointment.csv")
    
    sql = "INSERT INTO Appointment "\
        "(appointment_id, patient_id, scheduled_day, appointment_day, "\
        "sms_received, no_show, doctor_id) VALUES "\
        "(:1, :2, :3, :4, :5, :6, :7)"
    
    for (appointment_id, patient_id, scheduled_day, appointment_day,\
        sms_received, no_show, doctor_id) in data.itertuples(index=False):
        cursor.execute(sql, [appointment_id, patient_id,\
            scheduled_day, appointment_day, sms_received, no_show,\
            None if doctor_id == -1 else doctor_id])


def load_patients(cursor):
    data = pd.read_csv("data/patient.csv")

    sql = "INSERT INTO Patient "\
        "(patient_id, gender, age, neighbourhood, scholarship, hypertension, "\
        "diabetes, alcoholism, handicap, locker_id) VALUES "\
        "(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)"
        
    for (patient_id, gender, age, neighbourhood, scholarship, hypertension,\
        diabetes, alcoholism, handicap, locker_id) in data.itertuples(index=False):
        cursor.execute(sql, [patient_id, gender, age, neighbourhood,\
            scholarship, hypertension, diabetes, alcoholism, handicap,\
            None if locker_id == -1 else locker_id])
    
    
def load_patient_doctors(cursor):
    data = pd.read_csv("data/patient_doctor.csv")

    sql = "INSERT INTO Patient_Doctor "\
        "(patient_id, doctor_id) VALUES (:1, :2)"

    for (patient_id, doctor_id) in data.itertuples(index=False):
        cursor.execute(sql, [patient_id, doctor_id])
        

def save_lockers(conn):
    fetch_data("Locker", conn)\
        .to_csv("results/locker.csv", index=False)
    
    
def save_doctors(conn):
    fetch_data("Doctor", conn)\
        .to_csv("results/doctor.csv", index=False)


def save_appointments(conn):
    fetch_data("Appointment", conn)\
        .to_csv("results/appointment.csv", index=False)


def save_patients(conn):
    fetch_data("Patient", conn)\
        .to_csv("results/patient.csv", index=False)


def save_patient_doctors(conn):
    fetch_data("Patient_Doctor", conn)\
        .to_csv("results/patient_doctor.csv", index=False)