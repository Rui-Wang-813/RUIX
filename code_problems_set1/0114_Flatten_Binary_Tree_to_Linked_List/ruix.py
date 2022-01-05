from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        if root == None:
            return 
        
        # first, flatten both left and right of root.
        self.flatten(root.left)
        self.flatten(root.right)
        left, right = root.left, root.right
        
        # if root does not have left, then it is already flattened.
        if left == None:
            return
        
        # otherwise, append right to the end of left.
        left_end = left
        while left_end.right != None:
            left_end = left_end.right
        left_end.right = right
        
        # set the right to be the left, and left to be None.
        root.right = left
        root.left = None