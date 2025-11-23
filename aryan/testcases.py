import os
import random

def solve(grid):
    """
    This is the O(n^2) DP solution.
    dp[i][j] = total chants that have been applied *at or above* (i, j)
               on the same diagonal.
    total_answer = sum of chants we have to add at each step.
    """
    
    n = len(grid)
    if n == 0:
        return 0
    
    dp = [[0] * n for _ in range(n)]
    total_answer = 0
    
    for i in range(n):
        for j in range(n):
            # Get chants propagated from the cell diagonally above-left
            propagated_chants = 0
            if i > 0 and j > 0:
                propagated_chants = dp[i-1][j-1]
            
            # This is the cell's current value after previous chants
            current_value = grid[i][j] + propagated_chants
            
            chants_needed = 0
            if current_value < 0:
                # We must use long long here, but Python handles it.
                chants_needed = -current_value
            
            # The total answer is the sum of chants we add at each step
            total_answer += chants_needed
            
            # The dp state for (i+1, j+1) is the sum of previous
            # chants plus the new ones we just added at (i, j).
            dp[i][j] = propagated_chants + chants_needed
            
    return total_answer

def generate_test_cases():
    base_dir = "aryan_test_cases"
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # --- SETTINGS ---
    NUM_FILES = 60 # Reduced from 100 to save space
    
    # Each "max" file has T=2, n=500. n^2 = 250,000. Sum(n^2) = 500,000
    # Each "random" file has Sum(n^2) <= 500,000
    # 500k numbers * 12 bytes/num = 6MB per file
    # 60 files * 6MB = 360MB (uncompressed) -> Zips to ~80-90MB
    SUM_N_SQUARED_PER_FILE = 500_000
    MAX_N = 500
    MAX_VAL = 10**9
    
    print(f"🚀 Generating {NUM_FILES} test files (under 90MB) for Aryan...")

    for i in range(NUM_FILES):
        input_path = os.path.join(input_dir, f"input{i:02d}.txt")
        output_path = os.path.join(output_dir, f"output{i:02d}.txt")
        
        test_cases_in = []
        current_n_squared_sum = 0
        
        # --- Strategy for this file ---
        
        # File 00-09: Manual Edge Cases (10 files)
        if i == 0:
            # Sample 1
            test_cases_in.append([[-1, -1, 4], [-1, -1, 4], [-1, -1, 4]])
            # Sample 2
            test_cases_in.append([[-1, -2], [-3, -4]])
        elif i == 1:
            # n=1 cases
            test_cases_in.append([[-10]])
            test_cases_in.append([[10]])
            test_cases_in.append([[-MAX_VAL]]) # Forces long long
        elif i == 2:
            # All positive
            test_cases_in.append([[1, 2], [3, 4]])
        elif i == 3:
            # All negative (forces long long overflow for answer)
            grid = [[-MAX_VAL] * 10 for _ in range(10)] # 10*10 = 100
            test_cases_in.append(grid)
        elif i < 10:
             # Other small edge cases
            grid = [[random.randint(-100, 100) for _ in range(5)] for _ in range(5)]
            test_cases_in.append(grid)

        # File 10-19: MAX CONSTRAINTS (TLE cases for O(n^3))
        # 10 files as requested.
        elif i < 20:
            # Each file gets 2 test cases of n=500
            # 2 * 500^2 = 500,000
            T = 2
            n = 500 
            for _ in range(T):
                if current_n_squared_sum + n*n <= SUM_N_SQUARED_PER_FILE:
                    grid = [[random.randint(-MAX_VAL, MAX_VAL) for _ in range(n)] for _ in range(n)]
                    test_cases_in.append(grid)
                    current_n_squared_sum += n*n

        # File 20-59: High T, Small N (Random)
        else:
            while current_n_squared_sum < SUM_N_SQUARED_PER_FILE:
                n = random.randint(1, 22) # n*n is at most 484
                if current_n_squared_sum + n*n > SUM_N_SQUARED_PER_FILE:
                    break
                grid = [[random.randint(-100, 100) for _ in range(n)] for _ in range(n)]
                test_cases_in.append(grid)
                current_n_squared_sum += n*n


        # --- Write files ---
        with open(input_path, 'w') as f_in, open(output_path, 'w') as f_out:
            f_in.write(f"{len(test_cases_in)}\n") # Write T
            
            for grid in test_cases_in:
                n = len(grid)
                f_in.write(f"{n}\n")
                for row in grid:
                    f_in.write(" ".join(map(str, row)) + "\n")
                
                # Solve and write the answer
                answer = solve(grid)
                f_out.write(f"{answer}\n")
                
    print(f"✅ Generated {NUM_FILES} files in '{base_dir}/'.")
    print("⚠️  Total zip size should be safely under 90MB.")
    print("\n--- HOW TO ZIP ---")
    print("1. Go *inside* the 'aryan_test_cases' folder.")
    print("2. Select both 'input' and 'output' folders.")
    print("3. Right-click and compress them into a new zip file.")
    print("4. Upload that new zip file.")

if __name__ == "__main__":
    generate_test_cases()