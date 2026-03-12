from parser import Parser
from vm import VM
import sys

if __name__ == "__main__":    
    # 引数があるかチェック
    if len(sys.argv) < 2:
        print("Usage: python wspace.py [filename]")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        # ファイルを開いて中身を読み込む
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
        
        parser = Parser(text)
        vm = VM(parser.instructions)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
