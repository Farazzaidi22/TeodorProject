from script import Start_Editing
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import traceback


def Close():
    window.destroy()

def get_main_file_path():
    main_file_path = filedialog.askopenfilename(initialdir = "/home", title = "Select your main file", filetypes = [('Excel', ('*.xls', '*.xlsx'))])
    if main_file_path and ( main_file_path.endswith(".xlsx") or main_file_path.endswith(".xls") ):
        main_file.set(main_file_path)
        main_entry_error_label.config(text="")
    else:
        main_entry_error_label.config(text="select a valid excel file.")


def get_ref1_folder_path():
    ref_file_1 = filedialog.askopenfilename(initialdir = "/home", title = "Select your first reference file", filetypes = [('Excel', ('*.xls', '*.xlsx'))])
    if ref_file_1:
        ref1_folder.set(ref_file_1)
        ref1_entry_error_label.config(text="")
    else:
        ref1_entry_error_label.config(text="select a valid file.")

def get_ref2_folder_path():
    ref_file_2 = filedialog.askopenfilename(initialdir = "/home", title = "Select your first reference file", filetypes = [('Excel', ('*.xls', '*.xlsx'))])
    if ref_file_2:
        ref2_folder.set(ref_file_2)
        ref2_entry_error_label.config(text="")
    else:
        ref2_entry_error_label.config(text="select a valid file.")

def get_Nyinflyttade_folder_path():
    Nyinflyttade_file = filedialog.askopenfilename(initialdir = "/home", title = "Select your Nyinflyttade file", filetypes = [('Excel', ('*.xls', '*.xlsx'))])
    if Nyinflyttade_file:
        Nyinflyttade_folder.set(Nyinflyttade_file)
        Nyinflyttade_entry_error_label.config(text="")
    else:
        Nyinflyttade_entry_error_label.config(text="select a valid file.")

def get_Ny_fil_med_avlidna_folder_path():
    Ny_fil_med_avlidna_file = filedialog.askopenfilename(initialdir = "/home", title = "Select your Ny_fil_med_avlidna file", filetypes = [('Excel', ('*.xls', '*.xlsx'))])
    if Ny_fil_med_avlidna_file:
        Ny_fil_med_avlidna_folder.set(Ny_fil_med_avlidna_file)
        Ny_fil_med_avlidna_entry_error_label.config(text="")
    else:
        Ny_fil_med_avlidna_entry_error_label.config(text="select a valid file.")


def start_process():
    try:
        # int(record_entry.get())
        record_error_label.config(text="")
    except ValueError:
        record_error_label.config(text="Something missing a percentage or value.")
        return None
    # percentage = int(record_entry.get())
    main_file_path = main_file.get()
    ref1_folder_path = ref1_folder.get()
    ref2_folder_path = ref2_folder.get()
    Nyinflyttade_folder_path = Nyinflyttade_folder.get()
    Ny_fil_med_avlidna_folder_path = Ny_fil_med_avlidna_folder.get()

    if not main_file_path:
        main_entry_error_label.config(text="select a valid excel file.")
    elif not ref1_folder_path:
        ref1_entry_error_label.config(text="select a valid folder.")
    elif not ref2_folder_path:
        ref2_entry_error_label.config(text="select a valid folder.")
    elif not Nyinflyttade_folder_path:
        Nyinflyttade_entry_error_label.config(text="select a valid folder.")
    elif not Ny_fil_med_avlidna_folder_path:
        Ny_fil_med_avlidna_entry_error_label.config(text="select a valid folder.")
    else:
        Ny_fil_med_avlidna_entry_error_label.config(text="")
        Nyinflyttade_entry_error_label.config(text="")
        ref2_entry_error_label.config(text="")
        ref1_entry_error_label.config(text="")
        main_entry_error_label.config(text="")
        try:
            Start_Editing(main_file_path, ref1_folder_path, ref2_folder_path, Nyinflyttade_folder_path, Ny_fil_med_avlidna_folder_path)
            process_info_label.config(text="Success: files generated.")
        except:
            process_error_label.config(text="Error: Check error.txt file")
            with open('error.txt', 'w') as f:
                traceback.print_exc(file=f)


window = Tk()
window.geometry("465x200")
window.title("Excel Convertor")

