import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16\magick.exe"

from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
import pandas as pd

print("Loading video...")

video = VideoFileClip("videos/full_match.mp4")
events = pd.read_csv("data/events.csv")

clips = []

print("Processing highlights...")

for i in range(len(events)):

    time = events.loc[i, "time"]
    event = events.loc[i, "event"]

    if event == "wicket":
        before, after = 8, 8
    elif event == "six":
        before, after = 5, 5
    else:
        before, after = 4, 4

    start = max(0, time - before)
    end = time + after

    clip = video.subclip(start, end)

    text = event.upper()

    txt = TextClip(text, fontsize=50, color='white', bg_color='black')
    txt = txt.set_position(('center', 'top')).set_duration(clip.duration)

    final_clip = CompositeVideoClip([clip, txt])

    clips.append(final_clip)

print("Merging clips...")

final_video = concatenate_videoclips(clips)

print("Saving output...")

final_video.write_videofile("output/highlights.mp4")

print("Done! Highlights created.")