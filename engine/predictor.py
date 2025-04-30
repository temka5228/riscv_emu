from river import linear_model, compose, preprocessing, metrics, tree

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
        
class BimodalPredictor:
    def __init__(self, bht_bits=10):
        self.bht_bits = bht_bits
        self.bht_size = 1 << bht_bits
        self.bht = [1] * self.bht_size

    def _index(self, pc):
        return (pc >> 2) ^ (self.bht_size - 1)
    
    def predict(self, pc):
        return bool(self.bht[self._index(pc)])
    
    def update(self, pc, taken):
        self.bht[self._index(pc)] = 1 if taken else 0

class MLPredictor:
    def __init__(self):
        self.last_branch = {}
        self.model = compose.Pipeline(
            preprocessing.StandardScaler(),
            linear_model.LogisticRegression()
        )
        self.last_predict = 0
        self.metric = metrics.R2()

    def predict(self, pc):
        x = self.last_branch.copy()
        x['pc'] = pc % 64
        self.last_predict = self.model.predict_one(x)
        return self.last_predict
    
    def update(self, pc, taken):
        #self.metric.update(taken, self.model.predict_one(self.last_branch)) 
        self.model.learn_one(self.last_branch, taken)
        
        #print(self.metric)

    def update_last_branch(self, x:dict):
        self.last_branch = {'pc': x['pc']}

        for i in range(len(x['pred_json'])):        
            self.last_branch[f'pred_json_{i}'] = int(x['pred_json'][i])
        
        for i in range(len(x['pred_all'])):
            self.last_branch[f'pred_all_{i}'] = int(x['pred_all'][i])
