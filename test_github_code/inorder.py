def inorder_traversal(root):
    if root is None:
        return []
    result = []
    result.extend(inorder_traversal(root.left))  # Traverse left subtree
    result.append(root.value)  # Visit the root
    result.extend(inorder_traversal(root.right))  # Traverse right subtree
    return result
