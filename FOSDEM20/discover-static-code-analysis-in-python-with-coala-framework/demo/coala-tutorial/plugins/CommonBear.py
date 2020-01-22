from coalib.bears.LocalBear import Bear
from coalib.results.HiddenResult import HiddenResult

class CommonBear(Bear):

    missing_dependencies = []

    def run(self,
            filename,
            file):
        """
        Common Bear
        """

        yield HiddenResult(self, { 'name': 'CommonBear', 'loaded': True} )
    