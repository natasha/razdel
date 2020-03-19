<img src="https://github.com/natasha/natasha-logos/blob/master/razdel.svg">

![CI](https://github.com/natasha/razdel/workflows/CI/badge.svg) [![codecov](https://codecov.io/gh/natasha/razdel/branch/master/graph/badge.svg)](https://codecov.io/gh/natasha/razdel)

`razdel` — rule-based system for Russian sentence and word tokenization..

## Usage

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

## Installation

`razdel` supports Python 3.5+ and PyPy 3.

```bash
$ pip install razdel
```

## Quality, performance

Unfortunately, there is no single correct way to split text into sentences and tokens. For example, one may split `«Как же так?! Захар...» — воскликнут Пронин.` into three sentences `["«Как же так?!",  "Захар...»", "— воскликнут Пронин."]` while `razdel` splits it into two `["«Как же так?!", "Захар...» — воскликнут Пронин."]`. What would be the correct way to tokenizer `т.е.`? One may split in into `т.|е.`, `razdel` splits into `т|.|е|.`.

`razdel` tries to mimic segmentation of these 4 datasets : [SynTagRus](https://github.com/UniversalDependencies/UD_Russian-SynTagRus), [OpenCorpora](http://opencorpora.org), GICRYA and RNC from [morphoRuEval-2017](https://github.com/dialogue-evaluation/morphoRuEval-2017). These datasets mainly consist of news and fiction. `razdel` is optimized on these types of texts. Library may perform worse on other domains like social media, scientific articles, legal documents.

We measure absolute number of errors. There are a lot of trivial cases in the tokenization task. For example, text `чуть-чуть?!` is not non-trivial, one may split it into `чуть|-|чуть|?|!` while the correct tokenization is `чуть-чуть|?!`, such examples are rare. Vast majority of cases are trivial, for example text `в 5 часов ...` is correctly tokenized even via Python native `str.split` into `в| |5| |часов| |...`. Due to the large number of trivial case overall quality of all segmenators is high, it is hard to compare differentiate between for examlpe 99.33%, 99.95% and 99.88%, so we report the absolute number of errors.

`errors` — number of errors. For example, consider etalon segmentation is `что-то|?`, prediction is `что|-|то?`, then the number of errors is 3: 1 for missing split `то?` + 2 for extra splits `что|-|то`.

`time` — total seconds taken.

Definitions for `spacy_tokenize`, `aatimofeev` and other can be found in [segmenters.py](https://github.com/natasha/naeval/blob/master/neaval/segment/segmenters.py). [eval.ipynb](https://github.com/natasha/razdel/blob/master/eval.ipynb)

### Tokens
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
      <td>4217</td>
      <td>0.5</td>
      <td>2914</td>
      <td>0.5</td>
      <td>2402</td>
      <td>0.3</td>
      <td>8630</td>
      <td>0.3</td>
    </tr>
    <tr>
      <th>spacy_tokenize</th>
      <td>3283</td>
      <td>5.6</td>
      <td>2639</td>
      <td>5.5</td>
      <td>1742</td>
      <td>3.8</td>
      <td>4010</td>
      <td>3.5</td>
    </tr>
    <tr>
      <th>nltk.word_tokenize</th>
      <td>5712</td>
      <td>3.7</td>
      <td>67523</td>
      <td>3.9</td>
      <td>12149</td>
      <td>2.7</td>
      <td>13564</td>
      <td>2.8</td>
    </tr>
    <tr>
      <th>mystem</th>
      <td>4280</td>
      <td>4.9</td>
      <td>3624</td>
      <td>4.6</td>
      <td>2515</td>
      <td>3.6</td>
      <td><b>1812</b></td>
      <td>3.5</td>
    </tr>
    <tr>
      <th>moses</th>
      <td><b>1188</b></td>
      <td><b>2.0</b></td>
      <td><b>1641</b></td>
      <td><b>2.1</b></td>
      <td>1696</td>
      <td><b>1.7</b></td>
      <td>2486</td>
      <td><b>1.7</b></td>
    </tr>
    <tr>
      <th>segtok.word_tokenize</th>
      <td>1491</td>
      <td><b>2.4</b></td>
      <td><b>1552</b></td>
      <td><b>2.4</b></td>
      <td><b>1657</b></td>
      <td><b>1.8</b></td>
      <td><b>1238</b></td>
      <td><b>1.8</b></td>
    </tr>
    <tr>
      <th>aatimofeev</th>
      <td><b>1485</b></td>
      <td>56.2</td>
      <td><b>1225</b></td>
      <td>53.3</td>
      <td><b>630</b></td>
      <td>39.2</td>
      <td>2972</td>
      <td>47.6</td>
    </tr>
    <tr>
      <th>razdel.tokenize</th>
      <td><b>1158</b></td>
      <td><b>2.9</b></td>
      <td>1861</td>
      <td><b>3.0</b></td>
      <td><b>315</b></td>
      <td><b>2.0</b></td>
      <td><b>2264</b></td>
      <td><b>2.1</b></td>
    </tr>
  </tbody>
</table>

### Sentencies
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
      <td>19974</td>
      <td>0.7</td>
      <td>5986</td>
      <td>0.4</td>
      <td>9380</td>
      <td>0.5</td>
      <td>22483</td>
      <td>0.8</td>
    </tr>
    <tr>
      <th>segtok.split_single</th>
      <td>19450</td>
      <td>16.5</td>
      <td><b>4140</b></td>
      <td>10.3</td>
      <td>158672</td>
      <td><b>1.5</b></td>
      <td>172887</td>
      <td><b>3.1</b></td>
    </tr>
    <tr>
      <th>moses</th>
      <td>60212</td>
      <td>10.6</td>
      <td>39361</td>
      <td><b>5.4</b></td>
      <td>12238</td>
      <td>5.7</td>
      <td>168743</td>
      <td>385.1</td>
    </tr>
    <tr>
      <th>nltk.sent_tokenize</th>
      <td><b>16346</b></td>
      <td><b>8.8</b></td>
      <td>4194</td>
      <td><b>4.3</b></td>
      <td><b>6774</b></td>
      <td><b>4.2</b></td>
      <td><b>32391</b></td>
      <td><b>5.4</b></td>
    </tr>
    <tr>
      <th>deeppavlov</th>
      <td><b>10138</b></td>
      <td><b>9.9</b></td>
      <td><b>1180</b></td>
      <td>6.0</td>
      <td><b>8402</b></td>
      <td>5.6</td>
      <td><b>20717</b></td>
      <td>93.4</td>
    </tr>
    <tr>
      <th>razdel.sentenize</th>
      <td><b>9408</b></td>
      <td><b>5.4</b></td>
      <td><b>798</b></td>
      <td><b>3.4</b></td>
      <td><b>11020</b></td>
      <td><b>3.6</b></td>
      <td><b>10791</b></td>
      <td><b>5.4</b></td>
    </tr>
  </tbody>
</table>

## Support

- Chat — https://telegram.me/natural_language_processing
- Issues — https://github.com/natasha/razdel/issues

## Development

Test

```bash
pip install -e .
pip install -r requirements/ci.txt
make test
make int  # 2000 integration tests
```

Package:

```bash
make version
git push
git push --tags

make clean wheel upload
```

`mystem` errors on `syntag`:

```bash
# see naeval/data
cat syntag_tokens.txt | razdel-ctl sample 1000 | razdel-ctl gen | razdel-ctl diff --show moses_tokenize | less
```

Non-trivial token tests:

```bash
pv data/*_tokens.txt | razdel-ctl gen --recall | razdel-ctl diff space_tokenize > tests.txt
pv data/*_tokens.txt | razdel-ctl gen --precision | razdel-ctl diff re_tokenize >> tests.txt
```

Update integration tests:

```bash
cd razdel/tests/data/
pv sents.txt | razdel-ctl up sentenize > t; mv t sents.txt
```

`razdel` and `moses` diff:

```bash
cat data/*_tokens.txt | razdel-ctl sample 1000 | razdel-ctl gen | razdel-ctl up tokenize | razdel-ctl diff moses_tokenize | less
```

`razdel` performance

```bash
cat data/*_tokens.txt | razdel-ctl sample 10000 | pv -l | razdel-ctl gen | razdel-ctl diff tokenize | wc -l
```
