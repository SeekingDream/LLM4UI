import openai
import os
import subprocess
import csv
import ast
import re
import torch

import err_msg_extraction
import prompt_wrapper
from src.query import ask_chatbot
from src.enum_ids import enumerate_ids, get_elements_of_current_driver
from query_list import QUERY_LIST
from utils import ErrorReason
from src.dump_instrumentation import instrument_dump_and_save

openai.api_key = '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'


def response2code(response):
    candidates = response.split('```')
    new_candidates = []
    for candidate in candidates:
        if candidate.find('38534a424c453098') != -1:
            new_candidates.append([candidate, len(candidate.split('\n'))])
    new_candidates = sorted(new_candidates, key=lambda t: t[1])
    code = new_candidates[0][0]
    return code


def pipeline2prompt(pipeline):
    init_prompt = 'write a python script to use uiautomator2 library to conduct the following steps\n' + pipeline + '\n'
    init_prompt += 'my device name is 38534a424c453098, platformName is Android, platformVersion is 10.'
    init_prompt += 'start with the following code\n'
    init_prompt += 'import uiautomator2 as u2\n' \
                   '# Connect to device' \
                   "d = u2.connect('38534a424c453098')" \
                   '# Open YouTube app' \
                   "d.app_start('com.google.android.youtube', 'com.google.android.youtube.HomeActivity')"
    return init_prompt


def extract_number_from_string(s):
    match = re.search(r'\d+', s)
    if match:
        return int(match.group())
    else:
        return None


def execute_code(generated_code):
    with open('generated_code.py', 'w') as f:
        f.writelines(generated_code)

    process = subprocess.Popen(['python', 'generated_code.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr, process.returncode


def response2pipeline(response):
    sentence_list = response.split('\n')
    index_list = [i for i, s in enumerate(sentence_list) if s == '']
    st, ed = index_list[0], index_list[1]
    pipeline = sentence_list[st + 1:ed]
    return '\n'.join(pipeline)


def code2cap(source_code):
    tree = ast.parse(source_code)
    constant_variables = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if isinstance(node.value, ast.Dict):
                        constant_variables[target.id] = ast.literal_eval(node.value)
    for k in constant_variables:
        if 'platformName' in constant_variables[k]:
            return constant_variables[k]
    raise NotImplementedError


def error_analysis(error_msg):
    if error_msg.find('NoSuchElementError') != -1:
        return ErrorReason.NoSuchElementError
    elif error_msg.find('AttributeError') != -1:
        return ErrorReason.AttributeError
    else:
        return ErrorReason.Other


def get_error_line(error_msg):
    error_msg_split = error_msg.split('\n')
    for error_s in error_msg_split:
        if error_s.find('generated_code.py') != -1:
            line_no = extract_number_from_string(error_s)
            return line_no
    raise NotImplementedError


def modify_code(generated_code, error_line, page_ids):
    statements = generated_code.split('\n')
    node = ast.parse(statements[error_line - 1])
    new_programs = []
    old_statement = statements[error_line - 1]
    for page_id in page_ids:
        for child_node in ast.walk(node):
            if isinstance(child_node, ast.Str):
                current_string = child_node.value
                new_statement = old_statement.replace(current_string, page_id)
                statements[error_line - 1] = new_statement
                new_programs.append(statements)
    return new_programs


def get_clickable_element(ui_dict):
    new_key_list = []
    possible_property = [
        'checkable',
        # 'checked',
        'clickable',
        # 'enabled',
        'focusable',
        # 'focused',
        'scrollable',
        'long_clickable',
        # 'password',
        # 'selected'
    ]
    for k in ui_dict:
        element = ui_dict[k]
        for p in possible_property:
            if element[p]:
                new_key_list.append(k)
                break
    return new_key_list


def handle_query(query, prompt_handle_func, err_handle_func):
    answer_his = []
    ask_num = 0
    is_success = False
    final_script = ''

    process_step_response = ask_chatbot(query['init_prompt'])
    pipeline = response2pipeline(process_step_response)
    pipeline_prompt = pipeline2prompt(pipeline)
    print(pipeline)
    question_his = [pipeline_prompt]
    while not is_success:
        ask_num += 1
        user_input = question_his[-1] + '\n Just return the Code'

        response = ask_chatbot(user_input)
        response = response.strip()
        answer_his.append(response)

        generated_code = response2code(response)
        # desired_capability = code2cap(generated_code)       # Get the meta information of this UI page
        # page_ids = enumerate_ids(desired_capability)

        stdout, stderr, returncode = execute_code(generated_code)

        if returncode != 0:
            instrumented_code = instrument_dump_and_save(generated_code)
            execute_code(instrumented_code)
            ui_res = torch.load('tmp_ui.res')
            page_ids = get_clickable_element(ui_res)
            error_msg = str(stderr, 'utf-8')
            # error_line = get_error_line(error_msg)
            # error_reason = error_analysis(error_msg)

            error_msg_list = error_msg.split('\n')
            extract_err = err_handle_func(error_msg_list, page_ids)
            print('ERROR: \n', extract_err)
            print('------------------------------')
            next_input = prompt_handle_func(generated_code, extract_err)
            print('NEW INPUT: \n', next_input)
            print('*********************************')
            question_his.append(next_input)
        else:
            is_success = True
            final_script = generated_code

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
    for heuristic_error in range(3):
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
