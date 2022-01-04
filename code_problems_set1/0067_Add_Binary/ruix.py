class Solution:
    def addBinary(self, a: str, b: str) -> str:
        i, j = len(a)-1, len(b)-1
        
        res = ''
        
        c = 0
        while i >= 0 and j >= 0:
            v1, v2 = (1 if a[i] == '1' else 0), (1 if b[j] == '1' else 0)
            v = v1 + v2 + c
            
            c = v // 2
            v = v % 2
            
            res = ('1' if v else '0') + res
            
            i -= 1
            j -= 1
        
        while i >= 0:
            v = (1 if a[i] == '1' else 0) + c
            
            c = v // 2
            v = v % 2
            
            res = ('1' if v else '0') + res
            
            i -= 1
        while j >= 0:
            v = (1 if b[j] == '1' else 0) + c
            
            c = v // 2
            v = v % 2
            
            res = ('1' if v else '0') + res
            
            j -= 1
        
        if c: res = '1' + res
        return res

'''
Very straitforward, nothing to explain.
'''