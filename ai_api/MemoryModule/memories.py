from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from root_config import config
class MultiMemoryManager:

    # saves memories for differant covnersations.
    def __init__(self):
        self.memories = {}

    # creates memory and saves it or if alredy created returns it to use.
    def get_memory(self, conversation_id):
        if conversation_id not in self.memories:
            self.memories[conversation_id] = ConversationBufferWindowMemory(k=config["context_window"], memory_key=f"conversation_{conversation_id}", return_messages=True)
        return self.memories[conversation_id]

    # removs memory
    def clear_memory(self, conversation_id):
        if conversation_id in self.memories:
            del self.memories[conversation_id]
    
    # shows memories
    def show_mem(self):
        print(self.memories)


