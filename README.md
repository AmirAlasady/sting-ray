**Introduction**
===============

We present an AI personal assistant application that aims to be helpful, efficient, and make life easy for users. Our AI is designed to be dynamic, with the potential to develop its own personality in later updates.

**Core Features**
---------------

### 1. Multiple AI Model Support

Our system supports multiple AI models, including online models through APIs and a local offline API. Additionally, we provide a basic, customizable Transformer model that is ready for training on custom user data.

### 2. Multiple Conversations

We support multiple conversations, each with its own separate memory system. However, in offline mode, conversations share a single memory system for memory efficiency.

### 3. AI Responses and Content Generation

In each conversation, the AI can respond and generate content based on user queries.

### 4. RAG System Support

Our system supports a RAG (Read, Analyze, Generate) system, which allows users to upload files (currently only text and PDF formats are supported).

### 5. Agent Mode

Our AI is not only capable of thinking but can also execute actions, commands, and interact with external tools. Additionally, we provide custom tooling for any general action needed based on the design of the control message.

**System Structure**
=====================

### Directory Structure

The general structure of the app is as follows:

* `accounts`
	+ `migrations`
	+ `templates`
	+ `__pycache__`
* `ai_api`
	+ `migrations`
	+ `__pycache__`
* `assesstant_ai`
	+ `__pycache__`
* `core`
	+ `migrations`
	+ `static`
		- `css`
	+ `templates`
	+ `__pycache__`
* `media`
	+ `uploads`

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

**Usage**
=======

1. Clone the repository: `git clone https://github.com/AmirAlasady/sting-ray.git`
2. Install requirements: `pip install -r requirements.txt`
3. If using the native frontend, navigate to the server and run it: `python -m manage runserver 8000`
4. Navigate to the conversations tab and create a conversation
5. You can delete and change the name of the conversation
6. Access the conversation and interact with the AI agent
7. Optionally, upload files through the file upload form (text or PDF only)
8. Use the system prompt to make the model behave in a certain way
9. Interact with the system using text or audio input
10. Responses can be read with an auto-reader if supported by your browser
11. Select the AI model you want to use in the conversation (online or offline)
12. To use tools, navigate to `ai_api/views/py` and add custom tools based on the provided format

**Tool Behavior**
----------------

* Only use a tool if the user's message requires it and can fit the format of the correct tool
* Respond with the tool format only, without any additional explanations or comments, when a tool is needed
* If a tool is not needed, respond normally to the user's message
* **Available Tools**:

| Tool Name | Parameters/Inputs | Output Type | What it Does |
| --- | --- | --- | --- |
| add | [number1, number2] | the_sum_of_operands_1_plus_2 | adds the numbers together |
| sub | [number1, number2] | the_sub_of_operands_1_minuse_2 | subtracts number2 from number1 |

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