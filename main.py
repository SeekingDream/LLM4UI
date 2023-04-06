import openai
import os
import subprocess
import csv

import err_msg_extraction
import prompt_wrapper
from query import QUERY_LIST



openai.api_key = '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'


def response2code(answer):
    candidates = answer.split('```')
    new_candidates = []
    for candidate in candidates:
        if candidate.find('"deviceName": "emulator-5554"') != -1 or candidate.find("'deviceName': 'emulator-5554'") != -1:
            new_candidates.append([candidate, len(candidate.split('\n'))])
    new_candidates = sorted(new_candidates, key=lambda t: t[1])
    code = new_candidates[0][0]
    return code


def ask_chatbot(question):
    messages = [
        {
            "role": "user",
            "content": f"{question}, just return the python code without any text."
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        # prompt=f"Q: {question}, just return the code.\nA:",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.3
    )

    answer = response.choices[0].message['content'].strip()
    answer = response2code(answer)
    return answer


def handle_query(query, prompt_handle_func, err_handle_func):
    question_his = [query['init_prompt']]

    answer_his = []
    ask_num = 0
    is_success = False
    final_script = ''

    while not is_success:
        ask_num += 1
        user_input = question_his[-1]

        response = ask_chatbot(user_input)
        answer_his.append(response)

        with open('generated_code.py', 'w') as f:
            f.writelines(response)

        process = subprocess.Popen(['python', 'generated_code.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            error_msg = str(stderr, 'utf-8')
            error_msg_list = error_msg.split('\n')
            extract_err = err_handle_func(error_msg_list)
            print('ERROR: \n', extract_err)
            print('------------------------------')
            next_input = prompt_handle_func(response, extract_err)
            print('NEW INPUT: \n', next_input)
            print('*********************************')
            question_his.append(next_input)
        else:
            is_success = True
            final_script = response

        if ask_num >= 10:
            break
    return is_success, question_his, answer_his, final_script, ask_num


def save_results(save_path, question_his, answer_his, final_script, ask_num):
    with open(save_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow([final_script, ask_num])

        for q, a in zip(question_his, answer_his):
            writer.writerow([q, a])


def main():
    for heuristic_error in range(1):
        err_hand_func = getattr(err_msg_extraction, 'err_extraction_%d' % heuristic_error)

        for heuristic_prompt in range(1):
            prompt_hand_func = getattr(prompt_wrapper, 'prompt_wrapper_%d' % heuristic_prompt)

            save_dir = f'result_error_{heuristic_error}_prompt_{heuristic_prompt}'
            if not os.path.isdir(save_dir):
                os.mkdir(save_dir)

            for i, query_instance in enumerate(QUERY_LIST):
                app_name = query_instance['app_name']
                res = handle_query(query_instance, prompt_hand_func, err_hand_func)
                is_success, question_his, answer_his, final_script, ask_num = res

                if is_success:
                    print(i, app_name, 'successful to generate test case')
                else:
                    print(i, app_name, 'not generate successful')

                save_path = os.path.join(save_dir, '%d_%s.csv' % (i, app_name))
                save_results(save_path, question_his, answer_his, final_script, ask_num)


if __name__ == '__main__':
    main()