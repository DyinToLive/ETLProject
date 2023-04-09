import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

line = "===================================================================================================="

# here importing the data
directory = "./Test/output/"
student_performance = pd.read_csv(directory + "student_performance_info.csv")
effort_hours = 10

# here modify the student ID, None means all student
# id = None
# id = "SID20131151"
# id = "SID20149500"
id = "SID20182516"

# quick look at first 5 results
print(line)
print("Head: \n" + str(student_performance.head()))

# in case the student id is not provided, assume modeling all students' data
if id is not None:
    student_performance = student_performance[student_performance['Student_ID'] == id]

# check the shape of the data
# this shows the number of columns and rows
print(line)
print("Shape: " + str(student_performance.shape))

student_performance.plot.scatter(
    x="Effort_Hours",
    y="Marks",
    title="Scatterplot of Effort Hours and Marks percentages")

# print the correlations, anything higher than 0.8 is considered to be high
print(line)
print("Correlations: \n" + str(student_performance.corr()))

# describe the data
print(line)
print("Description: \n" + str(student_performance.describe()))

# divide the df into 2 array
X = student_performance['Effort_Hours'].values.reshape(-1, 1)
y = student_performance['Marks'].values.reshape(-1, 1)

# print the shape of each array
print(line)
print('X shape:', X.shape)
print('Y shape:', y.shape)

# training 70% of the total of data
# testing 30% of the total of data
# random_state being the seed
# if student ID is provided, then train 90% of the total data of that student
test_size = 0.1 if id is not None else 0.3
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_size, random_state = 42)

# now start training the model
regressor = LinearRegression()
regressor.fit(X_train, y_train)
print(line)
print("Intercept (the constant): " + str(regressor.intercept_[0]))
print("Slope (coefficient of x): " + str(regressor.coef_[0][0]))

y_pred = regressor.predict(X_test)

# printing the expected and actual value
df_preds = pd.DataFrame({'Actual': y_test.squeeze(), 'Predicted': y_pred.squeeze()})
print(line)
print("Prediction: \n" + str(df_preds))

mae = mean_absolute_error(y_test, y_pred) 
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(line)
print(f"mae: {mae:.2f}")
print(f"mse: {mse:.2f}")
print(f"rmse: {rmse:.2f}")

if id is not None:
    # get the student department by student ID
    # Load the data into a pandas dataframe
    student_counseling = pd.read_csv(directory + "student_counseling_info.csv")
    # Get the department for a specific student ID
    department = student_counseling.loc[student_counseling['Student_ID'] == id, 'Department_ID'].values[0]
    # Using format()
    output = '{:<15} {:<30} {}'.format('Student', 'Predicted Score in next paper', 'Department')
    output += '\n{:<15} {:<30} {}'.format(id, f'{regressor.predict([[effort_hours]])[0][0]}', department)
    print(line)
    print(output)

# visualize data, uncomment to visual all students data
plt.show()