# # import pandas library
# import pandas as pd
 
# # List of Tuples
# employees = [('Stuti', 28, 'Varanasi'),
#             ('Saumya', 31, 'Delhi'),
#             ('Aaditya', 25, 'Mumbai'),
#             ('Saumya', 32, 'Saumya'),
#             ('Saumya', 32, 'Delhi'),
#             ('Saumya', 32, 'Mumbai'),
#             ('Aaditya', 40, 'Dehradun'),
#             ('Seema', 32, 'Delhi')
#             ]

# students = [('Stuti', 28, 'Varanasi'),
#             ('Saumya', 38, 'Delhi'),
#             ('Aaditya', 25, 'Mumbai'),
#             ('Saumya', 34, 'Delhi'),
#             ('Saumya', 31, 'Delhi'),
#             ('Saumya', 32, 'Mumbai'),
#             ('Aaditya', 40, 'Dehradun'),
#             ('Seema', 32, 'Delhi')
#             ]
 
# # Creating a DataFrame object 
# df = pd.DataFrame(employees,columns = ['Name', 'Age', 'City'])
# df2 = pd.DataFrame(students,columns = ['Name', 'Age', 'City'])


# # print(df)

# # for index, row in df.iterrows():
# #     df1 = df.loc[df['Name'] == row['Name']]
# #     print (df1)

# # temp = df[df.duplicated(['Name'], keep=False)]

# # df2 = df[df.duplicated(subset=['Age','City'], keep=False)]
# # print(df2)

# # row = df.loc[df['Name'] == 'Saumya']
# # print( row['Name'])

# print(df)


# # df11 = df[df.Name.groupby(df.Name).transform(lambda x: (x.size == 1) | x.duplicated())]
# # df22 = df[df.Age.groupby(df.Age).transform(lambda x: (x.size == 1) | x.duplicated())]

# # df = pd.concat(df11 + df22)

# # print(df[['Name', 'Age']])

# # df = df[df[['Name', 'Age']].groupby(['Name', 'Age'], as_index=False).transform(lambda x: (x.size == 1) | x.duplicated())]

# # df = df.groupby(['Name', 'Age'])['City'].transform(lambda x: (x.size == 1) | x.duplicated())

# # df = df.groupby(df[['Name', 'Age']]).transform(lambda x: (x.size == 1) | x.duplicated())


# print('--------------------------------')

# # df = df[df.duplicated(subset=['Name','Age']) | ~df.duplicated(subset=['Name','Age'], keep=False)]
# # print (df)

# # for _, r in df.iterrows():
# #     df3 = df2.where((df2['Name'] == r['Name']) & (df2['Age'] == r['Age']))
# #     if not df3.empty:
# #         df3 = df3.dropna() 
# #         print(df3)


# df_BI_N = df.loc[(df['Name'] == df['City']) ]

# print(df_BI_N)

text = 'Quickly'
print(text.replace('Quic', ""))
print(text.replace('World', ""))