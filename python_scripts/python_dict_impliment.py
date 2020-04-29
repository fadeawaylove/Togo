import os
import math
import unittest

ENTRY_STATUS_DUMMY = "asjddh"  # 标识me_key为dummy状态


class DictEntry(object):

    def __init__(self, **kwargs):
        self.me_key = kwargs.get("me_key")
        self.me_hash = kwargs.get("me_hash") or (hash(self.me_key) if self.me_key is not None else self.me_key)
        self.me_value = kwargs.get("me_value")

    def from_new(self, new_slot):
        self.me_key = new_slot.me_key
        self.me_hash = new_slot.me_hash
        self.me_value = new_slot.me_value

    @property
    def is_active(self):
        return True if (self.me_key is not None and self.me_value is not None and self.me_key != ENTRY_STATUS_DUMMY) else False

    @property
    def is_unused(self):
        return True if self.me_key == self.me_value == None else False

    @property
    def is_dummy(self):
        return True if self.me_key == ENTRY_STATUS_DUMMY and self.me_value is None else False

    def __str__(self):
        return "{}: {}".format(self.me_key, self.me_value)

class DictObj(object):
    min_size = 8 

    def __init__(self):
        self.ma_smalltable = self._generate_table(self.min_size)  # 创建字典对象时，一定会创建一个大小为PyDict_MINSIZE==8的PyDictEntry数组。
        self.ma_fill = 0  # 所有处于Active以及Dummy的元素个数
        self.ma_used = 0 # 所有处于Active状态的元素个数
        self.ma_mask = self.min_size # 所有entry的元素个数（Active+Dummy+Unused）
        self.ma_table = self.ma_smalltable
    
    def _generate_table(self, size):
        return [DictEntry() for _ in range(size)]

    def _probing(self, j, size):
        # 探测方法
        i = math.log(size, 2)
        return int(((5*j)+1) % 2**i)

    def __setitem__(self, key, value):
        # 检查占用率
        if(self.ma_used / self.ma_mask > 2/3):  # 扩容
            self._expand_datalist()
        index = self._look_dict(key)
        slot = self.ma_table[index]
        if slot.is_active:
            slot.me_value = value
        elif slot.is_dummy or slot.is_unused:
            if slot.is_unused:
                self.ma_fill += 1
            self.ma_used += 1
            slot.from_new(DictEntry(me_key=key, me_value=value))
        # print("key: {}, index: {}".format(key, index))
        

    def __getitem__(self, key):
        index = self._look_dict(key)
        slot = self.ma_table[index]
        if slot.is_active:
            return slot.me_value
        else:
            raise Exception("Key error! [{}]".format(key))

    def _expand_datalist(self):
        print("---扩容---")
        old_table = self.ma_table
        i = int(math.log(self.ma_mask, 2))
        expand_num = 2 if self.ma_used > 50000 else 4
        while True:
            i += 1
            new_size = 2 ** i
            if new_size >= expand_num * self.ma_used:
                self.ma_mask = new_size
                self.ma_table = self._generate_table(new_size)
                break
        # 将以前的数据迁移过去
        self.ma_fill = self.ma_used = 0
        for old_slot in old_table:
            if old_slot.is_active:
                # self._process_insert(old_slot.me_hash & self.ma_mask - 1, old_slot)
                self[old_slot.me_key] = old_slot.me_value
    
    def _look_dict(self, key):
        key_hash = hash(key)
        origin_index = key_hash & self.ma_mask - 1
        # print("key: {}, origin_index: {}".format(key, origin_index))
        return self._real_look_dict(origin_index, key_hash)

    def _real_look_dict(self, index, key_hash):
        slot = self.ma_table[index]
        if slot.is_active or slot.is_dummy:  # active或者dummy
            if slot.me_hash != key_hash:
                next_index = self._probing(index, self.ma_mask)
                index = self._real_look_dict(next_index, key_hash)
        return index
    
    def __str__(self):
        return "{}".format({slot.me_key:slot.me_value for slot in self.ma_table if slot.me_key is not None and slot.me_value is not None})
    
    def items(self):
        return [(slot.me_key, slot.me_value) for slot in self.ma_table if slot.is_active]

    def keys(self):
        return [slot.me_key for slot in self.ma_table if slot.is_active]

    def values(self):
        return [slot.me_value for slot in self.ma_table if slot.is_active]

    def __len__(self):
        return self.ma_used

    def __delitem__(self, key):
        index = self._look_dict(key)
        slot = self.ma_table[index]
        if slot.is_active:
            slot.me_key = ENTRY_STATUS_DUMMY
            slot.me_value = None
            self.ma_used -= 1
        else:
            raise Exception("Key error! [{}]".format(key))


class TextDictObj(unittest.TestCase):

    def set_values(self):
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
        return d

    def test_set(self):
        d = DictObj()
        d["a"] = "name_a"
        
    def test_get(self):
        d = DictObj()
        d["a"] = "name_a"
        self.assertEqual(d["a"], "name_a")

    def test_keys(self):
        d = self.set_values()
        print(d.keys())

    def test_items(self):
        d = self.set_values()
        print(d.items())

    def test_values(self):
        d = self.set_values()
        print(d.values())
    
    def test_del(self):
        d = self.set_values()
        del d["a"]
        with self.assertRaises(BaseException):
            d["a"]

    def test_len(self):
        d = self.set_values()
        l1 = len(d)
        del d["a"]
        l2 = len(d)
        self.assertEqual(l1-l2, 1)

if __name__ == "__main__":
    unittest.main()
