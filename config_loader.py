# ====== Code Summary ======
# This module defines the `CONFIG` class used for application-wide configuration management.
# It loads settings from JSON files for various components such as LLM, embeddings, logging,
# database (SQL and FAISS), and proxy settings. It also configures the LoggerManager using
# values retrieved from the loaded configuration files.

# ====== Standard Library Imports ======
import os
import sys
import json
import pathlib

# ====== Internal Project Imports ======
from loggerplusplus import LoggerManager, LogLevels, LoggerConfig, Logger, logger_colors, time_tracker


def load_json_file(file_path):
    """
    Loads a JSON file and returns its contents.

    Args:
        file_path (str | Path): Path to the JSON file.

    Returns:
        dict: Parsed JSON content.
    """
    try:
        with open(file_path) as config:
            return json.load(config)
    except Exception:
        raise


class CONFIG:
    """
    Global configuration class that loads and provides access to settings used across the application.
    """

    ROOT_DIR = pathlib.Path(__file__).resolve().parent

    POPULATE_DOCUMENTS_FOLDER = os.path.join(ROOT_DIR, 'data', 'Evaluations de projet')
    CONFIG_DIR = os.path.join(ROOT_DIR, "config")
    TOOLS_DIR = os.path.join(ROOT_DIR, "tools")

    sys.path.append(TOOLS_DIR)  # Add tools directory to the path for imports

    CONFIG_STORE = load_json_file(os.path.join(CONFIG_DIR, "config.json"))
    SECRETS_STORE = load_json_file(os.path.join(CONFIG_DIR, "secrets.json"))

    # Proxy configuration
    if SECRETS_STORE.get("proxy"):
        os.environ["HTTP_PROXY"] = SECRETS_STORE["proxy"].get("http", "")
        os.environ["HTTPS_PROXY"] = SECRETS_STORE["proxy"].get("https", "")

    # GLiNER configuration
    GLINER_CONFIG = CONFIG_STORE["gliner"]
    GLINER_MODEL_NAME = GLINER_CONFIG["model_name"]
    GLINER_CONTEXT_WINDOW = GLINER_CONFIG["context_window"]
    GLINER_THRESHOLD = GLINER_CONFIG["threshold"]

    # Logging configuration
    LOG_CONFIG = CONFIG_STORE["log"]
    LOGGER_MANAGER_CONFIG = LOG_CONFIG["logger_manager"]

    LOGGER_MANAGER_ENABLE_FILES_LOGS_MONITORING_ONLY_FOR_ONE_LOGGER = LOGGER_MANAGER_CONFIG[
        "enable_files_logs_monitoring_only_for_one_logger"
    ]
    LOGGER_MANAGER_ENABLE_DYNAMIC_CONFIG_UPDATE = LOGGER_MANAGER_CONFIG["enable_dynamic_config_update"]
    LOGGER_MANAGER_ENABLE_UNIQUE_LOGGER_IDENTIFIER = LOGGER_MANAGER_CONFIG["enable_unique_logger_identifier"]

    LOGGER_CONFIG = LOG_CONFIG["logger"]
    LOGGER_COLORS = LOGGER_CONFIG["colors"]
    LOGGER_PATH = LOGGER_CONFIG["path"]
    LOGGER_DECORATOR_LOG_LEVEL = LOGGER_CONFIG["decorator_log_level"]
    LOGGER_PRINT_LOG_LEVEL = LOGGER_CONFIG["print_log_level"]
    LOGGER_FILE_LOG_LEVEL = LOGGER_CONFIG["file_log_level"]
    LOGGER_PRINT_LOG = LOGGER_CONFIG["print_log"]
    LOGGER_WRITE_TO_FILE = LOGGER_CONFIG["write_to_file"]
    LOGGER_DISPLAY_MONITORING = LOGGER_CONFIG["display_monitoring"]
    LOGGER_FILES_MONITORING = LOGGER_CONFIG["files_monitoring"]
    LOGGER_FILE_SIZE_UNIT = LOGGER_CONFIG["file_size_unit"]
    LOGGER_DISK_ALERT_THRESHOLD_PERCENT = LOGGER_CONFIG["disk_alert_threshold_percent"]
    LOGGER_FILES_SIZE_ALERT_THRESHOLD_PERCENT = LOGGER_CONFIG["log_files_size_alert_threshold_percent"]
    LOGGER_MAX_LOG_FILE_SIZE = LOGGER_CONFIG["max_log_file_size"]
    LOGGER_IDENTIFIER_MAX_WIDTH = LOGGER_CONFIG["identifier_max_width"]
    LOGGER_FILENAME_LINENO_MAX_WIDTH = LOGGER_CONFIG["filename_lineno_max_width"]


# ====== LoggerManager Configuration ======
LoggerManager.enable_files_logs_monitoring_only_for_one_logger = (
    CONFIG.LOGGER_MANAGER_ENABLE_FILES_LOGS_MONITORING_ONLY_FOR_ONE_LOGGER
)
LoggerManager.enable_dynamic_config_update = CONFIG.LOGGER_MANAGER_ENABLE_DYNAMIC_CONFIG_UPDATE
LoggerManager.enable_unique_logger_identifier = CONFIG.LOGGER_MANAGER_ENABLE_UNIQUE_LOGGER_IDENTIFIER

LoggerManager.global_config = LoggerConfig.from_kwargs(
    colors=getattr(logger_colors, CONFIG.LOGGER_COLORS),
    path=CONFIG.LOGGER_PATH,
    # Log levels
    decorator_log_level=getattr(LogLevels, CONFIG.LOGGER_DECORATOR_LOG_LEVEL),
    print_log_level=getattr(LogLevels, CONFIG.LOGGER_PRINT_LOG_LEVEL),
    file_log_level=getattr(LogLevels, CONFIG.LOGGER_FILE_LOG_LEVEL),
    # Output options
    print_log=CONFIG.LOGGER_PRINT_LOG,
    write_to_file=CONFIG.LOGGER_WRITE_TO_FILE,
    # Monitoring
    display_monitoring=CONFIG.LOGGER_DISPLAY_MONITORING,
    files_monitoring=CONFIG.LOGGER_FILES_MONITORING,
    file_size_unit=CONFIG.LOGGER_FILE_SIZE_UNIT,
    disk_alert_threshold_percent=CONFIG.LOGGER_DISK_ALERT_THRESHOLD_PERCENT,
    log_files_size_alert_threshold_percent=CONFIG.LOGGER_FILES_SIZE_ALERT_THRESHOLD_PERCENT,
    max_log_file_size=CONFIG.LOGGER_MAX_LOG_FILE_SIZE,
    # Layout
    identifier_max_width=CONFIG.LOGGER_IDENTIFIER_MAX_WIDTH,
    filename_lineno_max_width=CONFIG.LOGGER_FILENAME_LINENO_MAX_WIDTH,
)
