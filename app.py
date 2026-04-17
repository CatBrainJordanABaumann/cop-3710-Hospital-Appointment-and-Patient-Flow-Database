from dataload import *
import streamlit as st

conn, cursor = open_connection()
load_lockers(cursor)
load_doctors(cursor)
load_patients(cursor)
load_appointments(cursor)
load_patient_doctors(cursor)

st.title("Medical Appointment and Patient Flow Database")

funct = st.selectbox(
    "Select a function:",
    [
        "1. Appointment Count per Patient",
        "2. Doctors Ranked by Patient Count",
        "3. Patients in an Age Range",
        "4. Random Patient Profile",
        "5. Appointments on a Specific Day",
    ]
)

st.divider()


if funct == "1. Appointment Count per Patient":
    st.header("Appointment Count per Patient")

    patient_id_input = st.number_input(
        "Enter Patient ID", min_value=0, step=1, key="appt_patient"
    )

    if st.button("Get Appointment Count"):
        query = """
            SELECT p.patient_id, COUNT(a.appointment_id) AS appointment_count 
            FROM Patient p 
            LEFT JOIN Appointment a ON p.patient_id = a.patient_id
            WHERE p.patient_id = :patient_id
            GROUP BY p.patient_id
        """
        df = pd.read_sql_query(query, conn, params={"patient_id": int(patient_id_input)})
        if df.empty:
            st.warning("No patient found with that ID.")
        else:
            count = df["APPOINTMENT_COUNT"].iloc[0]
            st.success(
                f"Patient {int(patient_id_input)} has "
                f"**{int(count)}** appointment(s) scheduled."
            )
            st.dataframe(df)


elif funct == "2. Doctors Ranked by Patient Count":
    st.header("Doctors Ranked by Patient Count")

    if st.button("Show Doctor Rankings"):
        query = """
            SELECT doctor_id, patient_count,
            RANK() OVER (ORDER BY patient_count DESC) AS doctor_rank
            FROM (SELECT d.doctor_id, COUNT(pd.patient_id) AS patient_count
            FROM Doctor d
            LEFT JOIN Patient_Doctor pd ON d.doctor_id = pd.doctor_id
            GROUP BY d.doctor_id
            )
            ORDER BY doctor_rank
        """
        df = pd.read_sql_query(query, conn)
        st.dataframe(df)


elif funct == "3. Patients in an Age Range":
    st.header("Patients in an Age Range")

    col1, col2 = st.columns(2)
    with col1:
        age_min = st.number_input("Min Age", min_value=0, max_value=120, value=18, key="age_min")
    with col2:
        age_max = st.number_input("Max Age", min_value=0, max_value=120, value=40, key="age_max")

    if st.button("Find Patients by Age Range"):
        query = """
            SELECT p.patient_id, p.age, p.gender, p.neighbourhood, l.locker_id, l.user_type
            FROM Patient p
            LEFT JOIN Locker l ON p.locker_id = l.locker_id
            WHERE p.age BETWEEN :age_min AND :age_max
            ORDER BY p.age
        """
        df = pd.read_sql_query(
            query, conn, params={"age_min": int(age_min), "age_max": int(age_max)}
        )
        st.success(f"Found **{len(df)}** patient(s) between ages {int(age_min)} and {int(age_max)}.")
        st.dataframe(df)


elif funct == "4. Random Patient Profile":
    st.header("Random Patient Profile")

    if st.button("Get Random Patient"):
        query = """
    SELECT *
    FROM (
        SELECT
            p.patient_id,
            p.gender,
            p.age,
            p.neighbourhood,
            p.scholarship,
            p.hypertension,
            p.diabetes,
            p.alcoholism,
            p.handicap,
            l.locker_id,
            l.user_type
        FROM Patient p
        LEFT JOIN Locker l ON p.locker_id = l.locker_id
        ORDER BY DBMS_RANDOM.VALUE
    )
    WHERE ROWNUM = 1
"""
        df = pd.read_sql_query(query, conn)
        st.success(f"Randomly selected Patient ID: **{int(df['PATIENT_ID'].iloc[0])}**")
        st.dataframe(df)


elif funct == "5. Appointments on a Specific Day":
    st.header("Appointments on a Specific Day")

    target_day = st.text_input(
        "Enter appointment day (e.g. 2016-04-29)",
        value="2016-04-29",
        key="appt_day"
    )

    if st.button("Count Appointments"):
        query = """
            SELECT appointment_day, COUNT(*) AS total_appointments
            FROM Appointment
            WHERE appointment_day LIKE :target_day || '%'
            GROUP BY appointment_day
        """
        df = pd.read_sql_query(query, conn, params={"target_day": target_day.strip()})
        if df.empty:
            st.warning(f"No appointments found for '{target_day}'.")
        else:
            total = df["TOTAL_APPOINTMENTS"].sum()
            st.success(f"**{int(total)}** appointment(s) found on {target_day}.")
            st.dataframe(df)

