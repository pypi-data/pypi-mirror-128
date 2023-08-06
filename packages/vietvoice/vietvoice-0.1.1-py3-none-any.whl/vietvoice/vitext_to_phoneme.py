import string
import re

from underthesea import word_tokenize
from viphoneme import T2IPA_split

alphabet = 'abcdefghijklmnopqrstuvwxyzàáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ'
alphabet += string.punctuation
alphabet += ' '
alphabet = set(alphabet)

mapping = {'à':'à',
 'á':'á',
 'ã':'ã',
 'ả':'ả',
 'ạ':'ạ',
 'è':'è',
 'é':'é',
 'ẽ':'ẽ',
 'ẻ':'ẻ',
 'ì':'ì',
 'í':'í',
 'ĩ':'ĩ',
 'ỉ':'ỉ',
 'ị':'ị',
 'ò':'ò',
 'ó':'ó',
 'õ':'õ',
 'ỏ':'ỏ',
 'ọ':'ọ',
 'ù':'ù',
 'ú':'ú',
 'ũ':'ũ',
 'ủ':'ủ',
 'ụ':'ụ',
 'ỳ':'ỳ',
 'ý':'ý',
 'ỷ':'ỷ',
 'ầ':'ầ',
 'ấ':'ấ',
 'ẫ':'ẫ',
 'ẩ':'ẩ',
 'ậ':'ậ',
 'ề':'ề',
 'ế':'ế',
 'ễ':'ễ',
 'ể':'ể',
 'ệ':'ệ',
 'ồ':'ồ',
 'ố':'ố',
 'ỗ':'ỗ',
 'ổ':'ổ',
 'ộ':'ộ',
 'ằ':'ằ',
 'ắ':'ắ',
 'ẳ':'ẳ',
 'ặ':'ặ',
 'ờ':'ờ',
 'ớ':'ớ',
 'ỡ':'ỡ',
 'ở':'ở',
 'ợ':'ợ',
 'ừ':'ừ',
 'ứ':'ứ',
 'ữ':'ữ',
 'ử':'ử',
 'ự':'ự'}

_whitespace_re = re.compile(r'\s+')
def collapse_whitespace(text):
    return re.sub(_whitespace_re, ' ', text)

def vitext_clean(text):
    text  = text.strip()            
    text = text.lower()
    text = collapse_whitespace(text)
    text = text.replace('–', '-')
    
    text = re.sub('([.,!?()])', r' \1 ', text)
    text = re.sub('\s{2,}', ' ', text)

    for k, v in mapping.items():
        text = text.replace(k, v)
    
    for k in string.punctuation:
        if k not in [',', '.']:
            text = text.replace(k, ',')    
	
    return text

def vi2IPA(text):
    TK= word_tokenize(text)
    IPA=[]
    for tk in TK:
        ipa = T2IPA_split(tk, '/').replace(" ","_")        
        if ipa =="":
            IPA.append('/'+tk+'/')
        elif ipa[0]=="[" and ipa[-1]=="]":
            return []
        else:
            IPA.append(ipa)
        
    IPA = ' '.join(IPA)
    return IPA

def vitext_to_phoneme(text):
    phoneme = None
    if len(text) > 0 and set(text) <= alphabet:
        phoneme = vi2IPA(text)

    if len(text) == 0:
        print('text after cleaning is empty')

    if len(set(text) - alphabet) > 0:
        print('text contains invalid characters: {}'.format(set(text) - alphabet))

    return phoneme
