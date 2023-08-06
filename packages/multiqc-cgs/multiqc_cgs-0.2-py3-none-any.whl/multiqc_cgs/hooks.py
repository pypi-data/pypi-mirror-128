#!/usr/bin/env python
""" MultiQC hook functions - we tie into the MultiQC
core here to add in extra functionality. """

import logging
from multiqc.utils import report, config
from collections import OrderedDict

log = logging.getLogger('multiqc')

def after_modules():
    """ Plugin code to run when MultiQC modules have completed  """
    config_data = getattr(config, "multiqc_cgs", {})
    namespace_map = {}
    for index, data in enumerate(report.general_stats_headers):
        if len(data) > 0:
            namespace_map[list(data.items())[0][1]['namespace']] = index
    if config_data:
        log.info("multiqc_cgs: " + config.multiqc_cgs_version + " : modifying General Statistics!")
        for data_namespace in config_data:
            added_entries = []
            for field in config_data[data_namespace]:
                entry = {'namespace': data_namespace}
                for key in config_data[data_namespace][field]:
                    entry[key] = config_data[data_namespace][field][key]
                if 'title' not in entry:
                    entry['title'] = field
                if 'min' not in entry:
                    entry['min'] = 0
                if 'format' not in entry:
                    entry['format'] = '{:,.1f}'
                added_entries.append((field, entry))
            log.debug("Adding extra columns to general statistics: {}".format(added_entries))
            report.general_stats_headers[namespace_map[data_namespace]] = OrderedDict( list(report.general_stats_headers[namespace_map[data_namespace]].items()) + added_entries)
