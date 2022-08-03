
import tkinter as tk
from tkinter import ttk
from pytube import YouTube


class MainPage(tk.Tk):

    def __init__(self, root):

        self.root = root
        root.title("YouTube Video Downloader v 1.0")
        root.geometry('402x352')

        
        title = tk.Label(self.root, text="YT VIDEO DOWNLOADER", font=('Georgia',12))
        title.grid(column=0,row=0, columnspan=2, ipadx=110)
        
        prologue = tk.Label(self.root, text= 'Welcome! Enter the video URL:', font=('Arabic Typesetting',16))
        prologue.grid(column= 0, row= 1, sticky='w', ipady=20)

        entry_box = tk.Entry(self.root)
        entry_box.grid(column=0, row=2, ipadx=100)
        

        
        enter_btn = tk.Button(self.root, text= "Enter", command= lambda: self.getVideo(videoLink= entry_box.get()))
        enter_btn.grid(column=0, row=3, ipadx=60)
        
        


    def getVideo(self,videoLink='*['):
        
        if videoLink != '*[':
            
            try:
                
                yt = YouTube(videoLink)
                
                

            except:
                error_lbl = tk.Label(self.root, text= "~ Error - Video Not Found ~      ", fg='white')
                error_lbl.grid(column=0, row=4, ipadx=20, ipady=10, sticky='w')
                self.flashErrorPrompt()
                return None

            success_lbl = tk.Label(self.root, text= "~ Getting The Video - Please Wait ~", fg="green")
            success_lbl.grid(column=0, row=4, ipadx=20, ipady=10, sticky='w')
            self.openSecondWindow(yt)


    def flashErrorPrompt(self):

        self.root.after(50,self.blinkErrorPrompt)



    def blinkErrorPrompt(self):
    
        error_lbl = tk.Label(self.root, text= "~ Error - Video Not Found ~      ", fg='red')
        error_lbl.grid(column=0, row=4, ipadx=20, ipady=10, sticky='w')
        


    def openSecondWindow(self, yt):
        
        new_window = tk.Toplevel(self.root)
        new_window.title('YouTube Video Downloader v 1.0')
        new_window.geometry('402x352')

        vid_title_lbl = tk.Label(new_window, text= "Video Title: ", font=('Arabic Typesetting',16))
        vid_title_lbl.grid(column=0, row=1, sticky='w')

        videoTitle = tk.Label(new_window, text=str(yt.title))
        videoTitle.grid(column=0,row=2)
        

        select_res_prompt = tk.Label(new_window, text= "Available Video Resolutions: ", font=('Arabic Typesetting', 16))
        select_res_prompt.grid(column=0, row=3, sticky='w', ipady=10)


        filtered_resolutions = []
        allResolutions = set()

        for availableStream in yt.streams:
            if availableStream.is_progressive == True:
                allResolutions.add(str(availableStream.resolution)[:-1])
        

        for res in allResolutions:
            filtered_resolutions.append(int(res))
        filtered_resolutions = sorted(filtered_resolutions)
        for index in range(len(filtered_resolutions)):
            filtered_resolutions[index] = str(filtered_resolutions[index]) + 'p'
        
        res_menu = tk.StringVar()

        res_menu_drop = ttk.Combobox(new_window, width=16, values= filtered_resolutions, textvariable= res_menu)
        res_menu_drop.grid(column=0, row=3)


        saveDirectoryPrompt = tk.Label(new_window, text= "Save To: ", font=('Arabic Typesetting', 16))
        saveDirectoryPrompt.grid(column=0, row=4, sticky='w')

        directoryInput = tk.Entry(new_window)
        directoryInput.grid(column=0, row=5, ipadx=100)

        directoryExample = tk.Label(new_window, text= "e.g C:/User/MyFolder/Downloads", fg='grey', font=('Arabic Typesetting', 14))
        directoryExample.grid(column=0, row=6, sticky='w', ipadx=65)

        beginDownload = tk.Button(new_window, text= "Download Video", command= lambda: self.downloadVideo(n_win = new_window, yt=yt,userResolution= res_menu_drop.get(), userDirectory= directoryInput.get()))
        beginDownload.grid(column=0, row=8)

        
    def downloadVideo(self,n_win, yt, userResolution= "-", userDirectory= "-"):
        
        if (userResolution != "-") and (userDirectory.strip() != ""):
            
            video = yt.streams.filter(progressive=True, res= userResolution).first()
            max_file_size = video.filesize
            video.download(userDirectory)        

            d_lbl = tk.Label(n_win, text= "Downloading Finished!", fg='green', font=('Arabic Typesetting',16))
            d_lbl.grid(column=0, row=9, sticky='w')


window = tk.Tk()
mm = MainPage(window)
window.mainloop()

#https://www.youtube.com/watch?v=5DkkCDk1lpU
            
