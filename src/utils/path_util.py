import os


class PathUtil:

    @classmethod
    def initialize(cls, base_dir: str) -> None:
        """Initialize the paths with the specified base directory.

        Args:
            base_dir (str): The base directory of the application.
        """
        # Base Dir
        cls.base_dir = base_dir

        # Config Dir
        cls.config_dir = os.path.join(cls.base_dir, "config")

        cls.agents_dir = os.path.join(cls.config_dir, "agents")
        cls.tasks_dir = os.path.join(cls.config_dir, "tasks")

    @staticmethod
    def get_agent_config_path(agent_config: str) -> str:
        """Get the full path for the specified agent Yaml file.

        Args:
            agent_config (str): Yaml file name.

        Returns:
            str: the full path to agent config Yaml file.
        """
        return os.path.join(PathUtil.agents_dir, agent_config)
    
    @staticmethod
    def get_tasks_config_path(task_config: str) -> str:
        """Get the full path for the specified tasks Yaml file.

        Args:
            task_config (str): Yaml file name.

        Returns:
            str: the full path to tasks config Yaml file.
        """
        return os.path.join(PathUtil.tasks_dir, task_config)

    @staticmethod
    def get_config_file_path(config_file: str) -> str:
        """Get the full path for the specified config Yaml file.

        Args:
            config_file (str): Yaml file name.

        Returns:
            str: the full path to config Yaml file.
        """
        return os.path.join(PathUtil.config_dir, config_file)