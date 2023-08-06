import os, re

ANALYSIS_ID_KEY = "analysis_id"
WHATSOPT_URL_KEY = "whatsopt_url"
OPENMDAO = "openmdao"
GEMSEO = "gemseo"


def snakize(name):
    snaked = re.sub(
        r"(^|([a-z])\W?)([A-Z])",
        lambda m: m.group(2) + "_" + m.group(3).lower()
        if m.group(1)
        else m.group(3).lower(),
        name,
    )
    snaked = re.sub("[-\.\s]", "_", snaked)
    snaked = re.sub("__+", "_", snaked).lower()
    return snaked


def is_user_file(f):
    return (
        not re.match(r".*_base\.py$", f)
        and not re.match(r"^mda_init.*\.py$", f)
        and not re.match(r"^run_.*\.py$", f)
        and not re.match(r"^.*server/", f)
        and not re.match(r"^.*egmdo/", f)
    )


def is_analysis_user_file(name, f):
    return bool(re.match(rf"^{name}\.py$", f))


def find_analysis_base_files(directory="."):
    files = []
    for f in os.listdir(directory):
        if f.endswith("_base.py"):
            files.append(f)
    return files


def _extract_key(file, key):
    ident = None
    with open(file, "r") as f:
        for line in f:
            match = re.match(rf"^# {key}: (.*)", line)
            if match:
                ident = match.group(1)
                break
    return ident


def extract_mda_id(file):
    return _extract_key(file, ANALYSIS_ID_KEY)


def extract_origin_url(file):
    return _extract_key(file, WHATSOPT_URL_KEY)


def _get_key(key, directory="."):
    files = find_analysis_base_files(directory)
    val = None
    for f in files:
        newval = _extract_key(os.path.join(directory, f), key)
        if val and val != newval:
            raise ValueError(
                "Several {} key detected. "
                "Find #{} then #{}.\n"
                "Check header comments in {} files.".format(
                    key, val, newval, str(files)
                )
            )
        val = newval
    return val


def get_analysis_id(directory="."):
    return _get_key(ANALYSIS_ID_KEY, directory)


def get_whatsopt_url(directory="."):
    try:
        return _get_key(WHATSOPT_URL_KEY, directory)
    except ValueError:
        return False


def is_based_on(module, directory="."):
    files = find_analysis_base_files(directory)
    return len(files) > 0 and all(
        _detect_from_import(os.path.join(directory, f), module) for f in files
    )


def is_framework_switch(framework, directory="."):
    return (framework == GEMSEO and is_based_on(OPENMDAO, directory)) or (
        framework == OPENMDAO and is_based_on(GEMSEO, directory)
    )


def _detect_from_import(file, module):
    detected = False
    with open(file, "r") as f:
        for line in f:
            # TODO: Maybe would need more robust detection... We'll see!
            # first from/import detected gives the framework.
            match = re.match(rf"^(from|import) {module}\..*", line)
            if match:
                detected = True
                break
    return detected
