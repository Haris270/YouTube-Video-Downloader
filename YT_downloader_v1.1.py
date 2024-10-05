
import tkinter as tk
from tkinter import ttk
#from pytube import YouTube

from pytubefix import YouTube
from pytubefix.cli import on_progress


class MainPage(tk.Tk):

    def __init__(self, root):

        self.root = root
        root.title("YouTube Video Downloader v 1.0")
        root.geometry('402x352')
        self.openFirstWindow()

    def openFirstWindow(self):
        
        title = tk.Label(self.root, text="YT VIDEO DOWNLOADER", font=('Georgia',12))
        title.grid(column=0,row=0, columnspan=2, ipadx=110)
        
        prologue = tk.Label(self.root, text= 'Welcome! Enter the video URL:', font=('Perpetua',16))
        prologue.grid(column= 0, row= 1, sticky='w', ipady=20)
        self.obtainVideoLink()


    def obtainVideoLink(self):
        
        entry_box = tk.Entry(self.root)
        entry_box.grid(column=0, row=2, ipadx=100)
        

        enter_btn = tk.Button(self.root, text= "Enter", command= lambda: self.getVideo(videoLink= entry_box.get()))
        enter_btn.grid(column=0, row=3, ipadx=60)
        
        
    def getVideo(self,videoLink='*['):
        
        if videoLink != '*[':
            
            try:
                
                self.yt = YouTube(videoLink, on_progress_callback = on_progress)
                
            except:
                error_lbl = tk.Label(self.root, text= "~ Error - Video Not Found ~      ", fg='white')
                error_lbl.grid(column=0, row=4, ipadx=20, ipady=10, sticky='w')
                self.flashErrorPrompt()
                return None
        
        success_lbl = tk.Label(self.root, text= "~ Getting The Video - Please Wait ~", fg="green")
        success_lbl.grid(column=0, row=4, ipadx=20, ipady=10, sticky='w')

        self.getResolutions()


    def flashErrorPrompt(self):

        self.root.after(50,self.showErrorPrompt)


    def showErrorPrompt(self):
    
        error_lbl = tk.Label(self.root, text= "~ Error - Video Not Found ~      ", fg='red')
        error_lbl.grid(column=0, row=4, ipadx=20, ipady=10, sticky='w')
        

    def getResolutions(self):

        final_resolutions = []
        allResolutions = set()

        for availableStream in self.yt.streams:
            if availableStream.is_progressive == True:                        #Filter Out The Progressive Streams
                allResolutions.add(str(availableStream.resolution)[:-1])
        
        for res in allResolutions:
            final_resolutions.append(int(res))                                # Sort & List the Resolutions
        final_resolutions = sorted(final_resolutions)


        for index in range(len(final_resolutions)):
            final_resolutions[index] = str(final_resolutions[index]) + 'p'    # e.g "144" + 'p' --> "144p"

        self.openSecondWindow(final_resolutions)


    def openSecondWindow(self, final_resolutions):
        
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title('YouTube Video Downloader v 1.0')
        self.new_window.geometry('402x352')

        self.showTitle()
        self.showResolutions(final_resolutions)
        self.getDirectory()
        self.startDownload()
        self.downloadVideo()

    def showTitle(self):
               
        vid_title_lbl = tk.Label(self.new_window, text= "Video Title: ", font=('Perpetua',16))
        vid_title_lbl.grid(column=0, row=1, sticky='w')

        videoTitle = tk.Label(self.new_window, text=str(self.yt.title))
        videoTitle.grid(column=0,row=2, sticky='w')
        

    def showResolutions(self, final_resolutions):
               
        select_res_prompt = tk.Label(self.new_window, text= "Video Resolution: ", font=('Perpetua', 16))
        select_res_prompt.grid(column=0, row=3, sticky='w', ipady=10)
      
        res_menu = tk.StringVar()

        self.res_menu_drop = ttk.Combobox(self.new_window, width=12, values= final_resolutions, textvariable= res_menu)
        self.res_menu_drop.grid(column=0, row=3)


    def getDirectory(self):
               
        saveDirectoryPrompt = tk.Label(self.new_window, text= "Save To: ", font=('Arabic Typesetting', 16))
        saveDirectoryPrompt.grid(column=0, row=4, sticky='w')

        self.directoryInput = tk.Entry(self.new_window)
        self.directoryInput.grid(column=0, row=5, ipadx=100)

        directoryExample = tk.Label(self.new_window, text= "e.g C:/User/MyFolder/Downloads", fg='grey', font=('Arabic Typesetting', 14))
        directoryExample.grid(column=0, row=6, sticky='w', ipadx=65)


    def startDownload(self):
               
        beginDownload = tk.Button(self.new_window, text= "Download Video", command= lambda: self.downloadVideo(userResolution= self.res_menu_drop.get(), userDirectory= self.directoryInput.get()))
        beginDownload.grid(column=0, row=8)

        
    def downloadVideo(self, userResolution= "-", userDirectory= "-"):
        
        if (userResolution != "-") and (userDirectory.strip() != ""):
            
            video = self.yt.streams.filter(progressive=True, res= userResolution).first()
            video.download(userDirectory)        

            downloadFinished = tk.Label(self.new_window, text= "Downloading Finished!", fg='green', font=('Arabic Typesetting',16))
            downloadFinished.grid(column=0, row=9, sticky='w')


window = tk.Tk()
mm = MainPage(window)
window.mainloop()


