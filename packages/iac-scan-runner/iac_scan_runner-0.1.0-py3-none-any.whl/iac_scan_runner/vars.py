import os

ROOT_DIR = os.getenv("ROOT_DIR", os.getcwd())
TOOLS_DIR = os.getenv("TOOLS_DIR", f'{ROOT_DIR}/tools')
CONFIG_DIR = os.getenv("CONFIG_DIR", f'{ROOT_DIR}/config')
NODE_MODULES_DIR = os.getenv("NODE_MODULES_DIR", f'{ROOT_DIR}/node_modules')
TMP_DIR = os.getenv("TMP_DIR", f'{TOOLS_DIR}/tmp')
GIT_SECRETS_DIR = os.getenv("GIT_SECRETS_DIR", f'{TOOLS_DIR}/git-secrets')
CHECK_STYLE_PATH = os.getenv("CHECK_STYLE_PATH", f'{TOOLS_DIR}/checkstyle.jar')
CHECK_SHELL_PATH = os.getenv("CHECK_SHELL_PATH", f'{TOOLS_DIR}/shellcheck')
HADOLINT_PATH = os.getenv("HADOLINT_PATH", f'{TOOLS_DIR}/hadolint')
MDL_PATH = os.getenv("HADOLINT_PATH", f'{TOOLS_DIR}/mdl')
GIT_LEAKS_PATH = os.getenv("GIT_LEAKS_PATH", f'{TOOLS_DIR}/gitleaks')
TF_SEC_PATH = os.getenv("TF_SEC_PATH", f'{TOOLS_DIR}/tfsec')
TERRASCAN_PATH = os.getenv("TERRASCAN_PATH", f'{TOOLS_DIR}/terrascan')
SONAR_SCANNER_PATH = os.getenv("SONAR_SCANNER_PATH", f'{TOOLS_DIR}/sonar-scanner/bin/sonar-scanner')
