# encoding: utf-8

from warnings import warn
import optparse
import logging
import sys
import traceback

from django.core.management.base import BaseCommand
from django.conf import settings


class LoggingCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
        optparse.make_option('--log-level', dest='log_level', default='warning',
                             help="Log Level (debug, info, warning, or error)"),
    )

    def configure_logging(self, options):
        if getattr(settings, "LOGGING_PRECONFIGURED", False):
            return

        std_format = options.get("log_format", getattr(settings, "LOGGING_FORMAT",
            '%(asctime)s [%(name)s] %(levelname)8s %(module)s.%(funcName)s: %(message)s'))

        if "log_level" in options:
            log_level = options['log_level']
            try:
                log_level = int(log_level)
            except:
                log_level = getattr(logging, log_level.upper(), None)
                if not log_level:
                    print >> sys.stderr, "Unknown log level %s; using INFO instead" % log_level
                    log_level = logging.INFO
        else:
            verbosity = int(options.get("verbosity", 0))
            if verbosity > 1:
                log_level = logging.DEBUG
            elif verbosity > 0:
                log_level = logging.INFO
            else:
                log_level = logging.WARNING

        root_logger = logging.getLogger()

        # We're going to rudely reconfigure logging since it's probably been
        # configured incorrectly by now:
        for handler in root_logger.root.handlers:
            root_logger.removeHandler(handler)
            try:
                handler.close()
            except KeyError, e:
                warn("Error closing logger %s: %s (n.b. this may be a Ubuntu feature" % (handler, e))

        console_log = logging.StreamHandler(sys.stderr)
        console_log.setFormatter(logging.Formatter(std_format))
        console_log.setLevel(log_level)

        root_logger.setLevel(log_level)
        root_logger.addHandler(console_log)

        # Catch exceptions during logging: contrary to the docs this doesn't
        # work by default:
        logging.raiseExceptions = True

        def err_handler(self, record):
            exc_type, exc_val, tb = sys.exc_info()
            traceback.print_exception(exc_type, exc_val, tb, limit=None, file=sys.stderr)
            raise exc_val

        logging.Handler.handleError = err_handler
