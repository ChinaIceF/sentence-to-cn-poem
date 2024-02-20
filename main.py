import numpy
import pinyin
import model
import pickle

class Model_ND(object):
    def __init__(self, data, d):
        self.data = data
        self.d = d
        values = pinyin.pinyin.pinyin_dict.values()
        self.all_values_from_dict = []
        for v in values:
            if (v in self.all_values_from_dict) == False:
                self.all_values_from_dict.append(v)

        self.all_pinyin = self.all_values_from_dict
        self.all_pinyin_dict = dict(zip(self.all_pinyin, list(range(len(self.all_pinyin)))))

    def getP(self, pin):
        if self.d == 2:
            return self.data[self.all_pinyin_dict[pin[0]]][self.all_pinyin_dict[pin[1]]]
        if self.d == 1:
            return self.data[self.all_pinyin_dict[pin]]

    def getP_char(self, pin):
        if self.d == 2:
            comb = self.data[self.all_pinyin_dict[pin[0]]][self.all_pinyin_dict[pin[1]]]
            res = []
            for t, p in comb:
                res.append((chr(t[0]) + chr(t[1]), p))
            return res

        if self.d == 1:
            comb = self.data[self.all_pinyin_dict[pin]]
            res = []
            for t, p in comb:
                res.append((chr(t), p))
            return res

def get_pinyin(text):
    return pinyin.get(text, delimiter = ' ', format = 'strip').split(' ')

def progress(pin, model_2d, level = -1, head_char = -1, p_now = 1, p_all = 0):
    feed = 0.00000001
    level += 1
    if level >= len(pin)-1:
        return p_now

    uni_and_p = model_2d.getP([pin[level], pin[level+1]])
    for u, p in uni_and_p:
        if head_char == u[0] or head_char == -1:  # 符合条件
            p_post = p_now * p * 1 / (1 + feed)  # 小概率事件，重新分配概率
            #print(level, p_post)
            p_all += progress(pin, model_2d, level = level, head_char = u[1], p_now = p_post, p_all = 0)
        else: # 目标词并不在模型中，激活小概率事件
            p_post = p_now * p * feed / (1 + feed)  # 小概率事件，重新分配概率
            #print(level, p_post)
            p_all += progress(pin, model_2d, level = level, head_char = u[1], p_now = p_post, p_all = 0)

    return p_all


def estimate(text, pin, model_2d):
    p_all = progress(pin, model_2d, head_char = ord(text[0]))
    print(p_all ** (1/(len(pin)-1)))

def gen_2(chars, pin, model_2d):
    uni_and_p = model_2d.getP(pin)
    items = []
    weights = []
    for u, p in uni_and_p:
        if ord(chars[0]) != u[0] and ord(chars[1]) != u[1]:
            items.append(u)
            weights.append(p)

    if len(items) == 0:
        return ''
    else:
        index = numpy.random.choice(len(items), p=weights/numpy.array(weights).sum())
        return items[index]

def gen_1(char, pin, model_1d):
    uni_and_p = model_1d.getP(pin)
    items = []
    weights = []
    for u, p in uni_and_p:
        if ord(char) != u:
            items.append(u)
            weights.append(p)

    if len(items) == 0:
        raise ValueError(char)
    else:
        index = numpy.random.choice(len(items), p=weights/numpy.array(weights).sum())
        return items[index]


with open('model_1d.pickle', 'rb') as f:
    temp_1 = pickle.load(f)
    model_1d = Model_ND(temp_1, 1)

with open('model_2d.pickle', 'rb') as f:
    temp_2 = pickle.load(f)
    model_2d = Model_ND(temp_2, 2)

if __name__ == '__main__':

    # 创建 text.txt，并取消下面注释，以学习自己的语料库

    '''
    print('Building model 1d..')
    temp_1 = model.build_model_1d('text.txt')
    model_1d = Model_ND(temp_1, 1)
    print()

    print('Building model 2d..')
    temp_2 = model.build_model_2d('text.txt')
    model_2d = Model_ND(temp_2, 2)
    print()
    '''

    # 转换工具
    while True:
        text = input(">>")
        # 获取拼音
        pinyin_of_text = get_pinyin(text)
        target_length = len(text)

        text_generated = ''
        while len(text_generated) < target_length:
            l = len(text_generated)
            if target_length - l >= 2:
                result = gen_2(text[l:l+2], pinyin_of_text[l:l+2], model_2d)
                if len(result) == 2:
                    text_generated += chr(result[0]) + chr(result[1])
                else:
                    result = gen_1(text[l], pinyin_of_text[l], model_1d)
                    text_generated += chr(result)
                    result = gen_1(text[l+1], pinyin_of_text[l+1], model_1d)
                    text_generated += chr(result)
            else:
                result = gen_1(text[l], pinyin_of_text[l], model_1d)
                text_generated += chr(result)

        print(text_generated)
