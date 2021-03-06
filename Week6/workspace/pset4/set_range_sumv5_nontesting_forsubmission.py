# python3

from sys import stdin
#from wx import NullAcceleratorTable

# Splay tree implementation

# Vertex of a splay tree
class Vertex:
    def __init__(self, key, sum, left, right, parent):
        (self.key, self.sum, self.left, self.right, self.parent) = (key, sum, left, right, parent)

def update(v):
    if v == None:
        return
    v.sum = v.key + (v.left.sum if v.left != None else 0) + (v.right.sum if v.right != None else 0)
    if v.left != None:
        v.left.parent = v
    if v.right != None:
        v.right.parent = v

def smallRotation(v):
    parent = v.parent
    if parent == None:
        return
    grandparent = v.parent.parent
    if parent.left == v:
        m = v.right
        v.right = parent
        parent.left = m
    else:
        m = v.left
        v.left = parent
        parent.right = m
    update(parent)
    update(v)
    v.parent = grandparent
    if grandparent != None:
        if grandparent.left == parent:
            grandparent.left = v
        else: 
            grandparent.right = v

def bigRotation(v):
    if v.parent.left == v and v.parent.parent.left == v.parent:
    # Zig-zig
        smallRotation(v.parent)
        smallRotation(v)
    elif v.parent.right == v and v.parent.parent.right == v.parent:
    # Zig-zig
        smallRotation(v.parent)
        smallRotation(v)    
    else: 
    # Zig-zag
        smallRotation(v)
        smallRotation(v)



def splay(v):
    if v == None:
        return None
    while v.parent != None:
        if v.parent.parent == None:
            smallRotation(v)
            break
        bigRotation(v)
    return v


# Searches for the given key in the tree with the given root
# and calls splay for the deepest visited node after that.
# Returns pair of the result and the new root.
# If found, result is a pointer to the node with the given key.
# Otherwise, result is a pointer to the node with the smallest
# bigger key (next value in the order).
# If the key is bigger than all keys in the tree,
# then result is None.
def find(root, key):
    if root == None:
        return (None, None) 
    v = root
    last = root
    next = None
    while v != None:
        if v.key >= key and (next == None or v.key < next.key):
            next = v    
        last = v
        if v.key == key:
            break    
        if v.key < key:
            v = v.right
        else: 
            v = v.left
    #root = splay(next)      
    root = splay(last)
    update(root)
    return (next, root)

def split(root, key):
    if root == None:
        left = None
        right = None
        return (left, right) 
    (result, root) = find(root, key)  
    if result == None:    
        return (root, None)  
    right = splay(result)
    left = right.left
    right.left = None
    if left != None:
        left.parent = None
    update(left)
    update(right)
    return (left, right)

  
def merge(left, right):
    if left == None:
        return right
    if right == None:
        return left
    while right.left != None:
        right = right.left
    right = splay(right)
    right.left = left
    update(right)
    return right

  
# Code that uses splay tree to solve the problem
                                    
root = None


def insert(key):
    global root
#     if root == None:
#         root = Vertex(key, key, None, None, None)
#         return
    (left, right) = split(root, key)
    new_vertex = None
    if right == None or right.key != key:
        new_vertex = Vertex(key, key, None, None, None)  
    root = merge(merge(left, new_vertex), right)
        


def search(key): 
    global root
    if root == None:
        return False
    next, root = find(root, key)
    
    #self.update(self.root)
    if next == None:
        return False
    elif next.key != key:
        return False
    root = splay(next)
    update(root)
    return True     
  

def find2(root, key):
    if root == None:
        return (None, None) 
    v = root
    last = root
    next = None
    while v != None:
        if v.key >= key and (next == None or v.key < next.key):
            next = v    
        last = v
        if v.key == key:
            break    
        if v.key < key:
            v = v.right
        else: 
            v = v.left 
    splay(last)
    return next   

        
def erase(key):
    global root
    if root == None:
        return
    n, root = find(root, key)
    if n != None and n.key == key:
        next, root = find(root, key + 1)
        if next != None:
            splay(next)
            splay(n)
            n1 = n.left
            next.left = n1
            next.parent = None
            if n1 != None:
                n1.parent = next
            root = next
            update(root)
        else:
            splay(n)
            n1 = n.left
            root = n1
            if n1 != None:
                n1.parent = None
            splay(root)
    else:
        return
    update(root)      
            
        

    
def dosum(fr, to):
    global root
    if root == None:
        return 0
    (left, middle) = split(root, fr)
    (middle, right) = split(middle, to + 1)
    ans = 0
    if middle != None:
        ans += middle.sum
    result = merge(left, middle)
    root = merge(result, right)
    return ans



MODULO = 1000000001
n = int(stdin.readline())
last_sum_result = 0
for i in range(n):
    line = stdin.readline().split()
    if line[0] == '+':
        x = int(line[1])
        insert((x + last_sum_result) % MODULO)
    elif line[0] == '-':
        x = int(line[1])
        erase((x + last_sum_result) % MODULO)
    elif line[0] == '?':
        x = int(line[1])
        print('Found' if search((x + last_sum_result) % MODULO) else 'Not found')
    elif line[0] == 's':
        l = int(line[1])
        r = int(line[2])
        res = dosum((l + last_sum_result) % MODULO, (r + last_sum_result) % MODULO)
        print(res)
        last_sum_result = res % MODULO


