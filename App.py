
from flask import Flask, request, render_template
import ply.lex as lex

# Token definitions
tokens = (
    'IDENTIFIER', 'NUMBER', 'PLUS', 'EQUALS',
    'PRINT', 'READ', 'INT', 'END', 'STRING', 'COMMA', 'SEMICOLON'
)

# Reserved keywords
reserved = {
    'printf': 'PRINT',
    'read': 'READ',
    'int': 'INT',
    'end': 'END',
}

# Tokens that should appear in PR column
pr_tokens = ['PRINT', 'READ', 'INT', 'END']

t_PLUS = r'\+'
t_EQUALS = r'='
t_COMMA = r','
t_SEMICOLON = r';'
t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code']
        lexer.input(code)
        tokens_data = []
        for tok in lexer:
            token_info = {
                'token': tok.value,
                'pr': 'X' if tok.type in pr_tokens else '',
                'id': 'X' if tok.type == 'IDENTIFIER' else '',
                'cad': 'X' if tok.type == 'STRING' else '',
                'num': 'X' if tok.type == 'NUMBER' else '',
                'si': 'X' if tok.type in ['COMMA', 'SEMICOLON', 'PLUS', 'EQUALS'] else '',
                'tipo': tok.type
            }
            tokens_data.append(token_info)
        return render_template('index.html', tokens=tokens_data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
