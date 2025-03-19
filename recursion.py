def something(n):
    if n <= 0:
        return
    print(n)
    something(n-1)
    #print("Hello")
    something(n-2)

something(4)

"""
How I think this works:
1. n = 4
2. print(4)
3. something(4-1) 
    n = 3
    print(3)
    something(3-1)
    n = 2
    print(2)
    something(2-1)
    n = 1
    print(1)
    something(1-1)
    n = 0
    return #at this point something(n-1) has finished running and something(n-2) begins running
        
    
4.  n = 3 before it goes to something(n-2)
    something(3-1)
    print(1)
    something(1-2)
    n = -1
    return (stops running)
    
    when n = 2
    
    
"""
## console
# 4, 3, 2, 1