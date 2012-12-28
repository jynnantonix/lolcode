"""
lolcode.py
Author: Chirantan Ekbote

Simple interpreter for the esoteric programming language LOLCODE.
"""

from collections import deque
import sys, getopt, copy

class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms,args))
        self['IT'] = None
        self.outer = outer
    def find(self, var):
        "Find the innermost Env where var appears."
        return self if var in self else self.outer.find(var)

class FoundException(Exception):
    "A custom exception to catch return statements"
    def __init__(self):
        self.value = 'Found return statement outside function.'
    def __str__(self):
        return self.value

#--------------------------------------------------------------------------
# Global State Variables
#--------------------------------------------------------------------------

code = deque([])
global_env = Env()
statement, exp, func = {}, {}, {}
types = { 'TROOF':bool, 'NUMBR':int, 'NUMBAR':float, 'YARN':str }
values = { 'WIN':True, 'FAIL':False, 'NOOB':None }

#--------------------------------------------------------------------------
# Statement Evaluation Functions
#--------------------------------------------------------------------------

def found(env=global_env):
    raise FoundException

def funcDecl(env=global_env):
    #print("funcDecl")
    try:
        if (code[0].popleft() != 'HOW' or code[0].popleft() != 'DUZ' or
            code[0].popleft() != 'I'):
            raise IndexError

        name = code[0].popleft()    # Get the function name

        # Get the params
        params = []
        if len(code[0]) > 0:    # We have params
            if code[0].popleft() != 'YR':
                raise IndexError
            
            params.append(code[0].popleft())
            while len(code[0]) > 0:
                if code[0].popleft() != 'AN' or code[0].popleft() != 'YR':
                    raise IndexError
                params.append(code[0].popleft())

        code.popleft()  # Pop off function declaration

        # Get the body of the function and add the params to the front
        funcbody = deque([])
        funcbody.append(params)
        while not (len(code[0]) == 4 and code[0][0] == 'IF' and
                   code[0][1] == 'U' and code[0][2] == 'SAY' and
                   code[0][3] == 'SO'):
            funcbody.append(code.popleft())

        # Pop off keywords IF U SAY SO
        funcbody.append(code.popleft())

        # Add to the function dict
        func[name] = funcbody       
    except IndexError:
        print("Error: invalid function declaration.")
        sys.exit(1)

def loop(env=global_env):
    #print("loop")
    try:
        if not (code[0].popleft() == 'IM' and code[0].popleft() == 'IN' and
                code[0].popleft() == 'YR'):
            raise IndexError
        
        # Get the loop name
        name = code[0].popleft()

        # Get the loop condition
        if code[0].popleft() != 'WILE':
            raise IndexError       
        cond = code.popleft()

        # Get the body of the loop
        codeloop = deque([])
        while not (len(code[0]) == 4 and code[0][0] == 'IM' and
                   code[0][1] == 'OUTTA' and code[0][2] == 'YR' and
                   code[0][3] == name):
            codeloop.append(code.popleft())

        # Evaluate loop
        code.appendleft(deque(cond))
        while(expression(env)):
            # Add the code for the body of the loop and run it
            code.extendleft(reversed(copy.deepcopy(codeloop)))
            while not (len(code[0]) == 4 and code[0][0] == 'IM' and
                       code[0][1] == 'OUTTA' and code[0][2] == 'YR'
                       and code[0][3] == name):
                codeBlock(env)
                        
            # Put the loop condition expression back in
            code.appendleft(deque(cond))
            
        # Remove end of loop keywords
        code.popleft()
    except IndexError:
        print("Error: invalid loop.")
        sys.exit(1)

def inputBlock(env=global_env):
    #print("inputBlock")
    val = input('LOL>> ')
    try:
        scope = env.find(code[0][1])
    except AttributeError:  # Variable is not defined
        print("Error: invalid GIMMEH statement.")
        sys.exit(1)
    try:
        scope[code[0][1]] = values[val]
    except KeyError:    # Not WIN, FAIL, or NOOB
        try:
            scope[code[0][1]] = int(val)
        except ValueError:  # Not an int
            try:
                scope[code[0][1]] = float(val)
            except ValueError:
                # We have a string
                scope[code[0][1]] = val               
    code.popleft()  # Pop off GIMMEH statement
    
def printBlock(env=global_env):
    #print("printBlock")
    try:
        code[0].popleft()
        out = ''
        while code[0][0] != 'MKAY?':
            out += str(expression(env)).strip('"') + ' '
        print(out)
        code.popleft()
    except (KeyError, IndexError):
        print("Error: invalid VISIBLE statement.")
        sys.exit(1)

