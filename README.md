**Introduction**
===============

We present an AI personal assistant application that aims to be helpful, efficient, and make life easy for users. Our AI is designed to be dynamic, with the potential to develop its own personality in later updates.




## Installation:

**Note:** Install Python as a prerequisite and add it to the PATH.

1. Create a folder `<name_example>`.
2. Navigate to `<name_example>`: `cd <name_example>`.
3. Create a virtual environment: `python -m venv <env_name>`.
4. Navigate to `<env_name>`: `cd <env_name>`.
5. Activate the environment:

   
   .\Scripts\activate
   
7. Clone the repository:


   git clone https://github.com/AmirAlasady/sting-ray.git
 
9. Navigate to the cloned repository: `cd .\sting-ray\`.
10. Install requirements:


	pip install -r .\requirements.txt

12. Navigate to the `/sting-ray.git/root_config.py` file in the project and configure the options:
```python
config={
    "mode_name_online":'llama3-70b-8192', # model name for online API
    "api_key_online":'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', # put your key here from https://console.groq.com/keys
    "mode_name_offline":'llama3', # offline local model name
    "api_key_offline":'http://localhost:11434', # offline local endpoint
    "context_window":50, # context window "bigger is better but takes a lot of resources *not recommended for low-end devices to set above 50*"
    "root_ip_host":'127.0.0.1' # root IP *change this to local LAN IP for LAN usage or general deployment IP*
}
```

You can run this on LAN by changing the root_ip_host to your own device IP and saving the changes.


10. Run the server on the IP you selected on root_ip_host at port 8000:
- For local use: python -m manage runserver 127.0.0.1:8000
- For LAN use: python -m manage runserver 'your LAN private IP':8000
Note: Deactivate Windows network sharing firewall to allow the application to be used on LAN by other devices.

11. To enable offline models, there are two options:

a) Download open-source models from Hugging Face and adopt them to the AI class and the `ask` method, or from Ollama framework.
b) Train the pre-implemented transformer model on your custom dataset.

We will initialize with Ollama's 'llama 3 8B' model, but you can install any model you want from the hub.

To install Ollama:
1. [Download Ollama for Windows](https://ollama.com/download/windows).
2. Set it up.
3. To view and select models, visit the model hub at [Ollama Model Library](https://ollama.com/library).
4. Open CMD and run `ollama run 'model_name'`. In our case, it's 'llama3', so it'll be `ollama run llama3`. This will install the model if not already installed on the local machine and may take some time based on your internet speed. Next time you run the command, 'llama3' will be installed already from the first time, so it will launch faster.
5. After installing the model, expose it as an API endpoint by running the command `ollama serve` to start the Ollama server. Now you can use the offline model from the web app and engage in conversations.

Note: Each time the system restarts, the memory will be removed.



**Core Features**
---------------

### 1. Multiple AI Model Support

Our system supports multiple AI models based on the 'Ai' base class , including online models through APIs and a local offline API. Additionally, we provide a basic, customizable Transformer model that is ready for training on custom user data. 

### 2. Multiple Conversations

We support multiple conversations, each with its own separate memory system.  
we have a seprate memory system for each conversation, and in the single conversation the memory is shared withen the 2 ai models (online, offline)


### 3. AI Responses and Content Generation

In each conversation, the AI can respond and generate content based on user queries.

### 4. RAG System Support

Our system supports a RAG (Read, Analyze, Generate) system, which allows users to upload files (currently only text and PDF formats are supported).
where the user can chat with his own data sources 

### 5. Agent Mode
(advanced use cases only by modifing the 'ctl_prompt' in the (Ai) bas class module)
you can configre a custom prompt to allo for agentic behavior 
then by unmarcking the 
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
in the 'ai_api.views' file 
to wllow for injection of the ctl prompt 
Note!: this will run in parrallel for both model using the 'execute_in_parallel' found in 'Parrallel' module 
Our AI is not only capable of thinking but can also execute actions, commands, and interact with external tools. Additionally, we provide custom tooling for any general action needed based on the design of the control message.

## How to Use the System:

1. Run the server as explained earlier.
   ![Step 1](https://github.com/AmirAlasady/sting-ray/assets/96434221/75dd5c08-b2e8-4f0c-ae85-e906040b1dfe)

2. Open the URL link `http://<your_private_ip_or_local_host>:8000/showconvs`. You will be granted with the about page.

