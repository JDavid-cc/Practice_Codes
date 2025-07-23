import pandas as pd

# define same data
data = {
    'Name': ['Lito', 'Angelo', 'Karl'],
    'Age': [17, 25, 17],
    'Sex': ['Male', 'Make', 'Made']
}

df = pd.DataFrame(data)
file_path = '3rd Example.xlsx'
df.to_excel(file_path, index=False)