def assignment(env=global_env):
    #print("assignment")
    try:
        name = code[0].popleft()        # pop off variable name
        
        if code[0].popleft() != 'R':    # Pop off keyword R
            raise IndexError
        
        env.find(name)[name] = expression(env)
    except AttributeError:  # The variable has not been previously defined
        env[name] = expression(env)
    except IndexError:
        print("Error: invalid assignment.")
        sys.exit(1)
    
def declaration(env=global_env):
    #print("declaration")
    try:       
        if (code[0].popleft() != 'I' or code[0].popleft() != 'HAS' or
            code[0].popleft() != 'A'):
            raise IndexError
        
        name = code[0].popleft()
        if name in env: # Variable has been previously defined in this scope
            raise IndexError

        if len(code[0]) > 0 and code[0].popleft() == 'ITZ':
            env[name] = expression(env)
        else:
            env[name] = None
            code.popleft()
    except IndexError:
        print("Error: Invalid declaration.")
        sys.exit(1)
             
def elseIfBlock(env=global_env, depth=0):
    while code[0][0] != 'MEBBE' and code[0][0] != 'NO' and code[0][0] != 'OIC':
        code.popleft()

    if code[0][0] == 'MEBBE':
        code[0].popleft()
        # Check the MEBBE expression and evaluate if true
        if expression(env) == True:
            while (code[0][0] != 'MEBBE' and code[0][0] != 'NO' and
                   code[0][0] != 'OIC'):
                codeBlock(env)
        else:
            elseIfBlock(env, depth + 1)    # This MEBBE was not true
    elif code[0][0] == 'NO' and code[0][1] == 'WAI':
        code.popleft()
        # Evaluate the NO WAI code block
        while (code[0][0] != 'MEBBE' and code[0][0] != 'NO' and
               code[0][0] != 'OIC'):
            codeBlock(env)

    # Make sure we've reached OIC, end of if block
    while depth == 0 and code[0][0] != 'OIC':
        code.popleft()
    code.popleft()  # Pop off keyword OIC
    
def ifBlock(env=global_env):
    #print("ifblock")
    try:
        if code[0][0] != 'O' or code[0][1] != 'RLY?':
            raise IndexError
        # Pop off keywords and evaluate if block
        code.popleft()
        if env['IT']:    
            # Find the YA RLY keyword
            while 'YA' not in code[0] and 'RLY' not in code[0]:
                code.popleft()

            # Pop off YA RLY
            code.popleft()
        
            # Execute statements
            while (code[0][0] != 'MEBBE' and code[0][0] != 'NO' and
                   code[0][0] != 'OIC'):
                codeBlock(env)

            # Make sure we've reached keyword OIC
            while code[0][0] != 'OIC':
                code.popleft()
                
            # Now pop that off
            code.popleft()
        else:
            elseIfBlock(env)
    except IndexError:
        print("Error: invalid O RLY? block.")
        sys.exit(1)

def comment(env=global_env):
    #print("comment")
    if code[0][0] == 'BTW':
        code.popleft()
    elif code[0][0] == 'OBTW':
        try:
            while code[0][-1] != 'TLDR':    # Last token is not TLDR
                code.popleft()
            code.popleft()                  # Pop off line with TLDR
        except IndexError as err:
            print("Error: unexpected end of file. Expecting keyword TLDR")
            sys.exit(1)

#--------------------------------------------------------------------------
# Binary Operators and Functions
#--------------------------------------------------------------------------

def funcEval(env=global_env):
    #print("functionEval")
    # get the body of the function
    funcbody = copy.deepcopy(func[code[0].popleft()])

    # Get the params and create the environment
    params = funcbody.popleft()
    args = []
    while code[0][0] != 'MKAY?':
        args.append(expression(env))

    # Make sure we have the coorect number of arguments
    if len(args) != len(params):
        print("Error: invalid number of arguments in function call.")
        sys.exit(1)

    code[0].popleft()  # pop off MKAY?
    funcEnv = Env(params, args, env)    # Create the function environment

    # Add the function code and evaluate
    out = None
    code.extendleft(reversed(funcbody))
    try:
        while not (len(code[0]) == 4 and code[0][0] == 'IF' and
                   code[0][1] == 'U' and code[0][2] == 'SAY' and
                   code[0][3] == 'SO'):
            codeBlock(funcEnv)

        # We've reached the end so pop off the last keywords
        code.popleft()    
    except FoundException:
        # We've reached a return statement
        if code[0].popleft() != 'FOUND' or code[0].popleft() != 'YR':
            print('Error: invalid FOUND statement.')
            sys.exit(1)
        out = expression(funcEnv)

        # Now get rid of excess function code
        while not (len(code[0]) == 4 and code[0][0] == 'IF' and
                   code[0][1] == 'U' and code[0][2] == 'SAY' and
                   code[0][3] == 'SO'):
            code.popleft()

        # pop off keywords
        code.popleft()

    # Delete function environment and return output
    del funcEnv
    return out

