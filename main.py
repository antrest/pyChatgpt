import os
import openai
from rich import print
from rich.console import Console
from rich.markdown import Markdown
import prompt as P

os.system('cls' if os.name == 'nt' else 'clear')
# Load your API key from an environment variable or secret management service
# 初始化 openai api。 替换成自己的 api_token
OPENAI_TOKEN = 'xxxxxxxxxxxxxxxxxxxx'


openai.api_key = OPENAI_TOKEN

def format_cost(cost):
    # make cost 10 decimal points remove trailing zeros and decimal point
    # 修正 cost 为 10 位小数，去除末尾的 0 和小数点
    return "{:.10f}".format(cost).rstrip("0").rstrip(".")

def talk_to_chatbot(new_prompt, skip=False):
    # 每次都把初始的预设条件加在最上面
    conversation_history = [conversation_init['msg']]
    # 循环 conversation_data 并将 msg 添加到 conversation_history 中，直到 total_tokens 大于或等于 token_limit
    total_tokens = conversation_init['tokens']
    token_limit = 4096
    for data in conversation_data:
        total_tokens += data['tokens']
        if total_tokens < token_limit:
            conversation_history.append(data['msg'])
        else:
            break

    print(conversation_data)
    res = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=conversation_history)
    if skip:
        print('初始化完成，进行第一次请求...')
        return res
    
    # 用 utf-8 编码
    # new_reply = res['choices'][0]['message']['content'].encode('utf-8').decode('utf-8')
    new_reply = res['choices'][0]['message']['content']
    new_reply_obj = {"role": "assistant", "content": new_reply}

    # 换算 token 消耗 成 人民币
    global total_cost 
    cost = res['usage']['total_tokens'] * 0.0002 * 6.8 / 1000
    total_cost += cost


    # 打印出回复与 token 消耗
    print('提问消耗 token：', res['usage']['prompt_tokens'], ' 回答消耗 token：', res['usage']['completion_tokens'],' 本次消耗 token：', res['usage']['total_tokens'])
    console.print(f"[cyan]ChatGPT: [/] ([green]费用：[/]￥{format_cost(cost)} / ￥{format_cost(total_cost)})")
    console.print(Markdown(new_reply))
    print(f"——————————————————————————————————————————————————————————————————————")

    # 在本地记录 token 消耗

    conversation_data.append({"msg": new_prompt, "tokens": res['usage']['prompt_tokens'] - total_tokens})
    conversation_data.append({"msg": new_reply_obj, "tokens": res['usage']['completion_tokens']})

    return res

console = Console()
total_cost = 0

conversation_init = {"msg":{"role": "system", "content": P.init_prompt_song_ask}, "tokens": 0}
conversation_data = []

print("开启程序，初始化对话框...")

init_prompt = {"role": "user", "content": "来个跟我打个招呼，并开始问问题。"}
init_res = talk_to_chatbot(init_prompt)
conversation_init['token'] = init_res['usage']['prompt_tokens']


# create a while loop to keep asking the user for input
while True:
    # ask for user input
    user_input = input("我: ")
    if user_input == "exit":
        print("ChatGPT: 客官慢走！")
        break
    else:
        # call the function to get the chatbot response
        new_prompt = {"role": "user", "content": user_input}
        talk_to_chatbot(new_prompt)
        
       
