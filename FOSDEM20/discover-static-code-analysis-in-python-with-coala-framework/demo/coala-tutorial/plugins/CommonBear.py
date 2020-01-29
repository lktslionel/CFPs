import os.path

from coalib.bears.GlobalBear import GlobalBear
from coalib.results.Result import Result
from bears.general.CPDBear import CPDBear


class CommonBear(GlobalBear):
    # LANGUAGES = {'Python', 'Python 3'}
    # AUTHORS = {'The coala developers'}
    # AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    # LICENSE = 'AGPL-3.0'

    BEAR_DEPS = {CPDBear}

    def run(self,
            name: str, 
            dependency_results=None,
            **kwargs):
        
        print("args", name)
        print("dependency_results", dependency_results)
        print("kwargs", kwargs)

        yield Result(self, 'Your package does'
                         ' not contain a setup file.')