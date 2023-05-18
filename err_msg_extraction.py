from typing import List


def err_extraction_0(error_list, ori_page_ids: List):
    page_ids = [str(p) for p in ori_page_ids]
    page_ids_str = '; '.join(page_ids)
    return_str = '\n'.join(error_list)
    return_str += '\n Notice I have following IDs on the current pages: ' + page_ids_str
    return return_str


def err_extraction_1(error_list, ori_page_ids):
    page_ids = [str(p) for p in ori_page_ids]
    page_ids_str = '; '.join(page_ids)
    for i, err_s in enumerate(error_list):
        if err_s.find('"generated_code.py"') != -1:
            return_str = error_list[i + 2] + '\n Notice I have following IDs on the current pages: ' + page_ids_str
            return return_str
    raise NotImplementedError


def err_extraction_2(error_list, ori_page_ids):
    page_ids = [str(p) for p in ori_page_ids]
    page_ids_str = '; '.join(page_ids)
    for i, err_s in enumerate(error_list):
        if err_s.find('"generated_code.py"') != -1:
            return_str = '\n'.join(error_list[i:i + 3]) + '\n Notice I have following IDs on the current pages: ' + page_ids_str
            return return_str
    raise NotImplementedError


def err_extraction_3(error_list, page_ids):
    return error_list[-2]

