class Solution:
    def longestValidParentheses(self, s: str) -> int:
        if len(s) <= 1:
            return 0
        
        def check_is_valid(s: str, i: int, j: int) -> bool:
            c = 0
            while (i <= j):
                if s[i] == '(':
                    c += 1
                else:
                    c -= 1
                if c < 0:
                    return False
                i += 1
            return c==0
        
        max_len = 0
        
        for i in range(len(s)):
            j = i + max_len+1
            while j < len(s):
                if check_is_valid(s, i, j):
                    max_len = j - i + 1
                j += 2
        
        return max_len