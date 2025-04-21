import cv2
import os
import numpy as np

# 📁 Path to your PNG frames
frames_folder = r"D:\OpenToonz stuff\projects\Ball Bounce\outputs"
output_video_path = "output_video.mp4"
fps = 24  # 🎞️ Frames per second

# 📜 Get a sorted list of .png files
frame_files = sorted([
    os.path.join(frames_folder, f)
    for f in os.listdir(frames_folder)
    if f.lower().endswith(".png")
])

# 🛑 No frames found
if not frame_files:
    print("🚫 No PNG frames found in the folder.")
    exit()

# 🔍 Check size of the first frame
first_frame_path = frame_files[0]
first_img = cv2.imread(first_frame_path, cv2.IMREAD_UNCHANGED)

if first_img is None:
    print(f"❌ Could not read the first image: {first_frame_path}")
    exit()

height, width = first_img.shape[:2]
print(f"🖼️ First frame size: {width}x{height}")

# 🎬 Set up the video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

print("\n🎞️ Writing frames to video...\n")

# 🖼️ Process each frame
for frame_file in frame_files:
    print(f"📄 Loading: {frame_file}")
    frame = cv2.imread(frame_file, cv2.IMREAD_UNCHANGED)

    if frame is None:
        print(f"❌ Failed to load: {frame_file}. Skipping.")
        continue

    # If frame has alpha channel (i.e., 4 channels), composite onto white
    if frame.shape[2] == 4:
        print("🖌️ Compositing with white background...")
        bgr = frame[:, :, :3]
        alpha = frame[:, :, 3] / 255.0

        white_bg = np.ones_like(bgr, dtype=np.uint8) * 255
        composite = (bgr * alpha[..., None] + white_bg * (1 - alpha[..., None])).astype(np.uint8)
        frame = composite

    video_writer.write(frame)

video_writer.release()
print("\n🎉 Video successfully saved as:", output_video_path)
