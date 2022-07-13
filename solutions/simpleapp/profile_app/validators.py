from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class PassphraseValidator:
    def __init__(self, dictionary_file='/usr/share/dict/words'):
        self.min_words = 3
        with open(dictionary_file) as f: 
            self.words = set(word.strip() for word in f) 

    def get_help_text(self):
        return _('Your password must contain %s words' % self.min_words) 

    def validate(self, password, user=None):
        tokens = password.split(' ')
        if len(tokens) < self.min_words: 
            too_short = _('This password needs %s words' % self.min_words) 
            raise ValidationError(too_short, code='too_short') 
        if not all(token in self.words for token in tokens): 
            not_passphrase = _('This password is not a passphrase') 
            raise ValidationError(not_passphrase, code='not_passphrase') 