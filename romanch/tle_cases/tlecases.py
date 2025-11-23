import os
import random

# --- YOUR SOLUTION LOGIC (Do not change this to ensure outputs match your logic) ---
def solve(n, d, a):
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

# --- TEST CASE GENERATOR ---
def generate_max_constraints_cases():
    base_dir = "romanch_max_constraints"
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    
    # Create directories
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    print(f"🚀 Generating 5 MAXIMUM constraint test files in '{base_dir}'...")
    print(f"ℹ️  Each file will have Sum of N = 100,000 to check for TLE.")

    MAX_VAL = 1_000_000_000 # 10^9
    MAX_N_SUM = 100_000     # 10^5

    # We will generate exactly 5 files
    for file_idx in range(5):
        input_path = os.path.join(input_dir, f"input{file_idx:02d}.txt")
        output_path = os.path.join(output_dir, f"output{file_idx:02d}.txt")
        
        test_cases = []
        
        # --- FILE 00: The "Monolith" Even Case ---
        # One single test case with N=100,000 (Even)
        # d is reasonably small to force strict checking
        if file_idx == 0:
            t = 1
            n = 100_000
            d = random.randint(50, 5000)
            a = [random.randint(1, MAX_VAL) for _ in range(n)]
            test_cases.append((n, d, a))

        # --- FILE 01: The "Monolith" Odd Case ---
        # One single test case with N=99,999 (Odd)
        # Uses the skip logic heavily
        elif file_idx == 1:
            t = 1
            n = 99_999
            d = random.randint(100, 10000)
            a = [random.randint(1, MAX_VAL) for _ in range(n)]
            test_cases.append((n, d, a))

        # --- FILE 02: The "Split" Even Case ---
        # 5 test cases, each N=20,000. Total = 100,000
        # High d (Expect mostly YES)
        elif file_idx == 2:
            t = 5
            chunk_n = 20_000
            for _ in range(t):
                d = random.randint(MAX_VAL // 2, MAX_VAL) # Very high d
                a = [random.randint(1, MAX_VAL) for _ in range(chunk_n)]
                test_cases.append((chunk_n, d, a))

        # --- FILE 03: The "Split" Odd Case ---
        # 5 test cases, each N=19,999. Total approx 100,000
        # Low d (Expect mostly NO)
        elif file_idx == 3:
            t = 5
            chunk_n = 19_999
            for _ in range(t):
                d = random.randint(0, 100) # Very low d
                a = [random.randint(1, MAX_VAL) for _ in range(chunk_n)]
                test_cases.append((chunk_n, d, a))

        # --- FILE 04: The "Chaos" Mix ---
        # Many small-ish test cases summing exactly to 100,000
        # Random Even and Odd N
        elif file_idx == 4:
            current_sum = 0
            while current_sum < MAX_N_SUM:
                # Generate random N between 100 and 5000
                rem = MAX_N_SUM - current_sum
                if rem < 5000:
                    n = rem # Take strictly remainder
                else:
                    n = random.randint(100, 5000)
                
                if n == 0: break
                
                d = random.randint(0, MAX_VAL)
                a = [random.randint(1, MAX_VAL) for _ in range(n)]
                test_cases.append((n, d, a))
                current_sum += n

        # --- WRITE TO FILES ---
        with open(input_path, 'w') as f_in, open(output_path, 'w') as f_out:
            # First line is T
            f_in.write(f"{len(test_cases)}\n")
            
            for (n, d, a) in test_cases:
                # Write Input
                f_in.write(f"{n} {d}\n")
                f_in.write(" ".join(map(str, a)) + "\n")
                
                # Generate Output using YOUR logic
                # Passing a copy of list(a) because your solve() sorts in-place
                ans = solve(n, d, list(a))
                f_out.write(f"{ans}\n")

    print("✅ Done!")
    print("1. Go into 'romanch_max_constraints' folder.")
    print("2. Zip 'input' and 'output' folders.")
    print("3. Upload to HackerRank.")

if __name__ == "__main__":
    generate_max_constraints_cases()