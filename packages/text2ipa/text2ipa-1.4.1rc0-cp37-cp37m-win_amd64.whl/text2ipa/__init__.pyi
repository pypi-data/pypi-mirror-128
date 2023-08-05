'''Library converting Text to IPA'''
from typing import Any, List

def get_IPA(text: object, language: object, proxy: Any = None) -> str:
    '''Convert Text to IPA\n
    Parameters:\n
    - `text` : the content for converting to IPA
    - `language`: must be "am" or "br" (US English or UK English)
    - `proxy` : Optional parameter using for hide ip
    '''
    ...


def get_IPAs(bulk: List[str], language: str, proxy: Any = None) -> List[str]:
    '''Convert a list of text to IPA\n
    Parameters:\n
    - `bulk` : the list of contents for converting to IPA
    - `language`: must be "am" or "br" (US English or UK English)
    - `proxy` : Optional parameter using for hide ip
    '''
    ...


__all__ = ['get_IPA', 'get_IPAs']
