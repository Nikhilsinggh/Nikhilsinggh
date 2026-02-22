import pandas as pd
from datetime import datetime
import os
students = pd.read_csv("student_master.csv")

print(students)
def get_time():
    return datetime.now().strftime("%H:%M:%S")
def mark_attendance(roll_no):

    student = students[students["roll_no"] == roll_no]

    if student.empty:
        print("Student not found")
        return

    record = {
        "Roll No": roll_no,
        "Name": student.iloc[0]["name"],
        "Year": student.iloc[0]["year"],
        "Section": student.iloc[0]["section"],
        "Time": get_time(),
        "Status": "PENDING"
    }

    save_attendance(record)
def save_attendance(record):

    file_name = "attendance_today.xlsx"

    if os.path.exists(file_name):
        df = pd.read_excel(file_name)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])

    df.to_excel(file_name, index=False)

    print("Attendance recorded successfully")

