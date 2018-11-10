# razdel [![Build Status](https://travis-ci.org/natasha/razdel.svg?branch=master)](https://travis-ci.org/natasha/razdel)

`razdel` — библиотека для разделения русскоязычного текста на токены и предложения. Система построена на правилах. 

## Использование

```python
>>> from razdel import tokenize

>>> tokens = list(tokenize('Кружка-термос на 0.5л (50/64 см³, 516;...)'))
>>> tokens
[Substring(0, 13, 'Кружка-термос'),
 Substring(14, 16, 'на'),
 Substring(17, 20, '0.5'),
 Substring(20, 21, 'л'),
 Substring(22, 23, '(')
 ...]
 
>>> [_.text for _ in tokens]
['Кружка-термос', 'на', '0.5', 'л', '(', '50/64', 'см³', ',', '516', ';', '...', ')']
```

```python
>>> from razdel import sentenize

>>> text = '''
... - "Так в чем же дело?" - "Не ра-ду-ют".
... И т. д. и т. п. В общем, вся газета
... '''

>>> list(sentenize(text))
[Substring(1, 23, '- "Так в чем же дело?"'),
 Substring(24, 40, '- "Не ра-ду-ют".'),
 Substring(41, 56, 'И т. д. и т. п.'),
 Substring(57, 76, 'В общем, вся газета')]
```

## Установка

`razdel` поддерживает Python 2.7+, 3.4+ и PyPy 2, 3.

```bash
$ pip install razdel
```

## Качество

**Важно!** Качество оценивалось на четырёх датасетах: [SynTagRus](https://github.com/UniversalDependencies/UD_Russian-SynTagRus), [OpenCorpora](http://opencorpora.org), ГИКРЯ и РНК из репозитория [morphoRuEval-2017](https://github.com/dialogue-evaluation/morphoRuEval-2017). В основном это новостных тексты и литература. На текстах другой тематики (социальные сети, научные статьи) `razdel` может работать хуже.

Запись в таблице, например, "1863 (1857 + 6), 13.2s" означает 1857 precision-ошибок, 6 recall-ошибок, "13.2s" — время выполнения. Мы считаем число ошибок, а не их долю, потому что в задаче токенизации очень много тривиальных тестов. Например, тест "чуть-чуть?!" нетривиальный, в нём токенизатор может ошибиться, дать ответ "чуть", "-", "чуть", "?", "!",  хотя эталон "чуть-чуть", "?!", таких тестов мало. Большинство фраз простые, например для словосочетания "в 5 часов ...", правильный ответ даст даже `str.split`: "в", "5", "часов", "...". Из-за тривиальных тестов качество всех систем получается высокое, тяжело оценить разницу между, например, "98.33%, 99.12%, 97.05%, 98.8%", поэтому мы пишем абсолютное число ошибок.

Precision-ошибки считались так: возьмём все токены из разметки, например, "что-то", проверим, что токенизатор не делит их на части. Recall-ошибки считались так: возьмём все биграммы токенов, например, "что-то?", проверим, что разделение происходит там где нужно, результат "что", "-", "то", "?" не считается recall-ошибкой, "то" и "?" разделены.

Что такое, например, `spacy_tokenize`, `spacy_tokenize2` написано в [eval/zoo.py](https://github.com/natasha/razdel/blob/master/razdel/eval/zoo.py). Таблицы вычисляются в [eval.ipynb](https://github.com/natasha/razdel/blob/master/eval.ipynb)

### Токены
`errors (precision errors + recall errors), time`, чем меньше, тем лучше:
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>corpora</th>
      <th>syntag</th>
      <th>gicrya</th>
      <th>rnc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>re.findall(\w+|\d+|\p+)</th>
      <td>1863 (1857 + 6), 12.6s</td>
      <td>1613 (1460 + 153), 14.9s</td>
      <td>1188 (1188 + 0), 11.3s</td>
      <td>5005 (5002 + 3), 11.9s</td>
    </tr>
    <tr>
      <th>nltk.word_tokenize</th>
      <td>1666 (120 + 1546), 141.6s</td>
      <td>1685 (313 + 1372), 145.5s</td>
      <td>169 (169 + 0), 105.2s</td>
      <td>1987 (1752 + 235), 118.6s</td>
    </tr>
    <tr>
      <th>spacy_tokenize</th>
      <td>2846 (1122 + 1724), 69.8s</td>
      <td>2068 (987 + 1081), 72.6s</td>
      <td>905 (905 + 0), 51.2s</td>
      <td>2706 (2706 + 0), 54.6s</td>
    </tr>
    <tr>
      <th>spacy_tokenize2</th>
      <td>2102 (378 + 1724), 89.2s</td>
      <td>1272 (191 + 1081), 86.7s</td>
      <td>226 (226 + 0), 63.6s</td>
      <td>1877 (1877 + 0), 65.3s</td>
    </tr>
    <tr>
      <th>mystem</th>
      <td>2577 (908 + 1669), 70.6s</td>
      <td>2137 (720 + 1417), 70.5s</td>
      <td>1156 (950 + 206), 53.2s</td>
      <td>1297 (1124 + 173), 49.9s</td>
    </tr>
    <tr>
      <th>razdel.tokenize</th>
      <td>348 (270 + 78), 29.4s</td>
      <td>460 (383 + 77), 29.0s</td>
      <td>151 (151 + 0), 21.3s</td>
      <td>1755 (1752 + 3), 19.0s</td>
    </tr>
  </tbody>
</table>

### Предложения
<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>corpora</th>
      <th>syntag</th>
      <th>gicrya</th>
      <th>rnc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>re.split([.?!…])</th>
      <td>8027 (5615 + 2412), 13.1s</td>
      <td>2188 (1761 + 427), 6.1s</td>
      <td>4096 (2413 + 1683), 8.3s</td>
      <td>8191 (6587 + 1604), 9.4s</td>
    </tr>
    <tr>
      <th>nltk.sent_tokenize</th>
      <td>7752 (3703 + 4049), 58.1s</td>
      <td>1907 (951 + 956), 31.6s</td>
      <td>2212 (829 + 1383), 36.1s</td>
      <td>11390 (6216 + 5174), 42.5s</td>
    </tr>
    <tr>
      <th>segtok.split_single</th>
      <td>8981 (2306 + 6675), 75.2s</td>
      <td>1971 (1090 + 881), 49.5s</td>
      <td>79135 (914 + 78221), 12.9s</td>
      <td>86252 (1206 + 85046), 20.5s</td>
    </tr>
    <tr>
      <th>deepmipt</th>
      <td>4529 (925 + 3604), 35.3s</td>
      <td>579 (114 + 465), 24.5s</td>
      <td>3502 (1647 + 1855), 24.7s</td>
      <td>7487 (5965 + 1522), 26.0s</td>
    </tr>
    <tr>
      <th>razdel.sentenize</th>
      <td>4323 (584 + 3739), 25.7s</td>
      <td>369 (92 + 277), 18.6s</td>
      <td>5872 (1276 + 4596), 18.1s</td>
      <td>4903 (2007 + 2896), 21.7s</td>
    </tr>
  </tbody>
</table>

## Лицензия

MIT

## Поддержка

- Чат — https://telegram.me/natural_language_processing
- Тикеты — https://github.com/natasha/razdel/issues

