
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from abc import ABC

from langchain_community.llms import Ollama


class Ai(ABC):
    # controll prompt for agent controll behaviors 
    ctl_prompt = """
        
            """
    def ask():
        pass
    
class Llm_online(Ai):
    def __init__(self,api,temp,model):
        self.ctl=super().ctl_prompt
        self.api=api
        self.temp=temp
        self.model=model
        self.llm=ChatGroq(
            groq_api_key=self.api, 
            model_name=self.model,
            temperature=self.temp
            )
    def ask_online(self,question,mem,sys=''):
        prompt = ChatPromptTemplate.from_messages(
                    [
                        SystemMessage(
                            content=sys
                        ),  # This is the persistent system prompt that is always included at the start of the chat.

                        MessagesPlaceholder(
                            variable_name=mem.memory_key
                        ),  # This placeholder will be replaced by the actual chat history during the conversation. It helps in maintaining context.

                        HumanMessagePromptTemplate.from_template(
                            "{human_input}"
                        ),  # This template is where the user's current input will be injected into the prompt.
                    ]
                )
        conversation=LLMChain(
            llm=self.llm,  
            prompt=prompt, 
            verbose=False,   
            memory=mem,
        )
        response = conversation.predict(human_input=question)
        return response

        
class Llm_offline(Ai):
    def __init__(self,api,model):
        self.ctl=super().ctl_prompt
        self.api=api
        self.model=model
        self.llm=Ollama(
            base_url=self.api, 
            model=self.model,
            )
    def ask_offline(self,question,mem,sys=''):
        prompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessage(
                        content=sys
                    ),  # This is the persistent system prompt that is always included at the start of the chat.

                    MessagesPlaceholder(
                        variable_name=mem.memory_key
                    ),  # This placeholder will be replaced by the actual chat history during the conversation. It helps in maintaining context.

                    HumanMessagePromptTemplate.from_template(
                        "{human_input}"
                    ),  # This template is where the user's current input will be injected into the prompt.
                ]
            )
        conversation = LLMChain(
            llm=self.llm, 
            memory = mem,
            prompt=prompt,
        )
        response = conversation.predict(human_input=question)
        return response