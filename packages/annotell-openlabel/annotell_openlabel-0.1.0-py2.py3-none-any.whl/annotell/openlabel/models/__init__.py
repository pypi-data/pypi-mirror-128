from typing import Union

from .models import *

from .models import Type1 as DataTypes
from .models import Type2 as NumTypes
from .models import Type3 as RdfTypes
from .models import Type4 as StreamTypes
from .models import Type6 as VecTypes

DataTypeBase = Union[Text, Num, Vec, Boolean]
