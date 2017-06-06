# -*- coding: utf-8 -*-
import json
import falcon

from app import logger
from app.errors import InvalidParameterError

LOG = logger.get_logger()


class JSONTranslator(object):

    def process_request(self, req, res):
        if req.content_type == 'application/json':
            try:
                raw_json = req.stream.read()
            except Exception:
                message = 'Read Error'
                raise falcon('Bad request', message)
            try:
                req.context['data'] = json.loads(raw_json.decode('utf-8'))
                LOG.info(req.context['data'])
            except ValueError:
                error_msg = 'No JSON object could be decoded or Malformed JSON'
                InvalidParameterError(error_msg)
