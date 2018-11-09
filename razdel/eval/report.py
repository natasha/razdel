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
    __attributes__ = ['task', 'correct', 'total', 'time']

    def __init__(self, task, correct, total, time):
        self.task = task
        self.correct = correct
        self.total = total
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
    return Result(task, correct, total, time)


def result_rows(results):
    for _ in results:
        yield dict(
            dataset=_.task.dataset.name,
            model=_.task.model.name,
            metric=_.task.metric.name,
            correct=_.correct,
            total=_.total,
            time=_.time
        )


def show_results(table):
    models = table.model.unique()
    datasets = table.dataset.unique()
    table = table.pivot_table(
        index=['model', 'dataset'],
        columns='metric'
    )
    time = table.pop('time')
    correct = table.pop('correct')
    total = table.pop('total')
    table.columns = []  # remove levels
    table['time'] = time.precision + time.recall
    table['precision'] = total.precision - correct.precision
    table['recall'] = total.recall - correct.recall
    table['errors'] = table.precision + table.recall
    table = table.apply(
        '{0.errors:.0f} ({0.precision:.0f} '
        '+ {0.recall:.0f}), {0.time:.1f}s'.format,
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
