# Original: NadoCoding
# https://www.youtube.com/watch?v=bKPIcoou9N8
import os
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import * # __all__
from tkinter import filedialog
from PIL import Image

root = Tk()
root.title("Nadocoding Image Merger")

def add_file():
    files = filedialog.askopenfilenames(title="Select image files", \
        filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    
    for file in files:
        list_file.insert(END, file)

def del_file():
    #print(list_file.curselection())
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected == '':
        return
    #print(folder_selected)
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)

def merge_image():
    try:
        #print(list_file.get(0, END))
        images = [Image.open(x) for x in list_file.get(0, END)]
        # size -> size[0] : width, size[1] : height
        # widths = [x.size[0] for x in images]
        # heights = [x.size[1] for x in images]

        # [(10, 10), (20, 20), (30, 30)]
        widths, heights = zip(*(x.size for x in images))

        max_width, total_height = max(widths), sum(heights)
        
        result_img = Image.new("RGB", (max_width, total_height), (255, 255, 255))
        y_offset = 0
        # for img in images:
        #     result_img.paste(img, (0, y_offset))
        #     y_offset += img.size[1]

        for idx, img in enumerate(images):
            result_img.paste(img, (0, y_offset))
            y_offset += img.size[1]

            progress = (idx + 1) / len(images) * 100
            p_var.set(progress)
            progress_bar.update()

        dest_path = os.path.join(txt_dest_path.get(), "nado_photo.jpg")
        result_img.save(dest_path)
        msgbox.showinfo("Info", "Done")
    except Exception as err:
        msgbox.shoqerror("Error", err)      

def start():
    print("Width : ", cmb_width.get())
    print("Space : ", cmb_space.get())
    print("Format : ", cmb_format.get())

    if list_file.size() == 0:
        msgbox.showwarning("Warning", "Select image files")
        return

    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("Warning", "Select save path")
        return

    merge_image()

file_frame = Frame(root)
file_frame.pack(fill="x", padx=5, pady=5)

btn_add_file = Button(file_frame, padx=5, pady=5, width=12, text="Add files", command=add_file)
btn_add_file.pack(side="left")

btn_del_file = Button(file_frame, padx=5, pady=5, width=12, text="Remove files", command=del_file)
btn_del_file.pack(side="right")

list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

path_frame = LabelFrame(root, text="Path")
path_frame.pack(fill="x", padx=5, pady=5, ipady=5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4)

btn_dest_path = Button(path_frame, text="Find", width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)

frame_option = LabelFrame(root, text="Options")
frame_option.pack(padx=5, pady=5, ipady=5)

lbl_width = Label(frame_option, text="Width", width=8)
lbl_width.pack(side="left", padx=5, pady=5)

opt_width = ["Original", "1024", "800", "640"]
cmb_width = ttk.Combobox(frame_option, state="readonly", values=opt_width, width=10)
cmb_width.current(0)
cmb_width.pack(side="left", padx=5, pady=5)

lbl_space = Label(frame_option, text="Space", width=8)
lbl_space.pack(side="left", padx=5, pady=5)

opt_space = ["None", "Narrow", "Normal", "Wide"]
cmb_space = ttk.Combobox(frame_option, state="readonly", values=opt_space, width=10)
cmb_space.current(0)
cmb_space.pack(side="left", padx=5, pady=5)

lbl_format = Label(frame_option, text="Format", width=8)
lbl_format.pack(side="left", padx=5, pady=5)

opt_format = ["PNG", "JPG", "BMP"]
cmb_format = ttk.Combobox(frame_option, state="readonly", values=opt_format, width=10)
cmb_format.current(0)
cmb_format.pack(side="left", padx=5, pady=5)

frame_progress = LabelFrame(root, text="Progress")
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill="x", padx=5, pady=5)

frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="Exit", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text="Start", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)

root.resizable(False, False)
root.mainloop()