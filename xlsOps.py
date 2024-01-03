import datetime
import os
import xlsxwriter


def nowStamp():
    date = datetime.datetime.now()
    day = ("%02d" % (date.day,))
    month = (date.strftime("%b")).upper()
    hour = ("%02d" % date.hour)
    minute = ("%02d" % date.minute)
    return month + day + ' - ' + hour + '.' + minute


def workbookGen(name: str, dirPath, stamp=True):
    if stamp:
        name = name + ' ' + nowStamp() + '.xlsx'
    else:
        name = name + '.xlsx'
    return xlsxwriter.Workbook(dirPath + os.sep + name, {'nan_inf_to_errors': True})


def xlsFormat(df, sheetName, workbook: xlsxwriter.Workbook, formatcdx=False, formatHeader=False, formatRows=False,
              colWidth=15, colWidthList=False, posX=0, posY=0):
    # DEFAULT STYLES
    if formatHeader is False:
        formatHeader = {'bg_color': '#C0C0C0', 'border': 1, 'align': 'center', 'bold': True}
    if formatRows is False:
        formatRows = {'border': 1, 'align': 'center'}

    formats = []
    if formatcdx is not False:
        for x in formatcdx:
            # CREATES SPECIFIC FORMATS, ADDS ROW FORMATING TO SPECIFIC
            formats.append(workbook.add_format(formatRows | x[1]))

    worksheetExists = False

    for x in workbook.worksheets():
        if x.get_name() == sheetName:
            worksheet = x
            worksheetExists = True
            break

    if not worksheetExists:
        worksheet = workbook.add_worksheet(sheetName)
    formatHeader = workbook.add_format(formatHeader)
    formatRows = workbook.add_format(formatRows)

    # REMOVE EMPTY LINES
    df.dropna(inplace=True)

    # COLUMN WIDTH
    worksheet.set_column(0 + posX, df.shape[1] - 1 + posX, colWidth)
    if colWidthList is not False:
        # Example: [[col,width],[0,10]]
        for col in colWidthList:
            worksheet.set_column(col[0], col[0], col[1])

    # FORMAT TABLE
    for col, title in enumerate(df.columns):
        # FORMAT HEADER
        worksheet.write(0 + posY, col + posX, title, formatHeader)
    for row in range(df.shape[0]):
        # ELIMINAR LINHAS SEM VALOR
        for col in range(df.shape[1]):
            # FORMATROWS FORMATTING
            worksheet.write(row + 1 + posY, col + posX, df.iloc[row, col], formatRows)
            # SPECIFIC FORMATTING
            if formatcdx is not False:
                for i, formatt in enumerate(formatcdx):
                    if col in formatt[0]:
                        worksheet.write(row + 1 + posY, col + posX, df.iloc[row, col], formats[i])
