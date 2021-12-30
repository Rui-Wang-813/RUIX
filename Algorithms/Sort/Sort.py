from typing import List

class Sort:

    def bubble_sort(self, nums: List[int]) -> List[int]:
        n = len(nums)

        i = 0
        while i < n-1:
            j = 0
            # this ensures that nums[n-1-i] has n-i th largest element.
            while j < n-1-i:
                if nums[j] > nums[j+1]:
                    nums[j], nums[j+1] = nums[j+1], nums[j]
                j += 1
            i += 1
        
        return nums
    
    def selection_sort(self, nums: List[int]) -> List[int]:
        n = len(nums)
        
        for i in range(n-1):
            j = min(range(i,n), key=lambda i: nums[i])  # get the index of the min element in nums[i:]
            nums[i], nums[j] = nums[j], nums[i] # this ensures that nums[i] has (i+1)th min element.
        
        return nums
    
    def insertion_sort(self, nums: List[int]) -> List[int]:
        n = len(nums)

        i = 0
        while i < n-1:
            a = nums[i+1]   # the element to be inserted.

            # this ensures that either j=0 or nums[j] <= nums[i+1]
            j = i
            while j >= 0 and nums[j] > a:
                nums[j+1] = nums[j]
                j -= 1

            nums[j+1] = a   # insert a into position j+1.
            # this ensures that nums[:i+2] is in ascending order.

            i += 1
        
        return nums
    
    def shell_sort(self, nums: List[int]) -> List[int]:
        n = len(nums)

        step = n // 2       # step size starts from n//2.
        while step >= 1:
            start_idx = 0   # starting index of current iteration.
            # starting index can only be < step.
            while start_idx < step:

                # implement an insertion sort starting from start_idx.
                i = start_idx
                while i < n-step:
                    a = nums[i+step]

                    j = i
                    while j >= 0 and nums[j] > a:
                        nums[j+step] = nums[j]
                        j -= step

                    nums[j+step] = a

                    i += step

                start_idx += 1
            
            step //= 2
        
        return nums
    
    def quick_sort(self, nums: List[int]) -> List[int]:

        def do_quick_sort(nums: List[int], lb: int, ub: int) -> None:
            if lb >= ub:
                return

            # i is left pointer; j is right pointer.
            i, j = lb, ub
            pivot = nums[i] # choose the first element to be pivot. Can have different strategies.

            while i < j:

                # find the first element < pivot on right, put it into left pointer.
                while i < j and nums[j] >= pivot:
                    j -= 1
                if i < j:
                    nums[i] = nums[j]
                    i += 1
                
                # find the first element > pivot on left, put it into right pointer.
                while i < j and nums[i] <= pivot:
                    i += 1
                if i < j:
                    nums[j] = nums[i]
                    j -= 1
                
                # this ensures that for any i' such that i' < i, nums[i'] <= pivot, for any j' such that
                # j' > j, nums[j'] >= pivot.
            
            nums[i] = pivot # now i = j.

            do_quick_sort(nums, lb, i-1)
            do_quick_sort(nums, i+1, ub)

        do_quick_sort(nums, 0, len(nums)-1) # do not use slicing. It costs too much more time and space.

        return nums

    def merge_sort(self, nums: List[int]) -> List[int]:

        # helper function to merge two sorted lists.
        def merge_sorted_lists(arr1: List[int], arr2: List[int]) -> List[int]:
            arr = []

            n, m = len(arr1), len(arr2)
            i, j = 0, 0

            while i < n and j < m:
                # append min(arr1[i], arr2[j]) into arr.
                if arr1[i] < arr2[j]:
                    arr.append(arr1[i])
                    i += 1
                else:
                    arr.append(arr2[j])
                    j += 1
            
            # in case arr1 still has remaining elements.
            while i < n:
                arr.append(arr1[i])
                i += 1
            # in case arr2 still has remaining elements.
            while j < m:
                arr.append(arr2[j])
                j += 1
            
            return arr

        n = len(nums)
        if n <= 1:
            return nums
        
        # sort the two halves first.
        mid = n//2
        a = self.merge_sort(nums[:mid])
        b = self.merge_sort(nums[mid:])

        return merge_sorted_lists(a, b) # then merge the two sorted halves.
    
    # array as heap:
    #
    # root is at nums[0]
    # left child of nums[i] is nums[i*2 + 1]
    # right child of nums[i] is nums[i*2 + 2]
    # parent of nums[i] is nums[(i-1)//2]
    #
    # idea: make a max heap first, then take out its first element each time, then fix the remaining
    # heap.
    def heap_sort(self, nums: List[int]) -> List[int]:
        
        def fix_max_heap(i: int, n: int) -> None:

            j = i*2 + 1 # left child of node i.
            while j < n:
                # make j to be the larger child of node i.
                if (j < n-1 and nums[j+1] > nums[j]):
                    j += 1
                
                # this means heap starting at node i is already a max heap.
                if nums[i] >= nums[j]:
                    break

                nums[i], nums[j] = nums[j], nums[i] # move down the larger node.
                
                i = j
                j = i*2 + 1
            
        def make_max_heap() -> None:
            n = len(nums)
            i = (n-1) // 2  # make i to be the parent of the very last node of the heap (not yet max).

            # bottom up. make sure the heap starting at node i is max heap.
            while (i >= 0):
                fix_max_heap(i, n)
                i -= 1
        
        make_max_heap()     # turn nums into a max heap.

        n = len(nums)
        i = n - 1
        while i > 0:
            nums[0], nums[i] = nums[i], nums[0]     # take the root (max) to ith position.
            fix_max_heap(0, i)  # cut off the nums[i:] as they've already been the right sequence.
            i -= 1

        return nums
    
    def radix_sort(self, nums: List[int]) -> List[int]:
        flag = True                         # use flag to see if max radix has been achieved.
        base = 10                           
        rtok = 1                            # this is the radix.
        temp = [0 for _ in range(len(nums))]
        
        while flag:
            flag = False
            cnt = [0 for _ in range(10)]    # initialize cnt to have all 0's.

            # first, make cnt[i] be the number of elements with corresponding digit to be i.
            for n in nums:
                d = (n//rtok) % base
                cnt[d] += 1
                if d: flag = True

            # make cnt[i] to be the number of elements with corresponding digit to be <= i.
            for i in range(1, 10):
                cnt[i] += cnt[i-1]

            # puts nums[idx] at the last position assigned to its bin, which is cnt[(nums[idx]//rtok)%base].
            # i = (nums[idx]//rtok)%base is the corresponding digit of nums[idx], and cnt[i] records the last
            # position in nums assigned to set of nums elements with corresponding digit to be <= i.
            for i in range(len(nums)):
                idx = len(nums) - 1 - i
                cnt[(nums[idx]//rtok)%base] -= 1
                temp[cnt[(nums[idx]//rtok)%base]] = nums[idx]
            
            # put temp elements back to nums.
            for i in range(len(nums)):
                nums[i] = temp[i]
            
            # move the position forward.
            rtok *= base
        
        return nums