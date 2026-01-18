from src.memory.vector_store import VectorStore

# Singleton instance
_store = None

def get_store():
    global _store
    if _store is None:
        _store = VectorStore()
    return _store

def memory_tool(action, key=None, value=None):
    """
    Tool for long-term memory using Vector Database.
    
    Args:
        action (str): 'remember' (save) or 'recall' (search).
        key (str): Used as the text to remember or the query to recall.
        value (str): (Optional) Additional metadata/context to store.
    """
    store = get_store()
    
    if action == "remember":
        # 'key' is treated as the main text to embed
        text_to_store = key
        if not text_to_store:
             return "Error: 'key' (text to remember) is required."
        
        store.add(text_to_store, meta=value)
        return f"Stored in memory: {text_to_store}"

    elif action == "recall":
        # 'key' is treated as the query
        query = key
        if not query:
            return "Error: 'key' (search query) is required."
            
        results = store.search(query)
        if not results:
            return "No relevant memories found."
            
        return "\n".join([f"- {r['text']} (sim: {r['distance']:.2f})" for r in results])

    return "Invalid action. Use 'remember' or 'recall'."