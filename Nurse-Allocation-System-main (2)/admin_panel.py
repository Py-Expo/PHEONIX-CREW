import streamlit as st
from DEMO import NurseAllocationSystem

# Create an instance of NurseAllocationSystem
system = NurseAllocationSystem()

# Function to authenticate user
def authenticate(username, password):
    # Replace with your authentication logic
    return username == "admin" and password == "admin"

# Login page
def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.success("Login successful!")
            return True
        else:
            st.error("Invalid username or password.")
            return False

# Admin page
def admin_page():
    st.title("Admin Page")

    display_nurse_details()
    display_shift_details()
    display_ward_details()
    display_leave_requests()

# Function to display nurse details
def display_nurse_details():
    st.header("Nurse Details")
    st.subheader("Add Nurse")
    name = st.text_input("Nurse Name")
    specialty = st.text_input("Specialty")
    department = st.text_input("Department")
    if st.button("Add Nurse"):
        if name and specialty and department:
            system.add_nurse(name, specialty, department)
            st.success("Nurse added successfully.")
        else:
            st.error("Please fill in all fields.")

    st.subheader("Nurse List")
    nurses = system.nurses
    if nurses:
        for nurse in nurses:
            st.write(f"Name: {nurse.name}, Specialty: {nurse.specialty}, Department: {nurse.department}")
    else:
        st.write("No nurses added yet.")

# Function to display shift details
def display_shift_details():
    st.header("Shift Details")
    num_shifts = st.number_input("Enter the number of shifts", min_value=1, step=1)
    if st.button("Generate Shifts"):
        system.generate_shifts(num_shifts)
        st.success(f"{num_shifts} shifts generated successfully.")

    shifts = system.shifts
    if shifts:
        st.subheader("Shifts List")
        for shift in shifts:
            st.write(f"Date: {shift.date}, Start Time: {shift.start_time}, End Time: {shift.end_time}, "
                     f"Department Required: {shift.department_required}, Specialty Required: {shift.specialty_required}")
    else:
        st.write("No shifts generated yet.")

# Function to display ward details
def display_ward_details():
    st.header("Ward Details")
    num_wards = st.number_input("Enter the number of wards", min_value=1, step=1)
    if st.button("Add Wards"):
        for _ in range(num_wards):
            ward_name = st.text_input("Enter Ward Name")
            if ward_name:
                system.add_ward(ward_name)
                st.success(f"Ward '{ward_name}' added successfully.")

# Function to display leave requests
def display_leave_requests():
    st.header("Leave Requests")
    leave_request = st.selectbox("Nurse Name for Leave Request", [nurse.name for nurse in system.nurses])
    if st.button("Request Leave"):
        if leave_request:
            system.request_leave(leave_request)
            st.success(f"Leave requested for Nurse '{leave_request}'.")
        else:
            st.error("Please select a nurse.")

# Main Streamlit app
def main():
    if login():
        admin_page()

if __name__ == "__main__":
    main()
