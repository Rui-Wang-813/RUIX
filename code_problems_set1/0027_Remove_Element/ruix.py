from typing import List

class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        n = len(nums)
        
        # i is at head, j is at tail.
        i, j = 0, n-1
        while i < j:
            if nums[i] == val:
                # if nums[i] == val, swap nums[i] with nums[j] tails come closer. i do not increase
                # considering the possibility that original nums[j] == val.
                nums[i], nums[j] = nums[j], nums[i]
                j -= 1
            else:
                i += 1
        
        return i + 1 if nums[i] != val else i

'''
Easily proved that during the loop, everything before i is NOT val, everything after j IS val.
'''