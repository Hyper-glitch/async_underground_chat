# Chat client for reading and sending messages to the chat.

This project allows you to connect to the underground minecraft chat, read messages, register and authorise users, send messages.

## Setup

```bash
pip install -r requirements.txt
```

## Create **.env** file and set the <ins>following environmental variables, if you don't want to use default values</ins>:  
| Environmental               | Description                              |
|-----------------------------|------------------------------------------|
| `HOST`                      | hostname to listen chat                  |       
| `READ_PORT`                 | port for reading messages from the chat  |      
| `SEND_PORT`                 | port for sending messages to the chat    |
| `HISTORY_PATH`              | a path to write chat history             |
| `AUTH_TOKEN`                | token that authorize user in chat        |
| `NICKNAME`                  | your alias in chat                       |
| `TIMEOUT_EXPIRED_SEC`       | expired time in sec for a request        |
| `SERVER_PING_FREQUENCY_SEC` | time in sec between requests to a server |


## Running with required argument message
```bash
python main.py
```

## Running with flags hostname, send_port and nickname
```bash
python main.py -H minechat.dvmn.org -P 5050 -N my_nickname
```

## How does it work
[Screencast from 31.08.2022 16:49:50.webm](https://user-images.githubusercontent.com/54985705/187698619-03ae39e9-d2dc-442f-aafc-b61f35260564.webm)
