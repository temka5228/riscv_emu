from river import linear_model, compose, preprocessing, metrics, optim

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
        numeric_features = ['pc', 'pred_json', 'pred_all']
        numeric_pipeline = (
            compose.Select(*numeric_features) |
            preprocessing.StandardScaler()
        )

        binary_features = [f'pred_json_{i}' for i in range(4)] + [f'pred_all_{i}' for i in range(8)]

        binary_pipeline = compose.Select(*binary_features)

        self.preprocessor = numeric_pipeline + binary_pipeline

        self.model = self.preprocessor | linear_model.LogisticRegression(l1=0.15, intercept_lr=0.000)

        '''self.model = compose.Pipeline(
            preprocessing.StandardScaler(),
            linear_model.LogisticRegression()
        )'''
        self.last_predict = 0
        self.metric = metrics.R2()

    def predict(self, x:dict):
        x = self.preprocess_x(x)
        self.last_predict = self.model.predict_one(x)
        return self.last_predict
    
    def update(self, x:dict, taken):
        x = self.preprocess_x(x)
        y_pred = self.model.predict_one(x)
        self.metric.update(taken, y_pred if y_pred != None else 0) 
        #print(y_pred, taken, self.metric)
        self.model.learn_one(x, taken)

    def preprocess_x(self, x:dict):
        x['pc'] %= 128

        for i in range(len(x['pred_json'])):        
            x[f'pred_json_{i}'] = int(x['pred_json'][i])

        for i in range(len(x['pred_all'])):
            x[f'pred_all_{i}'] = int(x['pred_all'][i])

        x['pred_json'] = int(x['pred_json'], 2)
        x['pred_all'] = int(x['pred_all'], 2)

        return x

