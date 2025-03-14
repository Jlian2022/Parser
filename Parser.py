import ASTNodeDefs as AST
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]
        self.tokens = []
    













    
     # Move to the next position in the code.
    def advance(self):
        # TODO: Students need to complete the logic to advance the position.
        self.position += 1
        if self.position < len(self.code):
            self.current_char = self.code[self.position]
        else:
            self.current_char = None












    # Skip whitespaces.
    def skip_whitespace(self):
        # TODO: Complete logic to skip whitespaces.
        if self.current_char.isspace() == True:
            self.advance()
        else:
            self.current_char = None













    # Tokenize an identifier.
    def identifier(self):
        result = ''
        if self.current_char.isalpha() or self.current_char == "_":
            result += self.current_char
            while (True):
                self.advance()

                if self.current_char.isalpha() or self.current_char.isnumeric() or self.current_char == "_":
                    result += self.current_char

                else:
                    break
        
        return ('IDENTIFIER', result)
    














    

    def number(self):
        # TODO: Implement logic to tokenize numbers.
        result = ""
        while True:
            if self.current_char.isdigit() or self.current_char == '.':
                result += self.current_char
                self.advance()
            else:
                break
        if "." in result:
            return ('FNUMBER', float(result))
        
        return ('NUMBER', int(result))

















    


    #use by token from project 1 added minus and the bracket and the float
    def token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isalpha():
                ident = self.identifier()
                if ident[1] == 'if':
                    return ('IF', 'if')
                elif ident[1] == 'else':
                    return ('ELSE', 'else')
                elif ident[1] == 'while':
                    return ('WHILE', 'while')
                elif ident[1] == 'int':
                     return ('INT', 'int')
                elif ident[1] == 'float':
                     return ('FLOAT', 'float')
                return ident
            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()

            if self.current_char == "+":
                store_character = self.current_char
                self.advance()
                return ('PLUS', store_character)

            if self.current_char == "-":
                store_character = self.current_char
                self.advance()
                return ('MINUS', store_character)

            if self.current_char == "*":
                store_character = self.current_char
                self.advance()
                return ('MULTIPLY', store_character)

            if self.current_char == "/":
                store_character = self.current_char
                self.advance()
                return ('DIVIDE', store_character)

            if self.current_char == "(":
                store_character = self.current_char
                self.advance()
                return ('LPAREN', store_character)

            if self.current_char == ")":
                store_character = self.current_char
                self.advance()
                return ('RPAREN', store_character)

            # if self.current_char == ")":
            #     store_character = self.current_char
            #     self.advance()
            #     return ('RPAREN', store_character)

            # if self.current_char =="==":
            #     store_character = self.current_char
            #     self.advance()
            #     return ('EQ ',store_character)

            # if self.current_char =="=":
            #     store_character = self.current_char
            #     self.advance()
            #     return ('EQUALS ',store_character)

            if self.current_char == "=":
                store_character = self.current_char
                self.advance()
                if self.current_char == "=":
                    store_character += self.current_char
                    self.advance()
                    return ('EQ', store_character)

                return ('EQUALS', store_character)

            # if self.current_char =="!=":
            #     store_character = self.current_char
            #     self.advance()
            #     return ('NEQ ',store_character)

            if self.current_char == "!":
                store_character = self.current_char
                self.advance()
                if self.current_char == "=":
                    store_character += self.current_char
                    self.advance()
                return ('NEQ', store_character)

            if self.current_char == "<":
                store_character = self.current_char
                self.advance()
                return ('LESS', store_character)

            if self.current_char == ">":
                store_character = self.current_char
                self.advance()
                return ('GREATER', store_character)

            if self.current_char == ",":
                store_character = self.current_char
                self.advance()
                return ('COMMA', store_character)

            if self.current_char == ":":
                store_character = self.current_char
                self.advance()
                return ('COLON', store_character)

            if self.current_char == None:
                store_character = self.current_char
                self.advance()
                return ('EOF', store_character)

            if self.current_char.isdigit():
                return (self.current_char.number())

            if self.current_char.isalpha() or self.current_char == "_":
                return (self.current_char.identifier())

            if self.current_char == '{':
                 store_character = self.current_char
                 self.advance()
                 return ('LBRACE', store_character)
            if self.current_char == '}':
                store_character = self.current_char
                self.advance()
                return ('RBRACE', store_character)
            # TODO: Add logic for operators and punctuation tokens.

            raise ValueError(f"Illegal character at position {self.position}: {self.current_char}")

        return ('EOF', None)















    def tokenize(self): #use instructor code something is wrong with my code and I am not sure what it is so I plug Dr.Suma saha code in and it work and yea
        while True:
            token = self.token()
            self.tokens.append(token)
            if token[0] == 'EOF':
                break
        return self.tokens



















