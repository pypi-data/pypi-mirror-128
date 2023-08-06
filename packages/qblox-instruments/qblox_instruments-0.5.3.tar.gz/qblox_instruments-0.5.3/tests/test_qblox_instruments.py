#------------------------------------------------------------------------------
# Description    : Qblox Instruments test script
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
#------------------------------------------------------------------------------


#-- include -------------------------------------------------------------------

from qblox_instruments import build
from jsonschema        import validate

#-- functions -----------------------------------------------------------------

#------------------------------------------------------------------------------
def test_get_build_info():
    """
    Tests get build info function and checks if the returned dictionary has the
    correct format. If not, the test fails.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    """

    #Build info
    build_info = build.get_build_info()

    #Check build info
    build_info_schema = {"title": "Build information container.",
                        "description": "Contains build information.",
                        "required":    ["version", "date", "hash", "dirty"],
                        "properties": {
                            "version": {
                                "description": "Version string",
                                "type":        "string"
                            },
                            "date": {
                                "description": "Build date",
                                "type":        "string"
                            },
                            "hash": {
                                "description": "Git hash",
                                "type":        "string"
                            },
                            "dirty": {
                                "description": "Git dirty indication",
                                "type":        "boolean"
                            },
                        }}

    validate(build_info, build_info_schema)

#------------------------------------------------------------------------------
def test_version():
    """
    Test if __version__ matches version in the build information else fail.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    """

    #Test version
    assert build.__version__ == build.get_build_info()["version"]
