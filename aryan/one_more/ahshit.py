import os
import random
import sys

# Increase recursion depth just in case, though not needed for this iterative logic
sys.setrecursionlimit(2000)

def solve_python_logic(n, grid):
    """
    Python implementation of the User's C++ logic.
    Used to generate correct outputs.
    """
    ans = 0
    
    # Logic 1: Lower Triangle + Main Diagonal
    for k in range(n):
        row = n - 1 - k
        col = 0
        minn = float('inf')
        while row < n:
            val = grid[row][col]
            if val < minn:
                minn = val
            row += 1
            col += 1
        if minn < 0:
            ans = ans - minn

    # Logic 2: Upper Triangle
    for k in range(1, n):
        row = 0
        col = k
        minn = float('inf')
        while col < n:
            val = grid[row][col]
            if val < minn:
                minn = val
            row += 1
            col += 1
        if minn < 0:
            ans = ans - minn

    return ans

def generate_killer_cases():
    base_dir = "aryan_killer_tests"
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # --- THE KILLER CONFIGURATION ---
    # We want Total T = 200 with N = 500.
    # We split this into 5 files of T = 40 each to keep file size under 100MB.
    
    NUM_FILES = 5
    T_PER_FILE = 40   # 40 * 5 = 200 Total Cases
    N = 500           # Max N
    
    MAX_VAL = 1_000_000_000
    MIN_VAL = -1_000_000_000

    print(f"🚀 Generating {NUM_FILES} files.")
    print(f"💀 LOAD PER FILE: T={T_PER_FILE}, N={N} (Total ~10 Million ints per file)")
    
    for i in range(NUM_FILES):
        input_path = os.path.join(input_dir, f"input{i:02d}.txt")
        output_path = os.path.join(output_dir, f"output{i:02d}.txt")
        
        print(f"  > Generating File {i:02d}...", end=" ")
        
        with open(input_path, 'w') as f_in, open(output_path, 'w') as f_out:
            f_in.write(f"{T_PER_FILE}\n")
            
            for t in range(T_PER_FILE):
                f_in.write(f"{N}\n")
                
                grid = []
                
                # --- STRATEGY PER FILE ---
                
                # File 0: PURE RANDOM (I/O Killer)
                if i == 0:
                    for _ in range(N):
                        row = [random.randint(MIN_VAL, MAX_VAL) for _ in range(N)]
                        grid.append(row)

                # File 1: ALL NEGATIVE (Sum Overflow Killer)
                # Forces 'ans' to become massive (~500 * 10^9)
                elif i == 1:
                    for _ in range(N):
                        # Use a fixed large negative number
                        row = [-999999999] * N
                        grid.append(row)

                # File 2: DIAGONAL STRESS (Logic Killer)
                # Main diagonal is negative, everything else is positive.
                # Forces the minn check to run fully every time.
                elif i == 2:
                    for r in range(N):
                        row = []
                        for c in range(N):
                            if r == c:
                                row.append(-100000) # Negative diagonal
                            else:
                                row.append(100000)  # Positive background
                        grid.append(row)

                # File 3: ALTERNATING (CPU Branch Prediction Killer)
                # -1, 1, -1, 1... min check flips constantly
                elif i == 3:
                    for r in range(N):
                        row = [(100 if (r+c)%2==0 else -100) for c in range(N)]
                        grid.append(row)

                # File 4: RANDOM MIXED (Standard Heavy)
                else:
                    for _ in range(N):
                        row = [random.randint(-10000, 10000) for _ in range(N)]
                        grid.append(row)

                # --- WRITE INPUT ---
                for row in grid:
                    f_in.write(" ".join(map(str, row)) + "\n")

                # --- SOLVE & WRITE OUTPUT ---
                ans = solve_python_logic(N, grid)
                f_out.write(f"{ans}\n")
        
        print("Done.")

    print("\n✅ Generation Complete.")
    print("⚠️  WARNING: These files are roughly 80MB-90MB each.")
    print("    If upload fails, reduce T_PER_FILE to 20 in the script.")

if __name__ == "__main__":
    generate_killer_cases()