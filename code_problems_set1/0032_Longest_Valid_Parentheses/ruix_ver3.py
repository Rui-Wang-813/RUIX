class Solution:
    def longestValidParentheses(self, s: str) -> int:
        left = right = 0
        max_len = 0

        for i in range(len(s)):
            if s[i] == '(': left += 1
            else: right += 1

            if left == right:
                max_len = max(max_len, right * 2)
            elif left < right:
                left = right = 0
        
        left = right = 0
        for i in range(len(s)+1):
            if s[-i] == '(': left += 1
            else: right += 1

            if left == right:
                max_len = max(max_len, right * 2)
            elif left > right:
                left = right = 0
        
        return max_len

'''
proof of validity:
Let i and j denote the starting and ending indices of the longest valid subsequence.
Note that in the forward pass after (fully) processing each character, it's always the case that left >= right. (*)
This is in particular true after processing i-1 (immediately before processing i).

Case 1: If immediately before i left = right, then the forward pass will detect the length of the longest valid subsequence.
(The number of '(' and ')' is the same for any valid subseq. Thus after processing j, left = right.)

Case 2: If immediately before i left > right, the forward pass will not detect the longest valid subsequence, but we claim the backward pass will.
Similar to observation above, note that right >= left after fully processing each element in the backward pass. We detect the longest valid subsequence in the backward pass if and only if right = left after processing j+1 (immediately before processing j).
So what if right > left (in the backward pass immediately before processing j)?
Well, then the maximality of our subsequence from i to j would be contradicted.
Namely, we can increase j to j' so that (j,j'] has one more ')' than '(', and decrease i to i', so that [i',i) has one more '(' than ')'.
The resulting subsequence from i' to j' will have longer length and will still be valid (the number of '(' and ')' will be incremented by the same amount).
Thus, either the backward pass or forward pass (possibly both) will detect the longest valid subsequence.

one can take i' = i - 1 and j' = j + 1, since

left > right immediately before i in the forward pass implies that s[i] == '(', otherwise maximality would already be contradicted (one could find i0<i such that s[i0,i) is valid, and thus s[i0,j] would be valid). Similarly
right > left immediately after j+1 (before j) in the backward pass implies s[j] == ')'
'''