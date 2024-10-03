class LazySegmentTree:
    """
    Updates can be set a range to a value or add a value to a range.
    Queries can be max, min and sum over an index range.
    Values can be any numerical values allowing max, min, and sum,
    such as integers, floating point numbers or fractions (from the class
    Fraction).
    Updates over an empty range is valid and does nothing.
    Queries over an empty range is valid and returns the neutral value -inf, +inf or 0.
    """
    def __init__(self, tab):
        """stores an integer table tab.
        will be padded to get a table with a size of a power of 2.
        :param array tab: of positive length
        """
        self.N = 1
        while self.N < len(tab):
            self.N *= 2
        self.maxval = [float('-inf')] * 2 * self.N  # init with neutral values
        self.minval = [float('+inf')] * 2 * self.N
        self.sumval = [0] * 2 * self.N
        self.lazyset = [None] * 2 * self.N
        self.lazyadd = [0] * 2 * self.N
        for i, tabi in enumerate(tab):            # initialize with given table
            j = self.N + i
            self.maxval[j] = self.minval[j] = self.sumval[j] = tabi
        for node in range(self.N - 1, 0, -1):
            self._maintain(node)                    # maintain invariant

    def _maintain(self, node):
        """maintains the invariant for the given node
        :promize: the lazy values are None/0 for this node
        """
        # requires node and its direct descends to be clean
        ll = 2 * node
        r = 2 * node + 1
        assert self.lazyset[node] is None
        assert self.lazyadd[node] == 0
        assert self.lazyset[ll] is None
        assert self.lazyadd[ll] == 0
        assert self.lazyset[r] is None
        assert self.lazyadd[r] == 0
        self.maxval[node] = max(self.maxval[ll], self.maxval[r])
        self.minval[node] = min(self.minval[ll], self.minval[r])
        self.sumval[node] = self.sumval[ll] + self.sumval[r]

    def _clear(self, node, left, right):
        """propagates the lazy updates for this node to the subtrees.
        as a result the maxval, minval, sumval values for the node
        are up to date.
        """
        if self.lazyset[node] is not None:  # first do the pending set
            val = self.lazyset[node]
            self.minval[node] = val
            self.maxval[node] = val
            self.sumval[node] = val * (right - left)
            self.lazyset[node] = None
            if left < right - 1:            # not a leaf
                self.lazyset[2 * node] = val  # propagate to direct childs
                self.lazyadd[2 * node] = 0
                self.lazyset[2 * node + 1] = val
                self.lazyadd[2 * node + 1] = 0
        if self.lazyadd[node] != 0:        # then do the pending add
            val = self.lazyadd[node]
            self.minval[node] += val
            self.maxval[node] += val
            self.sumval[node] += val * (right - left)
            self.lazyadd[node] = 0
            if left < right - 1:            # not at a leaf
                self.lazyadd[2 * node] += val  # propagate to direct childs
                self.lazyadd[2 * node + 1] += val

    def add(self, i, j, val):
        self._add(i, j, val, 1, 0, self.N)

    def set(self, i, j, val):
        self._set(i, j, val, 1, 0, self.N)

    def max(self, i, j):
        return self._max(i, j, 1, 0, self.N)

    def min(self, i, j):
        return self._min(i, j, 1, 0, self.N)

    def sum(self, i, j):
        return self._sum(i, j, 1, 0, self.N)

    def _add(self, i, j, val, node, left, right):
        self._clear(node, left, right)
        if j <= left or right <= i:
            return   # disjoint intervals, nothing to do
        if i <= left and right <= j:
            self.lazyadd[node] += val
            self._clear(node, left, right)
        else:
            mid = (right + left) // 2
            self._add(i, j, val, 2 * node, left, mid)
            self._add(i, j, val, 2 * node + 1, mid, right)
            self._maintain(node)

    def _set(self, i, j, val, node, left, right):
        self._clear(node, left, right)
        if j <= left or right <= i:
            return   # disjoint intervals, nothing to do
        if i <= left and right <= j:
            self.lazyset[node] = val
            self.lazyadd[node] = 0
            self._clear(node, left, right)
        else:
            mid = (right + left) // 2
            self._set(i, j, val, 2 * node, left, mid)
            self._set(i, j, val, 2 * node + 1, mid, right)
            self._maintain(node)

    def _max(self, i, j, node, left, right):
        if j <= left or right <= i:
            return float('-inf')   # neutral value for max
        self._clear(node, left, right)
        if i <= left and right <= j:
            return self.maxval[node]
        else:
            mid = (right + left) // 2
            a = self._max(i, j, 2 * node, left, mid)
            b = self._max(i, j, 2 * node + 1, mid, right)
            return max(a, b)

    def _min(self, i, j, node, left, right):
        if j <= left or right <= i:
            return float('+inf')   # neutral value for min
        self._clear(node, left, right)
        if i <= left and right <= j:
            return self.minval[node]
        else:
            mid = (right + left) // 2
            a = self._min(i, j, 2 * node, left, mid)
            b = self._min(i, j, 2 * node + 1, mid, right)
            return min(a, b)

    def _sum(self, i, j, node, left, right):
        if j <= left or right <= i:
            return 0               # neutral value for sum
        self._clear(node, left, right)
        if i <= left and right <= j:
            return self.sumval[node]
        else:
            mid = (right + left) // 2
            a = self._sum(i, j, 2 * node, left, mid)
            b = self._sum(i, j, 2 * node + 1, mid, right)
            return a + b


tree = LazySegmentTree([0]*8)
# (i, j, tree.max(i, j), tree.min(i, j), tree.sum(i, j)))
# tree.add(i, j, int(t[3]))
# tree.set(i, j, int(t[3]))
