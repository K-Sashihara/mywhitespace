class VM:
    def __init__(self, instructions):
        self.instructions = instructions
        self.stack = []
        self.heap = {}
        self.call_stack = []
        self.labels = {}
        self.pc = 0
        self.flag = False
        self.trace = []
        self.error = ""
        self.run()
        
    def parse_label(self):
        for i, instr in enumerate(self.instructions):
            if instr["type"] == "flow" and instr["operation"] == "mark":
                self.labels[instr["label"]] = i

    def stack_manipulation(self, instr):
        operation = instr["operation"]
        if operation == "duplicate":
            self.stack.append(self.stack[-1])
        elif operation == "swap":
            self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
        elif operation == "discard":
            self.stack.pop()
        elif operation == "push":
            self.stack.append(instr["value"])
        elif operation == "copy":
            self.stack.append(self.stack[-1 - instr["value"]])
        elif operation == "slide":
            value = instr["value"]
            top = self.stack[-1]
            del self.stack[-value:]
            self.stack.append(top)
        
        self.pc += 1

    def heap_access(self, instr): 
        operation = instr["operation"]
        if operation == "store":
            value = self.stack.pop()
            address = self.stack.pop()
            self.heap[address] = value
        elif operation == "retrieve":
            address = self.stack.pop()
            value = self.heap.get(address)
            if value is None:
                self.error = f"Heap address {address} not found"
                raise
            self.stack.append(value)
        
        self.pc += 1

    def I_O(self, instr):
        operation = instr["operation"]
        if operation == "output_char":
            value = self.stack.pop()
            print(chr(value), end="")
        elif operation == "output_number":
            value = self.stack.pop()
            print(value, end="")
        elif operation == "input_char":
            value = input()
            if value:
                self.heap[self.stack.pop()] = ord(value)  # store the ASCII value of the first character
        elif operation == "input_number":
            value = int(input())
            self.heap[self.stack.pop()] = value
        
        self.pc += 1

    def arithmetic(self, instr):
        operation = instr["operation"]
        b = self.stack.pop()
        a = self.stack.pop()
        if operation == "add":
            self.stack.append(a + b)
        elif operation == "subtract":
            self.stack.append(a - b)
        elif operation == "multiply":
            self.stack.append(a * b)
        elif operation == "divide":
            if b == 0:
                print("Division by zero")
                raise
            self.stack.append(a // b)  # integer division
        elif operation == "modulo":
            if b == 0:
                print("Modulo by zero")
                raise
            self.stack.append(a % b)
        
        self.pc += 1

    def flow_control(self, instr):
        operation = instr["operation"]
        if operation == "mark":
            self.labels[instr["label"]] = self.pc
            self.pc += 1
        elif operation == "call":
            self.call_stack.append(self.pc+1)
            self.pc = self.labels.get(instr["label"])
            if self.pc is None:
                self.error = f"Label {instr['label']} not found"
        elif operation == "jump":
            self.pc = self.labels.get(instr["label"])
            if self.pc is None:
                self.error = f"Label {instr['label']} not found"
                raise
        elif operation == "jump_if_zero":
            value = self.stack.pop()
            if value == 0:
                self.pc = self.labels.get(instr["label"])
                if self.pc is None:
                    self.error = f"Label {instr['label']} not found"
                    raise
            else:
                self.pc += 1
        elif operation == "jump_if_negative":
            value = self.stack.pop()
            if value < 0:
                self.pc = self.labels.get(instr["label"])
                if self.pc is None:
                    self.error = f"Label {instr['label']} not found"
                    raise
            else:
                self.pc += 1
        elif operation == "end_subroutine":
            if not self.call_stack:
                print("Call stack is empty, cannot return")
                raise
            self.pc = self.call_stack.pop()
        elif operation == "end_program":
            self.flag = True

    def show_history(self):
        for i, pc in enumerate(self.trace):
            instr = self.instructions[pc["pc"]]
            print(f"{i}: PC={pc['pc']} INSTR={instr} STACK={pc['stack']} HEAP={pc['heap']}")
        
    def run(self):
        try:
            self.parse_label()  # Pre-parse labels for quick access
            while self.pc < len(self.instructions):
                if self.flag:
                    break
                instr = self.instructions[self.pc]
                if instr["type"] == "stack":
                    self.stack_manipulation(instr)
                elif instr["type"] == "heap":
                    self.heap_access(instr)
                elif instr["type"] == "io":
                    self.I_O(instr)
                elif instr["type"] == "arithmetic":
                    self.arithmetic(instr)
                elif instr["type"] == "flow":
                    self.flow_control(instr)

                self.trace.append({"pc": self.pc, "stack": self.stack.copy(), "heap": self.heap.copy()})

        except Exception as e:
            self.show_history()
            print(f"Error: {self.error}")
            print(self.labels)
