from indexing import index_video

# Use any YouTube video with captions
url = "https://www.youtube.com/watch?v=fNk_zzaMoSs&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab"

result = index_video(url)

print("\n--- TEST RESULTS ---")
print("Video ID:", result["video_id"])
print("Transcript length:", len(result["transcript"]))
print("Number of chunks:", len(result["chunks"]))
print(" chunks : ", result["chunks"][5])