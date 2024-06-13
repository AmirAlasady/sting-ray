import re
from django.shortcuts import get_object_or_404
import markdown
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# parrallel exe
from .Parrallel.parallel import execute_in_parallel

# import config
import root_config 

# memory manager 'CRUD memories'
from .MemoryModule.memories import MultiMemoryManager
Memory_manager = MultiMemoryManager()

# ai model load
from .Ai.models import Llm_online,Llm_offline
llama3_online=Llm_online(root_config.config['api_key_online'],0.7,root_config.config['mode_name_online'])
llama3_offline=Llm_offline(api=root_config.config['api_key_offline'],model=root_config.config['mode_name_offline'])

# load file works
from .filesManager.FileSystem import file_loader









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
    
    # api config 'auth, throttling' configration for get request
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    
    def get(self, request, pk):
        try:
            # obtain the conversation and check owner
            conversation = Conversation.objects.get(pk=pk)
            if conversation.user_owner != request.user:
                return Response({'error': 'you are not the owner! '}, status=403)

            # obtain the chat's of the requested covnersation and serialize it.
            chats = conversation.its_chats.all().filter(chat_type='n')    #only of type 'normal'
            chats_serialized = ChatSerializer(chats, many=True)
            return Response(chats_serialized.data)
        
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=404)

    
    def post(self, request, pk):
        #try:

        # obtain the conversation and check owner
        conversation = Conversation.objects.get(pk=pk)
        if conversation.user_owner != request.user:
            return Response({'error': 'you are not the owner!'}, status=403)
            
        # obtain files 
        files_of_conv=conversation.its_files.all()

        # initiate memory or create it if non exist
        mem= Memory_manager.get_memory(pk)

        # un-comment for activation agent behavior 
        """
        if not chats.exists():
           l3on_ctl=llama3_online.ctl
           l3of_ctl=llama3_offline.ctl
           func1 = llama3_online.ask_online
           args1 = (l3on_ctl, mem)
           func2 = llama3_offline.ask_offline
           args2 = (l3of_ctl, mem)
           execute_in_parallel(func1, func2, args1, args2) # Execute the functions in parallel
        """
        # ctl prompt injection for 1st post
        

        # read files if not read already
        file_loader(files_of_conv,llama3_online,llama3_offline,mem,execute_in_parallel)

        # obtain option leading flow
        option = request.data.get('option')
        if not option:
            return Response({'error': 'Option is required'}, status=400)
        # post request requirements
        query = request.data.get('query')
        system = request.data.get('system')
        
        print(f'query: {query} | system: {system}')
        # Process the post request

        if option == 'option1':
            if system:
                res=llama3_online.ask_online(query,mem,system)
                print(f'query: {query} | res: {res}')
            else:
                res=llama3_online.ask_online(query,mem)
                print(f'query: {query} | res: {res}')
            
        elif option == 'option2':
            if system:
                res=llama3_offline.ask_offline(query,mem,system)
                print(f'query: {query} | res: {res}')
            else:
                res=llama3_offline.ask_offline(query,mem)
                print(f'query: {query} | res: {res}')


        # add mrk down on the cliend side cus it confusses the ai !! add it with js fE
        res=markdown.markdown(res, extensions=['tables', 'fenced_code', 'def_list'])
        chat=Chat(query=query,answer=res, conversation=conversation, chat_type='n')
        chat.save()
        
        serializer = ChatSerializer(chat)
        return Response(serializer.data, status=201)

        #except Conversation.DoesNotExist:
            #return Response({'error': 'Conversation not found'}, status=404)

       
        

    def delete(self, request, pk):
        try:
            conversation = Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=404)

        if conversation.user_owner != request.user:
            return Response({'error': 'no such conversation'}, status=403)

        Memory_manager.clear_memory(pk)

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