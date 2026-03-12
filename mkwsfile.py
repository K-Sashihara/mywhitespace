message = "Hello, World!\n"

def to_binary(n):
    if n == 0:
        return "\n"
    sign = " " if n >= 0 else "\t"
    binary = ""
    n = abs(n)
    while n > 0:
        binary = (" " if n % 2 == 0 else "\t") + binary
        n //= 2
    return sign + binary + "\n"

def push(n):
    return "  " + to_binary(n)

def output_char():
    return "\t\n  "

def output_number():
    return "\t\n \t"

def end_program():
    return "\n\n\n"

code = ""
for char in message:
    code += push(ord(char))
    code += output_char()

code += end_program()

with open("helloworld.ws", "w") as f:
    f.write(code)