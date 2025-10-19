import os.path

import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.geometry("300x200")
        self.title("Youtube video downloader")

        self.download_path = ""
        self.video_link = ctk.StringVar(value="Video link")

        self.url_textbox = ctk.CTkEntry(self, textvariable=self.video_link)
        self.url_textbox.pack(pady=10)

        self.label = ctk.CTkLabel(self, text="Download path: Not selected")
        self.label.pack()

        self.directory_button = ctk.CTkButton(
            master=self,
            text="Select download location",
            command=self.select_file_location
        )
        self.directory_button.pack()

        self.download_video_button = ctk.CTkButton(
            master=self,
            text="Download video",
            command=self.download_video
        )
        self.download_video_button.pack(pady=10)

    def select_file_location(self):
        new_path = filedialog.askdirectory(title="Where to download video to")

        if new_path:
            self.download_path = new_path
            self.label.configure(text=f"Selected Path: {self.download_path}")
        else:
            self.label.configure(text="No folder selected")
        print(f"Stored Path: {self.download_path}")
        print(f"current link: {self.url_textbox}")

    def download_video(self):
        if self.download_path != "" and self.label != "Video link":
            output_template = os.path.join(self.download_path, "%(title)s.%(ext)s")
            YT_DLP_EXECUTABLE = "yt-dlp.exe" if os.name == 'nt' else "yt-dlp"
            download_video_command = [
                YT_DLP_EXECUTABLE,
                "-f",
                "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "-o",
                output_template,
                self.video_link.get()
            ]
            try:
                subprocess.run(download_video_command, check=True)
                print("Download completed successfully")
            except subprocess.CalledProcessError as e:
                print(f"Error during download: {e}")
            except FileNotFoundError:
                print("Error: yt-dlp executable not found. Check your PATH.")
            except Exception as e:
                error_message = f"An unexpected error occurred: {e}"
                print(f"{error_message}")
        else:
            print("empty fields")