import os

class DBManager:
    _TOP_LEVEL_DATABSE_DIRECTORY = "financials"
    _DATABASE_SUB_DIRECTORIES = ['balance_sheet', 'income_statement', 'cashflow_statement']

    def __init__(self, parent_path: str = "financials") -> None:
        """ ****************************************************
        * __init__()
        *
        * Description:
        *   Creates the top-level parent directory name, if provided.
        *
        * parent_path -> str (financials) : Parent database path
        **************************************************** """

        self._TOP_LEVEL_DATABSE_DIRECTORY = parent_path

    def setup(self) -> bool:
        """ ****************************************************
        * setup()
        *
        * Description:
        *   Sets up the database structure for the financial statements,
        *   only if it does not exist.
        *
        * returns (bool) : status of the setup procedure
        **************************************************** """

        status = True

        try:
            # Attempt to verify that the database sub-directories exist
            dirList = os.listdir(self._TOP_LEVEL_DATABSE_DIRECTORY)

            if dirList != self._DATABASE_SUB_DIRECTORIES:
                status = False

        except Exception as e:
            try:
                # Attempt to create the financials database
                os.mkdir(self._TOP_LEVEL_DATABSE_DIRECTORY)
                os.chmod(self._TOP_LEVEL_DATABSE_DIRECTORY, 0o777)

                for dbDir in self._DATABASE_SUB_DIRECTORIES:
                    path = os.path.join(self._TOP_LEVEL_DATABSE_DIRECTORY, dbDir)
                    os.mkdir(path)

            except Exception as e:
                status = False
                print(f'{self.setup.__name__}(): Fatal error. Could not set-up database structure.')

        return status

    def teardown(self, deleteDirs: bool = False, deleteFiles: bool = False) -> bool:
        """ ****************************************************
        * teardown()
        *
        * Description:
        *   Tears down the database structure
        *
        * deleteDirs -> bool  : Delete directory flag
        * deteleFiles -> bool : Delete files flag
        * returns (bool) : status of the teardown procedure
        **************************************************** """

        status = True

        if deleteDirs:
            try:
                # Remove the file structure at the root path
                os.remove(self._TOP_LEVEL_DATABSE_DIRECTORY)

            except Exception as e:
                status = False
                print(f'{self.teardown.__name__}(): Fatal error. Could not remove database directories.\n{e}')

        elif deleteFiles:
            try:
                for l_dir in self._DATABASE_SUB_DIRECTORIES:
                    path = os.path.join(self._TOP_LEVEL_DATABSE_DIRECTORY, l_dir) # Obatin the directory path

                    # List and remove the files
                    files = os.listdir(path)
                    for f in files:
                        f_path = os.path.join(path, f)

                        # Check is file and remove
                        if os.path.isfile(f_path):
                            os.remove(f_path)

            except Exception as e:
                status = False
                print(f'{self.teardown.__name__}(): Fatal error. Could not remove database files.\n{e}')

        return status