# Chat client for reading and sending messages to the chat.

This project allows you to connect to the underground minecraft chat, read messages, register and authorise users, send messages.

## Setup
The chat client requires a Python version at least 3.6.

```bash
pip install -r requirements.txt
```

## Create **.env** file and set the <ins>following environmental variables</ins>:  
| Environmental  | Description                             |
|----------------|-----------------------------------------|
| `HOST`         | hostname to listen chat                 |       
| `READ_PORT`    | port for reading messages from the chat |      
| `SEND_PORT`    | port for sending messages to the chat   |
| `HISTORY_PATH` | a path to write chat history            |
| `AUTH_TOKEN`   | token that authorize user in chat       |
| `NICKNAME`     | your alias in chat                      |


## Running with required argument message
```bash
python main.py -M here will be some message
```

## Running with flags hostname, send_port and nickname
```bash
python main.py -H minechat.dvmn.org -P 5050 -N my_nickname
```