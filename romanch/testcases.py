import os
import random

def solve(n, d, a):
    """
    Solution logic provided by user.
    Greedy with a single skip allowance for odd N.
    """
    a.sort()
    
    if n % 2 == 0:
        for i in range(1, n, 2):
            if a[i] - a[i-1] > d:
                return "NO"
        return "YES"
    else:
        flag = True # Have we used our "skip" yet?
        i = 1
        while i < n:
            if a[i] - a[i-1] > d:
                if flag:
                    flag = False
                    i += 1 # Skip current element, try next pair
                else:
                    return "NO"
            else:
                i += 2 # Valid pair, move to next
        return "YES"

def generate_test_cases():
    base_dir = "romanch_test_cases"
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    NUM_FILES = 100
    SUM_N_PER_FILE = 80_000
    MAX_VAL = 1_000_000_000

    print(f"🚀 Generating {NUM_FILES} test files (under 85MB) for Romanch...")

    for i in range(NUM_FILES):
        input_path = os.path.join(input_dir, f"input{i:02d}.txt")
        output_path = os.path.join(output_dir, f"output{i:02d}.txt")
        
        test_cases_in = []
        current_n_sum = 0
        
        # --- Strategy ---
        
        # File 00: Manual Tricky Cases
        if i == 0:
            test_cases_in.append((5, 1, [1, 2, 5, 8, 9])) # YES
            test_cases_in.append((4, 2, [1, 11, 10, 2])) # YES
            test_cases_in.append((3, 5, [1, 10, 100]))   # NO
            test_cases_in.append((4, 5, [1, 2, 3, 10]))  # NO
            test_cases_in.append((5, 1, [1, 3, 5, 6, 9])) # NO
            test_cases_in.append((7, 1, [1, 4, 5, 6, 7, 8, 9])) # YES
            test_cases_in.append((7, 1, [1, 3, 4, 6, 7, 9, 11])) # NO
            test_cases_in.append((4, 1000000000, [1, 2, 3, 1000000002])) # YES (1-2 ok, 3-10..02 ok) wait.. 
            # 1, 2, 3, 10...02.
            # (1,2) diff 1 <= d. OK.
            # (3, 10...02) diff 999999999 <= d. OK.
            # So YES is correct.
            
        # File 01: d=0 cases
        elif i == 1:
            test_cases_in.append((4, 0, [1, 1, 2, 2]))      # YES
            test_cases_in.append((5, 0, [1, 1, 2, 2, 100])) # YES
            test_cases_in.append((4, 0, [1, 1, 1, 2]))      # NO
            
        # File 02: n=1
        elif i == 2:
            test_cases_in.append((1, 0, [100]))
            
        elif i < 10:
            # Small randoms
            while current_n_sum < 5000:
                n = random.randint(2, 20)
                d = random.randint(0, 100)
                a = [random.randint(1, 1000) for _ in range(n)]
                test_cases_in.append((n, d, a))
                current_n_sum += n
                
        # File 10-19: ABSOLUTE MAX CONSTRAINTS (TLE check for O(n^2))
        # 10 files with one big test case N=100,000
        elif i < 20:
            T = 1
            n = 100_000 # Max constraint
            d = random.randint(1, 10000)
            a = [random.randint(1, MAX_VAL) for _ in range(n)]
            test_cases_in.append((n, d, a))
            
        # File 20-99: High T, Small N (Random stress)
        else:
            while current_n_sum < SUM_N_PER_FILE - 100:
                n = random.randint(1, 100)
                d = random.randint(0, 10000)
                a = [random.randint(1, MAX_VAL) for _ in range(n)]
                test_cases_in.append((n, d, a))
                current_n_sum += n

        # --- Write files ---
        with open(input_path, 'w') as f_in, open(output_path, 'w') as f_out:
            f_in.write(f"{len(test_cases_in)}\n") # Write T
            
            for (n, d, a) in test_cases_in:
                f_in.write(f"{n} {d}\n")
                f_in.write(" ".join(map(str, a)) + "\n")
                
                # Solve using your logic
                answer = solve(n, d, list(a))
                f_out.write(f"{answer}\n")
                
    print(f"✅ Generated {NUM_FILES} files in '{base_dir}/'.")
    print("⚠️  Total zip size should be ~70MB (Safe).")
    print("\n--- HOW TO ZIP ---")
    print("1. Go *inside* the 'romanch_test_cases' folder.")
    print("2. Select both 'input' and 'output' folders.")
    print("3. Right-click and compress them into a new zip file.")
    print("4. Upload that new zip file.")

if __name__ == "__main__":
    generate_test_cases()