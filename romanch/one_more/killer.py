import os
import random

# --- YOUR CORRECT LOGIC (To generate correct outputs) ---
def solve_correctly(n, d, a):
    a.sort()
    if n % 2 == 0:
        for i in range(1, n, 2):
            if a[i] - a[i-1] > d: return "NO"
        return "YES"
    else:
        # Efficient O(N) check using prefix/suffix logic implicitly
        # We simulate the "remove one" check greedily
        # 1. Check if removing index 0 works
        # 2. Check if removing index n-1 works
        # 3. Scan for the single mismatch
        
        # Actually, let's use the exact logic from your provided correct python script
        # to ensure consistency.
        flag = True 
        i = 1
        while i < n:
            if a[i] - a[i-1] > d:
                if flag:
                    flag = False
                    i += 1 
                else:
                    return "NO"
            else:
                i += 2
        return "YES"

def generate_killer_cases():
    base_dir = "romanch_killer_cases"
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    print(f"🚀 Generating 5 KILLER test files designed to break O(N^2)...")

    # We generate 5 files. All of them will target the weakness.
    for file_idx in range(5):
        input_path = os.path.join(input_dir, f"input{file_idx:02d}.txt")
        output_path = os.path.join(output_dir, f"output{file_idx:02d}.txt")
        
        test_cases = []
        
        # We want Sum of N to be high.
        # Let's put one MASSIVE case in each file.
        T = 1
        N = 99_999 # Must be Odd to trigger the heavy loop
        d = 100
        
        # --- THE TRAP CONSTRUCTION ---
        # We want pairs that work perfectly: (100, 200), (300, 400), (500, 600)...
        # And one GIANT number at the end: 1,000,000,000
        #
        # If you remove index 0 (100): (200, 300) -> Diff 100 OK... eventually hits end -> Fail
        # If you remove index N-1 (Giant): (100, 200), (300, 400)... -> ALL OK.
        #
        # This forces the brute force code to check indices 0, 1, 2... all failing,
        # until it finally hits index N-1 and succeeds.
        # Total Cost: 100,000 iterations * Vector Copy of 100,000 elements.
        
        a = []
        val = 100
        # Generate N-1 elements as perfect pairs
        for _ in range((N - 1) // 2):
            a.append(val)
            a.append(val + d) # Perfect pair with diff = d
            val += (d + 50)   # Gap between pairs
            
        # Add the "Trap" element at the end
        # It is so large it cannot pair with the previous element (val)
        a.append(1_000_000_000)
        
        # Double check logic:
        # Array is sorted.
        # Remove last element -> Rest are (x, x+d) pairs. Valid.
        # Remove any other element -> The parity shifts, and eventually we are left 
        # trying to pair the second-to-last element with 1,000,000,000. Fails.
        
        test_cases.append((N, d, a))

        # --- Write Files ---
        with open(input_path, 'w') as f_in, open(output_path, 'w') as f_out:
            f_in.write(f"{T}\n")
            for (n, d, arr) in test_cases:
                f_in.write(f"{n} {d}\n")
                f_in.write(" ".join(map(str, arr)) + "\n")
                
                # Generate Output
                ans = solve_correctly(n, d, list(arr))
                f_out.write(f"{ans}\n")

    print("✅ Done! These inputs force the C++ code to iterate until the very last index.")
    print("📂 Upload the zip from 'romanch_killer_cases'.")

if __name__ == "__main__":
    generate_killer_cases()