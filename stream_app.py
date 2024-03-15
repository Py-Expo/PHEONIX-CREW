import streamlit as st
from DEMO import NurseAllocationSystem
# Default nurse data
DEFAULT_NURSES = [
   {"name": "Alice", "specialty": "Pediatrics", "department": "Pediatrics"},
    {"name": "Bob", "specialty": "Cardiology", "department": "Cardiology"},
    {"name": "Charlie", "specialty": "Surgery", "department": "Surgery"},
    {"name": "David", "specialty": "Oncology", "department": "Oncology"},
    {"name": "Emma", "specialty": "Psychiatry", "department": "Psychiatry"},
    {"name": "Frank", "specialty": "Emergency Medicine", "department": "Emergency"},
    {"name": "Grace", "specialty": "Dermatology", "department": "Dermatology"},
    {"name": "Hannah", "specialty": "Neurology", "department": "Neurology"},
    {"name": "Isaac", "specialty": "Orthopedics", "department": "Orthopedics"},
    {"name": "Jack", "specialty": "Endocrinology", "department": "Endocrinology"},
    {"name": "Kevin", "specialty": "Gastroenterology", "department": "Gastroenterology"},
    {"name": "Lily", "specialty": "Hematology", "department": "Hematology"},
    {"name": "Mary", "specialty": "Radiology", "department": "Radiology"},
    {"name": "Nancy", "specialty": "Urology", "department": "Urology"},
    {"name": "Oliver", "specialty": "Nephrology", "department": "Nephrology"}
]
# Create an instance of NurseAllocationSystem

system = NurseAllocationSystem()


# Additional nurse attributes
nurse_attributes = {}

# Initialize default nurse data within the system
for nurse in DEFAULT_NURSES:
    name = nurse.get("name", "")
    specialty = nurse.get("specialty", "")
    department = nurse.get("department", "")
    experience = nurse.get("experience", "Junior")  # Default to "Junior" if not provided
    wards = nurse.get("wards", 1)  # Default to 1 ward if not provided
    
    # Store additional nurse attributes
    nurse_attributes[name] = {"experience": experience, "wards": wards}
    
    # Add nurse to the system
    system.add_nurse(name, specialty, department)

# Function to authenticate user
def authenticate(username, password):
    # Replace with your authentication logic
    return username == "admin" and password == "admin"

# Function to check if the user is logged in
def is_logged_in():
    return "logged_in" in st.session_state and st.session_state.logged_in

# Function to display the login page
def login_page():
    st.title("Login")

    if is_logged_in():
        return

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")

# Function to display the admin page
def admin_page():
    st.title("Admin Dashboard")

    if not is_logged_in():
        return

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a page", ["Nurse Details", "Shift Details", "Leave Requests"])

    if page == "Nurse Details":
        display_nurse_details()
    elif page == "Shift Details":
        display_shift_details()
    elif page == "Leave Requests":
        display_leave_requests()

# Function to display nurse details
def display_nurse_details():
    st.header("Nurse Management")
    st.subheader("Add Nurse")
    name = st.text_input("Nurse Name", placeholder="Enter nurse name")
    specialty = st.text_input("Specialty", placeholder="Enter specialty")
    department = st.text_input("Department", placeholder="Enter department")
    experience = st.selectbox("Experience", ["Junior", "Senior"])  # Assuming two levels of experience
    wards = st.number_input("Number of Wards", min_value=1, step=1)
    if st.button("Add Nurse"):
        if name and specialty and department:
            # Store additional nurse attributes
            nurse_attributes[name] = {"experience": experience, "wards": wards}
            system.add_nurse(name, specialty, department)
            st.success("Nurse added successfully.")
        else:
            st.error("Please fill in all fields.")

    st.subheader("Nurse List")
    nurses = system.nurses
    if nurses:
        for nurse in nurses:
            additional_attributes = nurse_attributes.get(nurse.name, {})
            experience = additional_attributes.get("experience", "")
            wards = additional_attributes.get("wards", "")
            st.write(f"Name: {nurse.name}, Specialty: {nurse.specialty}, Department: {nurse.department}, "
                     f"Experience: {experience}, Wards: {wards}")
    else:
        st.write("No nurses added yet.")

# Function to display shift details
def display_shift_details():
    st.header("Shift Management")
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

# Function to display leave requests
def display_leave_requests():
    st.header("Leave Requests")
    leave_request = st.selectbox("Nurse Name for Leave Request", [""] + [nurse.name for nurse in system.nurses])
    if st.button("Request Leave"):
        if leave_request:
            system.request_leave(leave_request)
            st.success(f"Leave requested for Nurse '{leave_request}'.")
        else:
            st.error("Please select a nurse.")

# Main Streamlit app
def main():
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #f0f2f6;
            }
            .stButton>button {
                color: #ffffff;
                background-color: #2e86de;
                border-radius: 5px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
    if not is_logged_in():
        login_page()
    else: 
        admin_page()

if __name__ == "__main__":
    main()
