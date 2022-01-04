class Solution:
    def mySqrt(self, x: int) -> int:
        if x <= 1: return x
        
        # make it a binary search in range[0,x//2]
        i, j = 0, x//2 + 1
        while i < j:
            n = j - i
            mid = i + n//2
            
            num = mid * mid
            if num == x:
                return mid
            if num < x:
                i = mid + 1
            elif num > x:
                j = mid
        
        return i - 1    # as we want to simply ignore the decimal part, we take i-1.