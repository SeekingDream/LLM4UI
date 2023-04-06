
def prompt_wrapper_0(err_code, extract_err):
    return f'I have the following code: \n```\n{err_code}\n```\n There is an error in above code, error message is \n {extract_err}\n. Fix the error and return the whole new code'