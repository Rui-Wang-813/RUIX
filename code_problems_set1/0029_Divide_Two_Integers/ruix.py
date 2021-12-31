class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        q = 0

        a, b = abs(dividend), abs(divisor)
        while a >= b:
            temp = b
            mul = 1
            while a >= temp:
                a -= temp
                q += mul
                mul += mul
                temp += temp
        
        a = 2**31 - 1
        if abs(dividend) + b > abs(dividend + divisor):
            return max(-q, -(a+1))
        else:
            return min(q, a)