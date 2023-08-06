# import jieba
import pkuseg
from transformers import BertTokenizer, BertModel
import re


class AutoPos:
    """

    用于自动清理获取位置的函数 do_basic_tokenize

    """

    def __init__(self, seg=None, tokenizer=None):
        if seg == None:
            self.seg = pkuseg.pkuseg(model_name='medicine')  # 程序会自动下载所对应的细领域模型
        else:
            self.seg = seg
        if tokenizer == None:
            self.tokenizer = BertTokenizer.from_pretrained(
                "uer/chinese_roberta_L-8_H-512", do_basic_tokenize=False)
        else:
            self.tokenizer = tokenizer

        pass

    def filterPunctuation(self, x):
        """[summary]

        中文标点转换成英文
        Args:
            x ([type]): [description]
        Returns:
            [type]: [description]
        """
        x = re.sub(r'[‘’]', "'", x)
        x = re.sub(r'[“”]', '"', x)
        x = re.sub(r'[…]', '...', x)
        x = re.sub(r'[—]', '-', x)
        # x = re.sub(r'[]', '℃', x)
        x = re.sub(r"&nbsp", "", x)

        E_pun = u',.!?[]()<>"\''
        C_pun = u'，。！？【】（）《》“‘'

        table = {ord(f): ord(t) for f, t in zip(C_pun, E_pun)}
        x = x.translate(table)
        x = x.replace("“", '"').replace(
            "”", '"').replace("‘", "'").replace("’", "'")
        return x

    def clearText(self, text):
        """
        清理文本中的回车等
        """
        text_or = text.lower()
        # 中文标点转换英文
        # text_or=unicodedata.normalize('NFKD',text_or)
        text_or = self.filterPunctuation(text_or)
        # 使用tab替换空格
        text = text_or.replace(" ", "ر").replace(
            "\t", "س").replace("\n", "ة").replace("\r", "ت")
        return text

    def clearTextDec(self, seg_list):
        """
        修正词语中的特殊符号
        返回为分词后空格分割

        """
        newtext = " ".join(seg_list)

        newtext = newtext.replace("ر", "[PAD]").replace("س", "[PAD]")
        newtext = newtext.replace("ة", "[SEP]").replace("ت", "[SEP]")
        return newtext.split(" ")

    def getTokenize(self, text):
        """
        进行分词和修正各种错误
        """

        # 清理掉文本中的空格等
        text = self.clearText(text)
        # 分词
        seg_list = self.seg.cut(text)
        # 恢复
        newtext = self.clearTextDec(seg_list)
        # print("newtext",newtext)
        # 分词
        pre_textList = self.tokenizer.tokenize(" ".join(newtext))

        return {"tokenize": pre_textList, "cut": newtext}

    def getPos(self, text, word, start=None):
        """
        自动获取位置信息
        """
        if start == None:
            start = text.index(word)
        pre_text = text[:start]
        # pre_textList=self.tokenizer.tokenize(" ".join(pre_text))
        pre_dict = self.getTokenize(pre_text)
        word_dict = self.getTokenize(word)

        return len(pre_dict['tokenize']), len(word_dict['tokenize'])


# text="[P]神志清，精神不振，颈静脉\t充盈，双肺呼吸音低，可闻及散在干湿性啰音"
# apos=AutoPos()
# textDict=apos.getTokenize(text)

# print("textDict",textDict)

# https://colab.research.google.com/drive/18Yxm30DApEKpWyCjef3SydbCu8Idccfl#scrollTo=ezZcsB24gWOh
