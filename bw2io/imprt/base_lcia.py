from __future__ import print_function
from ..strategies import add_cf_biosphere_activity_hash
from bw2data import methods, Method, mapping, config, Database
from bw2data.utils import recursive_str_to_unicode
from time import time
import functools
import warnings


class LCIAImportBase(object):
    def __init__(self, filepath, biosphere=None):
        self.filepath = filepath
        self.biosphere_name = biosphere or config.biosphere
        self.strategies = [
            functools.partial(add_cf_biosphere_activity_hash,
                              biosphere_db_name=self.biosphere_name),
        ]

    def apply_strategies(self):
        for func in self.strategies:
            try:
                func_name = func.__name__
            except AttributeError:  # Curried function
                func_name = func.func.__name__
            print(u"Applying strategy: {}".format(func_name))
            self.data = func(self.data)

    def write_methods(self, overwrite=False):
        for ds in self.data:
            if ds['name'] in methods:
                if overwrite:
                    del methods[ds['name']]
                else:
                    continue

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                method = Method(ds['name'])
                method.register(
                    description=ds['description'],
                    filename=ds['filename'],
                    unit=ds['unit'],
                )
                method.write(self.reformat_cfs(ds['data']))
                method.process()

    def reformat_cfs(self, ds):
        return [((self.biosphere_name, obj['code']), obj['amount'])
                for obj in ds]

    def format_flow(self, cf):
        return (config.biosphere, cf['code']), {
            'exchanges': [],
            'categories': cf['categories'],
            'name': cf['name'],
            'type': ("resource" if cf["categories"][0] == "resource"
                     else "emission"),
            'unit': cf['unit'],
        }

    def add_missing_cfs(self):
        new_flows = []
        for method in self.data:
            for cf in method['data']:
                if (self.biosphere_name, cf['code']) not in mapping:
                    new_flows.append(cf)

        new_flows = recursive_str_to_unicode(dict(
            [self.format_flow(cf) for cf in new_flows]
        ))

        if new_flows:
            biosphere = Database(config.biosphere)
            biosphere_data = biosphere.load()
            biosphere_data.update(**new_flows)
            biosphere.write(biosphere_data)
            biosphere.process()

            print(u"Added {} new biosphere flows".format(len(new_flows)))

    def statistics(self, print_stats=True):
        num_methods = len(self.data)
        num_cfs = sum([len(ds['data']) for ds in self.data])
        num_unlinked = sum([len([1 for cf in ds['data'] if not cf.get('code')])
                           for ds in self.data])
        if print_stats:
            print(u"{} methods\n{} cfs\n{} unlinked cfs".format(
                  num_methods, num_cfs, num_unlinked))
        return num_methods, num_cfs, num_unlinked
