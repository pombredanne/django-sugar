"""
Utilities to help localize performance problems
"""

from contextlib import contextmanager
import inspect
import time
import sys

from django.db import connection

__all__ = ['query_count']

@contextmanager
def query_count(desc=None, print_queries=False):
    """
    Display a list of the database query count delta for an arbitrary block of
    code enclosed in a with statement::

    with query_count("retrieve user contact preferences"):
        # actually do something

    would display:

    retrieve user contact preferences: 37 queries in 0.53 seconds
    """

    if not desc:
        desc = "[%s:%s]" % inspect.stack()[2][1:3]

    # TODO: Verbose mode which displays queries?
    original_query_count = len(connection.queries)

    start_time = time.time()
    yield
    elapsed = time.time() - start_time

    qc_diff = len(connection.queries) - original_query_count

    print >>sys.stderr, "%s: %d queries in %0.2f seconds" % (
        desc,
        qc_diff,
        elapsed
    )

    if print_queries:
        for i in connection.queries[:-qc_diff]:
            print >>sys.stderr, "\t%(time)s\t%(sql)s" % i