### About:
![About](https://github.com/AmirAlasady/sting-ray/assets/96434221/ce3fa527-ddd4-442b-87f7-270cab5d3faf)
Note: This is just a dummy frontend. We use a headless system, and anyone can create a custom frontend by using the APIs provided. However, this is just a simple head for testing. Keep in mind that the login and sign-up pages' forms are just a demo showcase to create accounts in the system. It's not required to create an account to use this dummy frontend for fast use.

3. Navigate to the conversations tab and create a conversation.
   ![Step 3](https://github.com/AmirAlasady/sting-ray/assets/96434221/a3e1b9ae-1b67-4da8-ba19-6e4b572284d1)

4. You can also rename/del the conversation and everything will be removed.
5. By pressing on the conversation name, you will be able to access the system and have a chat with audio (if the browser allows for it) and text.
   ![Step 5](https://github.com/AmirAlasady/sting-ray/assets/96434221/82f08725-8c9d-43a3-855f-abec839bb7b3) Note: you can move the forms as you like freely by dragging them to anywhere you want on the screen from the blue bar on top.

6. You can select between online or offline models by checking the option.
   ![Online Option](https://github.com/AmirAlasady/sting-ray/assets/96434221/0816ec01-ffe7-400f-a4b9-d997b1f0dc61)

7. You can use the system prompt to control the simple behavior of the system.
   ![Step 7](https://github.com/AmirAlasady/sting-ray/assets/96434221/0fc4c78f-1ee0-4b62-a0bb-65e47768e6ad)

8. You can upload multiple PDF, TXT files to the system to allow for RAG and a chat with your documents. As an example, we will include a needle in a haystack test. We will inject random text, a secret word of Amir, which is 'hi i love fish', and see if the model knows it or not.
   ![Step 8](https://github.com/AmirAlasady/sting-ray/assets/96434221/20715972-1756-4683-93ae-e43e7469dddd)
   Now let's import it to the chat files. Keep in mind that uploading files will take some time because we use chunking and we inject the data into the two models in parallel.
   ![Step 8 - Continued](https://github.com/AmirAlasady/sting-ray/assets/96434221/e181ae18-7c16-46e5-9ffa-b3449dd6387b)

9. All conversations use separate memory units, thus the AI doesn't know about things from different conversations.
   ![Offline](https://github.com/AmirAlasady/sting-ray/assets/96434221/4f2fe7a7-c63b-48c9-aef8-2779042fc24d)

10. Online and offline AI use the same memory in one conversation; thus, you can use any of them at any time in the conversation. Let's ask the offline model about what Amir's secret word is to see if it knows it. So first, change to offline mode. You can do the same test by using the offline mode in the beginning and then changing to online; it'll work the same.
    ![Step 10](https://github.com/AmirAlasady/sting-ray/assets/96434221/70f4eb2e-4aff-4873-8490-9c5df1e3dcc1)
    It knew about it as planned.


11. you can manage the system by creating a new admin account or use the test admin account provided by default 
with the credentials as 
Email: admin@test.com
Username: admin
First name: admin1
Last name: admin2
pass: 123

**Core System Project File**
---------------------------

The core system project file has the core router URLs to the other app locations as follows:

`assesstant_ai/urls.py`:
```python
urlpatterns = [
    path('', include("core.urls")),
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('accounts/', include('accounts.urls')),
    path('ai_api/', include('ai_api.urls'))
]
```

`core/urls.py`:
```python
urlpatterns = [
    path('', about, name='about'),
    path('showconvs', showconvs, name='showconvs'),
    path('details/<int:pk>', details, name='details'),
    path('deleate/<int:pk>', deleate, name='deleate'),
    path('ask/<int:pk>', ask, name='ask'),
    path('update/<int:pk>', update, name='update'),
    path('upload_file/<int:pk>', upload_file, name='upload_file'),
    path('deleate_file/<int:pk>/<int:id>', deleate_file, name='deleate_file')
]
```





**Message Types**
================

Our system uses four message types:

1. **Normal**: Always shown to the user
2. **System**: Not shown and only one is provided in each conversation
3. **RAG System**: Used for file handling flags
4. **Control Message**: A powerful message injected at system initiation to configure tools and agentic behavior


Here is the API endpoints documentation in Markdown format:

**Project URLs**
===============

### Core Endpoints
#### `GET /`

* Description: Welcome page
* Response: HTML content

#### `GET /showconvs`

* Description: Show all conversations
* Response: HTML content

#### `GET /details/<int:pk>`

* Description: Show conversation details
* Parameters:
	+ `pk`: Conversation ID (integer)
* Response: HTML content

#### `DELETE /deleate/<int:pk>`

* Description: Delete a conversation
* Parameters:
	+ `pk`: Conversation ID (integer)
* Response: HTTP 204 No Content

#### `GET /ask/<int:pk>`

* Description: Show conversation ask form
* Parameters:
	+ `pk`: Conversation ID (integer)
* Response: HTML content

#### `PUT /update/<int:pk>`

* Description: Update a conversation
* Parameters:
	+ `pk`: Conversation ID (integer)
* Request Body:
	+ `name`: New conversation name (string)
* Response: HTTP 200 OK

#### `POST /upload_file/<int:pk>`

* Description: Upload a file to a conversation
* Parameters:
	+ `pk`: Conversation ID (integer)
* Request Body:
	+ `file`: File to upload (multipart/form-data)
* Response: HTTP 201 Created

#### `DELETE /deleate_file/<int:pk>/<int:id>`

* Description: Delete a file from a conversation
* Parameters:
	+ `pk`: Conversation ID (integer)
	+ `id`: File ID (integer)
* Response: HTTP 204 No Content

**Accounts Endpoints**
=====================

#### `GET /`

* Description: Accounts index page
* Response: HTML content

#### `GET /login/`

* Description: Login form
* Response: HTML content

#### `POST /login/`

* Description: Login submission
* Request Body:
	+ `username`: Username (string)
	+ `password`: Password (string)
* Response: HTTP 302 Found (redirect to dashboard)

#### `GET /signup/`

* Description: Signup form
* Response: HTML content

#### `POST /signup/`

* Description: Signup submission
* Request Body:
	+ `username`: Username (string)
	+ `password`: Password (string)
	+ `email`: Email address (string)
* Response: HTTP 201 Created (redirect to login)

**AI API Endpoints**
=====================

#### `GET /conversations`

* Description: List all conversations
* Response: JSON array of conversation objects

#### `POST /conversations/create`

* Description: Create a new conversation
* Request Body:
	+ `name`: Conversation name (string)
* Response: JSON conversation object with ID

#### `GET /conversations/<int:pk>`

* Description: Get a conversation by ID
* Parameters:
	+ `pk`: Conversation ID (integer)
* Response: JSON conversation object

#### `PUT /conversations/update/<int:pk>`

* Description: Update a conversation
* Parameters:
	+ `pk`: Conversation ID (integer)
* Request Body:
	+ `name`: New conversation name (string)
* Response: HTTP 200 OK

#### `POST /files/upload/<int:pk>`

* Description: Upload a file to a conversation
* Parameters:
	+ `pk`: Conversation ID (integer)
* Request Body:
	+ `file`: File to upload (multipart/form-data)
* Response: HTTP 201 Created

#### `GET /files/show/<int:pk>`

* Description: List files in a conversation
* Parameters:
	+ `pk`: Conversation ID (integer)
* Response: JSON array of file objects

#### `DELETE /files/remove/<int:pk>/<int:file_id>`

* Description: Delete a file from a conversation
* Parameters:
	+ `pk`: Conversation ID (integer)
	+ `file_id`: File ID (integer)
* Response: HTTP 204 No Content
