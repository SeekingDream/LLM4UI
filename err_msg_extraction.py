
def err_extraction_0(error_list):
    return '\n'.join(error_list)


def err_extraction_1(error_list):
    for i, err_s in enumerate(error_list):
        if err_s.find('"generated_code.py"') != -1:
            return error_list[i + 2]
    raise NotImplementedError


def err_extraction_2(error_list):
    for i, err_s in enumerate(error_list):
        if err_s.find('"generated_code.py"') != -1:
            return '\n'.join(error_list[i:i + 3])
    raise NotImplementedError


def err_extraction_3(error_list):
    return error_list[-2]

