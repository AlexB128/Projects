import os
import imghdr
import openpyxl
import cv2

def get_files(path):
    files = os.listdir(path)
    paths = [os.path.join(path, file) for file in files if os.path.isfile(os.path.join(path, file))]
    return paths

def import_image(files, column_idx):
    defaultRowHeight = 15
    row_idx = 1
    files.sort()
    for file in files:
        if imghdr.what(file) != None:
            print(file)
            row_idx += 1
            img = openpyxl.drawing.image.Image(file)

            size_img = cv2.imread(file)
            height, width = size_img.shape[:2]

            cell_address = ws.cell(row=row_idx, column=column_idx).coordinate
            img.anchor = cell_address
            ws.add_image(img)

            h = 0
            height *= 0.75
            while h < height:
                h += ws.row_dimensions[row_idx] if ws.row_dimensions[row_idx].height else defaultRowHeight
                row_idx += 1

image_path = './'
excel_file = './image_merger.xlsx'
column_idx = 2

wb = openpyxl.Workbook()
ws = wb.worksheets[0]

print("Satrt")
files = get_files(image_path)
import_image(files, column_idx)

wb.save(excel_file)
print(excel_file)
print("End")