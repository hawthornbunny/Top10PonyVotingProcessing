import tkinter as tk
from tkinter import ttk, filedialog
from modules import duplicate
from modules import blacklist
from modules import durationcheck
from modules import fuzzycheck
from modules import upload_date
from modules import uploader_occurence
from modules import (
    data_pulling,
)  # Import of all the necesary functions from the modules folder
import os


# Mane program to be run


def browse_file():  # Function that asks for a CSV file
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    entry_var.set(file_path)


def run_checks():  # Function that runs all the rule
    csv_file = entry_var.get()
    data_pulling.set_count(csv_file)  # Checks everything
    fuzzycheck.links_to_titles(csv_file)
    duplicate.check_duplicates(csv_file)
    blacklist.check_blacklist(csv_file)
    upload_date.check_dates(csv_file)
    durationcheck.check_duration(csv_file)
    fuzzycheck.adapt_output_csv()
    fuzzycheck.delete_first_cell()
    uploader_occurence.check_uploader_occurence()

    delete_if_present(
        "outputs/processed_blacklist.csv"
    )  # Calls deleting outputs if present
    delete_if_present("outputs/processed_duplicates.csv")
    delete_if_present("outputs/processed_fuzzlist.csv")
    delete_if_present("outputs/processed_dates.csv")
    delete_if_present("outputs/durations_output.csv")
    delete_if_present("outputs/titles_output.csv")
    delete_if_present("outputs/uploaders_output.csv")
    delete_if_present("outputs/processed_uploaders.csv")


def delete_if_present(filepath):  # Deletes functions if present
    if os.path.exists(filepath):
        os.remove(filepath)


root = tk.Tk()  # Creating the GUI
root.title("Check Script")

entry_var = tk.StringVar()
entry = ttk.Entry(root, textvariable=entry_var)
entry.pack(padx=10, pady=10)


browse_button = ttk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=10)

run_button = ttk.Button(root, text="Run Checks", command=run_checks)
run_button.pack()

root.mainloop()
