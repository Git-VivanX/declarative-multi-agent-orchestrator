import logging

from src.memory.vector_store import VectorStore

class Agent:
    def __init__(self, id, role, goal, llm, tools):
        self.id = id
        self.role = role
        self.goal = goal
        self.llm = llm
        self.tools = tools
        self.memory = VectorStore() # Singleton access to persistent memory

    async def run(self, context: str):
        logging.info(f"Agent {self.id} starting. Role: {self.role}")
        
        # 1. Recall relevant memories
        relevant_memories = self.memory.search(context, k=2)
        memory_context = ""
        if relevant_memories:
            logging.info(f"Agent {self.id} found relevant memories.")
            memory_list = "\n".join([f"- {m['text']}" for m in relevant_memories])
            memory_context = f"\nRelevant Past Memories:\n{memory_list}\n"

        # 2. Augment Prompt
        prompt = f"Role: {self.role}\nGoal: {self.goal}\n{memory_context}Context:\n{context}"
        
        # 3. Generate
        response = await self.llm.generate(prompt, self.tools)
        
        # 4. Remember (Auto-save)
        # We store the response as a memory for future agents/executions
        self.memory.add(response, meta={"agent_id": self.id, "role": self.role})
        logging.info(f"Agent {self.id} finished and saved memory.")
        
        return response