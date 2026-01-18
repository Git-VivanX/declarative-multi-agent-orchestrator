from src.tools.memory_tool import memory_tool
import shutil
import os

# Clean up previous tests
if os.path.exists("src/memory/faiss_index.bin"):
    os.remove("src/memory/faiss_index.bin")
if os.path.exists("src/memory/metadata.json"):
    os.remove("src/memory/metadata.json")

print("--- Testing Memory Tool ---")

# 1. Store memories
print("\n1. Storing memories...")
logs = [
    "The user's name is Aditya.",
    "Aditya likes to code in Python.",
    "Python is a versatile language.",
    "The weather is sunny today."
]

for log in logs:
    print(memory_tool("remember", key=log))

# 2. Semantic Search
print("\n2. Searching (Semantic)...")

query1 = "What is the user's name?"
print(f"\nQuery: {query1}")
print(memory_tool("recall", key=query1))

query2 = "What does the user like?"
print(f"\nQuery: {query2}")
print(memory_tool("recall", key=query2))

query3 = "programming language"
print(f"\nQuery: {query3}")
print(memory_tool("recall", key=query3))

print("\n--- Test Complete ---")
