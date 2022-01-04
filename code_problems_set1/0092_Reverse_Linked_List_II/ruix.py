from typing import Optional, List

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        
        def do_reverse(node: Optional[ListNode], end: int) -> None:
            if end < 1:
                return
            if node == None or node.next == None:
                return
            
            # make sure the rest is reversed.
            do_reverse(node.next, end-1)
            
            # now, move the val at current node to the end.
            temp_v, temp_n = node.val, node
            i = 0
            while i < end:
                temp_n.val = temp_n.next.val
                temp_n = temp_n.next
                i += 1
            temp_n.val = temp_v
        
        # make sure temp to be the beginning of left.
        temp = head
        for _ in range(left-1):
            temp = temp.next

        do_reverse(temp, right-left)
        return head
    
    # helper to construct list of linked lists from list of lists.
    def constructLists(self, lists: List[List[int]]) -> List[Optional[ListNode]]:
        linkedLists = []
        for lst in lists:
            if len(lst) == 0:
                # nothing in this list, not even a head node.
                linkedLists.append(None)
            else:
                head = ListNode(lst[0])
                temp = head
                for i in range(1, len(lst)):
                    temp.next = ListNode(lst[i])
                    temp = temp.next
                linkedLists.append(head)
        
        return linkedLists
    
    # helper to print out linked list.
    def printLinkedList(self, lst: Optional[ListNode]):
        s = ""
        while lst != None:
            s += f'{lst.val} -> '
            lst = lst.next
        s = s[:-4]  # remove the last arrow.
        print(s)