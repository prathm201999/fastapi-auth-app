def postorder_traversal(root):
    if root is None:
        return []
    result = []
    result.extend(postorder_traversal(root.left))  # Traverse left subtree
    result.extend(postorder_traversal(root.right))  # Traverse right subtree
    result.append(root.value)  # Visit the root
    return result
