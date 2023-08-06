import numpy as np
from math import ceil,floor

class ColorfulData:
    """
    Create custom evenly distributed color palete
    \n`Get_Colors_Matched`: key,value relationship evenly distributed for given unique values
    \n`Get_Colors`: Evenly distributed for given length
    """

    @staticmethod
    def Get_Colors_Matched(items:list([any]),colorPalette:dict[int,any])->np.array:
        """
        Returns 2d ndarray of unique `items` for given `colorPalette`
        \nIf `colorPalette` is larger then unique `items`: \n\treturned values are equaly spaced from start to end of `colorPalette`
        \n\nIf `colorPalette` is smaller then unique `items`: \n\t`colorPalette` is expanded by repeating colors, in given order, then equaly spaced from start to end 
        """
        _items = np.unique(np.array(items))
        _itemcount = len(_items)
        _ret = ColorfulData.Get_Colors(_itemcount,colorPalette=colorPalette)
        _ret = np.column_stack(
            [np.array(_items), 
            _ret])
        
        return _ret

    @staticmethod 
    def Get_Colors(count:int,colorPalette:dict[int,any])->np.array:
        """
        Returns ndarray of given `count` for given `colorPalette`
        \nIf `colorPalette` is larger then `count`: \n\treturned values are equaly spaced from start to end of `colorPalette`
        \n\nIf `colorPalette` is smaller then `count`: \n\t`colorPalette` is expanded by repeating colors, in given order, then equaly spaced from start to end 
        """
        _paletteCount = len(colorPalette)
        _colorsCount = count
        _repeat = ceil(_colorsCount/_paletteCount)
        _colorsIn = np.repeat(np.array(colorPalette),_repeat)
        _remainder = len(_colorsIn)-_colorsCount
        _colorIndex = _colorsIn
        _skip = floor(_remainder/_colorsCount)
        _index = np.arange(start=0,stop=_paletteCount,step= _skip if _skip>1 else 1)

        if _skip > 0:
            
            _colorIndex = \
                [_colorsIn[x] for x in (_index)][:_colorsCount]

            print('')

        else:
            _colorIndex = \
                _colorsIn[:_colorsCount]

        #print(f'{str(_colorsCount).rjust(5)}:'
        #+f' x{_repeat}'
        #+f' new palette: {str(len(_colorsIn)).rjust(5)}'
        #+f' remainder: {str(_remainder).rjust(5)}'
        #+f' skip:{str(_skip).rjust(3)}'
        #+f' color index:{str(len(_colorIndex)).rjust(5)}')
    
        return _colorIndex
        
