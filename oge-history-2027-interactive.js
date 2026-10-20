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

  const previousVariant2 = previousSource.variants.find(
    (variant) => variant.id === 'artasov-oge-history-2026-v2'
  );
  if (!previousVariant2) return;

  const questions2 = structuredClone(previousVariant2.questions);
  questions2[0] = {
    type: 'match',
    text: 'Установите соответствие между событиями и годами.',
    left: [
      'Восстание декабристов на Сенатской площади в Санкт-Петербурге',
      'Принятие Новоторгового устава',
      'Заключение договора Руси с Византией'
    ],
    right: ['911 г.', '1068 г.', '1667 г.', '1825 г.', '1905 г.'],
    correct: [3, 2, 0]
  };
  questions2[1] = {
    type: 'digits',
    text: 'Расположите исторические события в хронологической последовательности.',
    context: [
      '1) Формирование Первого народного (земского) ополчения',
      '2) Смоленская война',
      '3) Избрание Земским собором на царствование Михаила Романова',
      '4) Заключение Деулинского перемирия с Речью Посполитой'
    ],
    correct: ['1342']
  };
  questions2[3] = {
    type: 'multi',
    text: 'Какие из перечисленных событий относятся к 1710-м гг.? Выберите два ответа.',
    options: [
      'Введение Табели о рангах',
      'Учреждение первых коллегий',
      'Заключение Ништадтского мирного договора между Россией и Швецией',
      'Основание Санкт-Петербурга',
      'Издание указа о единонаследии'
    ],
    correct: [1, 4]
  };
  questions2[12].options = [
    '«Хожение за три моря»',
    '«Житие протопопа Аввакума, им самим написанное»',
    '«Чтение о Борисе и Глебе»',
    'Изображение 4',
    'Изображение 5'
  ];

  const keys2 = [
    '431', '1342', 'половцы', '25; 52', '3', '2143; 4321', '125',
    'Николай Второй', 'Цусимское', '3', '2', 'Айгунский', '14; 41',
    '4', '2', '4', '1'
  ];
  questions2.forEach((question, index) => {
    question.sourceTask = index + 1;
    question.sourceVariant = 2;
    question.explanation = `Эталон из таблицы ответов: ${keys2[index]}.`;
  });
  window.localInteractiveSources
    .find((source) => source.id === 'artasov-oge-history-2027')
    .variants.push({
      id: 'artasov-oge-history-2027-v2',
      title: 'Вариант 2',
      questions: questions2
    });
})();
