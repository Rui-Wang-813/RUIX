from typing import List

class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
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
                    search(cand[i+1:], stk + [cand[i]], target-cand[i])
                    
                    # if cand[i] is already included as the first element, there is no reason
                    # to include any i' > i s.t. cand[i']==cand[i] because any sequence starting
                    # from cand[i'] must have been considered.
                    j = i + 1
                    while j < n and cand[j] == cand[i]:
                        j += 1
                    i = j
                
        search(candidates, [], target)
        
        return res