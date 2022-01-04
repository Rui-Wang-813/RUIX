from typing import List

class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        
        # use binary search to find where I should insert num in nums1.
        def binary_find_search(i: int, j: int, num: int) -> int:
            if i == j: return i
            if i == j - 1: return i if (num < nums1[i]) else j

            n = j - i
            mid = i + (n//2 if n%2 else n//2 - 1)

            if nums1[mid] == num:
                return mid
            if nums1[mid] < num:
                return binary_find_search(mid+1, j, num)
            else:
                return binary_find_search(i, mid, num)
        
        # while I have not inserted everything in nums2 into nums1.
        while n:
            idx = binary_find_search(0, m, nums2[n-1])
            
            # move everything behind idx back 1 position.
            i = m
            while i > idx:
                nums1[i] = nums1[i-1]
                i -= 1
            nums1[idx] = nums2[n-1]

            m += 1
            n -= 1