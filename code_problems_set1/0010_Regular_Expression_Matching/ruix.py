class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        # if the pattern is empty, then the text should be empty.
        if not p:
            return not s
        
        first_match = (len(s)!=0) and (p[0] in [s[0], '.']) # first char matches.
        
        if len(p) >= 2 and p[1] == '*':
            # pattern is '[char]*[...]'
            # either the first char of pattern matches to nothing or the first char matches to something.
            return self.isMatch(s, p[2:]) or (first_match and self.isMatch(s[1:], p))
        else:
            # if len(p) == 1: the first has to match.
            # if len(p) >= 2 and p[1] != *. The first has to match and the rest has to match.
            return first_match and self.isMatch(s[1:], p[1:])