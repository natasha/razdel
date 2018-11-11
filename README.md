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
      <th>re.findall(\w+|\d+|\p+)</th>
      <td>1863 (1857 + 6), 13.6s</td>
      <td>1613 (1460 + 153), 14.9s</td>
      <td>1188 (1188 + 0), 11.4s</td>
      <td>5005 (5002 + 3), 11.6s</td>
    </tr>
    <tr>
      <th>nltk.word_tokenize</th>
      <td>1666 (120 + 1546), 141.9s</td>
      <td>1685 (313 + 1372), 145.2s</td>
      <td>169 (169 + 0), 110.0s</td>
      <td>1987 (1752 + 235), 114.8s</td>
    </tr>
    <tr>
      <th>spacy_tokenize</th>
      <td>2846 (1122 + 1724), 75.3s</td>
      <td>2068 (987 + 1081), 71.9s</td>
      <td>905 (905 + 0), 54.0s</td>
      <td>2706 (2706 + 0), 53.3s</td>
    </tr>
    <tr>
      <th>spacy_tokenize2</th>
      <td>2102 (378 + 1724), 92.3s</td>
      <td>1272 (191 + 1081), 92.2s</td>
      <td>226 (226 + 0), 66.3s</td>
      <td>1877 (1877 + 0), 65.1s</td>
    </tr>
    <tr>
      <th>mystem</th>
      <td>2577 (908 + 1669), 74.7s</td>
      <td>2137 (720 + 1417), 73.1s</td>
      <td>1156 (950 + 206), 53.7s</td>
      <td>1297 (1124 + 173), 61.0s</td>
    </tr>
    <tr>
      <th>moses</th>
      <td>1335 (187 + 1148), 66.0s</td>
      <td>1405 (338 + 1067), 65.3s</td>
      <td>808 (808 + 0), 47.1s</td>
      <td>1748 (1745 + 3), 49.8s</td>
    </tr>
    <tr>
      <th>razdel.tokenize</th>
      <td>348 (270 + 78), 28.7s</td>
      <td>460 (383 + 77), 28.4s</td>
      <td>151 (151 + 0), 20.2s</td>
      <td>1755 (1752 + 3), 19.1s</td>
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
      <td>8027 (5615 + 2412), 10.2s</td>
      <td>2188 (1761 + 427), 6.4s</td>
      <td>4096 (2413 + 1683), 8.0s</td>
      <td>8191 (6587 + 1604), 9.5s</td>
    </tr>
    <tr>
      <th>moses</th>
      <td>17131 (8862 + 8269), 69.1s</td>
      <td>8274 (5255 + 3019), 45.9s</td>
      <td>6698 (1800 + 4898), 55.3s</td>
      <td>21743 (9300 + 12443), 68.4s</td>
    </tr>
    <tr>
      <th>nltk.sent_tokenize</th>
      <td>7752 (3703 + 4049), 54.4s</td>
      <td>1907 (951 + 956), 33.4s</td>
      <td>2212 (829 + 1383), 39.0s</td>
      <td>11390 (6216 + 5174), 48.7s</td>
    </tr>
    <tr>
      <th>segtok.split_single</th>
      <td>8981 (2306 + 6675), 78.6s</td>
      <td>1971 (1090 + 881), 49.0s</td>
      <td>79135 (914 + 78221), 16.4s</td>
      <td>86252 (1206 + 85046), 22.8s</td>
    </tr>
    <tr>
      <th>deepmipt</th>
      <td>4529 (925 + 3604), 37.4s</td>
      <td>579 (114 + 465), 22.7s</td>
      <td>3502 (1647 + 1855), 26.3s</td>
      <td>7487 (5965 + 1522), 28.8s</td>
    </tr>
    <tr>
      <th>razdel.sentenize</th>
      <td>4323 (584 + 3739), 26.7s</td>
      <td>369 (92 + 277), 16.0s</td>
      <td>5872 (1276 + 4596), 18.7s</td>
      <td>4903 (2007 + 2896), 26.7s</td>
    </tr>
  </tbody>
</table>

## Лицензия

MIT

## Поддержка

- Чат — https://telegram.me/natural_language_processing
- Тикеты — https://github.com/natasha/razdel/issues

## Разработка

Тесты

```bash
pip install -e .
pip install -r requirements.txt
make test
make int  # 2000 integration tests
```

Алиас `ctl`

```bash
source alias.sh
```

Посмотреть ошибки `mystem` на `syntag`

```bash
cat data/syntag_tokens.txt | ctl sample 1000 | ctl gen | ctl diff --show moses_tokenize | less
```

Нетривиальные тесты для токенов

```bash
pv data/*_tokens.txt | ctl gen --recall | ctl diff space_tokenize > tests.txt
pv data/*_tokens.txt | ctl gen --precision | ctl diff re_tokenize >> tests.txt
```

Обновить интеграционные тесты

```bash
cd razdel/tests/data/
pv sents.txt | ctl up sentenize > t; mv t sents.txt
```

Посмотреть различия токенизации `razdel` и `moses`

```bash
cat data/*_tokens.txt | ctl sample 1000 | ctl gen | ctl up tokenize | ctl diff moses_tokenize | less
```
