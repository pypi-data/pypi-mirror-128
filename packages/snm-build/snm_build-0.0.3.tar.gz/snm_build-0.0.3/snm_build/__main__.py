import platform
import sys
import logging
import json
import os
import xml.etree.ElementTree

import PyInstaller.__main__


class SnmBuildException(Exception):
    pass


def run_pyinstaller(json_data, build_dir, name):
    parameters = []
    for key, value in json_data.get("installer", {}).items():
        if key == "onefile" and value:
            parameters.append("--onefile")
        elif key == "windowed" and value:
            parameters.append("--windowed")
        elif key == "icon":
            parameters.append("--icon")
            parameters.append(os.path.abspath(value))
        elif key == "libs":
            parameters.append("--paths")
            for path in value:
                parameters.append(os.path.abspath(path))

    parameters.append("--name")
    parameters.append(name)
    parameters.append("--distpath")
    parameters.append(os.path.join(build_dir, "dist"))
    parameters.append("--workpath")
    parameters.append(os.path.join(build_dir, "build"))
    parameters.append("--specpath")
    parameters.append(build_dir)

    parameters.append(json_data.get("main"))

    PyInstaller.__main__.run(parameters)


def generate_rc(json_qt, rc_suffix, rc_dir):
    import PyQt5.pyrcc_main
    for rcc in json_qt.get("resources", []):
        rc_path, rc_filename = os.path.split(rcc)
        rc_filename_base = os.path.splitext(rc_filename)[0]
        if not PyQt5.pyrcc_main.processResourceFile([os.path.abspath(rcc)],
                                                    os.path.join(rc_dir, "{}{}.py".format(rc_filename_base,
                                                                                          rc_suffix)), []):
            raise SnmBuildException("Generate resources failed")


def generate_ui(json_qt, ui_dir, rc_suffix, rc_dir):
    import PyQt5.uic
    ui_compiler = PyQt5.uic.compiler.UICompiler()
    for form in json_qt.get("forms", []):
        try:
            ui_path, ui_filename = os.path.split(form)
            ui_filename_base = os.path.splitext(ui_filename)[0]
            ui_output_file = open(os.path.join(ui_dir, "{}_ui.py".format(ui_filename_base)), 'w')
            ui_compiler.compileUi(os.path.abspath(form),
                                  ui_output_file,
                                  True, rc_suffix, os.path.relpath(rc_dir))
            ui_output_file.close()

        except SyntaxError:
            raise SnmBuildException("\"{}\" form parse failed".format(form))


def generate_qt(json_data):
    json_qt = json_data.get("qt")
    if json_qt is not None:
        if 'PyQt5' not in sys.modules:
            raise SnmBuildException("\"PyQt5\" module not installed.")

        ui_dir = os.path.abspath(json_qt.get("ui_dir", '.'))
        if not os.path.exists(ui_dir):
            os.makedirs(ui_dir)

        rc_dir = os.path.abspath(json_qt.get("rc_dir", '.'))
        if not os.path.exists(rc_dir):
            os.makedirs(rc_dir)

        rc_suffix = "_rc"  # TODO move to bai

        generate_rc(json_qt, rc_suffix, rc_dir)
        generate_ui(json_qt, ui_dir, rc_suffix, rc_dir)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    try:

        bai_file_name = sys.argv[-1]
        logging.info("Reading {}...".format(bai_file_name))
        file = open(bai_file_name, 'r')
        json_data = json.load(file)
        # TODO validation json schema
        logging.debug("Json data: {}".format(json_data))

        name = json_data["name"]
        build_dir = os.path.abspath(json_data.get("build_dir", "."))
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        if "--noqt" not in sys.argv:
            generate_qt(json_data)

        if "--nobuild" not in sys.argv:
            run_pyinstaller(json_data, build_dir, name)

    except IndexError as e:
        logging.fatal("Missing argument. Usage: install_snm <arguments...> .bai")
        sys.exit(1)
    except FileNotFoundError as e:
        logging.fatal("{}: {}".format(e.strerror, e.filename))
        sys.exit(2)
    except SnmBuildException as e:
        logging.fatal(str(e))
        sys.exit(3)


