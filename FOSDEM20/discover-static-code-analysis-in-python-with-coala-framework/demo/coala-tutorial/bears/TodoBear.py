from coalib.bears.LocalBear import LocalBear

class TodoBear(LocalBear):


    def run(self,
            filename,
            file,
            user_input: str,
            id: int,
            user: str):
        """
        Communicates with the user.

        :param user_input: Arbitrary user input.
        """

        yield """
        
        FileName[{}]
        File[{}]
        UserInput[{}]
        id[{}]
        user[{}]
        """.format(filename, file, user_input, id, user)