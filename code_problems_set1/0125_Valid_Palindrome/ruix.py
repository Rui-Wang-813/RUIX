class Solution:
    def isAlpha(self, c: str) -> bool:
        return c >= 'a' and c <= 'z'
    
    def isNumeric(self, c: str) -> bool:
        return c >= '0' and c <= '9'
    
    def isAlphaNumeric(self, c: str) -> bool:
        return self.isAlpha(c) or self.isNumeric(c)

    def trim(self, s: str) -> str:
        _s = ''
        for c in s:
            if self.isAlphaNumeric(c):
                _s += c
        return _s

    def isPalindrome(self, s: str) -> bool:
        s = s.lower()
        
        s = self.trim(s)

        i, j = 0, len(s) - 1
        while i < j:
            if s[i] != s[j]: return False
            i += 1
            j -= 1
        
        return True

s = "A man, a plan, a canal: Panama"

sol = Solution()
print(sol.isPalindrome(s))