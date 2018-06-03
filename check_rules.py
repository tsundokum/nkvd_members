import json
import csv


from yargy import Parser, rule, and_, or_
from yargy.predicates import gram, is_capitalized, dictionary, in_, normalized, eq, caseless, type
from yargy.interpretation import fact
from rules import parse


examples = '''дежурный комендат домов № 2 и 2А комендантского отдела АХУ НКВД СССР
дежурный пом. зав. гаражом ОС ОГПУ
дежурный пом. оперпункта ст. Александров ДТО НКВД Ярославской ж. д.
дежурный тюрьмы № 1 ОМЗ УНКВД Тульской обл.
действующий резерв ГУГБ НКВД СССР'''.splitlines()
print(examples)

for ex in examples:
     p,r = parse(ex)
     if not p and not r:
         print(ex)
