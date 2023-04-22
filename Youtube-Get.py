#!/usr/bin/env python
'''
    Date: 4-18-2023
    Music get highest quality audio, then converted to .mp3
    Videos try for 720p resolution or better. If .mp4 not available, convert.
    pyTube v_12.1.3
    Python v_3.10.11
    moviepy v_1.0.3
'''
import os
from moviepy.editor import *
import pytube

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining 
    liveprogress = (int)(bytes_downloaded / total_size * 100)
    if liveprogress > on_progress.previousprogress:
        on_progress.previousprogress = liveprogress
        print(f"Download is {liveprogress}% complete.")

on_progress.previousprogress = 0

def download_video(youtube_url):
    print("Downloading video...")
    youtube = pytube.YouTube(youtube_url, on_progress_callback=on_progress)
    youtube.register_on_progress_callback(on_progress)

    # Get the highest quality video with resolution <= 720p
    video = youtube.streams.filter(progressive=True, res="720p").order_by("resolution").first()
    video_path = os.path.join(os.getcwd(), video.default_filename)
    video.download(output_path=os.getcwd())
    print(f"Video downloaded at {video_path}")

    # Convert the video to .mp4 if necessary
    if video.mime_type != "video/mp4":
        print("Converting video to .mp4...")
        video_clip = VideoFileClip(video_path)
        mp4_path = os.path.splitext(video_path)[0] + ".mp4"
        video_clip.write_videofile(mp4_path)
        video_clip.close()
        os.remove(video_path)
        video_path = mp4_path
        print(f"Video converted to {video_path}")

    return video_path

def download_audio(youtube_url):
    print("Downloading audio...")
    youtube = pytube.YouTube(youtube_url, on_progress_callback=on_progress)
    youtube.register_on_progress_callback(on_progress)

    # Get the highest quality audio
    audio = youtube.streams.filter(only_audio=True).order_by("bitrate").desc().first()
    audio_path = os.path.join(os.getcwd(), audio.default_filename)
    audio.download(output_path=os.getcwd())
    print(f"Audio downloaded at {audio_path}")

    # Convert the audio to .mp3
    print("Converting audio to .mp3...")
    audio_clip = AudioFileClip(audio_path)
    mp3_path = os.path.splitext(audio_path)[0] + ".mp3"
    audio_clip.write_audiofile(mp3_path)
    audio_clip.close()
    os.remove(audio_path)
    print(f"Audio converted to {mp3_path}")
    
    return mp3_path


if __name__ == "__main__":
    youtube_url = input("Enter the URL of the video you want to download: ")
    download_type = input("Do you want to download 'audio' or 'video'? ")
    if download_type.lower() == "audio":
        download_audio(youtube_url)
    elif download_type.lower() == "video":
        download_video(youtube_url)
    else:
        print("Invalid download type.")
