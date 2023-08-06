def diagprod(a, B):
    '''Efficiently calculate the expression diag(a) @ B.'''
    return (a * B.T).T
