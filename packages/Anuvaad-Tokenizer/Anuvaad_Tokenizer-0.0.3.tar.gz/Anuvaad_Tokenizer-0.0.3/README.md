# Anuvaad Tokenizer

Anuvaad Tokenizer is a python package, which can be used to tokenize paragraphs into sentences. It supports most of the Indian languages including English. This Tokenizer is built using regular expressions.

## Prerequisites

- python >= 3.6

## Installation
``` pip install Anuvaad_Tokenizer==0.0.3 ```
 
## Author

Anuvaad (nlp-nmt@tarento.com)

# Usage Example

## For English
```
from Anuvaad_Tokenizer.AnuvaadEnTokenizer import AnuvaadEnTokenizer 

para=" "  
tokenized_text = AnuvaadEnTokenizer().tokenize(para)
```
## For Hindi
```
from Anuvaad_Tokenizer.AnuvaadHiTokenizer import AnuvaadHiTokenizer

para=" "
tokenized_text = AnuvaadHiTokenizer().tokenize(para)
```
## For Kannada
```
from Anuvaad_Tokenizer.AnuvaadKnTokenizer import AnuvaadKnTokenizer

para=" "
tokenized_text = AnuvaadKnTokenizer().tokenize(para)
```
## For Telugu
```
from Anuvaad_Tokenizer.AnuvaadTeTokenizer import AnuvaadTeTokenizer

para=" "
tokenized_text = AnuvaadTeTokenizer().tokenize(para)
```
## For Tamil
```
from Anuvaad_Tokenizer.AnuvaadTaTokenizer import AnuvaadTaTokenizer

para=" "
tokenized_text = AnuvaadTaTokenizer().tokenize(para)
```
## LICENSE

MIT License 2021 
Developer - Anuvaad