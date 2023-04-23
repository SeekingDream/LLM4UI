import openai

MODEL_NAME_LIST = [
    'gpt-3.5-turbo',
    'gpt-4',
    'code-davinci-002'
]


def ask_chatbot(question, model_name='gpt-3.5-turbo', temperature=0.0) ->str:
    if model_name == 'gpt-3.5-turbo':
        return _ask_gpt35_turbo(question, temperature)
    elif model_name == 'gpt-4':
        return _ask_gpt4(question, temperature)
    else:
        raise NotImplementedError           # TODO add model here


def _ask_gpt35_turbo(question, temperature):
    messages = [
        {
            "role": "user",
            "content": f"{question}"
        }
    ]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=temperature
    )
    return response['choices'][0]['message']['content']


def _ask_gpt4(question, temperature):
    messages = [
        {
            "role": "user",
            "content": f"{question}"
        }
    ]
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=temperature
    )
    return response['choices'][0]['message']['content']