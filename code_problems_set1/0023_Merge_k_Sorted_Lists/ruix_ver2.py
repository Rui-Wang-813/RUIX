from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    # brute force, but much much faster. It uses provided sort method.
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        self.nodes = []
        head = point = ListNode(0)
        # first, simply add all values in all lists to one single list.
        for l in lists:
            while l:
                self.nodes.append(l.val)
                l = l.next
        # sort that list, and add one node for each element in the list in sorted sequence.
        for x in sorted(self.nodes):
            point.next = ListNode(x)
            point = point.next
        return head.next