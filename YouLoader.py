import sys
import os
import subprocess
from pytube import YouTube

# TODO: ffmpeg not work now
# import ffmpeg
#from ffmpeg import stream

# GUI
import tkinter as tk
from tkinter import filedialog

def check_url():
    global listvideo, listradio, yt, yt_filename
    tk_label_Msg.config(text="") # 清除提示訊息
    print(tk_url.get())
    if(tk_url.get() == ""): # 未輸入網址
        tk_label_Msg.config(text="網址欄位必須輸入!")
    else:
        try: # 捕捉影片不存在的錯誤
            # yt = YouTube('https://www.youtube.com/watch?v=Gg54Miwa8K4')
            yt = YouTube(tk_url.get()) # 取得輸入網址
        except: # 顯示影片不存在的訊息
            tk_label_Msg.config(text="找不到此YouTube影片")

        # yt_filename = yt.title + ".mp4"
        # yt_filename = yt_filename.replace(":", "").replace(" ", "_").replace("-", "_")
        #print(yt_filename)
        #tk_filename.set(yt_filename)
        # print(yt.streams.all())
        # print(yt.streams)
        for v1 in yt.streams:
            type(v1)
            listvideo.append(v1)
        rbvalue = 1 # 設定選項按鈕的值, rb = radio button
        for v2 in listvideo: # 建立影片格式選項按鈕
            type(v2)
            print("v2 = ", v2)
            rbtem = tk.Radiobutton(tk_frame3, text=v2, variable=tk_radio_video, value=rbvalue, command=rbVideo)
            if(rbvalue==1):
                rbtem.select()
                rbVideo()
            listradio.append(rbtem)
            rbtem.grid(row=rbvalue-1, column=0, sticky="w")
            rbvalue += 1
        tk_btn_download.config(state="normal")

def tk_askdirectory():
    tk_path.set(filedialog.askdirectory())
    print(tk_path.get())

def rbVideo():  # radio button video
    global itag
    tk_label_Msg.config(text="")
    # print("video=", video.get()-1)
    # print(listvideo[video.get()-1])
    # print(type(listvideo[video.get()-1]))
    # print(str(listvideo[video.get()-1]))
    # print(type(str(listvideo[video.get()-1])))
    print(tk_radio_video.get())
    strvideo = str(listvideo[tk_radio_video.get()-1])
    # <Stream: itag="134" mime_type="video/mp4" res="360p" fps="30fps" vcodec="avc1.4d401e" progressive="False" type="video">
    start1 = strvideo.find("itag=")
    end1 = strvideo.find("\" ", start1)
    itag = strvideo[start1+6:end1]
    print("itag = ", itag)
    start2 = strvideo.find("mime_type=", start1)
    mid2 = strvideo.find("/", start2)
    end2 = strvideo.find("\" ", mid2)
    video_or_audio = strvideo[start2+11:mid2]
    extension = strvideo[mid2+1:end2]
    print("vidoe_or_audio = ", video_or_audio)
    print("extension = ", extension)
    if(video_or_audio == "video"):
        start3 = strvideo.find("res=", end2)
        end3 = strvideo.find("\" ", start3)
        res = strvideo[start3+5:end3]
        start4 = strvideo.find("fps=", end3)
        end4 = strvideo.find("\" ", start4)
        fps = strvideo[start4+5:end4]
        start5 = strvideo.find("vcodec=", end4)
        end5 = strvideo.find("\" ", start5)
        vcodec = strvideo[start5+8:end5]
        print("res = ", res, " fps = ", fps, " vcodec = ", vcodec)
        yt_filename = yt.title + "_" + video_or_audio + res + fps + vcodec
    else:
        start3 = strvideo.find("abr=", end2)
        end3 = strvideo.find("\" ", start3)
        abr = strvideo[start3+5:end3]
        start4 = strvideo.find("acodec=", end3)
        end4 = strvideo.find("\" ", start4)
        acodec = strvideo[start4+8:end4]
        print("abr = ", abr, " acodec = ", acodec)
        yt_filename = yt.title + "_" + video_or_audio + abr + acodec
    yt_filename = yt_filename.replace(":", "").replace(" ", "_").replace("-", "_").replace(".", "_")
    tk_filename.set(yt_filename)

def clickDownload():
    tk_label_Msg.config(text="")
    savefilepath = tk_path.get()
    # print("savefilepath = ", savefilepath)
    # temppath = savefilepath.replace("\\", "\\\\") # 將\轉換成\\
    # savefilepath = temppath
    # print("savefilepath = ", savefilepath)
    try: # download fail
        yt.streams.get_by_itag(int(itag)).download(output_path=savefilepath, filename=tk_filename.get())
    except:
        tk_label_Msg.config(text="download fail")
    tk_label_Msg.config(text="download success")
    tk_btn_clr_yt_link.config(state="normal")

