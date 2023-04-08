import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import warnings
warnings.filterwarnings('ignore')

department_info = pd.read_csv("Department_Information.csv")
employee_info = pd.read_csv("Employee_Information.csv").rename(columns={'DOB': 'DOB_employee'})
student_counseling_info = pd.read_csv("Student_Counceling_Information.csv").rename(columns={'DOB': 'DOB_student','Department_Admission' : 'Department_ID'})
student_performance_data = pd.read_csv("Student_Performance_Data.csv").rename(columns={'Semster_Name' : 'Semester_Name'})


department_info['DOE'] = pd.to_datetime(department_info['DOE'], errors='coerce')
department_info['DOE'] = department_info['DOE'].dt.date
employee_info['DOB_employee'] = pd.to_datetime(employee_info['DOB_employee'], errors='coerce')
employee_info['DOB_employee'] = employee_info['DOB_employee'].dt.date
employee_info['DOJ'] = pd.to_datetime(employee_info['DOJ'], errors='coerce')
employee_info['DOJ'] = employee_info['DOJ'].dt.date
student_counseling_info['DOB_student'] = pd.to_datetime(student_counseling_info['DOB_student'], errors='coerce')
student_counseling_info['DOB_student'] = student_counseling_info['DOB_student'].dt.date
student_counseling_info['DOA'] = pd.to_datetime(student_counseling_info['DOA'], errors='coerce')
student_counseling_info['DOA'] = student_counseling_info['DOA'].dt.date
department_info.dropna(subset=['DOE'], inplace=True)
employee_info.dropna(subset=['DOB_employee'], inplace=True)
employee_info.dropna(subset=['DOJ'], inplace=True)
student_counseling_info.dropna(subset=['DOB_student'], inplace=True)
student_counseling_info.dropna(subset=['DOA'], inplace=True)


# check for uniqueness of Department_ID
if len(department_info["Department_ID"].unique()) != len(department_info):
    print("Department_ID is not unique. Removing duplicate rows...")
    department_info = department_info.drop_duplicates(subset=["Department_ID"])

# check for uniqueness of Department_Name
if len(department_info["Department_Name"].unique()) != len(department_info):
    print("Department_Name is not unique. Removing duplicate rows...")
    department_info = department_info.drop_duplicates(subset=["Department_Name"])

# check for missing values
if department_info.isnull().values.any():
    print("Department_Information table contains missing values. Removing rows...")
    department_info = department_info.dropna()

# filter out rows where the year value of DOE is less than 1900
department_info["DOE"] = pd.to_datetime(department_info["DOE"])
invalid_years = department_info.loc[department_info["DOE"].dt.year < 1900]
if not invalid_years.empty:
    print("Invalid year values found in DOE column. Removing rows...")
    department_info = department_info[department_info["DOE"].dt.year >= 1900]

# filter out rows with missing Department_Admission values
if student_counseling_info["Department_ID"].isnull().values.any():
    missing_values = student_counseling_info["Department_ID"].isnull().sum()
    print(f"There are {missing_values} missing values in the 'Department_Admission' column.")
    student_counseling_info.dropna(subset=["Department_ID"], inplace=True)

# check if Department_Admission does not exist
if not set(student_counseling_info["Department_ID"]).issubset(set(department_info["Department_ID"])):
    print("There are Department Choices in Student_Counseling_Information that do not exist in Department_Information.")

# check the range of marks and filter out invalid records
invalid_marks = student_performance_data[(student_performance_data['Marks'] < 0) | (student_performance_data['Marks'] > 100)]
if len(invalid_marks) > 0:
    sum_invalid_marks = len(invalid_marks)
    print(f"{sum_invalid_marks} mark(s) found and removed.")
    student_performance_data = student_performance_data[(student_performance_data['Marks'] >= 0) & (student_performance_data['Marks'] <= 100)]


# Validate and filter out rows with invalid Effort_Hours values
invalid_rows = student_performance_data[~(student_performance_data['Effort_Hours'].ge(0) & student_performance_data['Effort_Hours'].astype(str).str.isdigit())]
if not invalid_rows.empty:
    sum_invalid_rows = len(invalid_rows)
    print(f"{sum_invalid_rows} invalid row(s) found in Effort_Hours and removed.")
    student_performance_data = student_performance_data.drop(invalid_rows.index)

# A given Student_ID cannot have more than 1 mark per each Paper_ID
#TODO: This one isn't working
#if len(student_performance_data.groupby(['Student_ID', 'Paper_ID']).filter(lambda x: len(x)>1)) > 0:
   # print('Error: A given Student_ID cannot have more than 1 mark per each Paper_ID in the student_performance_data table')
  #  paper_count = student_performance_data.groupby(['Student_ID', 'Paper_ID']).size().reset_index(name='counts')
   # multi_marks = paper_count[paper_count['counts'] > 1]
  #  student_performance_data = student_performance_data[~student_performance_data.isin(multi_marks)].dropna()

#Updated, duplicated should work for this according to what i've looked at. The documentation just requires 
#an error exception, so I didn't include the paper_count etc... though it does work with it.
if len(student_performance_data.duplicated(subset=['Student_ID', 'Paper_ID'], keep= False)):
    print('Error: A given Student_ID cannot have more than 1 mark per each Paper_ID in the student_performance_data table.')

# check for missing values
if student_performance_data.isnull().values.any():
    missingvalues = student_performance_data.isnull().values.sum()
    print(f"Student_performance_data table contained {missingvalues} missing value(s). Removing rows...")
    student_performance_data = student_performance_data.dropna()

# Export cleaned up files to new csv files in the folder "output"
department_info.to_csv('./output/department_info.csv', index=False)
employee_info.to_csv('./output/employee_info.csv', index=False)
student_counseling_info.to_csv('./output/student_counseling_info.csv', index=False)
student_performance_data.to_csv('./output/student_performance_info.csv', index=False)
