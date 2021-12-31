class Solution:
    def longestValidParentheses(self, s: str) -> int:
        if len(s) <= 1:
            return 0
        
        # use dp[i] to record the longest valid parentheses sequence ending at i.
        dp = [0] * len(s)

        for i in range(1,len(s)):
            # a valid parentheses sequence cannot end at a '('.
            if s[i] == '(':
                continue
            if s[i-1] == '(':
                # the last two are '()', so dp[i] = dp[i-2] + 2. No other possibilities.
                dp[i] = (dp[i-2] if i>=2 else 0) + 2
            elif s[i-1] == ')':
                # the last two are '))'. If s[i-dp[i-1]-1] (the char just before the valid sequence
                # ending at s[i-1]) is '(', then apparently s[i-dp[i-1]-1:i] is a valid sequence, what's
                # more, if there is a valid sequence ending at s[i-dp[i-1]-2], they together composes a
                # longer valid sequence.
                if i-dp[i-1] >= 1 and s[i-dp[i-1]-1] == '(':
                    dp[i] = dp[i-1] + (dp[i-dp[i-1]-2] if i-dp[i-1] >= 2 else 0) + 2
        
        return max(dp)