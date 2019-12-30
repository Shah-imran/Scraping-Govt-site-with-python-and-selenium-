# import pandas as pd


# # Create some Pandas dataframes from some data.
# df1 = pd.DataFrame({'Data': [11, 12, 13, 14]})
# df2 = pd.DataFrame({'Data': [21, 22, 23, 24]})
# df3 = pd.DataFrame({'Data': [31, 32, 33, 34]})

# # Create a Pandas Excel writer using XlsxWriter as the engine.
# writer = pd.ExcelWriter('pandas_multiple.xlsx', engine='xlsxwriter')

# # Write each dataframe to a different worksheet.
# df1.to_excel(writer, sheet_name='Sheet1')
# df2.to_excel(writer, sheet_name='Sheet2')
# df3.to_excel(writer, sheet_name='Sheet3')

# # Close the Pandas Excel writer and output the Excel file.
# writer.save()
'''['1.Survey Number', '    12', '    *', '3.Extent of Land', 'Acre Gunta', '4.Revenue', 'Rs. Paise', 'Total Extent', '3.28.00.00', '(a)Land Revenue', '10.10', 'Karab(a)', '0.00.00.00', '(b)Jodi', '0.00', 'Karab(b)', '0.00.00.00', '(c)Cesses', '', 'Remaining', '3.28.00.00', '(d)Water Rate', '0.00', '2.Hissa: 2/2', 'Total', '10.10', '5.Soil Type', 'ಕಪ್ಪು', '7.Tree Details', '8.Irrigation Details as per Extent', 'Name', 'Nos', 'S.no', 'Water source', 'Kharif Ac Gun', 'Rabi Ac Gun', 'Garden Ac Gun', 'Total Ac Gun', '6.Patta', 'ಸರ್ಕಾರಿ', '', '', '', 'G.L.B.C.', '0.10.00.00', '0.00.00.00', '0.00.00.00', '0.10.00.00']'''
with open("html1.txt", "r", encoding="utf-8") as f:
    data = f.read()

    data = data.split("\n")
    data = data[:48]
    # data = data[8:]
    print(data)
    rmlist = ['1.Survey Number', '3.Extent of Land', 'Acre Gunta', '4.Revenue', 'Rs. Paise', 'Total Extent','(a)Land Revenue', 'Karab(a)','(b)Jodi', 'Karab(b)', '(c)Cesses', '', 'Remaining', '(d)Water Rate', 'Total', '5.Soil Type', '7.Tree Details', '8.Irrigation Details as per Extent', 'Name', 'Nos', 'S.no', 'Water source', 'Kharif Ac Gun', 'Rabi Ac Gun', 'Garden Ac Gun', 'Total Ac Gun', '6.Patta']
    for i in rmlist:
    	data.remove(i)
    for i in range(len(data)):
    	data[i] = data[i].replace("2.Hissa:", "")

    print(data)