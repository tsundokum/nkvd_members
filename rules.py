from yargy import Parser, rule, and_, or_
from yargy.predicates import gram, is_capitalized, dictionary, in_, normalized, eq, caseless, type
from yargy.interpretation import fact

DOT = eq('.')

POSITION = rule(
    or_(rule('врид', DOT.optional()),
        rule('врио', DOT.optional()),
        rule('и', DOT, 'о', DOT)).optional(),

    or_(
        rule('пом', DOT.optional()),
        rule('помощник'),
        rule('зам', DOT.optional()),
        rule('зав', DOT.optional()),
        rule('заместитель'),
        rule('бывший').optional(),
        rule('ст', DOT.optional()),
        rule('старший'),
        rule('главный'),
        rule('дежурный'),
        rule('нач', DOT.optional()),
        rule('еач', DOT.optional()),
        rule('гл', DOT.optional())),

    # or_(
    #     rule('ст', DOT.optional()),
    #     rule('нач', DOT.optional()),
    #     rule('пом', DOT.optional()),
    #     normalized('полкового')).optional(),

    # or_(rule('сотр', DOT.optional()),
    #     rule('пред', DOT.optional()),
    #     dictionary({'председатель', 'оперуполномоченный', 'особоуполномоченного', 'сотрудник', 'командир', 'уполномоченный', 'министра', 'особоуполномоченный', 'секретаря', 'авиатехник', 'эскадрильи', 'инспектор', 'комендант', 'коменданта', 'инспектора', 'шофер', 'авиатехник', 'военком', 'военцензор', 'ревизор', 'гоcавтоинспектор', 'нарком', 'директор', 'директора', 'командующий', 'инженер'})).optional(),
    #
    # or_(
    #     normalized('контрразведки'),
    #     normalized('оперпункта'),
    #     rule('штаба'),
    #     rule('для', 'особых', 'поручений'),
    #     rule('для', 'особых', 'поручения'),
    #     rule('для', 'поручений'),
    #     rule('вице', '-', 'консул'),
    #     rule('делопроизводитель', '-', 'машинистка'),
    #     rule('по', 'безопасности','движения'),
    #     rule('по', 'бюро', 'разовых', 'пропусков'),
    #     rule('действующий резерв'),
    #     rule('внутренних', 'дел')).optional()
)

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