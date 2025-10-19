import os.path
import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import threading

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.geometry("400x200")
        self.title("Youtube video downloader")

        self.download_path = ""
        self.video_link = ctk.StringVar(value="Video link")

        self.url_textbox = ctk.CTkEntry(self, textvariable=self.video_link)
        self.url_textbox.pack(pady=10)

        self.label = ctk.CTkLabel(self, text="Download path: Not selected")
        self.label.pack()

        self.format_var = ctk.StringVar(value="MP4")
        ctk.CTkLabel(self, text="Select Download Format:").pack(pady=(0, 10))
        self.format_option_menu = ctk.CTkOptionMenu(
            self,
            values=["MP4", "MP3"],
            variable=self.format_var,
            width=100
        )
        self.format_option_menu.pack(pady=5)

        self.directory_button = ctk.CTkButton(
            master=self,
            text="Select download location",
            command=self.select_file_location
        )
        self.directory_button.pack()

        self.download_video_button = ctk.CTkButton(
            master=self,
            text="Download video",
            command=self.start_download_thread
        )
        self.download_video_button.pack(pady=10)

    def select_file_location(self):
        new_path = filedialog.askdirectory(title="Where to download video to")

        if new_path:
            self.download_path = new_path
            self.label.configure(text=f"Selected Path: {self.download_path}")
        else:
            self.label.configure(text="No folder selected")

    def _download_video(self, video_link):
        output_template = os.path.join(self.download_path, "%(title)s.%(ext)s")
        YT_DLP_EXECUTABLE = "yt-dlp.exe" if os.name == 'nt' else "yt-dlp"
        selected_format = self.format_var.get()

        if selected_format == "MP4":
            format_options = [
                "-f",
                "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
            ]
        elif selected_format == "MP3":
            format_options = [
                "-x",
                "--audio-format", "mp3",
                "--audio-quality", "0"
            ]
        else:
            format_options = []
            self.after_idle(lambda: messagebox.showerror("Error", "Invalid format selected."))
            return

        download_video_command = [YT_DLP_EXECUTABLE] + format_options + [
            "-o",
            output_template,
            video_link
        ]

        try:
            subprocess.run(download_video_command, check=True)
            self.after_idle(lambda : messagebox.showinfo("Success", f"Download completed at {self.download_path}"))
        except FileNotFoundError:
            self.after_idle(lambda: messagebox.showerror("File not found", f"Error: yt-dlp not found"))
        except subprocess.CalledProcessError as e:
            self.after_idle(lambda : messagebox.showerror("Download failed", f"Error: {e}"))
        except Exception as e:
            self.after_idle(lambda : messagebox.showerror("Download failed", f"Error: {e}"))
        finally:
            self.after_idle(lambda: self.download_video_button.configure(state="normal", text="Download video"))

    def start_download_thread(self):
        video_url = self.video_link.get().strip()

        if not self.download_path:
            messagebox.showerror("Validation Error", "Please select a download location.")
            return

        if not video_url or video_url == "Video link":
            messagebox.showerror("Validation Error", "Please enter a valid video link.")
            return

        self.download_video_button.configure(state="disabled", text="Downloading...")
        self.update()

        download_thread = threading.Thread(
            target=self._download_video,
            args=(self.video_link.get(),),
            daemon=True
        )

        download_thread.start()
