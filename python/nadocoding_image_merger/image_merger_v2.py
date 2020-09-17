# Original: NadoCoding
# https://www.youtube.com/watch?v=bKPIcoou9N8
import os
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import *                   # __all__
from tkinter import filedialog
from PIL import Image
import openpyxl

root = Tk()
root.title("Nadocoding Image Merger")

images_folder = os.getcwd()
# Add files
def add_file():
    global images_folder

    files = filedialog.askopenfilenames(title="Select image files", \
        filetypes=(("PNG file", "*.png"), ("All files", "*.*")), \
        initialdir=images_folder)
    
    if files:
        for file in files:
            list_file.insert(END, file)

        images_folder = os.path.dirname(files[0])

# Delete files
def del_file():
    #print(list_file.curselection())
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

# Output file path
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected == "":
        # print("Cancel folder selextion")
        return
    #print(folder_selected)
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)

# Merge images
def merge_image():
    # print("Width : ", cmb_width.get())
    # print("Space : ", cmb_space.get())
    # print("Fromat : ", cmb_format.get())

    # try:
        # Width
        img_width = cmb_width.get()
        if img_width == "Original":
            img_width = -1
        else:
            img_width = int(img_width)

        # Space
        img_space = cmb_space.get()
        if img_space == "Narrow":
            img_space = 30
        elif img_space == "Normal":
            img_space = 60
        elif img_space == "Wide":
            img_space = 90
        else:
            img_space = 0

        # Output file format
        output_format = cmb_format.get().lower()

        images = [Image.open(x) for x in list_file.get(0, END)]    

        image_sizes = []
        if img_width > -1:
            # Change width
            image_sizes = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in images]
        else:
            # Original size
            image_sizes = [(x.size[0], x.size[1]) for x in images]

        widths, heights = zip(*(image_sizes))

        # File format option
        file_name = "image_merger." + output_format
        dest_path = os.path.join(txt_dest_path.get(), file_name)

        if output_format != 'xlsx':
            # width max, total height
            max_width, total_height = max(widths), sum(heights)
            
            # Output image size
            if img_space > 0: # space between images
                total_height += (img_space * (len(images) - 1))

            result_img = Image.new("RGB", (max_width, total_height), (255, 255, 255)) # white background

            # Merge images >>>>>>>>>>>>>>>>>>>>>>>>>>>
            y_offset = 0 # y position

            for idx, img in enumerate(images):
                # Change image size 
                if img_width > -1:
                    img = img.resize(image_sizes[idx])

                result_img.paste(img, (0, y_offset))
                y_offset += (img.size[1] + img_space) # height + space between images

                progress = (idx + 1) / len(images) * 100
                p_var.set(progress)
                progress_bar.update()
            # Merge images <<<<<<<<<<<<<<<<<<<<<<<<<<<

            result_img.save(dest_path)
        else:
            wb = openpyxl.Workbook()
            ws = wb.worksheets[0]

            column_idx = 2
            row_idx = 1
            defaultRowHeight = 15

            for idx, img in enumerate(images):
                # Change image size 
                if img_width > -1:
                    img = img.resize(image_sizes[idx])

                openpyxl_img = openpyxl.drawing.image.Image(img)

                width, height = image_sizes[idx]

                cell_address = ws.cell(row=row_idx, column=column_idx).coordinate
                openpyxl_img.anchor = cell_address
                ws.add_image(openpyxl_img)

                h = 0
                height *= 0.75
                while h < height:
                    h += ws.row_dimensions[row_idx] if ws.row_dimensions[row_idx].height else defaultRowHeight
                    row_idx += 1

                row_idx += int(img_space / 30)

                progress = (idx + 1) / len(images) * 100
                p_var.set(progress)
                progress_bar.update()

            wb.save(dest_path)

        msgbox.showinfo("Information", dest_path + " created.")
    # except Exception as err:
    #     msgbox.showerror("Error", err)

# Satrt
def start():
    # Option values
    # print("Width : ", cmb_width.get())
    # print("Space : ", cmb_space.get())
    # print("Format : ", cmb_format.get())
    
    p_var.set(0)
    progress_bar.update()
    
    # Check file list
    if list_file.size() == 0:
        msgbox.showwarning("Warning", "Select image files")
        return

    # Check output path
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("Warning", "Select output path")
        return

    # merge image files
    merge_image()

# File frame (Add/remove files)
file_frame = Frame(root)
file_frame.pack(fill="x", padx=5, pady=5)

btn_add_file = Button(file_frame, padx=5, pady=5, width=12, text="Add files", command=add_file)
btn_add_file.pack(side="left")

btn_del_file = Button(file_frame, padx=5, pady=5, width=12, text="Remove files", command=del_file)
btn_del_file.pack(side="right")

# List Frame
list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

# Output Path Frame
path_frame = LabelFrame(root, text="Output File Path")
path_frame.pack(fill="x", padx=5, pady=5, ipady=5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4)
txt_dest_path.insert(0, images_folder)

btn_dest_path = Button(path_frame, text="Find", width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)

# OPtion Frame
frame_option = LabelFrame(root, text="Options")
frame_option.pack(padx=5, pady=5, ipady=5)

# 1. Width option
lbl_width = Label(frame_option, text="Width", width=8)
lbl_width.pack(side="left", padx=5, pady=5)

opt_width = ["Original", "1024", "800", "640"]
cmb_width = ttk.Combobox(frame_option, state="readonly", values=opt_width, width=10)
cmb_width.current(0)
cmb_width.pack(side="left", padx=5, pady=5)

# 2. Space option
lbl_space = Label(frame_option, text="Space", width=8)
lbl_space.pack(side="left", padx=5, pady=5)

opt_space = ["None", "Narrow", "Normal", "Wide"]
cmb_space = ttk.Combobox(frame_option, state="readonly", values=opt_space, width=10)
cmb_space.current(0)
cmb_space.pack(side="left", padx=5, pady=5)

# 3. File Format option
lbl_format = Label(frame_option, text="Format", width=8)
lbl_format.pack(side="left", padx=5, pady=5)

opt_format = ["PNG", "JPG", "BMP", "XLSX"]
cmb_format = ttk.Combobox(frame_option, state="readonly", values=opt_format, width=10)
cmb_format.current(0)
cmb_format.pack(side="left", padx=5, pady=5)

# Progress Bar
frame_progress = LabelFrame(root, text="Progress")
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill="x", padx=5, pady=5)

# Execution Frame
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="Exit", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text="Start", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)

root.resizable(False, False)
root.mainloop()