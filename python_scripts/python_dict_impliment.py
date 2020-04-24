import os
import math


class DictObj(object):
    default_size = 8 

    def __init__(self):
        # [stauts, key, value]
        # status 0-未使用，1-已使用，2-已删除
        self.size = self.default_size
        self.data_list = self._genrate_data_list()
    
    def _genrate_data_list(self):
        return [[0, None, None] for _ in range(self.size)]

    def _probing(self, j):
        # 探测方法
        i = math.log(self.size, 2)
        return int(((5*j)+1) % 2**i)

    def __setitem__(self, key, value):
        # 检查占用率
        if(self._full_rate()> 2/3):  # 扩容
            self._expand_datalist()
        key_hash = hash(key)
        origin_index = key_hash & self.size - 1
        index = self._get_insert_index(origin_index, key_hash)
        self.data_list[index] = [1, key, value]
        print("key: {}, orgin_index: {}, index: {}".format(key, origin_index, index))
        return index

    def __getitem__(self, key):
        key_hash = hash(key)
        origin_index = key_hash & self.size - 1
        index = self._get_find_index(origin_index, key_hash)
        data = self.data_list[index]
        if data[0] in (0, 2):
            raise Exception("KeyError: {}".format(key))
        return self.data_list[index]

    def _full_rate(self):
        return self._used_slots() / self.size

    def _used_slots(self):
        return len([_ for _ in self.data_list if _[0] in (1,2)])

    def _filled_slots(self):
        return len([_ for _ in self.data_list if _[0] == 1])

    def _expand_datalist(self):
        print("---扩容---")
        old_data_list = self.data_list
        i = int(math.log(self.size, 2))
        expand_num = 2 if self._used_slots() > 50000 else 4
        while True:
            i += 1
            new_size = 2 ** i
            if new_size >= expand_num * self._used_slots():
                self.size = new_size
                self.data_list = self._genrate_data_list()
                break
        # 将以前的数据迁移过去
        for x in old_data_list:
            if x[0] == 1:
                self[x[1]] = x[2]

    def _get_insert_index(self, index, key_hash):
        status, k, v = self.data_list[index]
        if status == 0:  # 空slot直接插入
            pass
        elif status in (1, 2):  # 占用或dummy状态，探测下一个
            if status == 1 and key_hash == hash(k):
                pass
            else:
                prob_index = self._probing(index)
                index = self._get_insert_index(prob_index, key_hash)
        else:
            raise Exception("Wrong status: {}".format(status))
        return index

    def _get_find_index(self, index, key_hash):
        status, k, v = self.data_list[index]
        if status == 0:  # 空slot直接返回
            pass
        elif status in (1, 2):  # 占用或dummy状态，探测下一
            if key_hash != hash(k):
                index = self._get_find_index(self._probing(index), key_hash)
        else:
            raise Exception("Wrong status: {}".format(status))
        return index
    
    def __str__(self):
        return "{}".format({x[1]:x[2] for x in self.data_list if x[0] == 1})
    
    def items(self):
        return [[x[1], x[2]] for x in self.data_list if x[0] == 1]

    def keys(self):
        return [x[1] for x in self.data_list if x[0] == 1]

    def values(self):
        return [x[2] for x in self.data_list if x[0] == 1] 

    def __len__(self):
        return self._filled_slots()

    def __delitem__(self, key):
        key_hash = hash(key)
        origin_index = key_hash & self.size - 1
        index = self._get_find_index(origin_index, key_hash)
        data = self.data_list[index]
        if data[0] in (0, 2):
            raise Exception("KeyError: {}".format(key))
        else:
            self.data_list[index] = [2, data[1], data[2]]

if __name__ == "__main__":
    d = DictObj()
    d["a"] = "name_a"
    d["b"] = "name_b"
    d["c"] = "name_c"
    d["d"] = "name_d"
    d["e"] = "name_e"
    d["f"] = "name_f"
    d[1] = "name_1"
    d[2] = "name_2"
    d[3] = "name_3"
    d[4] = "name_4"
    d[5] = "name_5"
    d[6] = "name_6"
    d[7] = "name_7"
    d[8] = "name_8"
    d[9] = "name_9"
    d[10] = "name_10"
    # print(d)
    # print(d[9])
    # print(d["a"])
    # print(d["b"])
    # print(d["c"])
    # print(d["d"])
    # print(d["e"])
    # print(d["f"])
    # print(d["g"])
    d["a"] = "name_a_2"
    d[10] = "name_10_2"


    # print(len(d))
    # del d["x"]
    # print(len(d))
    # print(d.items())
    print(d)
    # print(d.keys())
    # print(d.values())