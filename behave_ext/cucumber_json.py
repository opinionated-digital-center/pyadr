# -*- coding: utf-8 -*-

# from __future__ import absolute_import
import base64
import copy

import six
from behave.formatter.base import Formatter
from behave.model_core import Status

try:
    import json
except ImportError:
    import simplejson as json


# -----------------------------------------------------------------------------
# CLASS: JSONFormatter
# -----------------------------------------------------------------------------
class CucumberJSONFormatter(Formatter):
    name = "json"
    description = "JSON dump of test run"
    dumps_kwargs = {}

    json_number_types = six.integer_types + (float,)
    json_scalar_types = json_number_types + (six.text_type, bool, type(None))

    def __init__(self, stream_opener, config):
        super(CucumberJSONFormatter, self).__init__(stream_opener, config)
        # -- ENSURE: Output stream is open.
        self.stream = self.open()
        self.feature_count = 0
        self.current_feature = None
        self.current_feature_data = None
        self._step_index = 0
        self.current_background = None
        self.current_background_data = None

    def reset(self):
        self.current_feature = None
        self.current_feature_data = None
        self._step_index = 0
        self.current_background = None

    # -- FORMATTER API:
    def uri(self, uri):
        pass

    def feature(self, feature):
        self.reset()
        self.current_feature = feature
        self.current_feature_data = {
            "id": self.generate_id(feature),
            "uri": feature.location.filename,
            "line": feature.location.line,
            "description": "",
            "keyword": feature.keyword,
            "name": feature.name,
            "tags": self.write_tags(feature.tags),
            "status": feature.status.name,
        }
        element = self.current_feature_data
        if feature.description:
            element["description"] = self.format_description(feature.description)

    def background(self, background):
        element = {
            "type": "background",
            "keyword": background.keyword,
            "name": background.name,
            "location": six.text_type(background.location),
            "steps": [],
        }
        self._step_index = 0
        self.current_background = element

    def scenario(self, scenario):
        if self.current_background is not None:
            self.add_feature_element(copy.deepcopy(self.current_background))
        element = self.add_feature_element(
            {
                "type": "scenario",
                "id": self.generate_id(self.current_feature, scenario),
                "line": scenario.location.line,
                "description": "",
                "keyword": scenario.keyword,
                "name": scenario.name,
                "tags": self.write_tags(scenario.tags),
                "location": six.text_type(scenario.location),
                "steps": [],
            }
        )
        if scenario.description:
            element["description"] = self.format_description(scenario.description)
        self._step_index = 0

    @classmethod
    def make_table(cls, table):
        table_data = {
            "headings": table.headings,
            "rows": [list(row) for row in table.rows],
        }
        return table_data

    def step(self, step):
        s = {
            "keyword": step.keyword,
            "step_type": step.step_type,
            "name": step.name,
            "line": step.location.line,
            "result": {"status": "skipped", "duration": 0},
        }

        if step.text:
            s["doc_string"] = {"value": step.text, "line": step.text.line}
        if step.table:
            s["rows"] = [{"cells": list(step.table.headings)}]
            s["rows"] += [{"cells": list(row.cells)} for row in step.table]

        if self.current_feature.background is not None:
            element = self.current_feature_data["elements"][-2]
            if len(element["steps"]) >= len(self.current_feature.background.steps):
                element = self.current_feature_element
        else:
            element = self.current_feature_element
        element["steps"].append(s)

    def match(self, match):
        if match.location:
            # -- NOTE: match.location=None occurs for undefined steps.
            match_data = {
                "location": six.text_type(match.location) or "",
            }
            self.current_step["match"] = match_data

    def result(self, result):
        self.current_step["result"] = {
            "status": result.status.name,
            "duration": int(round(result.duration * 1000.0 * 1000.0 * 1000.0)),
        }
        if result.error_message and result.status == Status.failed:
            # -- OPTIONAL: Provided for failed steps.
            error_message = result.error_message
            result_element = self.current_step["result"]
            result_element["error_message"] = error_message
        self._step_index += 1

    def embedding(self, mime_type, data):
        step = self.current_feature_element["steps"][-1]
        step["embeddings"].append(
            {
                "mime_type": mime_type,
                "data": base64.b64encode(data).replace("\n", ""),
            }
        )

    def eof(self):
        """
        End of feature
        """
        if not self.current_feature_data:
            return

        # -- NORMAL CASE: Write collected data of current feature.
        self.update_status_data()

        if self.feature_count == 0:
            # -- FIRST FEATURE:
            self.write_json_header()
        else:
            # -- NEXT FEATURE:
            self.write_json_feature_separator()

        self.write_json_feature(self.current_feature_data)
        self.current_feature_data = None
        self.feature_count += 1

    def close(self):
        self.write_json_footer()
        self.close_stream()

    # -- JSON-DATA COLLECTION:
    def add_feature_element(self, element):
        assert self.current_feature_data is not None
        if "elements" not in self.current_feature_data:
            self.current_feature_data["elements"] = []
        self.current_feature_data["elements"].append(element)
        return element

    @property
    def current_feature_element(self):
        assert self.current_feature_data is not None
        return self.current_feature_data["elements"][-1]

    @property
    def current_step(self):
        step_index = self._step_index
        if self.current_feature.background is not None:
            element = self.current_feature_data["elements"][-2]
            if step_index >= len(self.current_feature.background.steps):
                step_index -= len(self.current_feature.background.steps)
                element = self.current_feature_element
        else:
            element = self.current_feature_element

        return element["steps"][step_index]

    def update_status_data(self):
        assert self.current_feature
        assert self.current_feature_data
        self.current_feature_data["status"] = self.current_feature.status.name

    def write_tags(self, tags):
        return [
            {"name": tag, "line": tag.line if hasattr(tag, "line") else 1}
            for tag in tags
        ]

    def generate_id(self, feature, scenario=None):
        def convert(name):
            return name.lower().replace(" ", "-")

        id = convert(feature.name)
        if scenario is not None:
            id += ";"
            id += convert(scenario.name)
        return id

    def format_description(self, lines):
        description = "\n".join(lines)
        description = "<pre>%s</pre>" % description
        return description

    # -- JSON-WRITER:
    def write_json_header(self):
        self.stream.write("[\n")

    def write_json_footer(self):
        self.stream.write("\n]\n")

    def write_json_feature(self, feature_data):
        self.stream.write(json.dumps(feature_data, **self.dumps_kwargs))
        self.stream.flush()

    def write_json_feature_separator(self):
        self.stream.write(",\n\n")


# -----------------------------------------------------------------------------
# CLASS: PrettyJSONFormatter
# -----------------------------------------------------------------------------
class PrettyCucumberJSONFormatter(CucumberJSONFormatter):
    """
    Provides readable/comparable textual JSON output.
    """

    name = "json.pretty"
    description = "JSON dump of test run (human readable)"
    dumps_kwargs = {"indent": 2, "sort_keys": True}
