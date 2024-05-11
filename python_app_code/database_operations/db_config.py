from configparser import ConfigParser

# This script contains the configuration parameters for the database connection

def load_config(filename='database_operations/database.ini', section='postgresql'):
    """
    Load the configuration parameters from the specified INI file.

    Args:
        filename (str): The path to the INI file. Default is 'database_operations/database.ini'.
        section (str): The section name in the INI file to retrieve the parameters from. Default is 'postgresql'.

    Returns:
        dict: A dictionary containing the configuration parameters.

    Raises:
        Exception: If the specified section is not found in the INI file.
    """
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config