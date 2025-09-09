import timeit

def longest_common_suffix(a: str, b: str) -> int:
    n = min(len(a), len(b))
    for i in range(n): # for ; i < len(a) && i < len(b); i++ {
        if a[len(a) - 1 - i] != b[len(b) - 1 - i]:
            return i
    else:
        return n


class BoyerMoore():

    def __init__(self, pattern: str) -> None:
        last = len(pattern) - 1

        self.pattern: str = pattern
        self.bad_char_skip: dict[str, int] = {pattern[i]: last - i for i in range(last)}
        self.good_suffix_skip = [0]*len(pattern) 

        # First pass: set each value to the next index which starts a prefix of pattern.
        last_prefix = last
        for i in range(last, -1, -1):
            if pattern.startswith(pattern[i + 1:]): 
                last_prefix = i + 1
            # lastPrefix is the shift, and (last-i) is len(suffix).
            self.good_suffix_skip[i] = last_prefix + last - i

        # Second pass: find repeats of pattern's suffix starting from the front.
        for i in range(last): 
            len_suffix = longest_common_suffix(pattern, pattern[1:i + 1])
            if pattern[i - len_suffix] != pattern[last - len_suffix]:
            # (last-i) is the shift, and lenSuffix is len(suffix).
                self.good_suffix_skip[last - len_suffix] = len_suffix + last - i

        # print(self.bad_char_skip)


    def search(self, text: str) -> int:
        i = len(self.pattern) - 1
        while i < len(text):
            # Compare backwards from the end until the first unmatching character.
            j = len(self.pattern) - 1
            while j >= 0 and text[i] == self.pattern[j]:
                i -= 1
                j -= 1
            if j < 0: 
                return i + 1 # match
            i += max(self.bad_char_skip.get(text[i], 0), self.good_suffix_skip[j])
        return -1


class KnuthMorrisPratt():

    def __init__(self, pattern: str) -> None:
        self.pattern: str = pattern
        self.lps = [0] * len(pattern)
        l = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[l]:
                l += 1
                self.lps[i] = l
                i += 1
            else:
                if l != 0:
                    l = self.lps[l - 1]
                else:
                    self.lps[i] = 0
                    i += 1

    def search(self, text: str) -> int:
        m = len(self.pattern)
        n = len(text)

        if m == 0:
            return 0

        if m > n:
            return -1
   
        i = j = 0

        while i < n:
            if j < m and self.pattern[j] == text[i]:
                i += 1
                j += 1
            elif j != 0:
                j = self.lps[j - 1]
            else:
                i += 1
            if j == m:
                return i - j
        return -1 
    
def polynomial_hash(s: str, base: int, modulus: int):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

class RabinKarp():
    def __init__(self, pattern: str, base: int = 256, modulus: int = 101) -> None:
        self.pattern: str = pattern
        self.pattern_len = len(pattern)
        self.pattern_hash = polynomial_hash(pattern, base, modulus)
        self.base = base 
        self.modulus = modulus

    def search(self, text: str) -> int:
        text_len = len(text)

        if self.pattern_len == 0:
            return 0

        if self.pattern_len > text_len:
            return -1

        current_slice_hash = polynomial_hash(text[:self.pattern_len], self.base, self.modulus)
        h_multiplier = pow(self.base, self.pattern_len - 1) % self.modulus
        for i in range(text_len - self.pattern_len + 1):
            # print(f"pattern hash : {self.pattern_hash}, current hash: {current_slice_hash}")
            if self.pattern_hash == current_slice_hash:
                #print('hash equals')
                if text[i:i+self.pattern_len] == self.pattern:
                    #print("strings equals")
                    return i

            if i < text_len - self.pattern_len:
                #current_slice_hash = polynomial_hash(text[:text_len], self.base, self.modulus)
                current_slice_hash = (current_slice_hash - 
                                      ord(text[i]) * h_multiplier) % self.modulus
                current_slice_hash = (current_slice_hash * self.base + 
                                      ord(text[i + self.pattern_len])) % self.modulus
                if current_slice_hash < 0:
                    current_slice_hash += self.modulus   

        return -1

        







