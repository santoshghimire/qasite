import xlwt

style0 = xlwt.easyxf(
    'font: name FreeSans, bold on')
# style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

wb = xlwt.Workbook(encoding='utf-8')
ws = wb.add_sheet('Sheet1')
header = [
    'Question', 'Topic ID', 'Level', 'Correct',
    'Option 1', 'Option 2', 'Option 3', 'Option 4'
]

for count, i in enumerate(header):
    ws.write(0, count, i, style0)

wb.save('question-import-format.xlsx')
