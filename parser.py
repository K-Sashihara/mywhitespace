class Parser:
    def __init__(self, text):
        self.source = "".join([c for c in text if c in " \t\n"])
        self.pos = 0
        self.instructions = []
        self.parse()

    def read_number(self):
        """
        The first character is the sign, then the rest is the binary representation of the number.

        [Space] -> positive
        [Tab] -> negative

        [Space] -> 0
        [Tab] -> 1
        """
        sign = 1 if self.source[self.pos] == " " else -1
        self.pos += 1
        num = ""
        while self.source[self.pos] != "\n":
            num += "0" if self.source[self.pos] == " " else "1"
            self.pos += 1

        self.pos += 1  # skip the newline because it is the end of the number
        return int(num, 2) * sign if num else 0
    
    def read_label(self):
        label = ""
        while self.source[self.pos] != "\n":
            label += "0" if self.source[self.pos] == " " else "1"
            self.pos += 1

        self.pos += 1  # skip the newline because it is the end of the label
        return label
    
    def stack_manipulation(self):
        if self.source[self.pos] == " ":
            self.pos += 1
            self.instructions.append({"type": "stack", "operation": "push", "value": self.read_number()}) # pos is already updated in read_number
        elif self.source[self.pos] == "\n":
            self.pos += 1
            if self.source[self.pos] == " ":
                self.instructions.append({"type": "stack", "operation": "duplicate"})
            elif self.source[self.pos] == "\t":
                self.instructions.append({"type": "stack", "operation": "swap"})
            elif self.source[self.pos] == "\n":
                self.instructions.append({"type": "stack", "operation": "discard"})
            self.pos += 1
        elif self.source[self.pos] == "\t":
            self.pos += 1
            if self.source[self.pos] == " ":
                self.pos += 1
                self.instructions.append({"type": "stack", "operation": "copy", "value": self.read_number()})
            elif self.source[self.pos] == "\n":
                self.pos += 1
                self.instructions.append({"type": "stack", "operation": "slide", "value": self.read_number()})
            else:
                raise Exception(f"Invalid stack manipulation instruction at position {self.pos}")

    def I_O(self):
        if self.source[self.pos] == " ":
            self.pos += 1
            if self.source[self.pos] == " ":
                self.instructions.append({"type": "io", "operation": "output_char"})
            elif self.source[self.pos] == "\t":
                self.instructions.append({"type": "io", "operation": "output_number"})
            self.pos += 1
        elif self.source[self.pos] == "\t":
            self.pos += 1
            if self.source[self.pos] == " ":
                self.instructions.append({"type": "io", "operation": "input_char"})
            elif self.source[self.pos] == "\t":
                self.instructions.append({"type": "io", "operation": "input_number"})
            self.pos += 1
        else:
            raise Exception(f"Invalid I/O instruction at position {self.pos}")
        

    def heap_access(self):
        if self.source[self.pos] == " ":
            self.instructions.append({"type": "heap", "operation": "store"})
        elif self.source[self.pos] == "\t":
            self.instructions.append({"type": "heap", "operation": "retrieve"})
        else:
            raise Exception(f"Invalid heap access instruction at position {self.pos}")
        self.pos += 1

    def arithmetic(self):
        if self.source[self.pos] == " ":
            self.pos += 1
            if self.source[self.pos] == " ":
                self.instructions.append({"type": "arithmetic", "operation": "add"})
            elif self.source[self.pos] == "\t":
                self.instructions.append({"type": "arithmetic", "operation": "subtract"})
            elif self.source[self.pos] == "\n":
                self.instructions.append({"type": "arithmetic", "operation": "multiply"})
        elif self.source[self.pos] == "\t":
            self.pos += 1
            if self.source[self.pos] == " ":
                self.instructions.append({"type": "arithmetic", "operation": "divide"})
            elif self.source[self.pos] == "\t":
                self.instructions.append({"type": "arithmetic", "operation": "modulo"})
        else:
            raise Exception(f"Invalid arithmetic instruction at position {self.pos}")
        self.pos += 1

    def flow_control(self):
        if self.source[self.pos] == " ":
            self.pos += 1
            if self.source[self.pos] == " ":
                self.pos += 1
                self.instructions.append({"type": "flow", "operation": "mark", "label": self.read_label()})
            elif self.source[self.pos] == "\t":
                self.pos += 1
                self.instructions.append({"type": "flow", "operation": "call", "label": self.read_label()})
            elif self.source[self.pos] == "\n":
                self.pos += 1
                self.instructions.append({"type": "flow", "operation": "jump", "label": self.read_label()})
        elif self.source[self.pos] == "\t":
            self.pos += 1
            if self.source[self.pos] == " ":
                self.pos += 1
                self.instructions.append({"type": "flow", "operation": "jump_if_zero", "label": self.read_label()})
            elif self.source[self.pos] == "\t":
                self.pos += 1
                self.instructions.append({"type": "flow", "operation": "jump_if_negative", "label": self.read_label()})
            elif self.source[self.pos] == "\n":
                self.instructions.append({"type": "flow", "operation": "end_subroutine"})
                self.pos += 1
        elif self.source[self.pos] == "\n":
            self.pos += 1
            if self.source[self.pos] == "\n":
                self.instructions.append({"type": "flow", "operation": "end_program"})
                self.pos += 1
            else:
                raise Exception(f"Invalid flow control instruction at position {self.pos}")

    def parse(self):
        """
        IMP:
        [Space] -> stack manupulation
        [Tab][LF] -> I/O
        [Tab][Tab] -> heap access
        [Tab][Space] -> arithmetic
        [LF] -> flow control

        detect the IMP first, then the operation, then the value if needed.
        """
        instructions_for_debug = []
        try:
            while self.pos < len(self.source):
                c = self.source[self.pos]
                if c == " ":
                    self.pos += 1
                    self.stack_manipulation()
                elif c == "\t":
                    self.pos += 1
                    if self.source[self.pos] == "\n":
                        self.pos += 1
                        self.I_O()
                    elif self.source[self.pos] == "\t":
                        self.pos += 1
                        self.heap_access()
                    elif self.source[self.pos] == " ":
                        self.pos += 1
                        self.arithmetic()
                elif c == "\n":
                    self.pos += 1
                    self.flow_control()
                
                instructions_for_debug.append([self.instructions[-1], self.pos])

        except Exception as e:
            for i, (instr, pos) in enumerate(instructions_for_debug):
                print(f"{i}: {instr} pos: {pos}")
            raise 