window.minsize(700, 400)
window.maxsize(700, 400)

main_file= StringVar()
ref1_folder = StringVar()
ref2_folder = StringVar()
Nyinflyttade_folder = StringVar()
Ny_fil_med_avlidna_folder = StringVar()


heading = Label(window, text="EXCEL FILE EDITOR", font=("Helvetica", 15))
heading.place(x=160, y=10)

################# main
main_label = Label(window ,text="main File")
main_label.place(x=10, y=60)

main_entry = Entry(window, textvariable = main_file, width=60)
main_entry.place(x=100, y=60)

main_entry_error_label = Label(window, text="", fg='red', font=("Helvetica", 10))
main_entry_error_label.place(x=100, y=85)

main_button = ttk.Button(window, text="Browse Folder", command=get_main_file_path)
main_button.place(x=500, y=60)

################## ref 1
ref1_label = Label(window ,text="ref1 file ")
ref1_label.place(x=10, y=100)

ref1_entry = Entry(window, textvariable = ref1_folder, width=60)
ref1_entry.place(x=100, y=100)

ref1_entry_error_label = Label(window, text="", fg='red', font=("Helvetica", 10))
ref1_entry_error_label.place(x=160, y=125)

ref1_button = ttk.Button(window, text="Browse Folder", command=get_ref1_folder_path)
ref1_button.place(x=500, y=100)

################## ref 2
ref2_label = Label(window ,text="ref2 file ")
ref2_label.place(x=10, y=140)

ref2_entry = Entry(window, textvariable = ref2_folder, width=60)
ref2_entry.place(x=100, y=140)

ref2_entry_error_label = Label(window, text="", fg='red', font=("Helvetica", 10))
ref2_entry_error_label.place(x=160, y=165)

ref2_button = ttk.Button(window, text="Browse Folder", command=get_ref2_folder_path)
ref2_button.place(x=500, y=140)

################## Nyinflyttade
Nyinflyttade_label = Label(window ,text="Nyinflyttade file ")
Nyinflyttade_label.place(x=10, y=180)

Nyinflyttade_entry = Entry(window, textvariable = Nyinflyttade_folder, width=60)
Nyinflyttade_entry.place(x=100, y=180)

Nyinflyttade_entry_error_label = Label(window, text="", fg='red', font=("Helvetica", 10))
Nyinflyttade_entry_error_label.place(x=160, y=205)

Nyinflyttade_button = ttk.Button(window, text="Browse Folder", command=get_Nyinflyttade_folder_path)
Nyinflyttade_button.place(x=500, y=180)

################## Ny_fil_med_avlidna
Ny_fil_med_avlidna_label = Label(window ,text="Ny_fil_med_avlidna file ")
Ny_fil_med_avlidna_label.place(x=10, y=220)

Ny_fil_med_avlidna_entry = Entry(window, textvariable = Ny_fil_med_avlidna_folder, width=60)
Ny_fil_med_avlidna_entry.place(x=100, y=220)

Ny_fil_med_avlidna_entry_error_label = Label(window, text="", fg='red', font=("Helvetica", 10))
Ny_fil_med_avlidna_entry_error_label.place(x=160, y=230)

Ny_fil_med_avlidna_button = ttk.Button(window, text="Browse Folder", command=get_Ny_fil_med_avlidna_folder_path)
Ny_fil_med_avlidna_button.place(x=500, y=220)

# record_label = Label(window ,text="Percentage: ")
# record_label.place(x=10, y=140)

# record_entry = Entry(window, width=5)
# record_entry.place(x=95, y=140)


record_error_label = Label(window, text="", fg='red', font=("Helvetica", 10))
record_error_label.place(x=10, y=250)

start_button = ttk.Button(window ,text="Start", width=20, command=start_process)
start_button.place(x=140, y=300)

exit_button = ttk.Button(window, text="Exit", width=20, command=Close)
exit_button.place(x=290, y=300)

process_info_label = Label(window, text="", fg='green', font=("Helvetica", 10))
process_info_label.place(x=162, y=250)

process_error_label = Label(window, text="", fg='red', font=("Helvetica", 10))
process_error_label.place(x=162, y=250)

window.mainloop()