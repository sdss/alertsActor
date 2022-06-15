#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import pathlib
import click

import pytest

from clu import AMQPActor
from clu.testing import setup_test_actor

from clu.parsers.click import CluGroup

from alertsActor.tools import Timer

DATA_DIR = pathlib.Path(os.path.dirname(__file__)) / "data"


@click.group(cls=CluGroup)
def parser(*args):
    pass

@parser.command()
@click.argument('keyword', type=str)
@click.argument('value', type=int)
def modify_state_int(command, keyword, value):
    actor = command.actor
    actor.state[keyword] = value
    print(keyword, value, actor.state)

    command.finish()

@parser.command()
@click.argument('keyword', type=str)
@click.argument('value', type=str)
def modify_state_str(command, keyword, value):
    actor = command.actor
    actor.state[keyword] = value
    command.finish()


class TestActor(AMQPActor):
    parser = parser
    def __init__(self, **kwargs):
        super().__init__(name='test_actor',
                         schema=DATA_DIR / "schema.json",
                         **kwargs)

        self.state = dict()
        self.timer = Timer()

        self.timer.start(1, self.writeStatus)

    def writeStatus(self):
        for keyword, value in self.state.items():
            self.write(message_code="i",
                       message={keyword: value})
        self.timer.start(1, self.writeStatus)


@pytest.fixture
async def test_actor(rabbitmq, event_loop):

    port = rabbitmq.args["port"]

    actor = TestActor(port=port)
    await setup_test_actor(actor)

    yield actor
