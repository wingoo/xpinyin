#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path


class Pinyin(object):
    """translate chinese hanzi to pinyin by python, inspired by flyerhzm’s
    `chinese\_pinyin`_ gem

    usage
    -----
    ::
        In [1]: from xpinyin import Pinyin
        In [2]: p = Pinyin()
        In [3]: p.get_pinyin(u"上海")
        Out[3]: 'shanghai'
        In [4]: p.get_initials(u"上")
        Out[4]: 'S'
    请输入utf8编码汉字
    .. _chinese\_pinyin: https://github.com/flyerhzm/chinese_pinyin
    """

    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
            'Mandarin.dat')

    def __init__(self):
        self.dict = {}
        for line in open(self.data_path):
            k, v = line.split('\t')
            self.dict[k] = v
    
    def get_pinyin(self, chars=u'你好', splitter=''):
        result = self.get_pinyin_list(chars)
        return splitter.join(result)

    def get_pinyin_list(self, chars=u'你好'):
        result = []
        for char in chars:
            key = "%X" % ord(char)
            try:
                result.append(self.dict[key].split(" ")[0].strip()[:-1]
                        .lower())
            except:
                result.append(char)
        return result

    def get_initials(self, char=u'你'):
        try:
            return self.dict["%X" % ord(char)].split(" ")[0][0]
        except:
            return char

    def get_community_name_pinyin(self, chars): # {{{
        """
        get community name list with pinyin for redis auto complete
        """
        all_char = [] # all include hanzi and english character
        all_char_han = [] # only has hanzi
        all_char_pin = "" # hongri hongrixiao hongrixiaoqu
        all_char_pin_han = "" # hongri hongrixiao hongrixiaoqu
        all_char_pin_first = "" #hrxq hr hrx hrxq
        all_char_pin_first_han = "" #only has hanzi

        # 0. filter the name: a-z, A-Z, and char in dict
        comm_name = u""
        for char in chars:
            i_char = ord(char)
            if 65 <= i_char <= 90 or 97 <= i_char <= 122:
                comm_name += char.lower()

            key = "%X" % i_char
            if key in self.dict:
                comm_name += char
        # end for char

        #print comm_name
        # 1. get pinyin
        str = u""
        for char in comm_name:
            i_char = ord(char)
            if 65 <= i_char <= 90 or 97 <= i_char <= 122:
                str += char.lower()
            else:
                if len(str) > 0:
                    all_char.append(str)
                    all_char_pin += str
                    all_char_pin_first += str[0]
                    str = u""
                # end if len(str) > 0

                all_char.append(char)
                all_char_han.append(char)
                #result.append([ i.strip()[:-1].lower() for i in self.dict["%X" % i_char].split(" ")]) # too much sound
                curr = self.dict["%X" % i_char].split(" ")[0].strip()[:-1].lower()
                all_char_pin += curr # only get the first pinyin
                all_char_pin_han += curr
                all_char_pin_first += curr[0]
                all_char_pin_first_han += curr[0]
            # end if 65
        # end for char
        if len(str) > 0:
            all_char.append(str)
            all_char_pin += str
            all_char_pin_first += str[0]

        #print all_char_pin
        # 2. get all char
        result = []
        al = [all_char, all_char_han, all_char_pin, all_char_pin_han, all_char_pin_first, all_char_pin_first_han]
        for arr in al:
            data = [""]
            for i in xrange(len(arr)):
                data.append(data[i] + arr[i])
            result.extend(data[1:])

        #for i in result:
        #    print i

        return set(result)
    # end def }}}
