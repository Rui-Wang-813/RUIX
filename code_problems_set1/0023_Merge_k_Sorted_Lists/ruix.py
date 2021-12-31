from typing import List, Optional

# Definition for singly-linked list.
class ListNode:
     def __init__(self, val=0, next=None):
         self.val = val
         self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        n = len(lists)
        head_nodes = [lists[i] for i in range(n) if lists[i]]   # the nodes remained to be compared.

        num_reached_end = n - len(head_nodes)   # number of linked lists that already reached the end.

        # head is the head of the returned list, temp is something we'll move to add things at the tail
        # of the linked list.
        head, temp = None, None
        while num_reached_end < n:
            # find the node in the nodes to compare with smallest value.
            min_idx = min([i for i in range(len(head_nodes))], key=lambda i: head_nodes[i].val)
            min_node = head_nodes[min_idx]

            if temp:
                # if the head is already intialized.
                #
                # it is OK to directly use the node because temp.next is already in the list of nodes to
                # be compared.
                temp.next = min_node    
                temp = temp.next
            else:
                # if the head has not been initialized.
                head = min_node
                temp = head
            
            if min_node.next == None:
                # this linked list has reached its end. pop it and num_reached_end += 1
                head_nodes.pop(min_idx)
                num_reached_end += 1
            else:
                # otherwise, store the next node of min_node into the nodes to be compared.
                head_nodes[min_idx] = min_node.next
        
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

sol = Solution()
linkedLists = sol.constructLists([[1,4,5],[1,3,4],[2,6]])
sol.printLinkedList(sol.mergeKLists(linkedLists))