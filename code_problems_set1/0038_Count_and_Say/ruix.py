class Solution:
    def countAndSay(self, n: int) -> str:
        # base case.
        if n == 1:
            return '1'
        
        res = ''
        say = self.countAndSay(n-1)
        
        idx, current, num = 1, say[0], 1
        while True:
            # count how many numbers of current char there are.
            while idx < len(say) and say[idx] == current:
                idx += 1
                num += 1
            # add it to the result.
            res += str(num) + current

            if idx == len(say): break
            # if I've not reached the end.
            current = say[idx]
            num = 1
            idx += 1
        
        return res