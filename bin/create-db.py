#!/usr/bin/env python
from __future__ import absolute_import

from tracker.db import engine
from tracker.models import Base


if __name__ == '__main__':
    Base.metadata.create_all(engine)