def getBinArgs(env=global_env):
    # Get first expession
    x = expression(env)

    # Check for separator keyword AN
    if (code[0].popleft() != 'AN'):
        raise IndexError

    # Get second expression
    y = expression(env)
    
    return (x, y)

def both(env=global_env):
    try:
        if (code[0].popleft() != 'BOTH' or code[0].popleft() != 'OF'):
            raise IndexError

        # Get arguments
        x, y = getBinArgs(env)
            
        return bool(x and y)
    except IndexError:
        print("Error: invalid BOTH comparison.")
        sys.exit(1)


def either(env=global_env):
    try:
        if (code[0].popleft() != 'EITHER' or code[0].popleft() != 'OF'):
            raise IndexError

        # Get arguments
        x, y = getBinArgs(env)
            
        return bool(x or y)
    except IndexError:
        print("Error: invalid EITHER comparison.")
        sys.exit(1)


def neg(env=global_env):
    try:
        if code[0].popleft() != 'NOT':
            raise IndexError

        # Get expression value
        x = expression(env)
            
        return not x
    except IndexError:
        print("Error: invalid NOT operation.")
        sys.exit(1)


def allOf(env=global_env):
    try:
        if (code[0].popleft() != 'ALL' or code[0].popleft() != 'OF'):
            raise IndexError

        # Get arguments
        args = []
        while code[0][0] != 'MKAY?':
            args.append(expression(env))
            # See if there are any more arguments
            if code[0][0] == 'AN':
                code[0].popleft()   # Pop it off
        code[0].popleft()   # Pop off MKAY?
        
        return all(args)
    except IndexError:
        print("Error: invalid ALL operation.")
        sys.exit(1)

def anyOf(env=global_env):
    try:
        if (code[0].popleft() != 'ANY' or code[0].popleft() != 'OF'):
            raise IndexError

        # Get arguments
        args = []
        while code[0][0] != 'MKAY?':
            args.append(expression(env))
            # See if there are any more arguments
            if code[0][0] == 'AN':
                code[0].popleft()   # Pop it off
        code[0].popleft()  # pop off MKAY?
            
        return any(args)
    except IndexError:
        print("Error: invalid ANY operation.")
        sys.exit(1)
    
def cast(env=global_env):
    #print("cast")
    try:
        code[0].popleft()       # Pop off keyword MAEK 
        exp = expression(env)
        
        if code[0].popleft() != 'A':
            raise IndexError
        
        return types[code[0].popleft()](exp)       
    except (AttributeError, KeyError, IndexError, TypeError):
        print("Error: invalid cast.")
        sys.exit(1)

#--------------------------------------------------------------------------
# Math Operations and Comparisons
#--------------------------------------------------------------------------

def equals(env=global_env):
    #print('equals')
    try:
        if (code[0].popleft() != 'BOTH' or code[0].popleft() != 'SAEM'):
            raise IndexError

        # Get arguments
        x, y = getBinArgs(env)
   
        return x == y
    except IndexError:
        print("Error: invalid equals comparison.")
        sys.exit(1)

def notEquals(env=global_env):
    try:
        if (code[0].popleft() != 'DIFFRINT'):
            raise IndexError

        # Get arguments
        x, y = getBinArgs(env)
            
        return (x != y)
    except IndexError:
        print("Error: invalid not equals comparison.")
        sys.exit(1)

def greater(env=global_env):
    try:
        if (code[0].popleft() != 'BIGGR' or code[0].popleft() != 'OF'):
            raise IndexError

        # Get arguments
        x, y = getBinArgs(env)
            
        return max(x, y)
    except IndexError:
        print("Error: invalid greater than comparison.")
        sys.exit(1)

def less(env=global_env):
    try:
        if (code[0].popleft() != 'SMALLR' or code[0].popleft() != 'OF'):
            raise IndexError

        # Get arguments
        x, y = getBinArgs(env)
            
        return min(x, y)
    except IndexError:
        print("Error: invalid less than comparison.")
        sys.exit(1)

def add(env=global_env):
    try:
        if (code[0].popleft() != 'SUM' or code[0].popleft() != 'OF'):
            raise IndexError

        # Get arguments
        x, y = getBinArgs(env)
            
        return x + y
    except IndexError:
        print("Error: invalid addition operation.")
        sys.exit(1)

