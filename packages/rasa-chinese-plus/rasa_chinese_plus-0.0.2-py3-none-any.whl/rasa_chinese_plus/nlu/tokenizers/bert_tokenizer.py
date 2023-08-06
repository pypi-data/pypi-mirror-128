#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/11/21 9:04 下午
# @Author : daiyizheng
# @Version：V 0.1
# @File : bert_tokenizer.py
# @desc :

from typing import List, Text, Dict, Any

from rasa.shared.nlu.training_data.message import Message
from transformers import AutoTokenizer
from rasa.nlu.tokenizers.tokenizer import Tokenizer, Token


class BertTokenizer(Tokenizer):

    def __init__(self, component_config: Dict[Text, Any] = None) -> None:
        """
        :param component_config: {"pretrained_model_name_or_path":"", "cache_dir":"", "use_fast":""}
        """
        super(BertTokenizer, self).__init__(component_config)
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.component_config["pretrained_model_name_or_path"],
            cache_dir=self.component_config.get("cache_dir"),
            use_fast=True if self.component_config.get("use_fast") else False
        )

    @classmethod
    def required_packages(cls) -> List[Text]:
        return ["transformers"]

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = message.get(attribute)
        encoded_input = self.tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
        token_position_pair = zip(encoded_input.tokens(), encoded_input["offset_mapping"])
        tokens = [Token(text=token_text, start=position[0], end=position[1])
                  for token_text, position in token_position_pair]

        return self._apply_token_pattern(tokens)
