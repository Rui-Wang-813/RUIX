from typing import List

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        res = []
        candidates.sort()   # sort the candidates

        def search(cand: List[int], stk: List[int], target: int) -> None:
            i, n = 0, len(cand)
            while i < n:
                if cand[i] > target:
                    # as the cand is sorted, no further elements will be included.
                    return 
                if cand[i] == target:
                    # as the cand is sorted, only this element will be included
                    res.append(stk + [cand[i]])
                    return 
                else:
                    # this handles the case where cand[i] is included.
                    search(cand[i:], stk + [cand[i]], target-cand[i])
                
                i += 1

        search(candidates, [], target)
        
        return res