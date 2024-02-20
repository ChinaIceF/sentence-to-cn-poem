import pinyin
import numpy

#all_pinyin ='qing','li','si','nian','chun','teng','zi','jing','zhe','shou','ba','ling','jun','yue','ming','zheng','tong','ren','he','bai','fei','ju','xing','nai','zhong','xiu','yang','lou','zeng','qi','jiu','zhi','ke','tang','xian','jin','shi','fu','yu','shang','shu','zuo','wen','yi','ji','zhang','gu','hong','du','xin','fen','zhen','di','jie','heng','lu','san','jiang','er','dai','wu','hu','kong','man','yin','ou','hua','tian','bao','long','guang','she','niu','dou','xu','ru','xia','chen','fan','ta','xiong','zhou','lie','cai','chi','tai','huang','jiao','bin','zhu','dong','nan','mei','yan','gong','ya','wang','yao','lin','chan','wei','zan','xun','jia','sheng','you','yun','qian','feng','ying','gao','peng','meng','xue','ci','zong','dian','shuang','ku','zai','chu','qu','jian','xi','dao','can','cong','kai','guo','mang','ran','lai','wan','sui','bu','qin','sai','dang','niao','jue','e','beng','shan','cui','zhuang','hou','ti','zhan','xiang','gou','lian','liu','hui','ri','biao','chong','bo','ni','chuan','de','yuan','nao','chou','pan','luan','men','xie','chang','tan','huan','tu','dan','bei','hao','mu','rao','gui','ye','ting','diao','song','gua','bi','tuan','pu','xuan','ping','zhuan','lei','ge','rong','guan','mo','suo','huo','lang','chai','zhao','shun','sha','ma','cheng','le','zao','ce','shen','lao','hun','xiao','qiao','shui','duan','cang','hai','cao','mao','qiu','se','yong','ruo','han','lan','fang','bian','deng','mian','pei','fa','quan','an','juan','kan','luo','zhui','cha','pi','qie','dui','zou','ning','ai','kuo','duo','bie','geng','na','leng','liang','shuo','run','hei','ceng','ding','lve','que','die','cun','nuan','zhuo','mi','neng','zui','zu','lv','gun','bing','hen','nv','sun','rou','tou','tiao','chui','tao','ban','wo','qiang','mie','weng','chuang','piao','liao','da','qia','shao','fou','che','qiong','pian','tun','wai','cen','gan','pai','kuai','pa','kou','nong','chao','huai','min','gai','su','tui','kang','pin','kuang','keng','niang','sen','nu','sou','wa','kua','mai','cu','ze','miao','cuo','po','rang','qun','tie','kui','lun','sang','nen','gang','reng','shuai','a','nei','gen','sa','la','ne','zun','sao','pao','bang','kun','dun','zhai','zha','ben','pen','jiong','miu','rui','tuo','mou','ang','hang','pang','guai','te','re','za','ken','en','suan','ao','ruan','shai','kuan','nuo','seng','cuan','zei','zang','pou','shua','kao','zhun','gei','zen','zhua','nang','pie','fo','nie','cou','nou','chuo','chuai','nve','o','yai','zuan','ha','lia','diu','ca','shuan','ka','dia','nin',

values = pinyin.pinyin.pinyin_dict.values()
all_values_from_dict = []
for v in values:
    if (v in all_values_from_dict) == False:
        all_values_from_dict.append(v)

all_pinyin = all_values_from_dict
all_pinyin_dict = dict(zip(all_pinyin, list(range(len(all_pinyin)))))

def get_elements(alist):
    result = []
    times = []
    for o in alist:
        if (o in result) == False:
            result.append(o)
            times.append(1)
        else:
            i = result.index(o)
            times[i] += 1

    comb = [[result[i], times[i]] for i in range(len(times))]
    sorted_result = sorted(comb, key = lambda x: -times[comb.index(x)])
    return sorted_result


