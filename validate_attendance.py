import pandas as pd

# Load attendance file
df = pd.read_excel("attendance_today.xlsx", dtype=str)

# Convert all remaining PENDING → VALID
df.loc[df["Status"] == "PENDING", "Status"] = "VALID"

# Save updated attendance
df.to_excel("attendance_today.xlsx", index=False)

print("✅ Attendance VALIDATION completed")
