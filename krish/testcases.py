import os
import random
import shutil
import zipfile

# ==========================================
# CONFIGURATION
# ==========================================
NUM_FILES = 100
OUTPUT_DIR = "test_cases"
INPUT_DIR = os.path.join(OUTPUT_DIR, "input")
OUTPUT_SUBDIR = os.path.join(OUTPUT_DIR, "output")
ZIP_NAME = "krish_stack_overflow_tests.zip"

# Max constraints per problem statement
MAX_NM_SUM = 10**6  # Sum of N*M over all test cases in one file

# ==========================================
# THE SOLVER (Python version of Correct Logic)
# ==========================================
def solve(n, m, matrix):
    """
    Solves the problem for a single test case using the logic 
    verified to be correct (AP check + Mapping).
    Returns the output string ("p1 p2 ... pn" or "-1").
    """
    p = [-1] * n
    
    for i in range(n):
        row = sorted(matrix[i])
        
        # 1. Check Arithmetic Progression (Diff must be n)
        # If m=1, this loop doesn't run, which is correct (always AP of length 1)
        for j in range(m - 1):
            if row[j+1] - row[j] != n:
                return "-1"
        
        start_val = row[0]
        
        # 2. Integrity Check (Should technically never fail with this generator)
        if start_val < 0 or start_val >= n:
            return "-1"
            
        if p[start_val] != -1:
            return "-1"
            
        p[start_val] = i + 1
        
    # Final validation
    if -1 in p:
        return "-1"
        
    return " ".join(map(str, p))

def generate_output_for_file(input_filepath, output_filepath):
    with open(input_filepath, 'r') as fin:
        lines = fin.read().split()
    
    iterator = iter(lines)
    try:
        t = int(next(iterator))
    except StopIteration:
        return

    results = []
    for _ in range(t):
        n = int(next(iterator))
        m = int(next(iterator))
        matrix = []
        for _ in range(n):
            row = []
            for _ in range(m):
                row.append(int(next(iterator)))
            matrix.append(row)
        
        results.append(solve(n, m, matrix))
    
    with open(output_filepath, 'w') as fout:
        fout.write("\n".join(results))

# ==========================================
# TEST CASE GENERATORS
# ==========================================

def make_valid_case(n, m):
    """
    Generates a strictly valid case where a solution exists.
    Strategy:
    1. Assign start values 0..n-1 to rows randomly.
    2. Build AP: start, start+n, start+2n...
    3. Shuffle numbers within rows.
    """
    starts = list(range(n))
    random.shuffle(starts)
    
    matrix = []
    for i in range(n):
        s = starts[i]
        # Generate AP sequence
        row = [s + k*n for k in range(m)]
        random.shuffle(row) # Input is rarely sorted
        matrix.append(row)
        
    return matrix

def make_invalid_case(n, m):
    """
    Generates a case where answer is -1, BUT input is strictly VALID.
    Strategy:
    1. Create a valid matrix (distinct numbers 0..nm-1).
    2. Swap two numbers between two different rows.
    3. This breaks the AP property but preserves the set of numbers.
    Note: Only works if N > 1 and M > 1.
    """
    matrix = make_valid_case(n, m)
    
    if n > 1 and m > 1:
        # Pick two distinct rows
        r1, r2 = random.sample(range(n), 2)
        # Pick two column indices (can be same or different)
        c1 = random.randint(0, m-1)
        c2 = random.randint(0, m-1)
        
        # Swap to break the AP structure
        matrix[r1][c1], matrix[r2][c2] = matrix[r2][c2], matrix[r1][c1]
        
    return matrix

# ==========================================
# MAIN EXECUTION
# ==========================================

