#! /usr/bin/env python
# coding=utf-8
from __future__ import division

f_table = {}  # function table


class Tran:

    def __init__(self):
        self.v_table = {}  # variable table

    def update_v_table(self, name, value):
        self.v_table[name] = value

    def trans(self, node):
        # Translation

        # Assignment
        if node.getdata() == '[ASSIGNMENT]':
            r'''assignment : VARIABLE '=' NUMBER
                           | VARIABLE '[' expression ']' '=' NUMBER
                           | VARIABLE '=' VARIABLE
                           | VARIABLE '=' VARIABLE '[' expression ']'
                           | VARIABLE '=' num_list'''
            if len(node.getchildren()) == 3:
                if ord('0') <= ord(node.getchild(2).getdata()[0]) <= ord('9'):  # NUMBER
                    value = node.getchild(2).getvalue()
                    # update v_table
                    self.update_v_table(node.getchild(0).getdata(), value)
                elif node.getchild(2).getdata() == '[NUM_LIST]':  # num_list
                    self.trans(node.getchild(2))
                    value = node.getchild(2).getvalue()
                    # update v_table
                    self.update_v_table(node.getchild(0).getdata(), value)
                else:  # VARIABLE
                    value = self.v_table[node.getchild(2).getdata()]
                    # update v_table
                    self.update_v_table(node.getchild(0).getdata(), value)

            elif len(node.getchildren()) == 4:
                if node.getchild(2).getdata() == '=':  # NUMBER
                    arg = self.v_table[node.getchild(0).getdata()]
                    self.trans(node.getchild(1))
                    index = int(node.getchild(1).getvalue())
                    value = node.getchild(3).getvalue()
                    # update VARIABLE
                    arg[index] = value
                elif node.getchild(1).getdata() == '=':  # VARIABLE '[' expression ']'
                    arg1 = self.v_table[node.getchild(2).getdata()]
                    self.trans(node.getchild(3))
                    index = int(node.getchild(3).getvalue())
                    value = arg1[index]
                    # update v_table
                    self.update_v_table(node.getchild(0).getdata(), value)

        # Num_list
        elif node.getdata() == '[NUM_LIST]':
            '''num_list : '[' numbers ']' '''
            if len(node.getchildren()) == 1:
                self.trans(node.getchild(0))
                value = [float(x) for x in node.getchild(0).getvalue().split()]
                node.setvalue(value)

        # Numbers
        elif node.getdata() == '[NUMBERS]':
            '''numbers : NUMBER
                       | numbers ',' NUMBER'''
            if len(node.getchildren()) == 1:
                value = str(node.getchild(0).getvalue())
                node.setvalue(value)

            elif len(node.getchildren()) == 2:
                self.trans(node.getchild(0))

                value0 = node.getchild(0).getvalue()
                value1 = str(node.getchild(1).getvalue())
                value = value0 + ' ' + value1
                node.setvalue(value)

        # Operation
        elif node.getdata() == '[OPERATION]':
            '''operation : VARIABLE '=' expression
                         | VARIABLE '+' '=' expression
                         | VARIABLE '-' '=' expression
                         | VARIABLE '[' expression ']' '=' expression'''
            if len(node.getchildren()) == 3:
                if node.getchild(1).getdata()[0] == '=':  # '='
                    self.trans(node.getchild(2))
                    value = node.getchild(2).getvalue()
                    node.getchild(0).setvalue(value)
                    # update v_table
                    self.update_v_table(node.getchild(0).getdata(), value)
                elif node.getchild(1).getdata()[1] == '=':  # '+=' or '-='
                    arg1 = self.v_table[node.getchild(0).getdata()]
                    self.trans(node.getchild(2))
                    arg2 = node.getchild(2).getvalue()
                    op = node.getchild(1).getdata()[0]
                    if op == '+':
                        value = arg1 + arg2
                    elif op == '-':
                        value = arg1 - arg2
                    node.getchild(0).setvalue(value)
                    # update v_table
                    self.update_v_table(node.getchild(0).getdata(), value)

            elif len(node.getchildren()) == 4:
                arg = self.v_table[node.getchild(0).getdata()]
                self.trans(node.getchild(1))
                index = int(node.getchild(1).getvalue())
                self.trans(node.getchild(3))
                value = node.getchild(3).getvalue()
                # update VARIABLE
                arg[index] = value

        # Expression
        elif node.getdata() == '[EXPRESSION]':
            '''expr : expression '+' term
                    | expression '-' term
                    | term
                    | LEN '(' factor ')' '''
            if len(node.getchildren()) == 3:
                self.trans(node.getchild(0))
                arg0 = node.getchild(0).getvalue()
                self.trans(node.getchild(2))
                arg1 = node.getchild(2).getvalue()
                op = node.getchild(1).getdata()
                if op == '+':
                    value = arg0 + arg1
                elif op == '-':
                    value = arg0 - arg1
                node.setvalue(value)

            elif len(node.getchildren()) == 1:  # term
                self.trans(node.getchild(0))
                value = node.getchild(0).getvalue()
                node.setvalue(value)

            elif len(node.getchildren()) == 2:
                self.trans(node.getchild(1))
                value = len(node.getchild(1).getvalue())
                node.setvalue(value)

        # Term
        elif node.getdata() == '[TERM]':
            '''term : term '*' factor
                    | term '/' factor
                    | factor'''
            if len(node.getchildren()) == 3:
                self.trans(node.getchild(0))
                arg0 = node.getchild(0).getvalue()
                self.trans(node.getchild(2))
                arg1 = node.getchild(2).getvalue()
                op = node.getchild(1).getdata()
                if op == '*':
                    value = arg0 + arg1
                elif op == '/':
                    value = arg0 - arg1
                node.setvalue(value)
            elif len(node.getchildren()) == 1:
                self.trans(node.getchild(0))
                value = node.getchild(0).getvalue()
                node.setvalue(value)

        # Factor
        elif node.getdata() == '[FACTOR]':
            '''factor : NUMBER
                      | VARIABLE
                      | VARIABLE '[' expression ']'
                      | '(' expression ')' '''
            if len(node.getchildren()) == 1:
                if ord('0') <= ord(node.getchild(0).getdata()[0]) <= ord('9'):  # NUMBER
                    value = node.getchild(0).getvalue()
                    node.setvalue(value)
                elif node.getchild(0).getdata() == '[EXPRESSION]':              # '(' expr ')'
                    self.trans(node.getchild(0))
                    value = node.getchild(0).getvalue()
                    node.setvalue(value)
                else:                                                           # VARIABLE
                    value = self.v_table[node.getchild(0).getdata()]
                    node.setvalue(value)

            elif len(node.getchildren()) == 2:
                arg = self.v_table[node.getchild(0).getdata()]
                self.trans(node.getchild(1))
                index = int(node.getchild(1).getvalue())
                value = arg[index]
                node.setvalue(value)

        # Print
        elif node.getdata() == '[PRINT]':
            '''print : PRINT '(' VARIABLE ')' '''
            arg0 = self.v_table[node.getchild(0).getdata()]
            print arg0

        # If
        elif node.getdata() == '[IF]':
            r'''if : IF '(' condition ')' '{' statements '}' '''
            children = node.getchildren()
            self.trans(children[0])
            condition = children[0].getvalue()
            if condition:
                for c in children[1:]:
                    value = self.trans(c)
                    if isinstance(value, list) and value[0] == '[RETURN]':
                        return value

        # While
        elif node.getdata() == '[WHILE]':
            r'''while : WHILE '(' conditions ')' '{' statements '}' '''
            children = node.getchildren()
            while self.trans(children[0]):
                for c in children[1:]:
                    self.trans(c)

        # Conditions
        elif node.getdata() == '[CONDITIONS]':
            '''conditions : condition
                          | condition AND condition'''
            if len(node.getchildren()) == 1:
                self.trans(node.getchild(0))
                value = node.getchild(0).getvalue()
                node.setvalue(value)
            elif len(node.getchildren()) == 2:
                self.trans(node.getchild(0))
                arg0 = node.getchild(0).getvalue()
                self.trans(node.getchild(1))
                arg1 = node.getchild(1).getvalue()
                value = arg0 and arg1
                node.setvalue(value)

        # Condition
        elif node.getdata() == '[CONDITION]':
            '''condition : factor '>' factor
                         | factor '<' factor
                         | factor '<' '=' factor
                         | factor '>' '=' factor'''
            self.trans(node.getchild(0))
            arg0 = node.getchild(0).getvalue()
            self.trans(node.getchild(2))
            arg1 = node.getchild(2).getvalue()
            op = node.getchild(1).getdata()
            if op == '>':
                node.setvalue(arg0 > arg1)
            elif op == '<':
                node.setvalue(arg0 < arg1)
            elif op == '<=':
                node.setvalue(arg0 <= arg1)
            elif op == '>=':
                node.setvalue(arg0 >= arg1)

        # Function
        elif node.getdata() == '[FUNCTION]':
            '''function : DEF VARIABLE '(' variables ')' '{' statements '}' '''
            fname = node.getchild(0).getdata()
            self.trans(node.getchild(1))
            vname = node.getchild(1).getvalue()
            f_table[fname] = (vname, node.getchild(2))  # function_name : (variable_names, function)

        # Run_function
        elif node.getdata() == '[RUN_FUNCTION]':
            '''run_function : VARIABLE '(' expressions ')' '''
            fname = node.getchild(0).getdata()
            self.trans(node.getchild(1))
            vname1 = node.getchild(1).getvalue()

            vname0, fnode = f_table[fname]  # function_name : (variable_names, function)

            t = Tran()
            for i in range(len(vname1)):
                t.v_table[vname0[i]] = vname1[i]

            value = t.trans(fnode)
            # (已解决)暂时不能设置为当前节点的值，因为会导致被误认为return接着往上传值
            # 解决方案：只取列表['[BREAK]', return_list]中的return_list作为当前节点值
            if isinstance(value, list):
                node.setvalue(value[1])

            print t.v_table

        # Variables
        elif node.getdata() == '[VARIABLES]':
            '''variables :
                         | VARIABLE
                         | variables ',' VARIABLE'''
            if len(node.getchildren()) == 1:
                if node.getchild(0).getdata() == '[NONE]':  # NONE
                    value = []
                    node.setvalue(value)
                else:                                       # VARIABLE
                    value = [node.getchild(0).getdata()]
                    node.setvalue(value)

            elif len(node.getchildren()) == 2:
                self.trans(node.getchild(0))
                value0 = node.getchild(0).getvalue()
                value = [node.getchild(1).getdata()]
                value.extend(value0)
                node.setvalue(value)

        # Expressions
        elif node.getdata() == '[EXPRESSIONS]':
            '''expressions : expression
                           | expressions ',' expression'''
            if len(node.getchildren()) == 1:
                self.trans(node.getchild(0))
                value = [node.getchild(0).getvalue()]
                node.setvalue(value)
            elif len(node.getchildren()) == 2:
                self.trans(node.getchild(0))
                value0 = node.getchild(0).getvalue()
                self.trans(node.getchild(1))
                value = [node.getchild(1).getvalue()]
                value.extend(value0)
                node.setvalue(value)

        # Return
        elif node.getdata() == '[RETURN]':
            '''return : RETURN variables'''
            return ['[RETURN]', node.getchild(0).getvalue()]

        else:
            for c in node.getchildren():
                value = self.trans(c)
                if isinstance(value, list) and value[0] == '[RETURN]':
                    return value

        return node.getvalue()
