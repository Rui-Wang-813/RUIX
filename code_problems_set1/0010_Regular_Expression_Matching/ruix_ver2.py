class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        memo = {}

        def dp(i: int, j: int) -> bool:
            ans = False
            if (i,j) in memo:
                ans = memo[(i,j)]
            else:
                if j == len(p):
                    ans = i == len(s)
                else:
                    first_match = (len(s) > i) and (p[j] in [s[i], '.'])
                    if (j < len(p)-1) and (p[j+1] == '*'):
                        ans = dp(i,j+2) or (first_match and dp(i+1,j))
                    else:
                        ans = first_match and dp(i+1,j+1)
            
            memo[(i,j)] = ans
            return ans
        
        return dp(0,0)

'''
This version is very similar to the recursive version, except that it uses a dictionary to cache the
computed values.
'''