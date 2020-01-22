from coalib.bears.LocalBear import LocalBear
import CommonBear


class TodoBear(LocalBear):

    BEAR_DEPS = { CommonBear }

    def run(self,
            filename,
            file,
            dependency_results,
            user_input: str,
            id: int,
            user: str):
        """
        Communicates with the user.

        :param user_input: Arbitrary user input.
        """

        shared = dependency_results[CommonBear.name]

        yield "{}".format(shared)
        