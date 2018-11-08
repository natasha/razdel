# coding: utf-8
from __future__ import unicode_literals

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
    __attributes__ = ['task', 'score']

    def __init__(self, task, score):
        self.task = task
        self.score = score


def report_tasks(datasets, models, metrics):
    for dataset in datasets:
        for model in models:
            for metric in metrics:
                yield Task(dataset, model, metric)


def run_task(task):
    tests = task.metric.generate_tests(task.dataset.items)
    correct = 0
    total = 0
    for test in tests:
        if task.metric.is_correct(task.model.process, test):
            correct += 1
        total += 1
    score = correct / total
    return Result(task, score)


def result_rows(results):
    for task, score in results:
        yield dict(
            dataset=task.dataset.name,
            model=task.model.name,
            metric=task.metric.name,
            score=score
        )


def show_results(table):
    models = table.model.unique()
    datasets = table.dataset.unique()
    metrics = table.metric.unique()
    table = table.pivot_table(
        index='model',
        columns=['dataset', 'metric'],
        values='score'
    )
    table = table.reindex(
        index=models,
        columns=[
            (dataset, metric)
            for dataset in datasets
            for metric in metrics
        ]
    )
    table.index.name = None
    table.columns.names = None, None
    return table