def main():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(INPUT_DIR)
    os.makedirs(OUTPUT_SUBDIR)

    print(f"Generating {NUM_FILES} test files...")

    for i in range(NUM_FILES):
        file_id = f"{i:02}"
        cases = []
        
        # --- LOGIC FOR VARIETY ---
        
        # 1. EDGE CASES (Files 00-05)
        if i == 0: # Minimal Valid
            cases = [(1, 1, make_valid_case(1, 1))]
        elif i == 1: # Minimal N, Large M
            cases = [(1, 100, make_valid_case(1, 100))]
        elif i == 2: # Large N, Minimal M
            cases = [(100, 1, make_valid_case(100, 1))]
        elif i == 3: # Small Invalid (N>1, M>1)
            cases = [(2, 2, make_invalid_case(2, 2))]
        elif i == 4: # Mixed small
            cases = [
                (2, 3, make_valid_case(2, 3)),
                (3, 2, make_invalid_case(3, 2)),
                (1, 5, make_valid_case(1, 5))
            ]
            
        # 2. ABSOLUTE MAXIMUM CONSTRAINTS (Files 95-99)
        # Explicitly forcing N=1000, M=1000 (10^6 elements)
        elif i == 95:
            # Max N, Small M
            cases = [(1000, 50, make_valid_case(1000, 50))] 
        elif i == 96:
            # Small N, Max M
            cases = [(50, 1000, make_valid_case(50, 1000))]
        elif i == 97:
            # Max Square (Valid) - Half Max
            cases = [(700, 700, make_valid_case(700, 700))]
        elif i == 98:
            # ABSOLUTE MAX VALID: 1000x1000
            print(f"  -> Generating Absolute Max Valid Case (1000x1000) for file {i}")
            cases = [(1000, 1000, make_valid_case(1000, 1000))]
        elif i == 99:
            # ABSOLUTE MAX INVALID: 1000x1000
            print(f"  -> Generating Absolute Max Invalid Case (1000x1000) for file {i}")
            cases = [(1000, 1000, make_invalid_case(1000, 1000))]

        # 3. RANDOM MEDIUM/LARGE CASES (Files 05-94)
        else:
            # Regular random generation logic
            t = random.randint(5, 20)
            current_nm = 0
            
            # Slightly reduced target for normal files to keep zip size manageable
            # The huge files are handled explicitly in 95-99
            TARGET_NM = 200000 
            
            # Logic for files 85-94 (High Stress but not Max)
            if i >= 85:
                 TARGET_NM = 500000
                 t = 100 # Loop limit, likely breaks on size first

            for _ in range(t):
                # Random dimensions
                n = random.randint(1, 100)
                m = random.randint(1, 100)
                
                # Scale up for the higher file numbers
                if i >= 50:
                    if random.random() < 0.5:
                        n = random.randint(100, 500)
                        m = random.randint(1, 100)
                    else:
                        n = random.randint(1, 100)
                        m = random.randint(100, 500)

                # Safety break for size
                if current_nm + (n*m) > MAX_NM_SUM:
                    break
                
                if random.random() < 0.6:
                    cases.append((n, m, make_valid_case(n, m)))
                else:
                    if n > 1 and m > 1:
                        cases.append((n, m, make_invalid_case(n, m)))
                    else:
                        cases.append((n, m, make_valid_case(n, m)))
                
                current_nm += (n*m)
                if current_nm >= TARGET_NM: 
                    break

        # --- WRITE INPUT ---
        input_filename = f"input{file_id}.txt"
        input_path = os.path.join(INPUT_DIR, input_filename)
        
        with open(input_path, 'w') as f:
            f.write(f"{len(cases)}\n")
            for n, m, matrix in cases:
                f.write(f"{n} {m}\n")
                for row in matrix:
                    f.write(" ".join(map(str, row)) + "\n")
        
        # --- GENERATE OUTPUT ---
        output_filename = f"output{file_id}.txt"
        output_path = os.path.join(OUTPUT_SUBDIR, output_filename)
        generate_output_for_file(input_path, output_path)
        
        if i % 10 == 0:
            print(f"Generated case {i}...")

    # --- ZIP CREATION ---
    print("Compressing files...")
    with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(OUTPUT_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, OUTPUT_DIR)
                zipf.write(file_path, arcname)

    # Check size
    zip_size = os.path.getsize(ZIP_NAME) / (1024 * 1024)
    print(f"Done! Created {ZIP_NAME} ({zip_size:.2f} MB)")
    if zip_size > 85:
        print("WARNING: Zip size exceeds 85MB. Consider reducing TARGET_NM.")
    else:
        print("Zip size is within 85MB limit.")

if __name__ == "__main__":
    main()