class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens.pop(0)
        # Use these to track the variables and their scope
        self.symbol_table = {'global': {}}
        self.scope_counter = 0
        self.scope_stack = ['global']
        self.messages = []









    def error(self, message):
        self.messages.append(message)











    
    def advance(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)











    
    def enter_scope(self):
        new_scope = f"scope{self.scope_counter}" #make a new scope using the counter
        self.symbol_table[new_scope] = {} #add it to symbol table 
        self.scope_stack.append(new_scope) #update the scope stack
        self.scope_counter += 1 #increase counter
        










    
    def exit_scope(self):
        self.scope_stack.pop()

    










    def current_scope(self):
        return self.scope_stack[-1]











   
    def checkVarDeclared(self, identifier):
        if identifier not in self.symbol_table[self.current_scope()]:#this just check to see if the identifyer is in the current scope if it is not it wil return nothing else just the error message
            return None
        else:
            self.error(f"Variable {identifier} has already been declared in the current scope")











    def checkVarUse(self, identifier):
        temp_stack = self.scope_stack
        new_temp_stack = list(reversed(temp_stack))

        for variable in new_temp_stack:
            if identifier in self.symbol_table[variable]:
                return None
                
            
        self.error(f"Variable {identifier} has not been declared in the current or any enclosing scopes")













    def checkTypeMatch2(self, vType, eType, var, exp):

        if vType == eType: #same do nothing
            return None
        
        elif vType is None or eType is None:  #none do nothing
            return None
        
        elif vType != eType: #different log error
            self.error(f"Type Mismatch between {vType} and {eType}")



















    def add_variable(self, name, var_type):
        
        current_scope = self.current_scope()
        self.symbol_table[current_scope][name] = var_type
















    def get_variable_type(self, name):
        whatever_variable = list(reversed(self.scope_stack))
        for variable in whatever_variable:
            if name in self.symbol_table[variable]:
                return self.symbol_table[variable][name]
        return None













    
    def parse(self):
        return self.program()
















    def program(self):
        statements = []
        while True:
            if self.current_token[0] == 'EOF':
                break  # Exit the loop if EOF is encountered
            else:

        
                stmt = self.statement()
                statements.append(stmt)
        return statements


 













    def statement(self):  
        if self.current_token[0] == 'IDENTIFIER':
            if self.peek() == 'EQUALS':  
                return self.assign_stmt() 
            elif self.peek() == 'LPAREN':  
                return self.function_call()  
            else:
                raise ValueError(f"Unexpected token after identifier: {self.current_token}")
        elif self.current_token[0] == 'IF':
            return self.if_stmt()  
        elif self.current_token[0] == 'WHILE':
            return self.while_stmt()  
        elif self.current_token[0] in 'INT':
            var_type = self.current_token[1]
            self.advance()
            var_name = self.current_token[1]
            self.advance()

            self.checkVarDeclared(var_name)
            self.expect('EQUALS')
            expression = self.expression()

            self.checkTypeMatch2(var_type, expression.value_type, var_name, expression)
            self.add_variable(var_name, var_type)
            return AST.Declaration(var_type, var_name, expression)

        elif self.current_token[0] in 'FLOAT':
            var_type = self.current_token[1]
            self.advance()
            var_name = self.current_token[1]
            self.advance()

            self.checkVarDeclared(var_name)
            self.expect('EQUALS')
            expression = self.expression()

            self.checkTypeMatch2(var_type, expression.value_type, var_name, expression)
            self.add_variable(var_name, var_type)
            return AST.Declaration(var_type, var_name, expression)
        else:
            raise ValueError(f"Unexpected token: {self.current_token}")












    def decl_stmt(self):
        """
        Parses a declaration statement.
        Example:
        int x = 5
        float y = 3.5
        TODO: Implement logic to parse type, identifier, and initialization expression and also handle type checking
        """
        pass
        











    def assign_stmt(self):
        """
        Parses an assignment statement.
        Example:
        x = 10
        x = y + 5
        TODO: Implement logic to handle assignment, including type checking.
        """

        identifier = self.current_token[1]
        self.advance()

        self.checkVarUse(identifier)
        
        if self.current_token[0] == 'EQUALS':
            self.advance()
        else:
            raise ValueError(f"Expected token {'EQUALS'}, but got {self.current_token[0]}")
   
        expression = self.expression()


        vtype = self.get_variable_type(identifier)
        evtype = expression.value_type

        
        if vtype is None or evtype is None:
            return None
        
        if vtype != evtype: #different log error
            self.error(f"Type Mismatch between {vtype} and {evtype}")


        return AST.Assignment(identifier, expression)
    

















    def if_stmt(self):
        """
        Parses an if-statement, with an optional else block.
        Example:
        if condition {
            # statements
        }
        else {
            # statements
        }
        TODO: Implement the logic to parse the if condition and blocks of code.
        """
        if self.current_token[0] == "IF":
            self.advance()
            condition = self.boolean_expression()
            if self.current_token[0] == 'LBRACE':
                self.advance()
            else:
                raise ValueError(f"Expected token {'LBRACE'}, but got {self.current_token[0]}")
            
            self.enter_scope()
            then_block = self.block()
            else_block = None
            self.exit_scope()
            else_block = None
            if self.current_token[0] == 'ELSE':
                self.advance()
                
                if self.current_token[0] == 'LBRACE':
                    self.advance()
                else:
                    raise ValueError(f"Expected token {'LBRACE'}, but got {self.current_token[0]}")

                
                self.enter_scope()
                else_block = self.block()
                self.exit_scope()
            
        return AST.IfStatement(condition, then_block, else_block)

   



















    def while_stmt(self):
        """
        Parses a while-statement.
        Example:
        while condition {
            # statements
        }
        TODO: Implement the logic to parse while loops with a condition and a block of statements.
        """
        if self.current_token[0] == "WHILE":
            self.advance()
            condition = self.boolean_expression()
            if self.current_token[0] == 'LBRACE':
                    self.advance()
            else:
                raise ValueError(f"Expected token {'LBRACE'}, but got {self.current_token[0]}")
            self.enter_scope()
            block = self.block()
            self.exit_scope()
            
        return AST.WhileStatement(condition, block)













 
    def block(self):
        """
        Parses a block of statements. A block is a collection of statements grouped by `{}`.
        Example:
        
        x = 5
        y = 10
        
        TODO: Implement logic to capture multiple statements as part of a block.
        """
        statements = []
        while True:
            if self.current_token[0] == 'EOF' or  self.current_token[0] == 'RBRACE':
                break
            elif self.current_token[0] != 'EOF' or  self.current_token[0] != 'RBRACE':
                statements.append(self.statement())
        
        if self.current_token[0] == 'RBRACE':
            self.advance()
        else:
            raise ValueError(f"Expected token {'RBRACE'}, but got {self.current_token[0]}")
        return AST.Block(statements)
    

















    def expression(self):
        """
        Parses an expression. Handles operators like +, -, etc.
        Example:
        x + y - 5
        TODO: Implement logic to parse binary operations (e.g., addition, subtraction) with correct precedence and type checking.
        """

        left = self.term()  # Parse the first term
        while self.current_token[0] in ['PLUS', 'MINUS']:  # Handle + and -
            op = self.current_token  # Capture the operator
            self.advance()  # Skip the operator
            right = self.term()  # Parse the next term
            self.checkTypeMatch2(left.value_type, right.value_type, left, right)
            
            left = AST.BinaryOperation(left, op, right)
        return left

 















 
    def boolean_expression(self):
        """
        Parses a boolean expression. These are comparisons like ==, !=, <, >.
        Example:
        x == 5
        TODO: Implement parsing for boolean expressions and check for type compatibility.
        """
    
        
        left = self.term()
        while self.current_token[0] in ['EQ', 'NEQ', 'GREATER', 'LESS']:
            operator = self.current_token
            self.advance()
            right = self.term()
            self.checkTypeMatch2(left.value_type, right.value_type, left, right)
            left = AST.BooleanExpression(left, operator, right)
        return left
















    def term(self):
        """
        Parses a term. A term consists of factors combined by * or /.
        Example:
        x * y / z
        TODO: Implement parsing for multiplication and division and check for type compatibility.
        """
        left = self.factor()
        while self.current_token[0] in ['MULTIPLY', 'DIVIDE']:
            operator = self.current_token
            self.advance()
            right = self.factor()
            self.checkTypeMatch2(left.value_type, right.value_type, left, right)
            lt=left.value_type
            left = AST.BinaryOperation(left, operator, right,lt)
        return left
    
















    def factor(self):
        if self.current_token[0] == 'NUMBER':
            number = self.current_token
            self.advance()
            return AST.Factor(number, 'int')
        elif self.current_token[0] == 'FNUMBER':
            number = self.current_token
            self.advance()
            return AST.Factor(number, 'float')
        elif self.current_token[0] == 'IDENTIFIER':
            identifier = self.current_token[1]
            
            var_type = self.get_variable_type(identifier)
            self.checkVarUse(identifier)
            self.advance()
            
            return AST.Factor(identifier, var_type)
        elif self.current_token[0] == 'LPAREN':
            self.advance()
            expr = self.expression()
            if self.current_token[0] == 'RPAREN':
                self.advance()
            else:
                raise ValueError(f"Expected token {'RPAREN'}, but got {self.current_token[0]}")
            return expr
        else:
            raise ValueError(f"Unexpected token in factor: {self.current_token}")
        



















    def function_call(self):
        function_name =  self.current_token
        arguments = []
        self.advance()
        if self.current_token[0] == "LPAREN":
            self.advance()
            arguments.append(self.current_token)
            self.advance()
            while self.current_token[0]!='RPAREN':
                           
                if self.current_token[0] == 'COMMA':
                    self.advance()
                else:
                    arguments.append(self.current_token)
                    self.advance()
            self.advance()
        
        return AST.FunctionCall(function_name, arguments)
    
















    def arg_list(self):
        """
        Parses a list of function arguments.
        Example:
        (x, y + 5)
        """
        args = []
        
        args.append(self.current_token)
        if self.current_token != "RPAREN":
            while self.current_token[0] == "COMMA":
                self.advance()
                args.append(self.current_token)
        return args














    def expect(self, token_type):
        if self.current_token[0] == token_type:
            self.advance()
        else:
            raise ValueError(f"Expected token {token_type}, but got {self.current_token[0]}")

    def peek(self):
        return self.tokens[0][0] if self.tokens else None