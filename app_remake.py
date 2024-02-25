import tkinter as tk
from tkinter import ttk
from customtkinter import *
from bs4 import BeautifulSoup


class HtmlDataExtractor:
    def __init__(self, html_file_path_followers, html_file_path_following):
        self.html_file_path_followers = html_file_path_followers
        self.html_file_path_following = html_file_path_following

    def extract_data(self):
        with open(self.html_file_path_followers, "r", encoding="utf-8") as file:
            html_content_followers = file.read()

        with open(self.html_file_path_following, "r", encoding="utf-8") as file:
            html_content_following = file.read()

        soup_followers = BeautifulSoup(html_content_followers, "html.parser")
        soup_following = BeautifulSoup(html_content_following, "html.parser")

        followers = soup_followers.find_all('a', target='_blank')
        followings = soup_following.find_all('a', target='_blank')

        followers_list = [follower.get_text(strip=True) for follower in followers]
        following_list = [following.get_text(strip=True) for following in followings]

        not_following_back = [following for following in following_list if following not in followers_list]

        return not_following_back


app = CTk()
app.geometry("500x400")
app.maxsize(500, 400)
app.minsize(500,400)
app.title('Unfollow Unfollowers')

followers_entry = CTkEntry(master=app, placeholder_text="Followers File Path", width=200,
                text_color="#FFCC70")

following_entry = CTkEntry(master=app, placeholder_text="Following File Path", width=200,
                text_color="#FFCC70")

def analyze():
    # Get the values from the entry boxes
    
    # # Print the values (for demonstration)
    # print("Followers Path:", followers_path)
    # print("Following Path:", following_path)
    try:

        followers_path = f'{followers_entry.get()}'
        following_path = f'{following_entry.get()}'
        extractor = HtmlDataExtractor(followers_path, following_path)
        not_following_back = extractor.extract_data()
        for user in not_following_back:
            label = CTkLabel(master=frame, text=f'{user}', fg_color='#436850', width=200)
            label.pack(anchor="s", expand=True, pady=5, padx=30)

    except FileNotFoundError:
        label = CTkLabel(master=frame, text=f'Path Does Not Exist', fg_color='#D04848',width=200)
        label.pack(anchor="s", expand=True, pady=5, padx=30)
    
        

btn = CTkButton(master=app, text="Analyze", corner_radius=5, command=analyze)


btn.place(relx=0.5, rely=0.4, anchor="center") 

followers_entry.place(relx=0.5, rely=0.2, anchor="center") 
following_entry.place(relx=0.5, rely=0.3, anchor="center") 

frame = CTkScrollableFrame(master=app,
                           orientation="vertical", label_text='Users Not Following Back', width=500)
frame.place(relx=0.5, rely=0.8, anchor="center")
 


app.mainloop()
    