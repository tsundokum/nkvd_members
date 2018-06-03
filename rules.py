POSITION = rule(
    rule('врид', DOT.optional()),
        or_('врио', DOT.optional()).optional().optional(),

    or_(
        rule('пом', DOT.optional()),
        rule('зам', DOT.optional()),
        rule('бывший').optional(),
        rule('ст', DOT.optional()),
        rule('старший'),
        rule('главный'),
        rule('дежурный'),
        rule('сотр', DOT.optional()),
        rule('сотрудник'),
        rule('нач', DOT.optional()),
        rule('еач', DOT.optional()),
        rule('гл', DOT.optional()).optional(),

    or_(
        rule('ст', DOT.optional()),
        rule('пом', DOT.optional()),
        normalized('полкового'),
        normalized('инспектора'),
        normalized('секретаря'),
        normalized('особоуполномоченного'),
        normalized('наркома'),
        normalized('командующего'),
        normalized('директора')).optional(),

    or_(
        rule('сотр', DOT.optional()),
        rule('сотрудник'),
        normalized('коменданта'),
        normalized('оперпункта'),
        rule(dictionary({'председатель', 'оперуполномоченный', 'сотрудник', 'командир', 'уполномоченный', 'министра', 'особоуполномоченный', 'авиатехник', 'эскадрильи', 'инспектор', 'комендант', 'шофер', 'авиатехник', 'военком', 'военцензор', 'инспектора', 'ревизор', 'гоcавтоинспектор', 'нарком', 'директор', 'командующий', 'инженер'}))).optional(),

    or_(
        normalized('контрразведки'),
        rule('штаба'),
        rule('для', 'особых', 'поручений'),
        rule('для', 'особых', 'поручения'),
        rule('для', 'поручений'),
        rule('вице', '-', 'консул'),
        rule('делопроизводитель', '-', 'машинистка'),
        rule('по', 'безопасности','движения'),
        rule('по', 'бюро', 'разовых', 'пропусков'),
        rule('действующий резерв'),
        rule('внутренних', 'дел')).optional()


