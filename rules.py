from yargy import Parser, rule, and_, or_
from yargy.predicates import gram, is_capitalized, dictionary, in_, normalized, eq, caseless, type
from yargy.interpretation import fact

DOT = eq('.')

POSITION = rule(
    or_(eq('врид'),
        eq('врио')).optional(),
    or_(rule('пом', DOT.optional()),
        rule('зам', DOT.optional()),
        rule('ст', DOT.optional()),
        rule(dictionary({'заместитель'}))).optional(),
    normalized('полковой').optional(),
    or_(
        rule('сотр', DOT.optional()),
        rule(dictionary({'оперуполномоченный', 'сотрудник', 'командир', 'уполномоченный', 'шофер',
                         'следователь', 'наркома', 'работник', 'инспектор', 'комендант', 'разведчик',
                         'начальник', 'секретарь', 'особоуполномоченный', 'председатель', 'фельдъегерь',
                         'сотрудница', 'лейтенант', 'референт', 'слушатель', 'руководитель', 'переводчик', 'управляющий'
                         })),
        rule(caseless('нач'), DOT),
        rule(normalized('министра'), 'внутренних', 'дел')
    ),
    or_(rule(eq('контрразведки')),
        rule(eq('особой'), eq('роты'))).optional())

pos_parser = Parser(POSITION)

def parse(d):
    for match in pos_parser.findall(d):
        b, e = match.tokens[0].span[0], match.tokens[-1].span[1]
        return  d[b:e],  d[e+1:]
    return '', ''


# POSITION = rule(
#     eq('врид').optional(),
#     rule('ст', DOT.optional()).optional(),
#     or_(rule('врио', DOT.optional()).optional()),
#     or_(rule('пом', DOT.optional()),
#         rule('зам', DOT.optional()),
#         rule('бывший').optional()),
#         rule('сотр', DOT.optional().optional())).optional(),
#
#     normalized('полковой').optional(),
#     or_(
#         rule('сотр', DOT.optional().optional()),
#         rule(dictionary({'председатель', 'оперуполномоченный', 'сотрудник', 'командир', 'уполномоченный', 'министра', 'особоуполномоченный', 'авиатехник', 'эскадрильи', 'инспектор', 'комендант', })),
#         rule(caseless('нач'), DOT)),
#     or_(normalized('контрразведки').optional(),
#         rule('штаба'),
#         rule('для', 'особых', 'поручений')).optional(),
#         rule('делопроизводитель', '-', 'машинистка').optional())