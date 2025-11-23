import os
import random

def check(mid, expenses, D):
    """
    Greedy check: Can we split expenses into <= D groups
    such that no group sum exceeds 'mid'?
    """
    groups = 1
    current_sum = 0
    for x in expenses:
        if current_sum + x > mid:
            groups += 1
            current_sum = x
        else:
            current_sum += x
    return groups <= D

def solve(n, d, expenses):
    """
    Binary Search on Answer logic.
    Range: [max(expenses), sum(expenses)]
    """
    if not expenses:
        return 0
        
    low = max(expenses)
    high = sum(expenses)
    ans = high
    
    while low <= high:
        mid = (low + high) // 2
        if check(mid, expenses, d):
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
    return ans

def generate_test_cases():
    base_dir = "lavanya_test_cases"
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # --- SETTINGS ---
    NUM_FILES = 100
    
    # To allow N=10^5, we need the file limit to be at least 100,000.
    # 100 files * 100k numbers * ~7 bytes/num = ~70MB.
    # This is safely under 85MB.
    SUM_N_PER_FILE = 100_000
    MAX_VAL = 10**6 
    
    print(f"🚀 Generating {NUM_FILES} test files (under 85MB) for Lavanya...")

    for i in range(NUM_FILES):
        input_path = os.path.join(input_dir, f"input{i:02d}.txt")
        output_path = os.path.join(output_dir, f"output{i:02d}.txt")
        
        test_cases_in = []
        current_n_sum = 0
        
        # --- Strategy for this file ---
        
        # File 00-09: Manual Edge Cases (10 files)
        if i == 0:
            # Sample Case
            test_cases_in.append((10, 5, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
        elif i == 1:
            # N=1
            test_cases_in.append((1, 1, [100]))
        elif i == 2:
            # D=1 (Answer is sum)
            test_cases_in.append((5, 1, [10, 20, 30, 40, 50]))
        elif i == 3:
            # D=N (Answer is max element)
            test_cases_in.append((5, 5, [10, 20, 30, 40, 50]))
        elif i == 4:
            # Large values (Force long long for sum)
            test_cases_in.append((3, 2, [1000000, 1000000, 1000000]))
        elif i < 10:
            # Small randoms
            while current_n_sum < 1000:
                n = random.randint(1, 50)
                d = random.randint(1, n)
                e = [random.randint(1, 1000) for _ in range(n)]
                test_cases_in.append((n, d, e))
                current_n_sum += n

        # File 10-19: ABSOLUTE MAX CONSTRAINTS (TLE cases)
        # 10 files, each with ONE case of N=100,000.
        # This forces the O(N log Ans) solution. O(N^2) DP will die.
        elif i < 20:
            T = 1
            n = 100_000 # The hard limit
            d = random.randint(1, n)
            # Generate large random expenses
            e = [random.randint(1, MAX_VAL) for _ in range(n)]
            test_cases_in.append((n, d, e))

        # File 20-99: High T, Small N (Random stress test)
        else:
            while current_n_sum < SUM_N_PER_FILE - 100:
                n = random.randint(1, 500)
                d = random.randint(1, n)
                e = [random.randint(1, MAX_VAL) for _ in range(n)]
                test_cases_in.append((n, d, e))
                current_n_sum += n

        # --- Write files ---
        with open(input_path, 'w') as f_in, open(output_path, 'w') as f_out:
            f_in.write(f"{len(test_cases_in)}\n") # Write T
            
            for (n, d, e) in test_cases_in:
                f_in.write(f"{n} {d}\n")
                f_in.write(" ".join(map(str, e)) + "\n")
                
                # Solve and write the answer
                answer = solve(n, d, e)
                f_out.write(f"{answer}\n")
                
    print(f"✅ Generated {NUM_FILES} files in '{base_dir}/'.")
    print("⚠️  Total zip size should be safely under 85MB.")
    print("\n--- HOW TO ZIP ---")
    print("1. Go *inside* the 'lavanya_test_cases' folder.")
    print("2. Select both 'input' and 'output' folders.")
    print("3. Right-click and compress them into a new zip file.")
    print("4. Upload that new zip file.")

if __name__ == "__main__":
    generate_test_cases()