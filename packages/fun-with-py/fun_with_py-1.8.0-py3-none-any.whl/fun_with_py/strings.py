__author__ = "HSD, Hemant S D"
__email__ = "ashuhemantsingh@gmail.com"
__status__ = "planning"

import os

class String:
    """
    Class for the fun_with_py.
    Attributes
    ----------
    Private:
        None
        
    Methods
    -------
    Private:
        None
    Public:
        vowelsInString : returns a value in string 
        consonantsInString : returns a value in string 
        vowelsCount : returns a value in integer 
        consonantsCount : returns a value in integer
        isPalindrome : return True if the given string is palindrome
        reverse : return reverse string         
    """
    def __init__(self, string):
        """
        Creates a new instance of fun_with_py
        Parameters
        ----------
        string : str
            takes string  
        """
        self.value = string

    def vowelsInString(self):
        """
        return vowels from string
        """
        vowel = []
        vow = list('aeiouAEIOU')
        for i in self.value:
            if i in vow:
                vowel.append(i)
        return ''.join(vowel)

    def consonantsInString(self):
        """
        return consonants from string
        """
        consonant = []
        vow = list(' aeiouAEIOU')
        for i in self.value:
            if i in vow:
                pass
            else:
                consonant.append(i)
        return ''.join(consonant)
        
    def vowelsCount(self):
        """
        return total number vowels from string in integer
        """
        vowel = []
        vow = list('aeiouAEIOU')
        for i in self.value:
            if i in vow:
                vowel.append(i)
        return len(vowel)

    def consonantsCount(self):
        """
        return total nunber of consonants from string in integer
        """
        consonant = []
        vow = list(' aeiouAEIOU')
        for i in self.value:
            if i in vow:
                pass
            else:
                consonant.append(i)
        return len(consonant)

    def isPalindrome(self):
        """
        return True if the given string is palindrome
        """    
        val = self.value[::-1]
        if self.value == val:
            return True
        else:
            return False

    def reverse(self):
        """
        return reverse string
        """
        return self.value[::-1]




