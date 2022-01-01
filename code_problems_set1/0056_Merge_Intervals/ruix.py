from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda a: a[0])
        
        i = 0
        while (i < len(intervals)-1):
            a, b = intervals[i], intervals[i+1]
            if a[1] >= b[1]:
                intervals.remove(b)
            elif a[1] >= b[0] and a[1] <= b[1]:
                a[1] = b[1]
                intervals.remove(b)
            else:
                i += 1
        
        return intervals