# Copyright 2019 Canonical Ltd.  This software is licensed under the
# GNU Lesser General Public License version 3 (see the file LICENSE).
from collections import defaultdict
import json
import textwrap
from sys import stdout


def write_service_begin(stream, service_name):
    begin = (
        u"\n"
        u"{service_name} = ServiceFactory(\n"
        u"        {service_name!r},\n"
        u"        [\n"
    ).format(
        service_name=service_name
    )
    stream.write(begin)


def write_service_end(stream):
    stream.write(
        u"    ]\n"
        u")\n"
        u"\n"
    )


def write_endpoint_spec(stream, api_data):
    endpoint = (
        u"            EndpointSpec(\n"
        u"                {api_name!r},\n"
        u"                {url!r},\n"
        u"                {methods!r},\n"
        u"                {request_schema!r},\n"
        u"                {response_schema!r}\n"
        u"            ),\n"
    ).format(**api_data)
    stream.write(endpoint)


HEADER_TEXT = u"""\
# This file is AUTO GENERATED. Do not edit this file directly. Instead,
# re-generate it.

from acceptable.mocks import ServiceFactory, EndpointSpec

"""


def write_header(stream):
    stream.write(HEADER_TEXT)


def generate_service_factory(metadata, stream=stdout):
    write_header(stream)
    services = defaultdict(list)
    for module_data in metadata.values():
        if not isinstance(module_data, dict):
            continue
        for api_data in module_data['apis'].values():
            services[api_data['service']].append(api_data)
    for service_name, apis in services.items():
        write_service_begin(stream, service_name)
        for api in apis:
            write_endpoint_spec(stream, api)
        write_service_end(stream)


