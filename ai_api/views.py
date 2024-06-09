
import json
import os
import re
import PyPDF2
import chardet
from django.shortcuts import get_object_or_404
from groq import Groq
import markdown
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from langchain_community.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
# defs
def txt_parser(file):
    with file.file.open('rb') as f:
        file_content = f.read()
        detection = chardet.detect(file_content)
        if detection['encoding']:
            file_content = file_content.decode(detection['encoding'])
        else:
            # if encoding detection fails, you can fallback to a default encoding
            file_content = file_content.decode('utf-8', errors='replace')
    return file_content

def pdf_parser(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        for page in pdf.pages:
            text += page.extract_text()
    return text


# state record

# Ai
"""
def ask_llama3(q,context):
    ollama = Ollama(base_url='http://localhost:11434',model="llama3")
    if context is None:
        context = []

    context.append({
        "role": "user",
        "content": q,
    })

    a=ollama.predict(context)
    response = {
        
        "role": "assistant",
        "content": a,
    }
    
    context.append(response)
    return a
"""
memory = ConversationBufferMemory()

ollama = Ollama(base_url='http://localhost:11434',model="llama3")
conversation = ConversationChain(
    llm=ollama, 
    memory = memory,
    
)

def ask_llama3(q):
    a=conversation.predict(input=q)
    #a=ollama(q)
    return a

def ask_model2(x, context=None, temp=0):
    key = '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'
    client = Groq(api_key=key)

    if context is None:
        context = []

    context.append({
        "role": "user",
        "content": x,
    })

    chat_completion = client.chat.completions.create(
        messages=context,
        model="llama3-70b-8192",
        temperature=temp,
    )

    content = chat_completion.choices[0].message.content
    response = {
        "content": content,
        "role": "assistant",
    }
    
    context.append(response)

    return content


# Create your views here.
class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        conversations = user.its_conversations.all()
        print(conversations)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)
    


class CreateConversationView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    def post(self, request):
        user = request.user
        title = request.data.get('title')
        if not title:
            return Response({'error': 'Title is required'}, status=400)
        conversation = Conversation.objects.create(title=title, user_owner=user)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=201)
    



class ChangeConversationName(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        try:
            conversation = Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=404)

        if conversation.user_owner != request.user:
            return Response({'error': 'Error'}, status=403)

        # Validate new title (optional)
        new_title = request.data.get('title')
        if not new_title or len(new_title) > 30:
            return Response({'error': 'Invalid title. Title is required and cannot exceed 30 characters.'}, status=400)

        conversation.title = new_title
        conversation.save()

        return Response({'message': 'Conversation title updated successfully'}, status=200)
         
        



