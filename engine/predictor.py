class GSharePredictor:
    def __init__(self, history_bits=8, bht_bits=10):
        self.history_bits = history_bits
        self.bht_bits = bht_bits
        self.ghr_mask = (1 << history_bits) - 1
        self.bht_size = 1 << bht_bits

        self.bht = [1] * self.bht_size
        self.ghr = 0

    def _index(self, pc):
        pc_low = (pc >> 2) & (self.bht_size - 1)
        return pc_low ^ self.ghr
    
    def predict(self, pc):
        idx = self._index(pc)
        ctr = self.bht[idx]
        return ctr >= 2
    
    def update(self, pc, taken):
        idx = self._index(pc)
        if taken:
            if self.bht[idx] < 3:
                self.bht[idx] += 1
        else:
            if self.bht[idx] > 0:
                self.bht[idx] -= 1
        
        self.ghr = ((self.ghr << 1) | (1 if taken else 0)) & self.ghr_mask
        