def get_unicode(char):
    return ord(char)

def get_py_letter(char):
    return pinyin.get(char, delimiter = ' ', format = 'strip')

def get_all_unicode_amount(file):
    arr = numpy.zeros(65536)
    file = open(file, encoding = 'utf-8')
    data = file.read().split('\n')
    for i, line in enumerate(data):
        for char in line:
            try:
                arr[get_unicode(char)] = 1
            except:
                print(i, char)

    print(sum(arr))

def build_model_1d(filename):
    d = len(all_pinyin)
    model_size = (d)
    print('Modle_size:', model_size)

    model = [[] for _ in range(d)]
    all_biaodian = ['《', '》','：', '“', '”','、','‘', '’', ',', '﹑', '.', '!', '？','！','，', '。', '；']

    file = open(filename, encoding = 'utf-8')
    data = file.read()
    for bd in all_biaodian + ['\n']:
        data = data.replace(bd, '')

    for p, c in enumerate(list(data)):
        if p % 1000 == 0:
            print('\r', round(p / len(data) * 100, 3), '%              ', end = '')
        i = all_pinyin_dict[get_py_letter(c)]
        model[i].append(get_unicode(c))

    for i in range(d):
        ele_and_times = get_elements(model[i])
        _sum = sum(numpy.array([ele_and_times[n][1] for n in range(len(ele_and_times))]))
        model[i] = [(ele_and_times[n][0], ele_and_times[n][1]/_sum) for n in range(len(ele_and_times))]

    return model

def build_model_2d(filename):

    d = len(all_pinyin)
    model_size = (d, d)
    print('Modle_size:', model_size)

    model = [[[] for _ in range(d)] for _ in range(d)]

    added_data = insert_data_2d(model, filename)
    for i in range(d):
        for j in range(d):
            ele_and_times = get_elements(added_data[i][j])
            _sum = sum(numpy.array([ele_and_times[n][1] for n in range(len(ele_and_times))]))
            added_data[i][j] = [(ele_and_times[n][0], ele_and_times[n][1]/_sum) for n in range(len(ele_and_times))]

    return added_data


def insert_data_2d(model, filename):
    all_biaodian = ['《', '》','：', '“', '”','、','‘', '’', ',', '﹑', '.', '!', '？','！','，', '。', '；']

    file = open(filename, encoding = 'utf-8')
    data = file.read()
    for bd in all_biaodian + ['\n']:
        data = data.replace(bd, ' ')
    data = data.split(' ')

    for p, unit in enumerate(data):
        if p % 100 == 0:
            print('\r', round(p / len(data) * 100, 3), '%              ', end = '')

        if len(unit) < 2:
            continue

        chars = list(unit)
        for i in range(len(chars) - 1):
            a = chars[i]
            b = chars[i+1]

            ia = all_pinyin_dict[get_py_letter(a)]
            ib = all_pinyin_dict[get_py_letter(b)]

            model[ia][ib].append((get_unicode(a), get_unicode(b)))

    return model


if __name__ == '__main__':
    print('Building model 1d..')
    model_1d = build_model_1d('no_bad_words.txt')

    print('Building model 2d..')
    model_2d = build_model_2d('no_bad_words.txt')

    while True:
            chars = input('>>>')

            if len(chars) == 2:
                comb = model_2d[all_pinyin_dict[get_py_letter(chars[0])]][all_pinyin_dict[get_py_letter(chars[1])]]
                res = []
                for t, p in comb:
                    res.append((chr(t[0]) + chr(t[1]), p))
                print(res)

            if len(chars) == 1:
                comb = model_1d[all_pinyin_dict[get_py_letter(chars[0])]]
                res = []
                for t, p in comb:
                    res.append((chr(t), p))
                print(res)

            print('error')





#get_all_unicode_amount('no_bad_words.txt')

#keys = pinyin.pinyin.pinyin_dict.keys()
#print(len(keys))
