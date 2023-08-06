import re
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters, PunktTrainer, PunktLanguageVars
from nltk.tokenize import sent_tokenize

static_end = """
TT__TT
.
?
!
:
END_A
END_B
END_C
"""

class AnuvaadTaTokenizer(object):

    """
    abbrevations
    """
    _abbrevations_with_non_generalize_pattern = [r'நீ[.]',r'பே[.]',r'ம[.]',r'எண்[.]',r'சா[.]',r'ஆ[ ][.]',r'சா[ ][.]',r'எண்[ ][.]',r'திரு[.]',r'திருமதி[.]']
    _abbrevations_with_non_generalize = ['நீ.','பே.','ம.','எண்.','சா.','ஆ .','சா .','எண் .','திரு.','திருமதி.']
    _abbrevations_with_space_pattern = r'((\s)(([\u0B85-\u0BB9])([\u0B82-\u0B83,\u0BBE-\u0BD7])?([\u0B85-\u0BB9])?([\u0B82-\u0B83,\u0BBE-\u0BD7])?(\u002e)(\s)?){1,})'
    _abbrevations_with_space = []
    _abbrevations_without_space_pattern = r'(^(([\u0B85-\u0BB9])([\u0B82-\u0B83,\u0BBE-\u0BD7])?([\u0B85-\u0BB9])?([\u0B82-\u0B83,\u0BBE-\u0BD7])?(\u002e)(\s)?){1,})'
    _abbrevations_without_space = []
    _tokenizer = None
    _regex_search_texts = []
    _date_abbrevations  = []
    _time_abbreviations = []
    _table_points_abbrevations = []
    _brackets_abbrevations = []
    _decimal_abbrevations = []
    _url_abbrevations = []
    _dot_with_char_abbrevations = []
    _dot_with_quote_abbrevations = []
    _dot_with_number_abbrevations = []
    _dot_with_beginning_number_abbrevations = []

    def __init__(self, abbrevations = None):
        if abbrevations is not None:
            self._abbrevations_without_space.append(abbrevations)
        self._abbrevations_with_space = []
        self._abbrevations_without_space = []
        self._regex_search_texts = []
        self._date_abbrevations  = []
        self._time_abbreviations = []
        self._table_points_abbrevations = []
        self._brackets_abbrevations = []
        self._decimal_abbrevations = []
        self._url_abbrevations = []
        self._dot_with_char_abbrevations = []
        self._dot_with_quote_abbrevations = []
        self._dot_with_number_abbrevations = []
        self._dot_with_beginning_number_abbrevations = []
        self._decimal_beginning_with_dot_or_without_space = []
        self._tokenizer = PunktSentenceTokenizer(lang_vars=SentenceEndLangVars())

    def tokenize(self, text):
        print('--------------Process ta started-------------')
        text = self.serialize_with_abbrevations(text)
        text = self.serialize_dates(text)
        text = self.serialize_time(text)
        text = self.serialize_table_points(text)
        text = self.serialize_url(text)
        text = self.serialize_pattern(text)
        text = self.serialize_dots(text)
        text = self.serialize_end(text)
        text = self.serialize_brackets(text)
        text = self.serialize_dot_with_number(text)
        text = self.serialize_dot_with_number_beginning(text)
        text = self.serialize_quotes_with_number(text)
        text = self.serialize_bullet_points(text)
        text = self.serialize_decimal(text)
        text = self.serialize_decimal_begin_with_dot_or_without_space(text)
        text = self.add_space_after_sentence_end(text)
        text = self.serialize_consecutive_dots(text)
        sentences = self._tokenizer.tokenize(text)
        output = []
        for se in sentences:
            se = self.deserialize_dates(se)
            se = self.deserialize_time(se)
            se = self.deserialize_pattern(se)
            se = self.deserialize_url(se)
            se = self.deserialize_dots(se)
            se = self.deserialize_end(se)
            se = self.deserialize_decimal(se)
            se = self.deserialize_brackets(se)
            se = self.deserialize_dot_with_number(se)
            se = self.deserialize_dot_with_number_beginning(se)
            se = self.deserialize_quotes_with_number(se)
            se = self.deserialize_with_abbrevations(se)
            se = self.deserialize_bullet_points(se)
            se = self.deserialize_table_points(se)
            se = self.deserialize_decimal_begin_with_dot_or_without_space(se)
            se = self.deserialize_consecutive_dots(se)
            if se != '':
                output.append(se.strip())
        print('--------------Process finished-------------')
        return output

    def serialize_url(self, text):
        patterns = re.findall(r'(?:(?:https?):?:(?:(?://)|(?:\\\\))+(?:(?:[\w\d:#@%/;$()~_?\+-=\\\.&](?:#!)?))*)',text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._url_abbrevations.append(pattern)
                text = pattern_obj.sub('URL_'+str(index)+'_URL', text)
                index+=1
        return text

    def deserialize_url(self, text):
        index = 0
        if self._url_abbrevations is not None and isinstance(self._url_abbrevations, list):
            for pattern in self._url_abbrevations:
                pattern_obj = re.compile(re.escape('URL_'+str(index)+'_URL'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text

    def serialize_decimal(self, text):
        patterns = re.findall(r'(?:(?:[ ]|[(]|[-])[0-9]{1,}[.][0-9]{1,}(?:[ ]|[)]|[%]))',text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._decimal_abbrevations.append(pattern)
                text = pattern_obj.sub('DE_'+str(index)+'_DE', text)
                index+=1
        return text

    def deserialize_decimal(self, text):
        index = 0
        if self._decimal_abbrevations is not None and isinstance(self._decimal_abbrevations, list):
            for pattern in self._decimal_abbrevations:
                pattern_obj = re.compile(re.escape('DE_'+str(index)+'_DE'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text

    def add_space_after_sentence_end(self, text):
        sentence_ends = ['.','?','!',';',':','।']
        for sentence_end in sentence_ends:
            pattern = re.compile(r'['+sentence_end+'][ ]') #remove already correct patterns
            text = pattern.sub(sentence_end, text)
            pattern = re.compile(r'['+sentence_end+']')
            text = pattern.sub(sentence_end + ' ', text)
        return text

    def serialize_end(self, text):
        pattern_d = re.compile(r'(\u0965)')
        text = pattern_d.sub(' END_B', text)
        pattern = re.compile(r'(\u0964)')
        text = pattern.sub(' END_A ', text)
        # pattern_e = re.compile(r'( \u0020 )')
        # text = pattern_e.sub('END_C',text)
        return text

    def deserialize_end(self, text):
        pattern = re.compile(re.escape(' END_A'), re.IGNORECASE)
        text = pattern.sub('।', text)
        pattern = re.compile(re.escape(' END_B'), re.IGNORECASE)
        text = pattern.sub('॥', text)
        pattern = re.compile(re.escape('END_C'), re.IGNORECASE)
        text = pattern.sub('.',text)
        return text

    def serialize_bullet_points(self, text):
        pattern = re.compile(r'(?!^)[•]')
        text = pattern.sub('TT__TT UU__UU', text)
        return text

    def deserialize_bullet_points(self, text):
        pattern = re.compile(re.escape('TT__TT'), re.IGNORECASE)
        text = pattern.sub('', text)
        pattern = re.compile(re.escape('UU__UU'), re.IGNORECASE)
        text = pattern.sub('•', text)
        return text

    def serialize_table_points(self, text):
        patterns = re.findall(r'(?:(?:(?:[ ][(]?(?:(?:[0,9]|[i]|[x]|[v]){1,3}|[a-zA-Z\u0B82-\u0BD7]{1,1})[)])|(?:[ ](?:(?:[0-9]|[i]|[x]|[v]){1,3}|[a-zA-Z\u0B82-\u0BD7]{1,1})[.][ ])))',text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._table_points_abbrevations.append(pattern)
                text = pattern_obj.sub(' TT__TT RR_'+str(index)+'_RR', text)
                index+=1
        return text

    def deserialize_table_points(self, text):
        index = 0
        if self._table_points_abbrevations is not None and isinstance(self._table_points_abbrevations, list):
            for pattern in self._table_points_abbrevations:
                pattern_obj = re.compile(re.escape('RR_'+str(index)+'_RR'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text

    def serialize_brackets(self, text):
        patterns = re.findall(r'(?:[(](?:[0-9\u0B82-\u0BD7a-zA-Z][.]?|[ ]){1,}[)]?).',text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._brackets_abbrevations.append(pattern)
                text = pattern_obj.sub('WW_'+str(index)+'_WW', text)
                index+=1
        return text

    def deserialize_brackets(self, text):
        index = 0
        if self._brackets_abbrevations is not None and isinstance(self._brackets_abbrevations, list):
            for pattern in self._brackets_abbrevations:
                pattern_obj = re.compile(re.escape('WW_'+str(index)+'_WW'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text
    
    def serialize_dates(self, text):
        patterns = re.findall(r'[0-9]{1,4}[.][0-9]{1,2}[.][0-9]{1,4}',text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._date_abbrevations.append(pattern)
                text = pattern_obj.sub('DD_'+str(index)+'_DD', text)
                index+=1
        return text

    def deserialize_dates(self, text):
        index = 0
        if self._date_abbrevations is not None and isinstance(self._date_abbrevations, list):
            for pattern in self._date_abbrevations:
                pattern_obj = re.compile(re.escape('DD_'+str(index)+'_DD'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text

    def serialize_decimal_begin_with_dot_or_without_space(self, text):
        patterns = re.findall(r'[.]{0,}[0-9]{1,}[ ]{0,}[.][ ]{0,}[0-9]{1,}', text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._decimal_beginning_with_dot_or_without_space.append(pattern)
                text = pattern_obj.sub('DDS_'+str(index)+'_DDS', text)
                index+=1
        return text

    def deserialize_decimal_begin_with_dot_or_without_space(self, text):
        index = 0
        if self._decimal_beginning_with_dot_or_without_space is not None and isinstance(self._decimal_beginning_with_dot_or_without_space, list):
            for pattern in self._decimal_beginning_with_dot_or_without_space:
                pattern_obj = re.compile(re.escape('DDS_'+str(index)+'_DDS'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text

    def serialize_time(self, text):
        patterns = re.findall(r'[0-9]{1,2}[:][0-9]{1,2}',text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._time_abbreviations.append(pattern)
                text = pattern_obj.sub('TI_'+str(index)+'_ME', text)
                index+=1
        return text

    def deserialize_time(self, text):
        index = 0
        if self._time_abbreviations is not None and isinstance(self._time_abbreviations, list):
            for pattern in self._time_abbreviations:
                pattern_obj = re.compile(re.escape('TI_'+str(index)+'_ME'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text
    

    def serialize_quotes_with_number(self, text):
        patterns = re.findall(r'([ ][“][0-9a-zA-Z\u0B82-\u0BD7]{1,}[.])',text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._dot_with_quote_abbrevations.append(pattern)
                text = pattern_obj.sub(' ZZ_'+str(index)+'_ZZ', text)
                index+=1
        return text

    def deserialize_quotes_with_number(self, text):
        index = 0
        if self._dot_with_quote_abbrevations is not None and isinstance(self._dot_with_quote_abbrevations, list):
            for pattern in self._dot_with_quote_abbrevations:
                pattern_obj = re.compile(re.escape('ZZ_'+str(index)+'_ZZ'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text

    def serialize_dot_with_number_beginning(self, text):
        patterns = re.findall(r'(^[0-9]{1,}[.])',text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._dot_with_beginning_number_abbrevations.append(pattern)
                text = pattern_obj.sub('YY_'+str(index)+'_YY', text)
                index+=1
        return text

    def deserialize_dot_with_number_beginning(self, text):
        index = 0
        if self._dot_with_beginning_number_abbrevations is not None and isinstance(self._dot_with_beginning_number_abbrevations, list):
            for pattern in self._dot_with_beginning_number_abbrevations:
                pattern_obj = re.compile(re.escape('YY_'+str(index)+'_YY'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text

    def serialize_dot_with_number(self, text):
        patterns = re.findall(r'(?:[ ][0-9]{,2}[.][ ])',text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._dot_with_number_abbrevations.append(pattern)
                text = pattern_obj.sub(' XX_'+str(index)+'_XX', text)
                index+=1
        return text

    def deserialize_dot_with_number(self, text):
        index = 0
        if self._dot_with_number_abbrevations is not None and isinstance(self._dot_with_number_abbrevations, list):
            for pattern in self._dot_with_number_abbrevations:
                pattern_obj = re.compile(re.escape('XX_'+str(index)+'_XX'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text

    def serialize_dots(self, text):
        pattern = re.compile(r'([.]{3,})')
        text = pattern.sub('XX__XX', text)
        return text

    def deserialize_dots(self, text):
        pattern = re.compile(re.escape('XX__XX'), re.IGNORECASE)
        text = pattern.sub('......', text)
        return text

    def serialize_consecutive_dots(self, text):
        pattern = re.compile(r'([.\s]{3,})')
        text = pattern.sub('YY__YY', text)
        return text

    def deserialize_consecutive_dots(self, text):
        pattern = re.compile(re.escape('YY__YY'), re.IGNORECASE)
        text = pattern.sub('........', text)
        return text



    def serialize_pattern(self, text):
        patterns = re.findall(r'([\u0B82-\u0BD7][.]){2,}',text)
        index = 0
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._dot_with_char_abbrevations.append(pattern)
                text = pattern_obj.sub('$$_'+str(index)+'_$$', text)
                index+=1
        return text

    def deserialize_pattern(self, text):
        index = 0
        if self._dot_with_char_abbrevations is not None and isinstance(self._dot_with_char_abbrevations, list):
            for pattern in self._dot_with_char_abbrevations:
                pattern_obj = re.compile(re.escape('$$_'+str(index)+'_$$'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index+=1
        return text
           
    def serialize_with_abbrevations(self, text):
        index_for_with_space = 0
        index_for_without_space = 0
        index_no_gen = 0
        for abbrev in self._abbrevations_with_non_generalize_pattern:
            pattern_non_gen = re.compile(abbrev, re.IGNORECASE)
            text = pattern_non_gen.sub('#N' + str(index_no_gen) + 'G##', text)
            index_no_gen += 1
        patterns_wos = re.findall(self._abbrevations_without_space_pattern, text)
        patterns_wos = [tuple(j for j in pattern if j)[0] for pattern in patterns_wos]
        patterns_wos = list(sorted(patterns_wos, key = len))
        patterns_wos = patterns_wos[::-1]
        if patterns_wos is not None and isinstance(patterns_wos, list):
            for pattern in patterns_wos:
                pattern_obj = re.compile(re.escape(pattern))
                self._abbrevations_without_space.append(pattern)
                text = pattern_obj.sub('#WO'+str(index_for_without_space)+'S##', text)
                index_for_without_space+=1

        patterns = re.findall(self._abbrevations_with_space_pattern, text)
        patterns = [tuple(j for j in pattern if j)[0] for pattern in patterns]
        patterns = list(sorted(patterns, key = len))
        patterns = patterns[::-1]
        if patterns is not None and isinstance(patterns, list):
            for pattern in patterns:
                pattern_obj = re.compile(re.escape(pattern))
                self._abbrevations_with_space.append(pattern)
                text = pattern_obj.sub('##'+str(index_for_with_space)+'##', text)
                index_for_with_space+=1
        return text

    def deserialize_with_abbrevations(self, text):
        index_for_with_space= 0
        index_for_without_space = 0
        index_no_gen = 0
        for abbrev in self._abbrevations_with_non_generalize:
            pattern = re.compile(re.escape('#N'+str(index_no_gen)+'G##'), re.IGNORECASE)
            text = pattern.sub(abbrev, text)
            index_no_gen += 1
        if self._abbrevations_without_space is not None and isinstance(self._abbrevations_without_space, list):
            for pattern in self._abbrevations_without_space:
                pattern_obj = re.compile(re.escape('#WO'+str(index_for_without_space)+'S##'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index_for_without_space+=1
        if self._abbrevations_with_space is not None and isinstance(self._abbrevations_with_space, list):
            for pattern in self._abbrevations_with_space:
                pattern_obj = re.compile(re.escape('##'+str(index_for_with_space)+'##'), re.IGNORECASE)
                text = pattern_obj.sub(pattern, text)
                index_for_with_space+=1
        return text


class SentenceEndLangVars(PunktLanguageVars):
    text = []
    # with open('repositories/tokenizer_data/end.txt', encoding='utf8') as f:
    text = static_end
    sent_end_chars = text.split('\n')