config={
    "mode_name_online":'llama3-70b-8192',       # model name to online api
    "api_key_online":'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',   # put you key here from https://console.groq.com/keys
    "mode_name_offline":'llama3',                                   # offline local model name
    "api_key_offline":'http://localhost:11434',                 # offline local endpoint
    "context_window":50,         # context window "as bigger as better but takes a lot of resources *not recommended for low-end devices to set above 50*"
    "root_ip_host":'127.0.0.1'      # root ip *change this to local lan ip for LAN usage or general deployment ip*
}