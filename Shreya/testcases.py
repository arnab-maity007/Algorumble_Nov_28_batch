import os
import random

def solve(n):
    """
    CORRECT O(1) Logic:
    - If n is ODD, the game ends on turn n+1 (even number). Even turns are Kosuke.
      -> Kosuke Wins.
    - If n is EVEN, the game ends on turn n+1 (odd number). Odd turns are Shreya.
      -> Shreya Wins.
    """
    if n % 2 == 1:
        return "Kosuke"
    else:
        return "Shreya"

def generate_test_cases():
    base_dir = "shreya_test_cases"
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    NUM_FILES = 100
    MAX_VAL = 10**18
    
    print(f"🚀 Generating {NUM_FILES} CORRECT test files for Shreya...")

    for i in range(NUM_FILES):
        input_path = os.path.join(input_dir, f"input{i:02d}.txt")
        output_path = os.path.join(output_dir, f"output{i:02d}.txt")
        
        n = 0
        if i == 0: n = 1 
        elif i == 1: n = 6
        elif i == 2: n = 3
        elif i == 3: n = 98
        elif i == 4: n = 2
        elif i == 5: n = MAX_VAL
        elif i == 6: n = MAX_VAL - 1
        elif i == 7: n = 10
        elif i == 8: n = 11
        elif i == 9: n = 100
        elif i < 20: n = random.randint(10**17, MAX_VAL)
        else:
            if i < 50: n = random.randint(100, 100000)
            else: n = random.randint(100000, 10**15)

        with open(input_path, 'w') as f_in:
            f_in.write(f"{n}\n")
            
        with open(output_path, 'w') as f_out:
            f_out.write(f"{solve(n)}\n")
                
    print(f"✅ Generated {NUM_FILES} files.")
    print("1. Open 'shreya_test_cases'.")
    print("2. Select 'input' and 'output'.")
    print("3. Zip them.")

if __name__ == "__main__":
    generate_test_cases()