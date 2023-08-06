# -*- coding: utf-8 -*-
import unicodedata
import regex as re
class AutoTokenizerPosition:
    """
    用来处理只有关键词的ner数据
    
    起始位置
    tokenizer = BertTokenizer.from_pretrained("clue/albert_chinese_tiny")
    tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
    使用这个可以减少不必要的麻烦
    ## 安装

    ```

    > pip install tkitAutoTokenizerPosition
    
    # or
    
    > pip install git+https://github.com/napoler/tkit-AutoTokenizerPosition

    ```
    
    
    """
    def __init__(self,tokenizer):
        """[summary]
        
        ```
        tokenizer = BertTokenizer.from_pretrained("clue/albert_chinese_tiny")
        tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
        ```
        使用这个可以减少不必要的麻烦

        Args:
            tokenizer ([type]): [description]
        """
        self.tokenizer=tokenizer
        pass
    def E_trans_to_C(self,string):
        """[summary]
        
        中文标点转换成英文

        Args:
            string ([type]): [description]

        Returns:
            [type]: [description]
        """
        E_pun = u',.!?[]()<>"\''
        C_pun = u'，。！？【】（）《》“‘'
        table= {ord(f):ord(t) for f,t in zip(C_pun,E_pun)}
        return string.translate(table)
    
    


    def filterPunctuation(self,x):
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
        x = re.sub(r"&nbsp", "", x)
        return x
    def clear(self,text):
        """[summary]

        清理文本中文问题

        Args:
        text ([type]): [description]
        """
        text=text.lower()
        # 中文标点转换英文
        text=unicodedata.normalize('NFKD',text)
        text=self.filterPunctuation(text)
        text=text.replace("\t",self.tokenizer.pad_token).replace(" ",self.tokenizer.pad_token)
        text=text.replace("\n",self.tokenizer.sep_token).replace("\r",self.tokenizer.sep_token)
        return text
    def getWordList(self,text):
        """[summary]

        分词列表

        Args:
        text ([type]): [description]
        """
        text=self.clear(text)
        return self.tokenizer.tokenize(text)
    def getText(self,wordList):
        for i,w in enumerate(wordList):
            wordList[i]=w.replace("##", "")
        return "".join(wordList)
            
        
        pass
    def autoLen(self,text):
        """[summary]
        
        获取文本分词后位置

        Args:
            text ([type]): [description]
        """
        text=text.lower()
#         word=word.lower()
        realLen=len(self.getWordList(text))
        return realLen
    
    
    def findAll(self,text, word):
        """[summary]
        
        获取词语在文字中的所有开始位置

        Args:
            text ([type]): [description]
            word ([type]): [description]

        Yields:
            [type]: [description]
        """
        text=text.lower()
        word=word.lower()
        idx = text.find(word)
        while idx != -1:
            yield idx
            idx = text.find(word, idx + 1)
    def fixPosition(self,text,word,startList=[]):
        """[summary]
        
        自动获取分词后起始位置
        自动匹配所有存在的位置
        
        传入位置可以限制查找的位置

        Args:
            text ([type]): [description]
            word ([type]): [description]
            startList (list, optional): [description]. Defaults to [].

        Yields:
            [type]: [description]
        """
#         print(text,word)
        text=text.lower()
        word=word.lower()
        if len(startList) ==0:
            startList=self.findAll(text, word)
        for start in startList:
            s_start=self.autoLen(text[:start])
        #     print("s_start",s_start)
            startLen=self.autoLen(word)
            # print("s_end", s_start,s_start+startLen)  
            yield s_start,s_start+startLen
    def autoTypeWord(self,text,word,wType=None,startList=[]):
        """[summary]

        Args:
            text ([type]): [description]
            word ([type]): [description]
            wType ([type], optional): [description]. Defaults to None.
            startList (list, optional): [description]. Defaults to [].
        """
        for s_start,s_end in self.fixPosition(text,word,startList=[]):
#             print(s_start,s_end)
#             WordList=self.getWordList(it['text'])
            yield s_start,s_end,wType
