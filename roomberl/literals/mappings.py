from typing import Dict
from typing import List

from django.db import models
from literals.models import University, BaseLiterals
from literals.constant import LiteralsCategory

LITERALS_TYPES_MAPPING: Dict[LiteralsCategory, models.Model] = {
    LiteralsCategory.UNIVERSITY: University

}


ALL_LITERALS: List["BaseLiterals"] = [
    LiteralsCategory.UNIVERSITY

]
