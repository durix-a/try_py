import pandas

df1 = pandas.DataFrame({"col1": [1, 5, 9], "col2":[2, 6, 0]})
#print(df1)
df2 = pandas.DataFrame({"col1": [11, 15, 19], "col2":[21, 61, 10]})
#print(df2)

df1.loc[df2.index[0]] = df2.iloc[1]
#print(df1)
print(df2.shape)

for row in df2.iterrows():
    df1.loc[df1.shape[0]] = row[1]
    print(row[1].col1, "  ", row[1].col2)

print(df1)