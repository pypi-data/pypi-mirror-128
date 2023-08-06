from pathlib import Path
import logging
from shutil import copyfile

logger = logging.getLogger(__name__)


class ConfigInitializer():
    """Initialize the configuration file, if not present"""

    def __init__(self) -> None:
        pass

    @classmethod
    def initalize_config(cls, filepath: Path) -> None:
        """Checks for the presence of a configuration file for the current 
        user. If not present, creates the folders and a default configuration 
        file

        :param filepath: Path to the configuration file
        :type filepath: Path
        """

        cls.__create_directories()
        cls.__create_config_file(
            source_path=Path("default_config.ini"),
            destination_path=filepath)

    @classmethod
    def __create_directories(cls) -> None:
        try:
            directories = (Path.home() / ".barbucket/tv_screener")
            Path.mkdir(directories, parents=True)
        except FileExistsError:
            logger.debug(f"Necessary directories already exist.")
        else:
            logger.info(f"Created directories '{directories}'")

    @classmethod
    def __create_config_file(
            cls,
            source_path: Path,
            destination_path: Path) -> None:
        if Path.is_file(destination_path):
            logger.debug(f"Config file already exists.")
        else:
            copyfile(source_path, destination_path)
            logger.info(
                f"Created config file {destination_path} from default file.")
