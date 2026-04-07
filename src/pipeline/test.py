from indexing import index_video
from retrieval import get_context_from_vector_store
from augmentation import augment_context
import string


# Use any YouTube video with captions
url = "https://www.youtube.com/watch?v=fNk_zzaMoSs&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab"

result_of_indexing = index_video(url)

# print("\n--- TEST RESULTS ---")
# print("Video ID:", result["video_id"])
# print("Transcript length:", len(result["transcript"]))
# print("Number of chunks:", len(result["chunks"]))
# print(" chunks : ", result["chunks"][5])

query = str(input("enter the query : "))     # uear query

vectore_store = result_of_indexing["vector_store"]     # vector store created in indexing 

retrived_context = get_context_from_vector_store(vectore_store, query)    # retriving the context from the created vectore database

# print("Retrived context is : ", retrived_context)

final_prompt = augment_context(retrived_context, query)     # getting final prompt from augmentation
print("Final prompt is : ", final_prompt)