def clr_yt_link():
    for r in listradio:
        r.destroy()
    listradio.clear()
    listvideo.clear()
    tk_url.set("")
    tk_filename.set("")
    tk_btn_download.config(state="disabled")
    tk_btn_clr_yt_link.config(state="disabled")

### # stream = yt.streams.filter(file_extension='mp4', res='2160p')
### print(yt.title)
### # print(yt.streams.all())
### ### video download
### print(yt.streams.filter(res='2160p'))
### print(yt.streams.filter(res='2160p').first().default_filename)
### # yt.streams.filter(res='2160p').first().download()
### video_filename = yt.title + "_video"
### yt.streams.filter(res='2160p').first().download(filename=video_filename)
###
### ### audio download
### print(yt.streams.filter(type='audio', abr='160kbps', mime_type='audio/webm'))
### print(yt.streams.filter(type='audio', abr='160kbps', mime_type='audio/webm').first().default_filename)
### # yt.streams.filter(type='audio', abr='160kbps', mime_type='audio/webm').first().download()
### audio_filename = yt.title + "_audio"
### yt.streams.filter(type='audio', abr='160kbps', mime_type='audio/webm').first().download(filename=audio_filename)
###
### # TODO: merge video + audio to mp4 file
### video_webm_filename = video_filename + ".webm"
### # video_stream = Stream.input(video_webm_filename)
### audio_webm_filename = audio_filename + ".webm"
### # audio_stream = Stream.input(audio_webm_filename)
### mp4_filename = yt.title + ".mp4"
### mp4_filename = mp4_filename.replace(":", "")
### mp4_filename = mp4_filename.replace(" ", "_")
### mp4_filename = mp4_filename.replace("-", "_")
### print(video_webm_filename)
### print(audio_webm_filename)
### print(mp4_filename)

# tk gui
win = tk.Tk()
win.geometry("900x1200")
win.title("YouLoader") # YouTube downloader
tk_url = tk.StringVar()  # 影片網址
tk_path = tk.StringVar() # 存檔資料夾
tk_filename = tk.StringVar() # 存檔名稱
listvideo = [] # 影片格式串列
listradio = [] # 按鈕選項串列
tk_radio_video = tk.IntVar() # 選項按鈕值

### begin: tk_frame1
tk_frame1 = tk.Frame(win, width=900)
tk_frame1.pack()
tk_label_url = tk.Label(tk_frame1, text="YouTube網址:")
tk_entry_url = tk.Entry(tk_frame1, textvariable=tk_url)
tk_entry_url.config(width=60)
tk_btn_url = tk.Button(tk_frame1, text="確定", command=check_url)
tk_label_url.grid(row=0, column=0, sticky="e") # sticky="e" 靠右排列
tk_entry_url.grid(row=0, column=1)
tk_btn_url.grid(row=0, column=2)

tk_label_path = tk.Label(tk_frame1, text="存檔路徑:")
tk_entry_path = tk.Entry(tk_frame1, textvariable=tk_path)
tk_browse_btn = tk.Button(tk_frame1, text="Browse", command=tk_askdirectory)
tk_entry_path.config(width=60)
tk_label_path.grid(row=1, column=0, pady=6, sticky="e")
tk_entry_path.grid(row=1, column=1)
tk_browse_btn.grid(row=1, column=2)

tk_label_filename = tk.Label(tk_frame1, text="存檔名稱")
tk_entry_filename = tk.Entry(tk_frame1, textvariable=tk_filename)
tk_entry_filename.config(width=60)
tk_label_filename.grid(row=2, column=0, pady=3, sticky="e")
tk_entry_filename.grid(row=2, column=1)
### end: tk_frame1

### begin: tk_frame2
tk_frame2 = tk.Frame(win)
tk_frame2.pack()
tk_btn_download = tk.Button(tk_frame2, text="下載", command=clickDownload)
# tk_btn_download.pack(pady=6)
tk_btn_download.config(state="disabled") # 開始時設定[下載影片]按鈕無效
tk_btn_clr_yt_link = tk.Button(tk_frame2, text="清除yt link", command=clr_yt_link)
tk_btn_clr_yt_link.config(state="disabled") # 開始時設定[下載影片]按鈕無效
tk_btn_download.grid(row=1, column=0, pady=6, sticky="e")
tk_btn_clr_yt_link.grid(row=1, column=1)

tk_label_Msg = tk.Label(win, text="", fg="red") # 訊息標籤
tk_label_Msg.pack()
### end: tk_frame2

### begin: tk_frame3
tk_frame3 = tk.Frame(win) # 選項按鈕區
tk_frame3.pack()
### end: tk_frame3

win.mainloop()
