import os
import PyPDF2
import chardet


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


def file_loader(files,llama3_online,llama3_offline,mem,execute_in_parallel):
    for file in files:
        print(file.is_read)
        if file.is_read=='f':
            chunk_size =0
            chunks_list=[]
            filename, file_extension = os.path.splitext(file.file.name)
            print(f'file name: {filename}')
            print(file_extension)
            if file_extension == '.txt':
                file_content=txt_parser(file)
                chunk_size=int(len(file_content)/2)
                print(f'formatted len=: {len(file_content)}')
                print(f'chunk_sizen=: {chunk_size}')
                for i in range(0,len(file_content),chunk_size):
                    prompt='understand and consider and [REMEMBER!!] the following data or stream of data,\
                    as a knoledge because i will recall you and ask you about it, the data is:[ {x} ] and the rest is:  '
                    g=prompt.replace('{x}', file_content[i:i+chunk_size])
                    chunks_list.append(g)
                try:
                    for j in chunks_list:
                        chunk_online=j
                        chunk_offline=j
                        func1 = llama3_online.ask_online
                        args1 = (chunk_online, mem)
                        func2 = llama3_offline.ask_offline
                        args2 = (chunk_offline, mem)
                        execute_in_parallel(func1, func2, args1, args2)
                    file.is_read = 't'
                    file.save()
                except: 
                    file.is_read = 'f'
                    file.save()
                    print('failed api call')
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
                    for j in chunks_list:
                        chunk_online=j
                        chunk_offline=j
                        func1 = llama3_online.ask_online
                        args1 = (chunk_online, mem)
                        func2 = llama3_offline.ask_offline
                        args2 = (chunk_offline, mem)
                        execute_in_parallel(func1, func2, args1, args2)
                    file.is_read = 't'
                    file.save()
                except: 
                    file.is_read = 'f'
                    file.save()
                    print('failed api call')
            else:
                print(f"{file.file.name} has an unknown file extension")
        else:
            print('nothing new')