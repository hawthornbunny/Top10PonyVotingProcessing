import asyncio
import os
import threading
from tkinter import filedialog, messagebox, StringVar
from classes.gui import GUI


def get_api_key():
    """Get the Youtube API key from the key entry box or, if not present,
    from the .env file. Failure to find a key results in a message box
    prompting the user to input a key"""

    key = GUI._var_yt_api_key.get().strip()

    if not key:
        key = os.getenv("apikey", "")

    if not key or key == "YOUR_API_KEY":
        messagebox.showinfo("Error", "Please provide a Youtube API key.")

    return key


def browse_file_csv(entry_var: StringVar, saving=False):
    """Returns a handler for a "Browse" button. Opens a file dialog and sets the
    variable `entry_var` to the selected file. Whether the file to be used is for saving
    or opening, `saving` should be used to adjust what the prompt will say."""
    def handler():
        dialog = filedialog.asksaveasfilename if saving else filedialog.askopenfilename

        file_path = dialog(filetypes=[("CSV Files", "*.csv")])

        if not file_path:
            return entry_var.get()
        elif not file_path.endswith(".csv"):
            file_path += ".csv"

        entry_var.set(file_path)
        return file_path

    return handler


def task(async_func):
    """A long running function, or long enough to cause the window to freeze, for the current process, which will run in a seperate
    thread so that the GUI event loop isn't blocked."""

    def threaded(self: GUI, *args, **kwargs):
        self.before()

        self.task = threading.Thread(
            target=lambda: asyncio.run(async_func(self, *args, **kwargs))
        )

        self.task.start()
        self._update_loop()

    return threaded
