from typing import *

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.ans = float('-inf')

        # the returned value of this function is the largest sum of path ending at root.
        # this value can be used to calculate the left and right value of some root.
        def postorder_dfs(root: TreeNode) -> int:
            if not root: return 0

            left = max(0, postorder_dfs(root.left))
            right = max(0, postorder_dfs(root.right))

            # self.ans records all possible values.
            self.ans = max(self.ans, left + right + root.val)

            return max(left, right) + root.val

        postorder_dfs(root)
        return self.ans
    
    def constructBSTFromList(self, tree: List[int]) -> TreeNode:
        if len(tree) == 0: return None

        root = TreeNode(tree[0])
        stk = [root]
        idx = 1

        layer_size = 1
        while True:
            for i in range(layer_size):
                if (idx == len(tree)): return root

                node = (TreeNode(tree[idx]) if tree[idx] else None)
                stk[i].left = node
                stk.append(node)

                idx += 1
                if (idx == len(tree)): return root

                node = (TreeNode(tree[idx]) if tree[idx] else None)
                stk[i].right = node
                stk.append(node)

                idx += 1

            stk = stk[layer_size:]
    
    def printBST(self, root: Optional[TreeNode]) -> None:

        def printer(node: Optional[TreeNode], indent: int) -> None:
            if node == None: return

            print(' ' * indent + f'{node.val:<3}')
            printer(node.left, indent + 3)
            printer(node.right, indent + 3)
        
        printer(root, 0)

sol = Solution()
root = sol.constructBSTFromList([10,9,20,None,None,15,7])
sol.printBST(root)
print(sol.maxPathSum(root))