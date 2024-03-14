import random
import datetime
from openpyxl import Workbook

class Nurse:
    def __init__(self, name, specialty, experience_level, experience_years, department):
        self.name = name
        self.specialty = specialty
        self.experience_level = experience_level
        self.experience_years = experience_years
        self.department = department
        self.on_leave = False

class Shift:
    def __init__(self, shift_id, date, start_time, end_time, specialty_required, department_required):
        self.shift_id = shift_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.specialty_required = specialty_required
        self.department_required = department_required
        self.assigned_nurse = None

class NurseAllocationSystem:
    def __init__(self):
        self.nurses = []
        self.shifts = []
        self.wards = []  # Added 'wards' attribute

    def add_nurse(self, name, specialty, department):
        experience_level = random.choice(["Junior", "Intermediate", "Senior"])
        experience_years = random.randint(1, 10)  # Random years of experience between 1 and 10
        nurse = Nurse(name, specialty, experience_level, experience_years, department)
        self.nurses.append(nurse)
        print(f"Added Nurse: {name}, Specialty: {specialty}, Experience Level: {experience_level}, Experience Years: {experience_years}, Department: {department}")

    def add_ward(self, name):
        self.wards.append(name)
        print(f"Added Ward: {name}")

    def request_leave(self, nurse_name):
        for nurse in self.nurses:
            if nurse.name == nurse_name:
                nurse.on_leave = True
                print(f"{nurse_name} is on leave.")
                break
        else:
            print(f"No nurse with the name {nurse_name} found.")

    def generate_shifts(self, num_shifts):
        specialties = {
            "Eye": ["Ophthalmology"],
            "Gynecologist": ["Obstetrics", "Gynecology"],
            "Dentist": ["Dentistry"],
            "ENT": ["Otorhinolaryngology"],
            "Psychology": ["Psychiatry"]
        }

        start_date = datetime.date.today()
        for i in range(num_shifts):
            shift_id = i + 1
            date = start_date + datetime.timedelta(days=i)
            start_time = "08:00"
            end_time = "16:00"
            department_required = random.choice(list(specialties.keys()))
            specialty_required = random.choice(specialties[department_required])
            shift = Shift(shift_id, date, start_time, end_time, specialty_required, department_required)
            self.shifts.append(shift)

    def assign_nurses_to_shifts(self):
        for shift in self.shifts:
            eligible_nurses = [nurse for nurse in self.nurses if nurse.specialty == shift.specialty_required and nurse.department == shift.department_required and not nurse.on_leave]
            if eligible_nurses:
                shift.assigned_nurse = random.choice(eligible_nurses)

    def display_shifts(self):
        for shift in self.shifts:
            assigned_nurse_name = 'Not Assigned'
            experience_level = 'N/A'
            experience_years = 'N/A'

            if shift.assigned_nurse:
                assigned_nurse_name = shift.assigned_nurse.name
                experience_level = shift.assigned_nurse.experience_level
                experience_years = shift.assigned_nurse.experience_years

            print(f"Shift ID: {shift.shift_id}, Date: {shift.date}, "
                  f"Start Time: {shift.start_time}, End Time: {shift.end_time}, "
                  f"Department Required: {shift.department_required}, "
                  f"Specialty Required: {shift.specialty_required}, "
                  f"Assigned Nurse: {assigned_nurse_name}, "
                  f"Experience Level: {experience_level}, "
                  f"Experience Years: {experience_years}")

    def export_shifts_to_excel(self, filename='shifts.xlsx'):
        wb = Workbook()
        ws = wb.active

        ws.append(["Shift ID", "Date", "Start Time", "End Time", "Department Required", "Specialty Required", "Assigned Nurse", "Experience Level", "Experience Years"])

        for shift in self.shifts:
            assigned_nurse_name = shift.assigned_nurse.name if shift.assigned_nurse else 'Not Assigned'
            experience_level = shift.assigned_nurse.experience_level if shift.assigned_nurse else 'N/A'
            experience_years = shift.assigned_nurse.experience_years if shift.assigned_nurse else 'N/A'

            ws.append([shift.shift_id, shift.date, shift.start_time, shift.end_time, shift.department_required, shift.specialty_required, assigned_nurse_name, experience_level, experience_years])

        wb.save(filename)

if __name__ == "__main__":
    system = NurseAllocationSystem()

    print("Adding Nurses:")
    system.add_nurse("Alice", "Ophthalmology", "Eye")
    system.add_nurse("Bob", "Obstetrics", "Gynecologist")
    system.add_nurse("Charlie", "Dentistry", "Dentist")
    system.add_nurse("David", "Otorhinolaryngology", "ENT")
    system.add_nurse("Eve", "Psychiatry", "Psychology")

    num_shifts = int(input("Enter the number of shifts: "))
    system.generate_shifts(num_shifts)

    system.assign_nurses_to_shifts()

    print("\nShifts:")
    system.display_shifts()

    while True:
        try:
            print("\nOptions:")
            print("1. View shift details by ID")
            print("2. Add a new shift")
            print("3. Add a new ward")
            print("4. Request leave")
            print("0. Exit")

            option = input("Choose an option: ")

            if option == "1":
                shift_id = int(input("Enter the Shift ID to view details: "))
                shift = next((shift for shift in system.shifts if shift.shift_id == shift_id), None)
                if shift:
                    print("\nShift Details:")
                    print(f"Shift ID: {shift.shift_id}, Date: {shift.date}, "
                          f"Start Time: {shift.start_time}, End Time: {shift.end_time}, "
                          f"Department Required: {shift.department_required}, "
                          f"Specialty Required: {shift.specialty_required}")
                    if shift.assigned_nurse:
                        print(f"Assigned Nurse: {shift.assigned_nurse.name}, "
                              f"Experience Level: {shift.assigned_nurse.experience_level}, "
                              f"Experience Years: {shift.assigned_nurse.experience_years}")
                    else:
                        print("No nurse assigned to this shift yet.")
                else:
                    print("Shift ID not found.")

            elif option == "2":
                print("Existing Shift IDs:")
                for shift in system.shifts:
                    print(shift.shift_id)
                new_shift_department = input("Enter the department for the new shift: ")
                new_shift_specialty = input("Enter the specialty for the new shift: ")
                system.generate_shifts(1)
                system.shifts[-1].department_required = new_shift_department
                system.shifts[-1].specialty_required = new_shift_specialty
                system.assign_nurses_to_shifts()
                print("\nNew shift added successfully.")

            elif option == "3":
                new_ward_name = input("Enter the name of the new ward: ")
                system.add_ward(new_ward_name)

            elif option == "4":
                nurse_name = input("Enter the name of the nurse requesting leave: ")
                system.request_leave(nurse_name)

            elif option == "0":
                print("Exiting program.")
                break

            else:
                print("Invalid option. Please choose again.")

        except ValueError:
            print("Invalid input. Please enter a valid Shift ID (an integer).")
