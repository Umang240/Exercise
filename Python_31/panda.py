import pandas as pd
# Exercise 1
# data = [10, 20, 30, 40, 50]
# s = pd.Series(data)
# print(s)

data1 = {"Name" :["John", "Jane", "Doe", "Kate"],
         "Age" : ["28", "34", "45", "28"],
         "City" : ["New York", "Los Angeles", "Chicago", "Houston"]
         }
df = pd.DataFrame(data1)
# print(df.iloc[2])

unique_Age = df["Age"].unique()
print(unique_Age)

df.to_csv('trading_data.csv', index=False)

print(iloc[2])

# Student Grade Manager


# Exercise 2
import pandas as pd

# Step 1: Create the data
data = {
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Subject": ["Math", "Science", "Math", "Science"],
    "Grade": [85, 90, 78, 88]
}

# Step 2: Create DataFrame
df = pd.DataFrame(data)

# Step 3: Print the DataFrame
print("All student grades:")
print(df)

# Step 4: Find the average grade
average_grade = df["Grade"].mean()
print("\nAverage grade:", average_grade)

# Step 5: Find the highest and lowest grades
print("\nHighest grade:", df["Grade"].max())
print("Lowest grade:", df["Grade"].min())

# Step 6: Export to CSV
df.to_csv("student_grades.csv", index=False)