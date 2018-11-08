# coding: utf-8
from __future__ import unicode_literals

from time import time as clock

from razdel.utils import Record


class Dataset(Record):
    __attributes__ = ['name']

    def __init__(self, name, items):
        self.name = name
        self.items = items


class Model(Record):
    __attributes__ = ['name']

    def __init__(self, name, process):
        self.name = name
        self.process = process


class Metric(Record):
    __attributes__ = ['name']

    def __init__(self, name, generate_tests, is_correct):
        self.name = name
        self.generate_tests = generate_tests
        self.is_correct = is_correct


class Task(Record):
    __attributes__ = ['dataset', 'model', 'metric']

    def __init__(self, dataset, model, metric):
        self.dataset = dataset
        self.model = model
        self.metric = metric


class Result(Record):
    __attributes__ = ['task', 'score', 'time']

    def __init__(self, task, score, time):
        self.task = task
        self.score = score
        self.time = time


def report_tasks(datasets, models, metrics):
    for dataset in datasets:
        for model in models:
            for metric in metrics:
                yield Task(dataset, model, metric)


def run_task(task):
    tests = task.metric.generate_tests(task.dataset.items)
    correct = 0
    total = 0
    start = clock()
    for test in tests:
        if task.metric.is_correct(task.model.process, test):
            correct += 1
        total += 1
    time = clock() - start
    score = correct / total
    return Result(task, score, time)


def result_rows(results):
    for task, score, time in results:
        yield dict(
            dataset=task.dataset.name,
            model=task.model.name,
            metric=task.metric.name,
            score=score,
            time=time
        )


def harm_mean(a, b):
    return 2 * a * b / (a + b)


def show_results(table):
    models = table.model.unique()
    datasets = table.dataset.unique()
    table = table.pivot_table(
        index=['model', 'dataset'],
        columns='metric'
    )
    time = table.pop('time')
    score = table.pop('score')
    table.columns = []  # remove levels
    table['time'] = time.precision + time.recall
    table['precision'] = score.precision
    table['recall'] = score.recall
    table['f1'] = harm_mean(score.precision, score.recall)
    table = table.apply(
        'f1:{0.f1:.4f} (p:{0.precision:.2f}, '
        'r:{0.recall:.2f}), {0.time:.1f}s'.format,
        axis=1
    )
    table = table.unstack()
    table = table.reindex(
        index=models,
        columns=datasets
    )
    table.index.name = None
    table.columns.name = None
    return table
