# Adapted for numpy/ma/cdms2 by convertcdms.py
import string
import types
import numpy
import numpy.ma
import cdms2
import os
import cdutil

def checkStringOrNone(self,name,value):
    """
    Checks to see if value is a string or None
    :param name: The name of the value
    :type name: str

    :param value: The value to check the type of
    :type value: any

    :returns: If value is None or a string, value will be returned. If not, an error will be raised.
    """
    if not type(value) in [types.StringType,types.NoneType]:
        raise ValueError,name+' must be a string or None'
    return value


def checkListNumbers(self,name,value):
    """
    Checks to make sure a list or tuple contains values that are only numbers
    :param name: string name of the value being checked
    :type name: str
    :param value: A list or tuple, which will be checked to determine if the contents are all numbers.
    :type value: list or tuple
    :returns: If value contains only numbers, value will be returned. Else, an exception is raised.
    """
    if not type(value) in [types.ListType,types.TupleType,types.NoneType]:
        raise ValueError, name + ' must be a list/tuple/None'
    if not value is None:
        for v in value:
            if not type(v) in [types.IntType,types.LongType,types.FloatType]:
                raise ValueError, name + ' list/tuple elements must be numbers'
    return value
    
def setSlab(self,name,value):
    """
    If value is a numpy ndarray or numpy MA, this function sets the object's data field to the value.
    :param name: string name of the value being checked
    :type name: str
    :param value:
    :returns: If value is a numpy ndarray or numpy MA, returns ('data',value).
            If value is a string, and the string is a filename in the system's path, returns ('file',value).
            If value is None, returns name,value.
    """
    if isinstance (value,numpy.ndarray ) or numpy.ma.isMA(value):
        self.data=value
        return ('data',value)
    elif type(value) == types.StringType:
        if os.path.exists(value):
            return('file',value)
        else:
            raise ValueError, value+" : file does not exist...."
    elif type(value) == types.NoneType:
        return name,value
    else:
        raise ValueError, name+" must be a slab, a file name or None"

def checkAxisType(self,name,value):
    return checkInStringsListInt(self,name,value,[
                          ['uniform','rect','linear'],
                          'gaussian',
                          ['equal','equal area','equalarea','equal-area'],]
                          )
    
def checkAction(self,name,value):
    return checkInStringsListInt(self,name,value,['select','mask'])
    
def  setDataSetGrid(self,name,value):
    if isinstance(value,cdutil.WeightedGridMaker):
        return value
    else:
        self.grid.grid=value
    
def setGrid(self,name,value):
    if isinstance(value,cdms2.grid.AbstractGrid):
        return value
    elif value is None:
        self.var=None
        self.file=None
        self.longitude.__init__()
        self.latitude.__init__()
        self.weightsMaker=None
        return None
    else:
        raise ValueError, name+" must be a grid object or None"
        
def setSlabOnly(self,name,value):
    if isinstance (value,numpy.ndarray ) or numpy.ma.isMA(value):
        return value
    elif type(value) == types.NoneType:
        return value
    else:
        raise ValueError, name+" must be a slab or None"
    
def getSlab(self,name):
    value=getattr(self,'_'+name)
    try:
        times=self.times
        times_type=self.times_type
    except:
        times=None
        times_type=''
    if times_type == 'indices':
        times=slice(times[0],times[1])
        
    if isinstance (value,numpy.ndarray ) or numpy.ma.isMA(value):
        return value
    elif type(value)==types.StringType:
        f=cdms2.open(value)
        if not times is None:
            v=f(self.var,time=times)
        else:
            v=f(self.var)
        f.close()
        return v
    else:
        return None

def checkNumberOrNone(self,name,value):
    if not type(value) in [types.IntType,types.FloatType,types.LongType,types.NoneType]:
        raise ValueError,name+' must be an integer, a float, or None'
    return value

def checkIntOrNone(self,name,value):
    if not type(value) in [types.IntType,types.LongType,types.NoneType]:
        raise ValueError,name+' must be an integer or None'
    return value

    
def checkInStringsList(self,name,value,values):
    """ check if value is in values"""
    if not type(value)==types.StringType:
        raise ValueError, name + 'must be a string'
    elif not string.lower(value) in values:
        err=name+" must be in ('"+values[0]
        for v in values[1:-1]:
            err=err+", '"+v+"'"
        err=err+" or '"+values[-1]+"')"
        raise ValueError, err
    self._basic_set(name,string.lower(value))

def checkInStringsListInt(self,name,value,values):
    """ checks the line type"""
    val=[]
    str1=name + ' can either be ('
    str2=' or ('
    i=0
    for v in values:
        if not v=='': # skips the invalid/non-contiguous values
            str2=str2+str(i)+', '
            if type(v) in [types.ListType,types.TupleType]:
                str1=str1+"'"+v[0]+"', "
                for v2 in v:
                    val.append(v2)
            else:
                val.append(v)
                str1=str1+"'"+v+"', "
            i=i+1
    err=str1[:-2]+')'+str2[:-2]+')'
    if type(value)==types.StringType:
        value=string.lower(value)
        if not value in val:
            raise ValueError, err
        i=0
        for v in values:
            if type(v) in [types.ListType,types.TupleType]:
                if value in v:
                    return i
            elif value==v:
                return i
            i=i+1
    elif type(value)==types.IntType or (type(value)==types.FloatType and int(value)==value):
        if not value in range(len(values)):
            raise ValueError, err
        else:
            return int(value)
    else:
        raise ValueError, err

 
def checkNumber(self,name,value):
    if not type(value) in [types.IntType,types.FloatType,types.LongType]:
        raise ValueError,name+' must be an integer or a float'
    return value
