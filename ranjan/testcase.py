import os
import random

def generate_nuclear_tests():
    base_dir = "ranjan_nuclear_tests"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # SETTINGS
    NUM_FILES = 100          # Change to 100 if you really want to make them cry
    MAX_T = 100000          # 10^5 test cases per file
    MAX_C = 10000000        # 10^7 max value

    print(f"☢️  Generating {NUM_FILES} FILES with {MAX_T} queries each...")
    print(f"🔥  Total Queries: {NUM_FILES * MAX_T}...")

    for i in range(NUM_FILES):
        filename_in = f"input{i:02d}.txt"
        filename_out = f"output{i:02d}.txt"
        
        path_in = os.path.join(base_dir, filename_in)
        path_out = os.path.join(base_dir, filename_out)
        
        c_values = []

        # --- STRATEGY ---
        
        # File 00-04: EDGE CASE HELL (Small numbers, Powers of 2, Primes)
        if i < 5:
            # Mix of small numbers, powers of 2, and randoms
            c_values.extend([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
            
            # Powers of 2 up to Max
            val = 1
            while val <= MAX_C:
                c_values.append(val)
                val *= 2
            
            # Mersenne (Power of 2 - 1)
            val = 2
            while val <= MAX_C:
                c_values.append(val - 1)
                val *= 2
                
            # Fill the rest with Randoms
            remaining = MAX_T - len(c_values)
            c_values.extend([random.randint(1, MAX_C) for _ in range(remaining)])

        # File 05-09: BITWISE TRICKERY (Sparse and Dense bits)
        elif i < 10:
            # Numbers like 1111100000, 1010101010, etc.
            # To check if their bit manipulation logic holds up
            for _ in range(MAX_T):
                # 50% chance of random, 50% chance of specific bit pattern
                if random.random() > 0.5:
                    c_values.append(random.randint(1, MAX_C))
                else:
                    # Create weird numbers
                    mask = random.getrandbits(24) # 2^24 covers 10^7 range
                    mask = mask % MAX_C
                    if mask == 0: mask = 1
                    c_values.append(mask)

        # File 10-39: PURE CHAOS (Uniform Random Max Constraints)
        elif i < 40:
            # Just 100,000 random numbers up to 10^7
            # This stresses I/O the most
            c_values = [random.randint(1, MAX_C) for _ in range(MAX_T)]

        # File 40-49: THE WALL (Every value is MAX_C)
        else:
            # Checking if they handle the largest number repeatedly without caching issues
            # or overflow errors in calculation.
            c_values = [MAX_C] * MAX_T # All values are 10,000,000

        # --- WRITE TO FILE ---
        with open(path_in, 'w') as f:
            # Header: Number of Test Cases in this file
            f.write(f"{len(c_values)}\n")
            # Join them for faster write than loop
            f.write('\n'.join(map(str, c_values)))
        
        # Dummy Output
        with open(path_out, 'w') as f:
            f.write("0")

    print(f"✅ Done! Folder '{base_dir}' is ready.")
    print("👉 Pro Tip: Select all files inside -> Right Click -> Compress/Zip -> Upload Zip to HackerRank.")

if __name__ == "__main__":
    generate_nuclear_tests()