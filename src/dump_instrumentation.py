import ast

import astunparse



def instrument_dump_and_save(src_code):
    """
    Instruments the statements "r = dump()" and "torch.save(r, 'tmp_ui.res')" after each statement
    in the given Python source code. Returns the modified source code as a string.
    """
    # Parse the source code into an AST
    tree = ast.parse(src_code)

    # Create a new list of nodes that includes the original statements and the instrumented statements
    new_nodes = []
    for node in tree.body:
        new_nodes.append(node)
        dump_stmt = ast.parse('r = dump_ui()').body[0]
        save_stmt = ast.parse('torch.save(r, "tmp_ui.res")').body[0]
        new_nodes.append(dump_stmt)
        new_nodes.append(save_stmt)

    # Replace the original list of nodes with the new list
    tree.body = new_nodes

    # Convert the modified AST back to source code
    new_code = 'from src.dump_ui import dump_ui\nimport torch\n' + astunparse.unparse(tree)
    return new_code


