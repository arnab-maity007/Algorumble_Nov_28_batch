import os
import random
import string

def solve(s, t):
    """
    O(N) solution for Isomorphic Strings.
    Checks if there is a 1-to-1 mapping between characters of s and t.
    """
    if len(s) != len(t):
        return "NO"
    
    s_to_t_map = {}
    t_to_s_map = {}
    
    for char_s, char_t in zip(s, t):
        # Check forward mapping (s -> t)
        if char_s in s_to_t_map:
            if s_to_t_map[char_s] != char_t:
                return "NO"
        else:
            s_to_t_map[char_s] = char_t
            
        # Check backward mapping (t -> s)
        if char_t in t_to_s_map:
            if t_to_s_map[char_t] != char_s:
                return "NO"
        else:
            t_to_s_map[char_t] = char_s
            
    return "YES"

def generate_test_cases():
    base_dir = "atharv_test_cases"
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    NUM_FILES = 100
    # 400k chars per file -> ~80MB total zip size. Safe.
    SUM_S_PER_FILE = 400_000 
    
    # Use safe characters (no whitespace) so cin >> s works perfectly
    SAFE_CHARS = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"

    print(f"🚀 Generating {NUM_FILES} test files for Atharv...")

    for i in range(NUM_FILES):
        input_path = os.path.join(input_dir, f"input{i:02d}.txt")
        output_path = os.path.join(output_dir, f"output{i:02d}.txt")
        
        test_cases_in = []
        current_s_sum = 0
        
        # --- Strategy ---
        
        # File 00-09: Manual Edge Cases
        if i == 0:
            test_cases_in = [("egg", "add"), ("foo", "bar"), ("paper", "title"), ("baba", "kiki"), ("badc", "baba")]
        elif i == 1:
            test_cases_in = [("a", "a"), ("a", "b"), ("ab", "aa"), ("aa", "ab"), ("abc", "def")]
        elif i == 2:
            test_cases_in = [("a", "ab"), ("ab", "a"), ("hello", "world!"), ("123", "456")]
        elif i < 10:
            # Short random strings
            while current_s_sum < 10000: 
                n = random.randint(1, 20)
                s = "".join(random.choices(SAFE_CHARS, k=n))
                if random.random() > 0.5: # YES
                    # Valid mapping
                    chars_s = list(set(s))
                    if len(chars_s) > len(SAFE_CHARS): # Fallback
                        t = s
                    else:
                        chars_t = random.sample(SAFE_CHARS, len(chars_s))
                        mapping = dict(zip(chars_s, chars_t))
                        t = "".join(mapping[c] for c in s)
                else: # NO
                    t = "".join(random.choices(SAFE_CHARS, k=n))
                test_cases_in.append((s, t))
                current_s_sum += n

        # File 10-39: High T, Small N (Stress loop)
        elif i < 40:
            while current_s_sum < SUM_S_PER_FILE - 100:
                n = random.randint(1, 100)
                s = "".join(random.choices(SAFE_CHARS, k=n))
                # 50/50 chance YES/NO
                if random.random() > 0.5:
                    chars_s = list(set(s))
                    if len(chars_s) > len(SAFE_CHARS):
                        t = s
                    else:
                        chars_t = random.sample(SAFE_CHARS, len(chars_s))
                        mapping = dict(zip(chars_s, chars_t))
                        t = "".join(mapping[c] for c in s)
                else:
                    t = "".join(random.choices(SAFE_CHARS, k=n))
                test_cases_in.append((s, t))
                current_s_sum += n

        # File 40-99: MAX CONSTRAINTS (TLE check for inefficient solutions)
        else:
            # ~4 cases per file, each with N=100k
            T = 4
            n = 100_000 
            for _ in range(T):
                s = "".join(random.choices(SAFE_CHARS, k=n))
                
                if random.random() > 0.5: # YES case
                    chars_s = list(set(s))
                    if len(chars_s) > len(SAFE_CHARS):
                        t = s
                    else:
                        chars_t = random.sample(SAFE_CHARS, len(chars_s))
                        mapping = dict(zip(chars_s, chars_t))
                        t = "".join(mapping[c] for c in s)
                else: # NO case
                    # Create tricky failure: s[0]!=s[1] but t[0]==t[1]
                    s_list = list(s)
                    t_list = list("".join(random.choices(SAFE_CHARS, k=n)))
                    
                    # Force t[0] == t[1]
                    t_list[1] = t_list[0]
                    
                    # Force s[0] != s[1]
                    if s_list[0] == s_list[1]:
                        new_char = random.choice(SAFE_CHARS)
                        while new_char == s_list[0]:
                            new_char = random.choice(SAFE_CHARS)
                        s_list[1] = new_char
                        
                    s = "".join(s_list)
                    t = "".join(t_list)

                test_cases_in.append((s, t))

        # --- Write files ---
        with open(input_path, 'w') as f_in, open(output_path, 'w') as f_out:
            f_in.write(f"{len(test_cases_in)}\n") # Write T
            
            for s, t in test_cases_in:
                # Handle empty edge case just in case
                if not s: s = "a"
                if not t: t = "a"
                
                f_in.write(f"{s} {t}\n") # Write on one line for cin >> s >> t
                
                answer = solve(s, t)
                f_out.write(f"{answer}\n")
                
    print(f"✅ Generated {NUM_FILES} files in '{base_dir}/'.")
    print("⚠️  Total zip size should be ~80MB (Safe).")
    print("\n--- HOW TO ZIP ---")
    print("1. Go *inside* the 'atharv_test_cases' folder.")
    print("2. Select both 'input' and 'output' folders.")
    print("3. Right-click and compress them into a new zip file.")
    print("4. Upload that new zip file.")

if __name__ == "__main__":
    generate_test_cases()