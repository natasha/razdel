# razdel [![Build Status](https://travis-ci.org/natasha/razdel.svg?branch=master)](https://travis-ci.org/natasha/razdel)

`razdel` — библиотека для разделения русскоязычного текста на токены и предложения. Система построена на правилах. 

`razdel` — a library for Russian sentence and word tokenization. It is a rule-based system.


## Использование (Usage)

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

## Установка (Installation)

`razdel` поддерживает Python 2.7+, 3.4+ и PyPy 2, 3.

`razdel` supports Python 2.7+, 3.4+ and PyPy 2, 3.

```bash
$ pip install razdel
```

## Качество (Quality)

**Важно!** К сожалению, в задаче разделения текста на предложения и токены нет одного правильного ответа. Как, например, разбить на предложения текст `«Как же так?! Захар...» — воскликнут Пронин.`? Можно считать, что это одно предложение, можно разбить на три `«Как же так?!| |Захар...»| |— воскликнут Пронин.`, `razdel` разобьёт на два `«Как же так?!| |Захар...» — воскликнут Пронин.`. Как разделить на токены сокращение `т.е.`? Можно считать, что это один токен, можно рабить на `т.|е.`, `razdel` разобъёт на `т|.|е|.`.

`razdel` старается разбивать текст на предложения и токены так, как это сделано в 4 датасетах: 

 - [SynTagRus](https://github.com/UniversalDependencies/UD_Russian-SynTagRus), 
 - [OpenCorpora](http://opencorpora.org), 
 - ГИКРЯ и РНК из репозитория [morphoRuEval-2017](https://github.com/dialogue-evaluation/morphoRuEval-2017). 

В основном это новостные тексты и литература. Правила `razdel` заточены под них. На текстах другой тематики (социальные сети, научные статьи) библиотека может работать хуже.

Мы считаем число ошибок, а не их долю, потому что в задаче токенизации очень много тривиальных тестов. Например, тест `чуть-чуть?!` нетривиальный, в нём токенизатор может ошибиться, дать ответ `чуть|-|чуть|?|!`,  хотя эталон `чуть-чуть|?!`, таких тестов мало. Большинство фраз простые, например для словосочетания `в 5 часов ...`, правильный ответ даст даже `str.split`: `в| |5| |часов| |...`. Из-за тривиальных тестов качество всех систем получается высокое, тяжело оценить разницу между, например, `99.33% 99.12% 99.95% 99.88%`, поэтому мы пишем абсолютное число ошибок.

`errors` — число ошибок, состоит из precision и recall-ошибок. Precision-ошибки считались так: возьмём все токены из разметки, например, `что-то`, проверим, что токенизатор не делит их на части. Recall-ошибки считались так: возьмём все биграммы токенов, например, `что-то?`, проверим, что разделение происходит между токенами, результат `что|-|то|?` не считается recall-ошибкой, `то` и `?` разделены.

`time` — время выполнения.

Что такое, например, `spacy_tokenize`, `spacy_tokenize2` написано в [eval/zoo.py](https://github.com/natasha/razdel/blob/master/razdel/eval/zoo.py). Таблицы вычисляются в [eval.ipynb](https://github.com/natasha/razdel/blob/master/eval.ipynb)



**Important!** Unfortunately, there is no correct output in the task of sentence and word tokenization. For example, to break up the text, `«Как же так?! Захар...» — воскликнут Пронин.`, we can split it into three sentences `["«Как же так?!",  "Захар...»", "— воскликнут Пронин."]` but `razdel` sentence tokenizer splits it into two `["«Как же так?!", "Захар...» — воскликнут Пронин."]`. Another issue is with abbrevations, although the tokenizer should recognize it as a single token, `razdel` word tokenizer split it up into `["т", ".", "е", "."]`.

`razdel` tries to split sentences and words/tokens as how it is done in these datasets:

 - [SynTagRus] (https://github.com/UniversalDependencies/UD_Russian-SynTagRus)
 - [OpenCorpora] (http://opencorpora.org)
 - GIKRYA and RNC corpora from [morphoRuEval-2017](https://github.com/dialogue-evaluation/morphoRuEval-2017)

These are mainly news and literary texts. The rules in `razdel` are based on these texts. On other domains (like social media, scientific articles), the library may not perform well.

We consider the absolute no. of errors and not the percentage because there are a lot of trival cases in the tokenization tasks that requires only simple rules and they should not be wrong. For example, this token is non-trival to split `чуть-чуть?!`, most tokenizer will mistakenly split the multi-word reduplication example and output `["чуть", "-", "чуть", "?", "!"]` but the correct tokenization should be `["чуть-чуть, "?!"]`; but examples like these are few in the datasets. For most cases, the dataset contains trival examples, e.g. `в 5 часов ...` that even the Python native `str.split` can output the right tokenization `["в", "5", "часов", "..."]`. Due to these trival test cases, the quality of the other systems can be relatively high, and it makes it different to diffientiate the quality of systems that achieved 99.33%, 99.12%, 99.95% and 99.88%, thus we report the absolute no. of errors instead of the percentage.

In the following table, `error` refers to the total no. of errors that sums the "precision-errors" and "recall-errors". We consider the following as a "precision-error". "Precision-errors" refers to the no. of tokens that should be seperated but wasn't split by the tool, e.g. `что-то?` should be split into `["что-то", "?"]` but the tool didn't split it.  "Recall-errors" refers to the no. of tokens that was split but wasn't split correctly, e.g. `что-то?` was split wrongly into `["что", "-", "то", "?"]` by the tool.

`time` in the following table refers to the runtime taken to complete the tokenization of the respective datasets.



### Токены
<table border="0" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="2" halign="left">corpora</th>
      <th colspan="2" halign="left">syntag</th>
      <th colspan="2" halign="left">gicrya</th>
      <th colspan="2" halign="left">rnc</th>
    </tr>
    <tr>
      <th></th>
      <th>errors</th>
      <th>time</th>
      <th>errors</th>
      <th>time</th>
      <th>errors</th>
      <th>time</th>
      <th>errors</th>
      <th>time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>re.findall(\w+|\d+|\p+)</th>
      <td>1863</td>
      <td>13.39</td>
      <td>1613</td>
      <td>14.74</td>
      <td>1188</td>
      <td>11.89</td>
      <td>5005</td>
      <td>12.64</td>
    </tr>
    <tr>
      <th>nltk.word_tokenize</th>
      <td>1666</td>
      <td>141.41</td>
      <td>1685</td>
      <td>146.76</td>
      <td>169</td>
      <td>106.38</td>
      <td>1987</td>
      <td>116.64</td>
    </tr>
    <tr>
      <th>spacy_tokenize</th>
      <td>2846</td>
      <td>73.26</td>
      <td>2068</td>
      <td>72.23</td>
      <td>905</td>
      <td>50.41</td>
      <td>2706</td>
      <td>51.05</td>
    </tr>
    <tr>
      <th>spacy_tokenize2</th>
      <td>2102</td>
      <td>90.61</td>
      <td>1272</td>
      <td>89.12</td>
      <td>226</td>
      <td>63.28</td>
      <td>1877</td>
      <td>67.53</td>
    </tr>
    <tr>
      <th>mystem</th>
      <td>2577</td>
      <td>73.33</td>
      <td>2137</td>
      <td>72.51</td>
      <td>1156</td>
      <td>55.75</td>
      <td>1297</td>
      <td>57.73</td>
    </tr>
    <tr>
      <th>moses</th>
      <td>1335</td>
      <td>64.10</td>
      <td>1405</td>
      <td>65.34</td>
      <td>808</td>
      <td>49.13</td>
      <td>1748</td>
      <td>52.48</td>
    </tr>
    <tr>
      <th>segtok.word_tokenize</th>
      <td>414</td>
      <td>52.69</td>
      <td>584</td>
      <td>54.60</td>
      <td>830</td>
      <td>40.70</td>
      <td><b>1252</b></td>
      <td>39.18</td>
    </tr>
    <tr>
      <th>razdel.tokenize</th>
      <td><b>348</b></td>
      <td><b>27.99</b></td>
      <td><b>460</b></td>
      <td><b>28.36</b></td>
      <td><b>151</b></td>
      <td><b>21.22</b></td>
      <td>1755</td>
      <td><b>18.54</b></td>
    </tr>
  </tbody>
</table>

### Предложения
<table border="0" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="2" halign="left">corpora</th>
      <th colspan="2" halign="left">syntag</th>
      <th colspan="2" halign="left">gicrya</th>
      <th colspan="2" halign="left">rnc</th>
    </tr>
    <tr>
      <th></th>
      <th>errors</th>
      <th>time</th>
      <th>errors</th>
      <th>time</th>
      <th>errors</th>
      <th>time</th>
      <th>errors</th>
      <th>time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>re.split([.?!…])</th>
      <td>8027</td>
      <td>10.19</td>
      <td>2188</td>
      <td>6.59</td>
      <td>4096</td>
      <td>7.79</td>
      <td>8191</td>
      <td>10.37</td>
    </tr>
    <tr>
      <th>moses</th>
      <td>17131</td>
      <td>73.15</td>
      <td>8274</td>
      <td>47.13</td>
      <td>6698</td>
      <td>55.79</td>
      <td>21743</td>
      <td>69.20</td>
    </tr>
    <tr>
      <th>nltk.sent_tokenize</th>
      <td>7752</td>
      <td>57.96</td>
      <td>1907</td>
      <td>34.52</td>
      <td><b>2212</b></td>
      <td>39.40</td>
      <td>11390</td>
      <td>49.64</td>
    </tr>
    <tr>
      <th>segtok.split_single</th>
      <td>8981</td>
      <td>79.18</td>
      <td>1971</td>
      <td>49.67</td>
      <td>79135</td>
      <td><b>13.92</b></td>
      <td>86252</td>
      <td>23.07</td>
    </tr>
    <tr>
      <th>deepmipt</th>
      <td>4529</td>
      <td>38.37</td>
      <td>579</td>
      <td>23.20</td>
      <td>3502</td>
      <td>26.86</td>
      <td>7487</td>
      <td>26.18</td>
    </tr>
    <tr>
      <th>razdel.sentenize</th>
      <td><b>4323</b></td>
      <td><b>26.75</b></td>
      <td><b>369</b></td>
      <td><b>16.09</b></td>
      <td>5872</td>
      <td>19.46</td>
      <td><b>4903</b></td>
      <td><b>19.56</b></td>
    </tr>
  </tbody>
</table>

## Лицензия (License)

MIT

## Поддержка (Support)

- Чат (Chat) — https://telegram.me/natural_language_processing
- Тикеты (Gihtub Issues) — https://github.com/natasha/razdel/issues


## Разработка (Contributing/Development)

Тесты (Tests)

```bash
pip install -e .
pip install -r requirements.txt
make test
make int  # 2000 integration tests
```

Алиас (Alias) `ctl`

```bash
source alias.sh
```

Посмотреть ошибки `mystem` на `syntag`.

To check the errors made by the `mystem` tool on the `syntag` corpus.

```bash
cat data/syntag_tokens.txt | ctl sample 1000 | ctl gen | ctl diff --show moses_tokenize | less
```

Нетривиальные тесты для токенов (Non-trivial test tokens)

```bash
pv data/*_tokens.txt | ctl gen --recall | ctl diff space_tokenize > tests.txt
pv data/*_tokens.txt | ctl gen --precision | ctl diff re_tokenize >> tests.txt
```

Обновить интеграционные тесты (Update the Continuous Integration (CI) tests)

```bash
cd razdel/tests/data/
pv sents.txt | ctl up sentenize > t; mv t sents.txt
```

Посмотреть различия токенизации `razdel` и `moses`

```bash
cat data/*_tokens.txt | ctl sample 1000 | ctl gen | ctl up tokenize | ctl diff moses_tokenize | less
```

Измерить производительность `razdel`

To check the diffference between `razdel` and `moses` tokenizers

```bash
cat data/*_tokens.txt | ctl sample 10000 | pv -l | ctl gen | ctl diff tokenize | wc -l
```
