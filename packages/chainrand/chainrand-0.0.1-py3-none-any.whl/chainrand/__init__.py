class CRNG(object):
    
    """
    Verifiably-fair hybrid-chain RNG.
    
    The numbers are generated from the output bits of AES-256-CBC
    encryption on an incrementing counter with the SHA-256
    of the seed as the key.
    """
    def __init__(self, seed):
        """Construct a new CRNG object.

        Parameters
        ----------
        seed : str
            The seed for the RNG. If empty, defaults to the empty string.
        """ 
        import math
        from Crypto.Cipher import AES
        from Crypto.Hash import SHA256
        from Crypto.Util import Counter
        m = SHA256.new()
        m.update(seed.encode('utf-8'))
        self._math = math
        iv = chr(0) * 16
        self._counter = [0] * 16
        self._cipher = AES.new(m.digest(), AES.MODE_CBC, iv)
        self._offset = 0
        self._gauss_spare = 0 
        self._gauss_has_spare = False       
    
    def _is_iter(self, x):
        try:
            iter(x)
            return True
        except Exception as e:
            return False

    def _is_array(self, x):
        try:
            n = len(x)
            j = x[0] if n else 0
            return True
        except Exception as e:
            return False

    def _is_number(self, x):
        try:
            return x + 0.0 == x * 1.0
        except Exception as e:
            return False                

    def __call__(self):
        """
        Alias to random(). 
        Returns a random number uniformly distributed 
        in the interval [0.0, 1.0), in multiples of 2 ** -53.
    
        Returns
        -------
        float
            a random number uniformly distributed 
            in the interval [0.0, 1.0)
        """
        if self._offset + 8 > 16:
            self._offset = 0
        if self._offset == 0:
            cb = '%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c' % tuple(self._counter)
            self._block = self._cipher.encrypt(cb)
            i = 0
            while i < 16:
                if self._counter[i] < 255:
                    self._counter[i] += 1
                    break 
                self._counter[i] = 1
                i += 1
        b = self._block
        o = self._offset
        if isinstance(b[o], int):
            result = (
                (b[o + 1] >> 3) +
                (b[o + 2] << 5) +
                (b[o + 3] << 13) +
                (b[o + 4] << 21) +
                (b[o + 5] << 29) +
                (b[o + 6] << 37) +
                (b[o + 7] << 45) 
            )
        else:
            result = (
                (ord(b[o + 1]) >> 3) +
                (ord(b[o + 2]) << 5) +
                (ord(b[o + 3]) << 13) +
                (ord(b[o + 4]) << 21) +
                (ord(b[o + 5]) << 29) +
                (ord(b[o + 6]) << 37) +
                (ord(b[o + 7]) << 45) 
            )
        
        self._offset += 8 
        return result / 9007199254740992.0
    
    def random(self):
        """
        Returns a random number uniformly distributed 
        in the interval [0.0, 1.0), in multiples of 2 ** -53.
    
        Returns
        -------
        float
            A random number uniformly distributed 
            in the interval [0.0, 1.0)
        """
        return self()

    def randrange(self, start=None, stop=None, step=None):
        """
        Returns a random integer uniformly distributed in [start, stop).  
        The integers are spaced with intervals of |step|.
    
        Parameters
        ----------
        start : int, optional
            The start of the range. (default=`0`)
        stop : int
            The end of the range.
        step : int, optional
            The interval step. (default=`1`)
        
        Returns
        -------
        int
            A random integer uniformly distributed in [start, stop).
        """
        if not self._is_number(start):
            if not self._is_number(stop):
                return None
            start, stop = stop, start
        floor = self._math.floor
        if not self._is_number(stop):
            start, stop = 0, start
        if not self._is_number(step) or step == 0:
            step = 1
        if stop < start:
            step = -step
        d = floor(abs(float(stop - start) / step))
        return int(floor(start + floor(d * self()) * step))

    def randint(self, a=None, b=None):
        """
        Returns a random integer uniformly distributed in [start, stop].  
        The integers are spaced with intervals of |step|.
    
        Parameters
        ----------
        start : int, optional
            The start of the range. (default=`0`)
        stop : int
            The end of the range.
        
        Returns
        -------
        int
            A random integer uniformly distributed in [start, stop].
        """
        if not self._is_number(a):
            if not self._is_number(b):
                return None
            a, b, = b, a
        if not self._is_number(b):
            a, b = 0, a
        if b < a:
            a, b = b, a
        return int(self._math.floor(a + (b + 1 - a) * self()))

    def shuffle(self, x):
        """
        Shuffles the array in-place.

        Parameters
        ----------
        population : list
            The population.


        Returns
        -------
        None
        """
        i = len(x) - 1 
        while i > 0:
            j = int((i + 1) * self())
            x[i], x[j] = x[j], x[i]
            i -= 1
        return x

    def sample(self, population, k=1, weights=None):
        """
        Returns `k` random elements from the population, 
        sampling **without** replacement.

        If `k` is more than the length of the population, 
        only `k` elements will be returned.

        If weights is not provided, every element of population 
        will be equally weighted.

        If weights is a non-empty array and is of different 
        length to population,  
        only the first `Math.min(population.length, weights.length)` 
        elements of population are sampled.

        If the sum of the weights is less than or equal to zero,  
        every element of population will be equally weighted.

        Parameters
        ----------
        population : list
            The population.
        k : int
            The number of elements to choose.
        weights : list<float>, optional
            The weights of the population. 

        Returns
        -------
        list 
            An array of `k` random elements from the population.
        """
        weights_sum = 0
        collected = []
        weights_is_iter = self._is_iter(weights)
        weights_is_array = self._is_array(weights)
        population_is_iter = self._is_iter(population)
        population_is_array = self._is_array(population)

        if not population_is_iter:
            return collected
        if not population_is_array:
            population = list(population)
        n = len(population)
        if weights_is_iter and not weights_is_array:
            weights = list(weights)
        weighted = weights_is_iter
        if weighted:
            n = min(n, len(weights))
            weights_sum = sum(weights[:n])
            weighted = weights_sum > 0
        if not weighted:
            n = len(population)
            weights_sum = n 
        k = max(0, (k if self._is_number(k) else 1))

        visited = [False] * n
        for j in range(k):
            r = weights_sum * self()
            for i in range(n):
                if not visited[i]:
                    r -= weights[i] if weighted else 1 
                    if r < 0:
                        collected.append(population[i])
                        weights_sum -= weights[i] if weighted else 1 
                        visited[i] = True
                        break
        if len(collected) < k:
            for i in range(n):
                if not visited[i]:
                    collected.append(population[i])
        return self.shuffle(collected)

    def choice(self, population, weights=None):
        """
        Returns a random element from the population.

        If weights is not provided, every element of population will be equally weighted.

        If weights is a non-empty array and is of different length to population,  
        only the first `Math.min(population.length, weights.length)` elements of population are sampled.

        If the sum of the weights is less than or equal to zero,  
        every element of population will be equally weighted.

        Parameters
        ----------
        population : list
            The population.
        weights : list<float>, optional
            The weights of the population. 

        Returns
        -------
        mixed
            A random element in the population.
        """
        collected = self.sample(population, 1, weights)
        return collected[0] if len(collected) else None

    def gauss(self, mu=None, sigma=None):
        """
        Normal distribution, also called the Gaussian distribution. 

        Parameters
        ----------
        mu : float, optional
            The mean. (default=`0.0`)
        sigma : float, optional
            The standard deviation. (default=`1.0`)

        Returns
        -------
        float
            A random number from the Gaussian distribution.
        """
        if not self._is_number(sigma):
            sigma = 1 
        if not self._is_number(mu):
            mu = 0 
        if self._gauss_has_spare:
            self._gauss_has_spare = False
            return self._gauss_spare * sigma + mu 
        while 1:
            u = 2 * self() - 1
            v = 2 * self() - 1
            s = u * u + v * v
            if not (s >= 1 or s == 0):
                break
        s = self._math.sqrt(-2.0 * self._math.log(s) / s)
        self._gauss_has_spare = True 
        self._gauss_spare = v * s 
        return u * s * sigma + mu
