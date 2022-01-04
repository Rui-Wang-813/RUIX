from typing import Optional, List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:

        # helper function to do the validation.
        def validate(root: Optional[TreeNode], lb: float, ub: float) -> bool:
            if not root: return True
            # in this case, the value of root is out of the range it is supposed to be.
            if root.val <= lb or root.val >= ub: return False

            # left and right subtrees have to be valid, and any element in left subtress has to be < root
            # value, any element in right subtree has to be > root value.
            if validate(root.left, lb, root.val) and validate(root.right, root.val, ub):
                return True
            return False
        
        return validate(root, float('-inf'), float('inf'))