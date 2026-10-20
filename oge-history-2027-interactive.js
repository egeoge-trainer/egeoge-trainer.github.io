window.localInteractiveSources = window.localInteractiveSources || [];

(() => {
  const previousSource = window.localInteractiveSources.find(
    (source) => source.id === 'artasov-oge-history-2026'
  );
  const previousVariant = previousSource?.variants.find(
    (variant) => variant.id === 'artasov-oge-history-2026-v1'
  );
  if (!previousVariant) return;

  const questions = structuredClone(previousVariant.questions);

  questions[1] = {
    type: 'digits',
    text: 'Расположите исторические события в хронологической последовательности.',
    context: [
      '1) Взятие русскими войсками Плевны',
      '2) Продажа Аляски Россией США',
      '3) Отмена крепостного права в России',
      '4) Издание «Положения о губернских и уездных земских учреждениях»'
    ],
    correct: ['3421']
  };

  questions[3] = {
    type: 'multi',
    text: 'Какие из перечисленных событий относятся к 1880-м гг.? Выберите два ответа.',
    options: [
      'Создание «Союза борьбы за освобождение рабочего класса»',
      'Основание первой марксистской группы «Освобождение труда»',
      'Издание Манифеста «О незыблемости самодержавия»',
      'Заключение военной конвенции между Россией и Францией',
      'Начало строительства Транссибирской магистрали'
    ],
    correct: [1, 2]
  };

  questions[6].left = [
    'Во всех земских собраниях большинство составляли представители…',
    'Наименьшую долю представители крестьян имели в…',
    'Чуть более полутора тысяч человек во всех земских собраниях составляли представители…'
  ];

  const keys = [
    '431', '3421', 'Уложенная комиссия', '23; 32', '5', '1423; 2314', '245',
    'двенадцатый', 'Юрий Долгорукий', '3', '3', 'Борис Годунов', '34; 43',
    '5', '3', '1', '4'
  ];
  questions.forEach((question, index) => {
    question.sourceTask = index + 1;
    question.sourceVariant = 1;
    question.explanation = `Эталон из таблицы ответов: ${keys[index]}.`;
  });

  window.localInteractiveSources.push({
    subjectId: 'history_oge',
    id: 'artasov-oge-history-2027',
    title: 'Типовые экзаменационные варианты',
    year: '2027',
    description: 'Под редакцией И. А. Артасова · ОГЭ · 2027',
    authorLine: 'И. А. Артасов · ОГЭ · 2027',
    variants: [{
      id: 'artasov-oge-history-2027-v1',
      title: 'Вариант 1',
      questions
    }]
  });
})();
