class Numeric:
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
        reverse : returns reverse of numbers 
        isMultipleOf : returns true if given number is multiple of it 
         : returns a value in integer 
        consonantsCount : returns a value in integer 
    """
    def __init__(self, number):
        """
        Creates a new instance of 
        Parameters
        ----------
        string : str
            takes string  
        """
        self.value = number
        if type(self.value) == int or type(self.value) == float:
            pass
        else:
            print("Please input a numeric value not string this might cause error")


    def reverse(self):
        """
        return reverse integer
        """
        val = str(self.value)
        val = val[::-1]
        return int(val)

    def isMultipleOf(self, num):
        """
        return true if it is divisible by given number
        """
        val = self.value
        if val%num == 0:
            return True
        else:
            return False