def main():

    text1 = ""
    text2 = "abc"
    text3 = " abc"
    text4 = " abc abc "
    text5 = " абвгд "

    with open("data/стаття_1.txt", "r") as f:
        art1 = f.read()

    with open("data/стаття_2.txt", "r") as f:
        art2 = f.read()



    # bmoor = BoyerMoore("abc")
    # print(f"text: '{text1}', pattern: '{bmoor.pattern}', index: {bmoor.search(text1)}")
    # print(f"text: '{text2}', pattern: '{bmoor.pattern}', index: {bmoor.search(text2)}")
    # print(f"text: '{text3}', pattern: '{bmoor.pattern}', index: {bmoor.search(text3)}")
    # print(f"text: '{text4}', pattern: '{bmoor.pattern}', index: {bmoor.search(text4)}")
    # print(f"text: '{text5}', pattern: '{bmoor.pattern}', index: {bmoor.search(text5)}")

    # bmoor = BoyerMoore("вг")
    # print(f"text: '{text1}', pattern: '{bmoor.pattern}', index: {bmoor.search(text1)}")
    # print(f"text: '{text2}', pattern: '{bmoor.pattern}', index: {bmoor.search(text2)}")
    # print(f"text: '{text3}', pattern: '{bmoor.pattern}', index: {bmoor.search(text3)}")
    # print(f"text: '{text4}', pattern: '{bmoor.pattern}', index: {bmoor.search(text4)}")
    # print(f"text: '{text5}', pattern: '{bmoor.pattern}', index: {bmoor.search(text5)}")
    # print(f"text: 'art1', pattern: '{bmoor.pattern}', index: {bmoor.search(art1)}")

    bmoor = BoyerMoore("")
    print(f"text: '{text1}', pattern: '{bmoor.pattern}', index: {bmoor.search(text1)}")
    print(f"text: '{text4}', pattern: '{bmoor.pattern}', index: {bmoor.search(text4)}")

    bmoor = BoyerMoore("Двійковий або логарифмічний пошук")
    print(f"text: 'art1', pattern: '{bmoor.pattern}', index: {bmoor.search(art1)}")

    # bmoor = BoyerMoore(art1)
    # print(f"text: 'art1', pattern: 'art1', index: {bmoor.search(art1)}")
    
    # bmoor = BoyerMoore(art1[5:])
    # print(f"text: 'art1', pattern: 'art1', index: {bmoor.search(art1)}")
    

    kmp = KnuthMorrisPratt("abc")
    print(f"text: '{text1}', pattern: '{kmp.pattern}', index: {kmp.search(text1)}")
    print(f"text: '{text2}', pattern: '{kmp.pattern}', index: {kmp.search(text2)}")
    print(f"text: '{text3}', pattern: '{kmp.pattern}', index: {kmp.search(text3)}")
    print(f"text: '{text4}', pattern: '{kmp.pattern}', index: {kmp.search(text4)}")
    print(f"text: '{text5}', pattern: '{kmp.pattern}', index: {kmp.search(text5)}")

    kmp = KnuthMorrisPratt("вг")
    print(f"text: '{text1}', pattern: '{kmp.pattern}', index: {kmp.search(text1)}")
    print(f"text: '{text2}', pattern: '{kmp.pattern}', index: {kmp.search(text2)}")
    print(f"text: '{text3}', pattern: '{kmp.pattern}', index: {kmp.search(text3)}")
    print(f"text: '{text4}', pattern: '{kmp.pattern}', index: {kmp.search(text4)}")
    print(f"text: '{text5}', pattern: '{kmp.pattern}', index: {kmp.search(text5)}")
    print(f"text: 'art1', pattern: '{kmp.pattern}', index: {kmp.search(art1)}")

    kmp = KnuthMorrisPratt("")
    print(f"text: '{text1}', pattern: '{kmp.pattern}', index: {kmp.search(text1)}")
    print(f"text: '{text4}', pattern: '{kmp.pattern}', index: {kmp.search(text4)}")

    kmp = KnuthMorrisPratt("Двійковий або логарифмічний пошук")
    print(f"text: 'art1', pattern: '{kmp.pattern}', index: {kmp.search(art1)}")

    kmp = KnuthMorrisPratt(art1)
    print(f"text: 'art1', pattern: 'art1', index: {kmp.search(art1)}")
    
    kmp = KnuthMorrisPratt(art1[5:])
    print(f"text: 'art1', pattern: 'art1', index: {kmp.search(art1)}")


    rk = RabinKarp('abc')
    print(f"text: '{text1}', pattern: '{rk.pattern}', index: {rk.search(text1)}")
    print(f"text: '{text2}', pattern: '{rk.pattern}', index: {rk.search(text2)}")
    print(f"text: '{text3}', pattern: '{rk.pattern}', index: {rk.search(text3)}")
    print(f"text: '{text4}', pattern: '{rk.pattern}', index: {rk.search(text4)}")
    print(f"text: '{text5}', pattern: '{rk.pattern}', index: {rk.search(text5)}")

    rk = RabinKarp("вг")
    print(f"text: '{text1}', pattern: '{rk.pattern}', index: {rk.search(text1)}")
    print(f"text: '{text2}', pattern: '{rk.pattern}', index: {rk.search(text2)}")
    print(f"text: '{text3}', pattern: '{rk.pattern}', index: {rk.search(text3)}")
    print(f"text: '{text4}', pattern: '{rk.pattern}', index: {rk.search(text4)}")
    print(f"text: '{text5}', pattern: '{rk.pattern}', index: {rk.search(text5)}")
    print(f"text: 'art1', pattern: '{rk.pattern}', index: {rk.search(art1)}")

    rk = KnuthMorrisPratt("")
    print(f"text: '{text1}', pattern: '{rk.pattern}', index: {rk.search(text1)}")
    print(f"text: '{text4}', pattern: '{rk.pattern}', index: {rk.search(text4)}")

    rk = KnuthMorrisPratt("Двійковий або логарифмічний пошук")
    print(f"text: 'art1', pattern: '{rk.pattern}', index: {rk.search(art1)}")

    rk = KnuthMorrisPratt(art1)
    print(f"text: 'art1', pattern: 'art1', index: {rk.search(art1)}")
    
    rk = KnuthMorrisPratt(art1[5:])
    print(f"text: 'art1', pattern: 'art1', index: {rk.search(art1)}")
    
    # print(insertion_sort_my([random.randint(min_value, max_value) for _ in range(10)]))
    # print(insertion_sort_old([random.randint(min_value, max_value) for _ in range(10)]))
    # print(merge_sort([random.randint(min_value, max_value) for _ in range(10)]))
    # print(sorted([random.randint(min_value, max_value) for _ in range(10)]))
        
    # code_insertion_sort_my = "insertion_sort_my(random_lst.copy())"
    # time_insertion_sort_my = timeit.timeit(code_insertion_sort_my, globals=globals(), number=number)
    # print(f"time_insertion_sort_my: {time_insertion_sort_my}")

    # code_insertion_sort_old = "insertion_sort_old(random_lst.copy())"
    # time_insertion_sort_old = timeit.timeit(code_insertion_sort_old, globals=globals(), number=number)
    # print(f"time_insertion_sort_old: {time_insertion_sort_old}")

    # code_merge_sort = "merge_sort(random_lst.copy())"
    # time_merge_sort = timeit.timeit(code_merge_sort, globals=globals(), number=number)
    # print(f"time_merge_sort: {time_merge_sort}")

    # code_sorted = "sorted(random_lst.copy())"
    # time_sorted = timeit.timeit(code_sorted, globals=globals(), number=number)
    # print(f"time_sorted: {time_sorted}")
    
    


    
