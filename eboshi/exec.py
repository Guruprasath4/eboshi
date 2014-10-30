#!/usr/bin/env python
# encoding: utf-8

import logging

from cliff.command import Command

import requests
import os.path
from eboshi.session import Session
from eboshi.project import Project
from ast import literal_eval

class Exec(Command):
    "schedule azkaban job"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Exec, self).get_parser(prog_name)
        parser.add_argument('--url', required=True)
        parser.add_argument('--username', required=True)
        parser.add_argument('--password', required=True)
        parser.add_argument('--project', required=True)
        parser.add_argument('--flow', required=True)
        return parser

    def take_action(self, parsed_args):
        url = parsed_args.url
        username = parsed_args.username
        password = parsed_args.password
        session = Session(url, username, password)
        session_id = session.get_session_id()
        project = parsed_args.project
        flow = parsed_args.flow
        params = {"ajax":"executeFlow"}
        params["session.id"] = session_id
        params["project"] = project
        params["flow"] = flow
        r = requests.get(url + "/executor", params=params)
        jc = r.json()
        if jc.get("execid") is None:
            raise Exception("exec failed. project=%s. flow=%s. message=%s. error=%s" % (jc.get("project"), jc.get("flow"), jc.get("message"), jc.get("error")))
        else:
            print "exec succeeded. execid=%s. project=%s. flow=%s. message=%s" % (jc.get("execid"), jc.get("project"), jc.get("flow"), jc.get("message"))