class ConversationDetailView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    def get(self, request, pk):
        try:
            conversation = Conversation.objects.get(pk=pk)
            if conversation.user_owner != request.user:
                return Response({'error': 'no such conversation'}, status=403)

            chats = conversation.its_chats.all().filter(chat_type='n')    #[1:]
            chats_serialized = ChatSerializer(chats, many=True)

            return Response(chats_serialized.data)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def post(self, request, pk):
        try:
            conversation = Conversation.objects.get(pk=pk)
            chats = conversation.its_chats.all()
            # obtain files of the conversation
            files_of_conv=conversation.its_files.all()
            
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=404)

        if conversation.user_owner != request.user:
            return Response({'error': 'no such conversation'}, status=403)

        # Check if it's the first post request
        if not chats.exists():
            # Create a new chat object if it's the first post request
            prompt = """
                    **How you should behave during our conversation:**
                    **Behavior:**
                    * You will only use a tool if the user's message requires it and can fit the format of the correct tool.
                    * You will respond with the tool format only, without any additional explanations or comments, when a tool is needed.
                    * If a tool is not needed, you will respond normally to the user's message, providing a helpful and accurate answer.
                    * dont give the answe even if you know it dont give the answer at all. NEVER ANSWER ANYTHING WITHOU USING THE TOOL FOR IT !!
                    **Note:** When a tool is not required, respond to the user's message as you would in a normal conversation, providing a helpful and accurate answer.
                    **Note:** if no tool is required. there is no need for using any tool so just interact normally with me and my messages dont do like 'the result is 0'.
                    **Rules:**
                    * If a tool is needed, you will respond with the json format as: `
                        {
                            "tool_name": tool_name,
                            "operands":[operand1,operand3 . . . ]
                        }
                        `
                    * The number of operands can vary depending on the specific tool so when you resond and provide the operands in the dictionarry do not type the [. . .]\
                    thats just a refrerance of the possability of having more than one or 2 operands based on differant tools.
                    * **Note:** When listing operands, separate them with commas (`,`).
                    **Available Tools:**
                    | Tool_name | Parameters/Inputs | Output Type | What it Does |
                    | --- | --- | --- | --- |
                    | add | [number1, number2] | the_sum_of_operands_1_plus_2 | adds the numbers together |      
                    | sub | [number1, number2] | the_sub_of_operands_1_minuse_2 | subtracts number2 from number1 | 
                     """
            html_q_controll = markdown.markdown(prompt, extensions=['tables', 'fenced_code', 'def_list'])
            try:             
                answer = ask_model2(html_q_controll)
                chat = Chat(query=html_q_controll, answer=answer, conversation=conversation,chat_type='c')
                chat.save()
            except:
                print('failed online api call')
            try:
                ask_llama3(html_q_controll)
            except:
                print('failed local call')
            
        # basic knoledge template . . . 
        
        #   files reading sector
        for file in files_of_conv:
            # Open the file and read its contents
            print(file.is_read)
            if file.is_read=='f':
                chunk_size =0
                chunks_list=[]
                ffilename, file_extension = os.path.splitext(file.file.name)
                print(file_extension)
                if file_extension == '.txt':
                    file_content=txt_parser(file)
                    #formatted=prompt.replace('{x}', file_content)
                    chunk_size=int(len(file_content)/2)
                    print(f'formatted len=: {len(file_content)}')
                    print(f'chunk_sizen=: {chunk_size}')
                    # chunking 
                    for i in range(0,len(file_content),chunk_size):
                        prompt='understand and consider and [REMEMBER!!] the following data or stream of data,\
                        as a knoledge because i will recall you and ask you about it, the data is:[ {x} ] and the rest is:  '
                        g=prompt.replace('{x}', file_content[i:i+chunk_size])
                        chunks_list.append(g)
                    try:
                        print('online')
                        for j in chunks_list:
                            j = markdown.markdown(j, extensions=['tables', 'fenced_code', 'def_list'])
                            answer = ask_model2(j)
                            print('answer---------------')
                            chat = Chat(query=j, answer=answer, conversation=conversation, chat_type='r')
                            chat.save()
                        file.is_read = 't'
                        file.save()
                        print('end online')
                    except: 
                        file.is_read = 'f'
                        file.save()
                        print('failed api call')
                    try:
                        print('local')
                        for jj in chunks_list:
                            jj = markdown.markdown(jj, extensions=['tables', 'fenced_code', 'def_list'])
                            ask_llama3(jj)
                            print('answer---------------')
                        print('end local')
                        file.is_read = 't'
                        file.save()
                    except:
                        file.is_read = 'f'
                        file.save()
                        print('failed local call')
                    

                elif file_extension == '.pdf':
                    print(f"{file.file.name} is a .pdf file")
                    file_content=pdf_parser(file.file.path)
                    chunk_size=int(len(file_content)/2)
                    print(f'formatted len=: {len(file_content)}')
                    print(f'chunk_sizen=: {chunk_size}')
                    # chunking 
                    for i in range(0,len(file_content),chunk_size):
                        prompt='understand and consider and [REMEMBER!!] the following data or stream of data,\
                        as a knoledge because i will recall you and ask you about it, the data is:[ {x} ] and the rest is:  '
                        g=prompt.replace('{x}', file_content[i:i+chunk_size])
                        chunks_list.append(g)
                    try:
                        print('online')
                        for j in chunks_list:
                            j = markdown.markdown(j, extensions=['tables', 'fenced_code', 'def_list'])
                            answer = ask_model2(j)
                            print('answer---------------')
                            chat = Chat(query=j, answer=answer, conversation=conversation, chat_type='r')
                            chat.save()
                        file.is_read = 't'
                        file.save()
                        print('end online')
                        # make a flag to indecate the read state by onlinemodel or ofline model to avoid a model that read it but other didnt and dont make the mboth read if one didnt


                    except: 
                        file.is_read = 'f'
                        file.save()
                        print('failed api call')
                    try:
                        print('local')
                        for jj in chunks_list:
                            jj = markdown.markdown(jj, extensions=['tables', 'fenced_code', 'def_list'])
                            ask_llama3(jj)
                        file.is_read = 't'
                        file.save()
                        print('end local')
                    except:
                        file.is_read = 'f'
                        file.save()
                        print('failed local call')
                   
                elif file_extension in ['.doc', '.docx']:
                    print(f"{file.file.name} is a .doc or .docx file")
                    file.is_read = 't'
                    file.save()
                else:
                    print(f"{file.file.name} has an unknown file extension")
            else:
                print('nothing new')


        query = request.data.get('query')
        option = request.data.get('option')
        system = request.data.get('system')
        if system: 
            last_system_chat = Chat.objects.filter(conversation=conversation,chat_type='s').order_by('-id').first()  # Order by descending ID and get the first object
            template=f'this is a system message follow what is says the message: {system}. end of system message: acknowledge and act and follow what is says!'
            template = markdown.markdown(template, extensions=['tables', 'fenced_code', 'def_list'])
            if last_system_chat:
                last_system_chat.delete()
                print("Last system chat deleted successfully!")
            else:
                print("No system chat found for conversation:", conversation)
            try:
                answer = ask_model2(template)
                chat = Chat(query=system, answer=answer, conversation=conversation, chat_type='s')
                chat.save()
            except:
                print('failed to inject system message to llama3 online api.')
            
            try:
                ask_llama3(template)
            except:
                print('failed to inject system message to llama3 ofline api.')

        if not query:
            return Response({'error': 'Query is required'}, status=400)
        if not option:
            return Response({'error': 'Option is required'}, status=400) 

        # Process the post request
        if option == 'option1':
            context = []
            for chat in chats:
                context.append({
                    "role": "user",
                    "content": chat.query,
                    "role": "assistant",
                    "content": chat.answer,
                })
            try:
                query = markdown.markdown(query, extensions=['tables', 'fenced_code', 'def_list'])
                answer = ask_model2(query, context)
                # agent tooling
                pattern = r'{.*?}'
                match = re.search(pattern, answer, re.DOTALL)
                if match:
                    json_str = match.group(0)
                    json_dict = json.loads(json_str)
                    print((json_dict))
                    res=0
                    if json_dict['tool_name']=='add':
                        res=float(json_dict['operands'][0])+float(json_dict['operands'][1])
                        print(f'result of add is: {res}')
                    elif json_dict['tool_name']=='sub':
                        res=float(json_dict['operands'][0])-float(json_dict['operands'][1])
                        print(f'result of sub is: {res}')
                    
                    tmp_prompt=f'the result is {res}'
                    html = markdown.markdown(tmp_prompt, extensions=['tables', 'fenced_code', 'def_list'])
                    #here consider saving the json ai answer for the ai to future refrance its self using that template as i aggreed up with
                    chat = Chat(query=query, answer=html, conversation=conversation)
                    chat.save()
                else:
                    print("No JSON dictionary found (ONLINE)")
                    html = markdown.markdown(answer, extensions=['tables', 'fenced_code', 'def_list'])
                    chat = Chat(query=query, answer=html, conversation=conversation)
                    chat.save()
            except:
                return Response({'error': 'rate limmit reached'}, status=500)

        if option == 'option2':
            try:
                query = markdown.markdown(query, extensions=['tables', 'fenced_code', 'def_list'])
                answer = ask_llama3(query)
                # agent tooling
                pattern = r'{.*?}'
                match = re.search(pattern, answer, re.DOTALL)
                if match:
                    res=0
                    json_str = match.group(0)
                    json_dict = json.loads(json_str)
                    print((json_dict))
                    if json_dict['tool_name']=='add':
                        res=float(json_dict['operands'][0])+float(json_dict['operands'][1])
                        print(f'result of add is: {res}')
                    elif json_dict['tool_name']=='sub':
                        res=float(json_dict['operands'][0])-float(json_dict['operands'][1])
                        print(f'result of sub is: {res}')
                    tmp_prompt=f'the result is {res}'
                    html = markdown.markdown(tmp_prompt, extensions=['tables', 'fenced_code', 'def_list'])
                    chat = Chat(query=query, answer=html, conversation=conversation)
                    chat.save()
                else:
                    print("No JSON dictionary found (OFLINE)")
                    html = markdown.markdown(answer, extensions=['tables', 'fenced_code', 'def_list'])
                    chat = Chat(query=query, answer=html, conversation=conversation)
                    chat.save()
            except:
                print('offline problems')
        
        serializer = ChatSerializer(chat)
        return Response(serializer.data, status=201)
        

    def delete(self, request, pk):
        try:
            conversation = Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=404)

        if conversation.user_owner != request.user:
            return Response({'error': 'no such conversation'}, status=403)

        conversation.delete()
        return Response({'message': 'Conversation deleted'}, status=204)
    






class FilesView(APIView):
    permission_classes = [IsAuthenticated]  # Optional: Add authentication
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    def validate_file(self, value):
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
        if not any(value.name.lower().endswith(ext) for ext in allowed_extensions):
            raise ValidationError(f"Unsupported file type. Only PDFs (.pdf), DOCX (.docx), or DOC (.doc) files are allowed.")

    def post(self, request ,pk):
        try:
            conversation = Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=404)

        if conversation.user_owner != request.user:
            return Response({'error': 'no such conversation'}, status=403)
        
        file = request.FILES.get('file')
        file=Files_data(file=file,conversation=conversation,is_read='f')
        file.save()
        return Response(status=200)
    
    def get(self, request, pk):
        try:
            conversation = Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=404)

        if conversation.user_owner != request.user:
            return Response({'error': 'no such conversation'}, status=403)
        
        files = conversation.its_files.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    def delete(self, request,  pk, file_id):
        try:
            conversation = Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=404)

        if conversation.user_owner != request.user:
            return Response({'error': 'no such conversation'}, status=403)
        try:
            file_to_delete = conversation.its_files.all().filter(pk=file_id)
            file_to_delete.delete()
            return Response(status=200)
        except Files_data.DoesNotExist:
            return Response(status=404)