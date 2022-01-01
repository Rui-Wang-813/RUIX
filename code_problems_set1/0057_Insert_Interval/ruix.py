from typing import List

class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        a = newInterval

        # use binary search to find where to insert.
        def binary_search_insert(i: int, j: int) -> int:
            n = j - i
            if n == 0:
                # zero gap, just insert at i.
                return i
            if n == 1:
                # length 1, insert at i or i+1 depending on intervals[i][0].
                return i if intervals[i][0] >= a[0] else i+1

            # the mid index of [i,j).
            mid = (n//2 if n%2 else n//2 - 1) + i

            b = intervals[mid]
            if b[0] > a[0]:
                # should insert left of mid.
                return binary_search_insert(i, mid)
            elif b[0] < a[0]:
                # should insert right of mid.
                return binary_search_insert(mid+1, j)
            else:
                # just insert at mid. (push the original mid to right)
                return mid
        
        idx = binary_search_insert(0, len(intervals))   # find where to insert.

        ans = intervals[:idx]   # first get the left half of the answer.
        
        # the original intervals do not have overlap, so check if new interval has overlap with any
        # interval in the right half of intervals.
        while idx < len(intervals):
            b = intervals[idx]
            if a[1] >= b[0] and a[1] < b[1]:
                # new interval overlaps but do not cover the interval, set the upper bound of new 
                # interval to be same as this interval.
                a[1] = b[1]
                idx += 1
            elif a[1] < b[0]:
                break
            else:
                # new interval covers this interval, just skip it.
                idx += 1
        
        # decide if new interval overlaps with the last one before it.
        if len(ans) and ans[-1][1] >= a[0]:
            # the last one overlaps with new interval, choose the larger upper bound to be the new
            # upper bound of the last interval, now the new interval is already merged.
            ans[-1][1] = max(ans[-1][1], a[1])
        else:
            # the last one does not overlap with new interval, just append the new interval.
            ans.append(a)
        
        return ans + intervals[idx:]    # concatenate the left and right half of answer.

intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]]
newInterval = [4,8]

sol = Solution()
print(sol.insert(intervals, newInterval))