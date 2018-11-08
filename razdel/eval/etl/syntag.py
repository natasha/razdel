# coding: utf-8
from __future__ import unicode_literals

import re

from .common import is_sent


def parse_sents(lines):
    lines = iter(lines)
    for line in lines:
        match = re.match(r'^# sent_id = (.+)$', line)
        if match:
            id = match.group(1)
            match = re.match(r'^([^.]+).xml_\d+$', id)
            doc = match.group(1)
            line = next(lines)
            match = re.match(r'# text = (.+)$', line)
            text = match.group(1).strip()
            if is_sent(text):
                yield doc, text