def sub(env=global_env):
    try:
        if (code[0].popleft() != 'DIFF' or code[0].popleft() != 'OF'):
            raise IndexError

        # Get arguments
        x, y = getBinArgs(env)
            
        return x - y
    except IndexError:
        print("Error: invalid subtraction operation.")
        sys.exit(1)

def mul(env=global_env):
    try:
        if (code[0].popleft() != 'PRODUKT' or code[0].popleft() != 'OF'):
            raise IndexError
        
        # Get arguments
        x, y = getBinArgs(env)
            
        return x * y
    except IndexError:
        print("Error: invalid multiplication operation.")
        sys.exit(1)

def div(env=global_env):
    try:
        if (code[0].popleft() != 'QUOSHUNT' or code[0].popleft() != 'OF'):
            raise IndexError

        # Get arguments
        x, y = getBinArgs(env)
            
        return x / y
    except IndexError:
        print("Error: invalid division operation.")
        sys.exit(1)

def mod(env=global_env):
    try:
        if (code[0].popleft() != 'MOD' or code[0].popleft() != 'OF'):
            raise IndexError

        # Get arguments
        x, y = getBinArgs(env)
            
        return x % y
    except IndexError:
        print("Error: invalid modulo operation.")
        sys.exit(1)

def string(env=global_env):
    try:
        if '"' not in code[0][0]:
            raise IndexError
        
        out = code[0].popleft()
        # Test to see if we have a long string
        if out.count('"') < 2:
            while '"' not in code[0][0]:
                out += ' ' + code[0].popleft()
            out += ' '+ code[0].popleft()

        return out.strip('"')
    except IndexError:
        print("Error: invalid YARN.")
        sys.exit(1)

def atom(env=global_env):
    #print("atom")
    try:
        out = values[code[0][0]]
        code[0].popleft()
    except KeyError:
        try:
            out = int(code[0][0])
            code[0].popleft()
        except ValueError:
            try:
                out = float(code[0][0])
                code[0].popleft()
            except ValueError:
                # We have a string
                out = string()
    return out

def bothBranch(env=global_env):
    try:
        if code[0][1] == 'OF':
            return both(env)
        else:
            return equals(env)
    except IndexError:
        print("Error: invalid BOTH expression.")
        sys.exit(1)

#--------------------------------------------------------------------------
# Main Expression Evaluation Function
#--------------------------------------------------------------------------

# Create expression dispatch dictionary
exp = { 'BOTH':bothBranch, 'DIFFRINT':notEquals, 'BIGGR':greater, 'SMALLR':less,
        'SUM':add, 'DIFF':sub, 'PRODUKT':mul, 'QUOSHUNT':div, 'MOD':mod,
        'MAEK':cast, 'EITHER':either, 'ALL':allOf, 'ANY':anyOf, 'NOT':neg }

def expression(env=global_env):
    #print("expression")
    out = None
    try:
        out = exp[code[0][0]](env)
    except KeyError:
        try:
            out = env.find(code[0][0])[code[0][0]]
            #print("variable")
            code[0].popleft()
        except AttributeError:  # code[0][0] is not a variable
            if code[0][0] in func:
                #print('function')
                out = funcEval(env)
            else:
                out = atom(env)

    # If there's nothing left, pop off empty command list
    if len(code[0]) == 0:
        code.popleft()

    return out
            
#--------------------------------------------------------------------------
# Main Program
#--------------------------------------------------------------------------

# Create statement dispatch dictionary
statement = {'IM':loop, 'I':declaration, 'BTW':comment, 'VISIBLE':printBlock, 
             'O':ifBlock, 'OBTW':comment, 'FOUND':found, 'GIMMEH':inputBlock,
             'HOW':funcDecl}            

def codeBlock(env=global_env):
    try:
        statement[code[0][0]](env)
    except KeyError:
        if 'R' in code[0]:  # Maybe it's an assignment
            assignment(env)
        else:               # Must be an expression
            env['IT'] = expression(env)
             
def program():
    try:
        while code[0][0] != 'HAI':
            code.popleft()

        # Now the program starts   
        code.popleft()
        while code[0][0] != 'KTHXBAI':
            codeBlock(global_env)
        sys.exit()
    except IndexError:
        print("Error: unexpected end of file. Expecting keyword KTHXBAI")
        sys.exit(1)
    except Exception as err:
        print("Unexpected error:", err)
        sys.exit(1)

if __name__ == "__main__":
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'f:')
    except getopt.GetoptError:
        print(err)
        sys.exit(1)

    file = None
    for option, value in optlist:
        if option == '-f':
            file = open(value, 'r')

    for line in file:
        if len(line) > 1: #There is more than just a newline character          
            softbreaks = line.split(',')
            for token in softbreaks:
                code.append(deque(token.split()))

    program()
