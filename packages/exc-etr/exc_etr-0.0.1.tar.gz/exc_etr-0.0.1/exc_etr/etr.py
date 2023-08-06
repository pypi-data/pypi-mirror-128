#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    Exc_ETR Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Exc_ETR.
#    Exc_ETR is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Exc_ETR is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Exc_ETR.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
r"""
   Exc_ETR project : exc_etr/etr.py

   ETR class

   (pimydoc)ETR format
   ⋅-  [A] utf8 encoded
   ⋅
   ⋅-  [B] empty lines        : lines only made of spaces are discarded
   ⋅
   ⋅-  [C] comment lines      : lines starting with '#' are discarded
   ⋅                            Beware, don't add a comment at the end of a line !
   ⋅                            Don't:
   ⋅                              :abbreviation: ᵛⁱ : [vi]  # a comment
   ⋅                            Do:
   ⋅                              # a comment
   ⋅                              :abbreviation: ᵛⁱ : [vi]
   ⋅
   ⋅                            → see ETR.options["comment_char"]
   ⋅
   ⋅-  [D] ⬂ syntax          : lines ending with ⬂ are joined to the next line
   ⋅                             with \n between the two lines.
   ⋅
   ⋅                            → see ETR.options["tobecontinued_char"]
   ⋅
   ⋅                            If ⬂ appears elsewhere in a line, a warning
   ⋅                            will be raised.
   ⋅
   ⋅-  [E] left-spaces syntax : if True, lines beginning with spaces are joined
   ⋅                            to the precedent line with \n between the two lines.
   ⋅
   ⋅                            → see ETR.options["allow_leftspaces_syntax(json)"]
   ⋅
   ⋅-  [F] nested file        : +++ (=file to be included line prefix)
   ⋅                            the string after +++ will be stripped.
   ⋅
   ⋅                            it's a relative path based on the parent file,
   ⋅                            absolute path IS NOT allowed.
   ⋅                            e.g. if the file "directory/myfile.txt" contains the line
   ⋅                                +++ subdirectory/mynestedfile.txt
   ⋅                            the nested file will be directory/subdirectory/mynestedfile.txt
   ⋅
   ⋅                            Beware, don't add a comment at the end of a line !
   ⋅
   ⋅                            → see ETR.options["filetobeincluded_lineprefix"]
   ⋅
   ⋅- [G] abbreviations       :
   ⋅
   ⋅    An abbreviation is a tag already defined (see [I] section).
   ⋅
   ⋅    :abbreviation: ᴺ  : [N]    # every "ᴺ" string will by replaced by "[N]"
   ⋅    :abbreviation: ᵛⁱ : [vi]   # every "ᵛⁱ" string will by replaced by "[vi]"
   ⋅
   ⋅                            Beware, don't add a comment at the end of a line !
   ⋅                            Don't:
   ⋅                              :abbreviation: ᵛⁱ : [vi]  # a comment
   ⋅                            Do:
   ⋅                              # a comment
   ⋅                              :abbreviation: ᵛⁱ : [vi]
   ⋅
   ⋅                            → see ETR.options["abbreviations_definitions regex"]
   ⋅
   ⋅- [H] flags:
   ⋅
   ⋅    A flag is a tag already defined (see [I] section).
   ⋅
   ⋅    :flag:          🏴‍☠️ : pirate  # the meaning of 🏴‍☠️ is 'pirate'
   ⋅
   ⋅                           Beware, don't add a comment at the end of a line !
   ⋅                            Don't:
   ⋅                              :flag: đđ special_d  # a comment
   ⋅                            Do:
   ⋅                              # a comment
   ⋅                              :flag: đđ special_d
   ⋅
   ⋅                            → see ETR.options["flag_definitions regex"]
   ⋅
   ⋅- [I] tags
   ⋅
   ⋅    Beside "abbreviation" and "flags", other tags may be added:
   ⋅
   ⋅      %%authorised tags(json)"%%["abbreviation", "flag", "new_tag"]
   ⋅      :new_tag: key
   ⋅      :new_tag: key : content
   ⋅
   ⋅    Please note that the "content" part is optional.
   ⋅
   ⋅    You may reduce authorized tags to zero tag:
   ⋅      %%authorised tags(json)"%%[]
   ⋅    Be careful since the syntax is tricky. See [K] section of this document.
   ⋅
   ⋅- [J] variables
   ⋅
   ⋅    Variables may contain a (str)value:
   ⋅
   ⋅        /context/ 123
   ⋅
   ⋅    .read_variables["context"] will contain ((str)"123", fals)
   ⋅
   ⋅    Variable names DO NOT contain spaces; variable value may
   ⋅    contain any character:
   ⋅
   ⋅       /my_variable/ value with spaces and /special/ characters
   ⋅
   ⋅    fals contains the informations about the last initialization of
   ⋅    the variable.
   ⋅
   ⋅- [K] options tools redefinition:
   ⋅    Simple tags expecting a string:
   ⋅    - %%comment_lineprefix%%#
   ⋅    - %%tobecontinued_char%%⬂
   ⋅    - %%filetobeincluded_lineprefix%%
   ⋅
   ⋅    Tag expecting a json-boolean that will be json.loads():
   ⋅    - %%allow_leftspaces_syntax(json)%%True
   ⋅      or
   ⋅      %%allow_leftspaces_syntax(json)%%False
   ⋅
   ⋅    Tag expecting a json-list of strings that will be json.loads():
   ⋅    - %%authorised tags(json)"%%["abbreviation"]
   ⋅      or
   ⋅      %%authorised tags(json)"%%["abbreviation", "flag"]
   ⋅
   ⋅        !!! Beware: DO NOT WRITE
   ⋅        !!!   %%authorised tags(json)"%%["abbreviation", "flag",]
   ⋅        !!! with a last comma ! json.loads() can't interpret such a string
   ⋅        !!! Write instead:
   ⋅        !!!   %%authorised tags(json)"%%["abbreviation", "flag"]
   ⋅
   ⋅    Tag expecting a json-string that will be re.compile'd():
   ⋅    - %%tag_kv(regex)%%^\:(?P<name>[^:]+)\:
   ⋅      \s*(?P<key>[^\s]*)\s*\(:\s*(?P<value>[^\s]*))?$
   ⋅
   ⋅      This regex needs 3 groups : 'name', 'key', 'value'. (see ETR-ERRORID012)
   ⋅
   ⋅                            → see ETR.options["options_definition(regex)"]
   ⋅
   ⋅- [L] options regex redefinition:
   ⋅
   ⋅      %%options_definition(regex)%%°°(?P<name>[^:]+)°°(?P<value>.+)
   ⋅
   ⋅      This regex needs 2 groups : 'name', 'value'. (see ETR-ERRORID011)
   ⋅
   ⋅      so that you may write:
   ⋅      °°comment_lineprefix°°|||
   ⋅      |||this a comment
   ____________________________________________________________________________

   CLASS:
   o  ETR     class
"""
import copy
import json
import os.path
import re
import traceback

from exc_errors.errors import TextFileError, TextFileWarn
from exc_fal.fal import FileAndLine
from exc_motherclass.motherclass import MotherClassErr
from exc_etr.utils import path_of
from exc_etr.etr_line import ETRLine, TLFF
from exc_etr.etr_line import ETRLINE_INTTYPE__NORMAL, ETRLINE_INTTYPE__COMMENTEMPTY
# I don't understand why pylint doesn't find ETRLINE_INTTYPE__OPTIONSDEFINITION in etr_line:
#   pylint: disable=no-name-in-module
from exc_etr.etr_line import ETRLINE_INTTYPE__OPTIONSDEFINITION
from exc_etr.etr_line import ETRLINE_INTTYPE__VARIABLE, ETRLINE_INTTYPE__TAG
from exc_etr.etr_line import ETRLINE_INTTYPE__NONE


# (pimydoc)ETR.options
# ⋅ETR.options is a dict(str:None|bool|func) describing what to do when
# ⋅reading/writing.
# ⋅
# ⋅
# ⋅o  "allow_leftspaces_syntax(json)" [JSON ! see below]
# ⋅   a boolean allowing (or not) the left-spaces syntax
# ⋅
# ⋅o  "authorised tags(json)" [JSON ! see below]
# ⋅   (list of str) list of authorised tags
# ⋅
# ⋅o  "comment_lineprefix"
# ⋅   (str)line prefix defining a comment line
# ⋅
# ⋅o  "filetobeincluded_lineprefix"
# ⋅   (str)line prefix defining an import
# ⋅
# ⋅o  "options_definition(regex)" [JSON ! see below]
# ⋅   Regex defining how modify the items of .options.
# ⋅   This regex must have the following groups:
# ⋅        'name', 'value'
# ⋅
# ⋅o  "read line:normal:yield": (bool)
# ⋅    yield an ETRLine object if a "normal line" has been read ?
# ⋅o  "read line:normal:event": None,
# ⋅    name of the method to be called if a "normal line" has been read.
# ⋅
# ⋅o  "read line:empty line/comment:yield": (bool)
# ⋅    yield an ETRLine object if an empty line or a comment has been read ?
# ⋅o  "read line:empty line/comment:event": None,
# ⋅    name of the method to be called if an empty line or a comment has been read.
# ⋅
# ⋅o  "read line:None:event": None,
# ⋅    name of the method to be called if a None line (=error) has been read.
# ⋅
# ⋅o  "read line:options_definition:yield": (bool)
# ⋅    yield an ETRLine object if a "options_definition" line has been read ?
# ⋅o  "read line:options_definition:event": None,
# ⋅    name of the method to be called if a "options_definition" line has been
# ⋅    read.
# ⋅
# ⋅o  "read line:variable:yield": (bool)
# ⋅    yield an ETRLine object if a variable line has been read ?
# ⋅o  "read line:variable:event": None
# ⋅    name of the method to be called if a variable line has been read.
# ⋅
# ⋅o  "read line:tag:yield": (bool)
# ⋅    yield an ETRLine object if a tag line has been read ?
# ⋅o  "read line:tag:event": None
# ⋅    name of the method to be called if a tag line has been read.
# ⋅
# ⋅o  "remove left spaces": True
# ⋅   if True lstrip() the read line.
# ⋅
# ⋅o  "tag(regex)" [REGEX ! see below]
# ⋅    (str/bytes) regex defining a tag key/value
# ⋅    This regex must have the following groups:
# ⋅        'name', 'key', 'value'
# ⋅
# ⋅o  "tobecontinued_char"
# ⋅   (str)character defining a to-be-continued line
# ⋅
# ⋅o  "variable(regex)" [REGEX ! see below]
# ⋅   (str/bytes) regex defining a variable setting.
# ⋅
# ⋅If a key contains the "(regex)" suffix, its value must be (str)regex
# ⋅or a (byte)re.compile() object.
# ⋅
# ⋅If a key contains the "(json)" suffix, its value is a Python object
# ⋅that can be read from a string through json.loads()
# ⋅
# ⋅Please not that there is no "read line:None:yield" entry since
# ⋅None is always yielded in this case.
DEFAULT_OPTIONS = {
    "allow_leftspaces_syntax(json)": True,

    "authorised tags(json)": ("abbreviation", "flag"),

    "comment_lineprefix": "#",

    "filetobeincluded_lineprefix": "+++",

    "options_definition(regex)": re.compile(r"%%(?P<name>[^:]+)%%(?P<value>.+)\s*$"),

    "read line:normal:yield": True,
    "read line:normal:event": None,

    "read line:empty line/comment:yield": False,
    "read line:empty line/comment:event": None,

    "read line:options_definition:yield": False,
    "read line:options_definition:event": None,

    "read line:variable:yield": False,
    "read line:variable:event": None,

    "read line:tag:yield": False,
    "read line:tag:event": None,

    "read line:None:event": None,

    "remove left spaces": True,

    "tag_kv(regex)": re.compile(r"^\:(?P<name>[^:]+)\:\s*"
                                r"(?P<key>[^\s]*)\s*"
                                r"(\:\s*(?P<value>[^\s]*))?\s*$"),

    "tobecontinued_char": "⬂",

    "variable(regex)": re.compile(r"^\/(?P<name>[^\s]+)\/\s*"
                                  r"(?P<value>.*)\s*$"),
}


class ETR(MotherClassErr):
    """
        ETR class

        Use this class to read ETR-based text files.


        _______________________________________________________________________

        ATTRIBUTES:
        o (ListOfErrorMessages) errors

        o (dict) options
            (pimydoc)ETR.options
            ⋅ETR.options is a dict(str:None|bool|func) describing what to do when
            ⋅reading/writing.
            ⋅
            ⋅
            ⋅o  "allow_leftspaces_syntax(json)" [JSON ! see below]
            ⋅   a boolean allowing (or not) the left-spaces syntax
            ⋅
            ⋅o  "authorised tags(json)" [JSON ! see below]
            ⋅   (list of str) list of authorised tags
            ⋅
            ⋅o  "comment_lineprefix"
            ⋅   (str)line prefix defining a comment line
            ⋅
            ⋅o  "filetobeincluded_lineprefix"
            ⋅   (str)line prefix defining an import
            ⋅
            ⋅o  "options_definition(regex)" [JSON ! see below]
            ⋅   Regex defining how modify the items of .options.
            ⋅   This regex must have the following groups:
            ⋅        'name', 'value'
            ⋅
            ⋅o  "read line:normal:yield": (bool)
            ⋅    yield an ETRLine object if a "normal line" has been read ?
            ⋅o  "read line:normal:event": None,
            ⋅    name of the method to be called if a "normal line" has been read.
            ⋅
            ⋅o  "read line:empty line/comment:yield": (bool)
            ⋅    yield an ETRLine object if an empty line or a comment has been read ?
            ⋅o  "read line:empty line/comment:event": None,
            ⋅    name of the method to be called if an empty line or a comment has been read.
            ⋅
            ⋅o  "read line:None:event": None,
            ⋅    name of the method to be called if a None line (=error) has been read.
            ⋅
            ⋅o  "read line:options_definition:yield": (bool)
            ⋅    yield an ETRLine object if a "options_definition" line has been read ?
            ⋅o  "read line:options_definition:event": None,
            ⋅    name of the method to be called if a "options_definition" line has been
            ⋅    read.
            ⋅
            ⋅o  "read line:variable:yield": (bool)
            ⋅    yield an ETRLine object if a variable line has been read ?
            ⋅o  "read line:variable:event": None
            ⋅    name of the method to be called if a variable line has been read.
            ⋅
            ⋅o  "read line:tag:yield": (bool)
            ⋅    yield an ETRLine object if a tag line has been read ?
            ⋅o  "read line:tag:event": None
            ⋅    name of the method to be called if a tag line has been read.
            ⋅
            ⋅o  "remove left spaces": True
            ⋅   if True lstrip() the read line.
            ⋅
            ⋅o  "tag(regex)" [REGEX ! see below]
            ⋅    (str/bytes) regex defining a tag key/value
            ⋅    This regex must have the following groups:
            ⋅        'name', 'key', 'value'
            ⋅
            ⋅o  "tobecontinued_char"
            ⋅   (str)character defining a to-be-continued line
            ⋅
            ⋅o  "variable(regex)" [REGEX ! see below]
            ⋅   (str/bytes) regex defining a variable setting.
            ⋅
            ⋅If a key contains the "(regex)" suffix, its value must be (str)regex
            ⋅or a (byte)re.compile() object.
            ⋅
            ⋅If a key contains the "(json)" suffix, its value is a Python object
            ⋅that can be read from a string through json.loads()
            ⋅
            ⋅Please not that there is no "read line:None:yield" entry since
            ⋅None is always yielded in this case.

        o (dict) read_tags
            (pimydoc)ETR.read_tags
            ⋅Definition of all tags read in the read file(s).
            ⋅
            ⋅.read_tags[(str)name] = ((str)key, (str)value)
            ⋅  e.g. self.read_tags["abbreviation"] = ("e.g.", "exempli gratia")
            ⋅
            ⋅NOTE: will be flushed at each call of .read() before reading the main file.

        o (list of str)_nested_files
            (pimydoc)ETR._nested_files
            ⋅Path of all nested files; required to avoid cyclic imports.
            ⋅NOTE: will be flushed at each call of .read() before reading the main file.

        METHODS:
        o  __init__(self, options=None)
        o  _expand_abbrev(self, src: str) -> str
        o  _parse_read_line(self, line: str)
        o  _init_optionsdef(self, ptooldef, fals)
        o  _init_optionsdef__regex_checks(self, name, fals)
        o  _parse_read_line(self, line: str)
        o  _parse_read_line__tag(self, line: str, fals)
        o  _parse_read_line__variable(self, line: str, fals)
        o  _read(self, source_filename: str)
        o  _read2(self, source_filename, line_to_be_continued, next_line)
        o  _read_action(self, line_inttype=ETRLINE_INTTYPE__NORMAL, fals=None, flags=None,
                        line=None)
        o  _read_action2(self, line_inttype=ETRLINE_INTTYPE__NORMAL, fals=None, flags=None,
                         line=None)

        o  improved_str(self)
        o  postread_checks(self)
        o  read(self, source_filename: str)
    """
    def __eq__(self,
               other):
        """
            ETR.__eq__()


            ___________________________________________________________________

            ARGUMENT: <ETR>other, the object to be compared to <self>.
        """
        return self.errors == other.errors and \
            self.options == other.options and \
            self.read_tags == other.read_tags and \
            self._nested_files == other._nested_files

    def __init__(self,
                 options=None):
        """
            ETR.__init__()


            ___________________________________________________________________

            ARGUMENTS:
            o (None/dict)options, a dict of regexes and list of
              chars allowing to detect markers in the source string.

              Default options are defined in the OPTIONS variable.
              See OPTIONS initialization to understant <options>
              format.

              About the <options> argument:
                - by defaut, reasonable values are loaded
                - you may want to set other options values by
                  setting <options> to a dict {...}.

            o options :
                (pimydoc)ETR.options
                ⋅ETR.options is a dict(str:None|bool|func) describing what to do when
                ⋅reading/writing.
                ⋅
                ⋅
                ⋅o  "allow_leftspaces_syntax(json)" [JSON ! see below]
                ⋅   a boolean allowing (or not) the left-spaces syntax
                ⋅
                ⋅o  "authorised tags(json)" [JSON ! see below]
                ⋅   (list of str) list of authorised tags
                ⋅
                ⋅o  "comment_lineprefix"
                ⋅   (str)line prefix defining a comment line
                ⋅
                ⋅o  "filetobeincluded_lineprefix"
                ⋅   (str)line prefix defining an import
                ⋅
                ⋅o  "options_definition(regex)" [JSON ! see below]
                ⋅   Regex defining how modify the items of .options.
                ⋅   This regex must have the following groups:
                ⋅        'name', 'value'
                ⋅
                ⋅o  "read line:normal:yield": (bool)
                ⋅    yield an ETRLine object if a "normal line" has been read ?
                ⋅o  "read line:normal:event": None,
                ⋅    name of the method to be called if a "normal line" has been read.
                ⋅
                ⋅o  "read line:empty line/comment:yield": (bool)
                ⋅    yield an ETRLine object if an empty line or a comment has been read ?
                ⋅o  "read line:empty line/comment:event": None,
                ⋅    name of the method to be called if an empty line or a comment has been read.
                ⋅
                ⋅o  "read line:None:event": None,
                ⋅    name of the method to be called if a None line (=error) has been read.
                ⋅
                ⋅o  "read line:options_definition:yield": (bool)
                ⋅    yield an ETRLine object if a "options_definition" line has been read ?
                ⋅o  "read line:options_definition:event": None,
                ⋅    name of the method to be called if a "options_definition" line has been
                ⋅    read.
                ⋅
                ⋅o  "read line:variable:yield": (bool)
                ⋅    yield an ETRLine object if a variable line has been read ?
                ⋅o  "read line:variable:event": None
                ⋅    name of the method to be called if a variable line has been read.
                ⋅
                ⋅o  "read line:tag:yield": (bool)
                ⋅    yield an ETRLine object if a tag line has been read ?
                ⋅o  "read line:tag:event": None
                ⋅    name of the method to be called if a tag line has been read.
                ⋅
                ⋅o  "remove left spaces": True
                ⋅   if True lstrip() the read line.
                ⋅
                ⋅o  "tag(regex)" [REGEX ! see below]
                ⋅    (str/bytes) regex defining a tag key/value
                ⋅    This regex must have the following groups:
                ⋅        'name', 'key', 'value'
                ⋅
                ⋅o  "tobecontinued_char"
                ⋅   (str)character defining a to-be-continued line
                ⋅
                ⋅o  "variable(regex)" [REGEX ! see below]
                ⋅   (str/bytes) regex defining a variable setting.
                ⋅
                ⋅If a key contains the "(regex)" suffix, its value must be (str)regex
                ⋅or a (byte)re.compile() object.
                ⋅
                ⋅If a key contains the "(json)" suffix, its value is a Python object
                ⋅that can be read from a string through json.loads()
                ⋅
                ⋅Please not that there is no "read line:None:yield" entry since
                ⋅None is always yielded in this case.
        """
        # NOTE: self.errors will be flushed at each call of .read() before reading the main file.
        MotherClassErr.__init__(self)

        if options:
            self.options = options
        else:
            self.options = copy.deepcopy(DEFAULT_OPTIONS)

        # (pimydoc)ETR.read_tags
        # ⋅Definition of all tags read in the read file(s).
        # ⋅
        # ⋅.read_tags[(str)name] = ((str)key, (str)value)
        # ⋅  e.g. self.read_tags["abbreviation"] = ("e.g.", "exempli gratia")
        # ⋅
        # ⋅NOTE: will be flushed at each call of .read() before reading the main file.
        self.read_tags = {}

        # (pimydoc)ETR.read_variables
        # ⋅.read_variables[variable_name] = (value, fals)
        # ⋅
        # ⋅The fals item is the last time the variables has been set.
        self.read_variables = {}

        # (pimydoc)ETR._nested_files
        # ⋅Path of all nested files; required to avoid cyclic imports.
        # ⋅NOTE: will be flushed at each call of .read() before reading the main file.
        self._nested_files = []

    def _expand_abbrev(self,
                       src: str) -> str:
        """
            ETR._expand_abbrev()

            Internal method.

            Expand in <src> all abbreviations defined in self.options["abbreviations"]


            __________________________________________________________________

            ARGUMENT:
                o src : the string to be modified

            RETURNED VALUE : the modified string
        """
        if "abbreviation" not in self.read_tags:
            return src

        for before, after in sorted(self.read_tags["abbreviation"].items(),
                                    key=lambda item: len(item[0]),
                                    reverse=True):
            src = src.replace(before, after)
        return src

    def _init_optionsdef(self,
                         optdef,
                         fals):
        """
            ETR._init_optionsdef()

            Internal method.

            Method called when by ._read2() by reading a line when ._read2 detects
            a new "options_definition".
            With _init_optionsdef we may initialize "on the fly" (=not before
            reading the file) .options[] .

            <optdef> contains the re.Match informations describing the target
            substring find at <fals>.


            ___________________________________________________________________

            ARGUMENTS:
            o  optdef         : (re.Match)
            o  (list of FAL)fals: the FALs objects associated to the <optdef>.

            no RETURNED VALUE
        """
        if optdef.group("name") not in self.options:
            # (pimydoc)error::ETR-ERRORID006
            # ⋅This error will be raised if a tag name is declared in a
            # ⋅options_definition(regex) line when it is not an authorized
            # ⋅name.
            # ⋅
            # ⋅The only authorized names are the keys of `.options` .
            # ⋅
            # ⋅By example, with:
            # ⋅
            # ⋅ # this is a comment
            # ⋅ %%XYZx%%|||
            # ⋅
            # ⋅ |||this a comment
            # ⋅ Not a comment
            # ⋅ # not a comment
            # ⋅ A
            # ⋅ B⏎
            # ⋅
            # ⋅... raises an error since "XYZx" isn't a key of .options .
            error = TextFileError()
            error.msgid = "ETR-ERRORID006"
            error.msg = "Ill-formed file : " \
                f"Illegal name ('{optdef.group('name')}') for a " \
                "'options_definition(regex)'. " \
                f"Authorized names are {tuple(self.options.keys())}."
            error.fals = fals
            self.errors.append(error)
        else:
            # (pimydoc)ETR.options
            # ⋅ETR.options is a dict(str:None|bool|func) describing what to do when
            # ⋅reading/writing.
            # ⋅
            # ⋅
            # ⋅o  "allow_leftspaces_syntax(json)" [JSON ! see below]
            # ⋅   a boolean allowing (or not) the left-spaces syntax
            # ⋅
            # ⋅o  "authorised tags(json)" [JSON ! see below]
            # ⋅   (list of str) list of authorised tags
            # ⋅
            # ⋅o  "comment_lineprefix"
            # ⋅   (str)line prefix defining a comment line
            # ⋅
            # ⋅o  "filetobeincluded_lineprefix"
            # ⋅   (str)line prefix defining an import
            # ⋅
            # ⋅o  "options_definition(regex)" [JSON ! see below]
            # ⋅   Regex defining how modify the items of .options.
            # ⋅   This regex must have the following groups:
            # ⋅        'name', 'value'
            # ⋅
            # ⋅o  "read line:normal:yield": (bool)
            # ⋅    yield an ETRLine object if a "normal line" has been read ?
            # ⋅o  "read line:normal:event": None,
            # ⋅    name of the method to be called if a "normal line" has been read.
            # ⋅
            # ⋅o  "read line:empty line/comment:yield": (bool)
            # ⋅    yield an ETRLine object if an empty line or a comment has been read ?
            # ⋅o  "read line:empty line/comment:event": None,
            # ⋅    name of the method to be called if an empty line or a comment has been read.
            # ⋅
            # ⋅o  "read line:None:event": None,
            # ⋅    name of the method to be called if a None line (=error) has been read.
            # ⋅
            # ⋅o  "read line:options_definition:yield": (bool)
            # ⋅    yield an ETRLine object if a "options_definition" line has been read ?
            # ⋅o  "read line:options_definition:event": None,
            # ⋅    name of the method to be called if a "options_definition" line has been
            # ⋅    read.
            # ⋅
            # ⋅o  "read line:variable:yield": (bool)
            # ⋅    yield an ETRLine object if a variable line has been read ?
            # ⋅o  "read line:variable:event": None
            # ⋅    name of the method to be called if a variable line has been read.
            # ⋅
            # ⋅o  "read line:tag:yield": (bool)
            # ⋅    yield an ETRLine object if a tag line has been read ?
            # ⋅o  "read line:tag:event": None
            # ⋅    name of the method to be called if a tag line has been read.
            # ⋅
            # ⋅o  "remove left spaces": True
            # ⋅   if True lstrip() the read line.
            # ⋅
            # ⋅o  "tag(regex)" [REGEX ! see below]
            # ⋅    (str/bytes) regex defining a tag key/value
            # ⋅    This regex must have the following groups:
            # ⋅        'name', 'key', 'value'
            # ⋅
            # ⋅o  "tobecontinued_char"
            # ⋅   (str)character defining a to-be-continued line
            # ⋅
            # ⋅o  "variable(regex)" [REGEX ! see below]
            # ⋅   (str/bytes) regex defining a variable setting.
            # ⋅
            # ⋅If a key contains the "(regex)" suffix, its value must be (str)regex
            # ⋅or a (byte)re.compile() object.
            # ⋅
            # ⋅If a key contains the "(json)" suffix, its value is a Python object
            # ⋅that can be read from a string through json.loads()
            # ⋅
            # ⋅Please not that there is no "read line:None:yield" entry since
            # ⋅None is always yielded in this case.
            if optdef.group("name").endswith("(regex)"):
                try:
                    self.options[optdef.group("name")] = \
                       re.compile(optdef.group("value"))
                    self._init_optionsdef__regex_checks(name=optdef.group("name"),
                                                        fals=fals)

                except re.error as err:
                    # (pimydoc)error::ETR-ERRORID007
                    # ⋅This error will be raised it's impossible to compile the
                    # ⋅regex defining a new options_definition.
                    # ⋅
                    # ⋅By example, with: (regex splitted on two lines)
                    # ⋅  %%tag_kv(regex)%%^\:?P<name>[^:]+)\:
                    # ⋅    \s*(?P<key>[^\s]*)\s*\:\s*(?P<value>[^\s]*)$
                    # ⋅
                    # ⋅An error will be raise since we should have:
                    # ⋅    ^\:(?P<name>[^:]+)\...
                    # ⋅and not:
                    # ⋅    ^\:?P<name>[^:]+)\...
                    error = TextFileError()
                    error.msgid = "ETR-ERRORID007"
                    error.msg = "Ill-formed file : " \
                        f"can't interpret new options_definition. " \
                        f"Can't compile regex {optdef.group('value')} " \
                        f"Python error is '{err}' ."
                    error.fals = fals
                    self.errors.append(error)
            elif optdef.group("name").endswith("(json)"):
                try:
                    self.options[optdef.group("name")] = \
                        json.loads(optdef.group("value"))
                except json.decoder.JSONDecodeError as err:
                    # (pimydoc)error::ETR-ERRORID008
                    # ⋅This error will be raised it's impossible to json-loads()
                    # ⋅the source string defining a json value.
                    # ⋅
                    # ⋅By example, with:
                    # ⋅  %%authorised tags(json)%%("abbreviation", "tag")
                    # ⋅
                    # ⋅An error will be raise since we should have:
                    # ⋅  %%authorised tags(json)%%["abbreviation", "tag"]
                    # ⋅and not:
                    # ⋅  %%authorised tags(json)%%("abbreviation", "tag")
                    error = TextFileError()
                    error.msgid = "ETR-ERRORID008"
                    error.msg = "Ill-formed file : " \
                        "can't interpret json string " \
                        f"'{optdef.group('value')}'. " \
                        f"Python error is '{err}' ."
                    error.fals = fals
                    self.errors.append(error)
            else:
                self.options[optdef.group("name")] = optdef.group("value")

    def _init_optionsdef__regex_checks(self,
                                       name,
                                       fals):
        """
            ETR._init_optionsdef__regex_checks()

            Internal method.
            Submethod of _init_optionsdef() .

            Check if the regex in self.options[name] is OK


            ___________________________________________________________________

            ARGUMENTS:
            o  (str)name: key in .options[]
            o  (list of FAL)fals: the FALs objects associated to the <optdef>.

            no RETURNED VALUE
        """
        regex = self.options[name]

        # (pimydoc)error::ETR-ERRORID011
        # ⋅Error raised if the regex named 'options_definition(regex)' doesn't
        # ⋅have 2 groups, namely 'name', 'value'. (see ETR-ERRORID011)
        # ⋅
        # ⋅By example you can define this regex this way:
        # ⋅  %%options_definition(regex)%%°°(?P<name>[^:]+)°°(?P<value>.+)
        # ⋅but not this way:
        # ⋅  %%options_definition(regex)%%°°(?P<nameZZZ>[^:]+)°°(?P<value>.+)
        if name == "options_definition(regex)":
            if "name" not in regex.groupindex or \
               "value" not in regex.groupindex:
                error = TextFileError()
                error.msgid = "ETR-ERRORID011"
                error.msg = "Ill-formed file : " \
                    "Regex defined for 'options_definition(regex)' tag" \
                    "must have a 'name' and a 'value' group names." \
                    f"Read regex is '{regex.pattern}'; regex.groupindex is {regex.groupindex} ."
                error.fals = fals
                self.errors.append(error)

        # (pimydoc)error::ETR-ERRORID012
        # ⋅Error raised if the regex named 'tag_kv(regex)' doesn't
        # ⋅have 3 groups : 'name', 'key', 'value'. (see ETR-ERRORID012)
        # ⋅
        # ⋅By example you can define this regex this way:
        # ⋅  %%tag_kv(regex)%%^\:(?P<name>[^:]+)\:
        # ⋅    \s*(?P<key>[^\s]*)\s*\(:\s*(?P<value>[^\s]*))?$
        # ⋅but not this way:
        # ⋅  %%tag_kv(regex)%%^\:(?P<name>[^:]+)\:
        # ⋅    \s*(?P<keyZZZ>[^\s]*)\s*\(:\s*(?P<value>[^\s]*))?$
        if name == "tag_kv(regex)":
            if "name" not in regex.groupindex or \
               "key" not in regex.groupindex or \
               "value" not in regex.groupindex:
                error = TextFileError()
                error.msgid = "ETR-ERRORID012"
                error.msg = "Ill-formed file : " \
                    "Regex defined for 'tag_kv(regex)' tag" \
                    "must have a 'name', a 'value' and a 'key' group names." \
                    f"Read regex is '{regex.pattern}'; regex.groupindex is {regex.groupindex} ."
                error.fals = fals
                self.errors.append(error)

    def _parse_read_line(self,
                         line: str):
        """
            ETR._parse_read_line()

            Internal method used to parse a line that has just been read.


            ___________________________________________________________________

            ARGUMENT:
                o (str)line: the line that has been read

            RETURNED VALUE: ( (None|str)line,
                              (tuple of str)flags
                            )
                line:  the line to be yielded or None if the line doesn't have to be yielded
                flags: a tuple of str or None if the line doesn't have to be yielded
        """
        read_flags = []

        # ---- is(are) there flag(s) ? ----------------------------------------
        if "flag" in self.read_tags:
            for flag_symbol, flag_value in self.read_tags["flag"].items():
                if flag_symbol in line:
                    line = line.replace(flag_symbol, "").strip()
                    read_flags.append(flag_value)

        # ---- is there abbreviation(s) to expand ? ---------------------------
        line = self._expand_abbrev(src=line)

        # ---- returned value -------------------------------------------------
        # (pimydoc)flags
        # ⋅Flags are sorted alphabetically via the sorted() function.
        # ⋅In fine, flags must be a tuple of strings : they can't be None.
        return (line.replace(self.options["tobecontinued_char"],
                             ""),
                tuple(sorted(read_flags)))

    def _parse_read_line__tag(self,
                              line: str,
                              fals):
        """
            ETR._parse_read_line__tag()

            Submethod of ETR._parse_read_line()

            Check if <line> contains a tag; if it's the case, modify .read_tags .


            ___________________________________________________________________

            ARGUMENTS:
            o  (str)line        : the line where the tag could be read.
            o  (list of FAL)fals: the FALs objects associated to the <line>.

            RETURNED VALUE: ((bool)has a tag been read in <line> ?,
                             (str)tag name,
                             (str)tag value,
                            )
        """
        res = False

        tag = re.search(self.options["tag_kv(regex)"],
                        line)
        if tag:
            res = True
            if tag.group("name") in self.options["authorised tags(json)"]:

                # empty .read_tags[tag.group("name")] ? Let's create an empty dict
                # for it:
                if tag.group("name") not in self.read_tags:
                    self.read_tags[tag.group("name")] = {}

                # if possible: .read_tags[~name][~key] = ~value
                if tag.group("key") in self.read_tags[tag.group("name")]:
                    # (pimydoc)error::ETR-ERRORID004
                    # ⋅This error will be raised if a tag is defined twice for the same key.
                    # ⋅
                    # ⋅By example...
                    # ⋅  :abbreviation: ᵛⁱ : v+i
                    # ⋅  :abbreviation: ᵛⁱ : something else
                    # ⋅
                    # ⋅... raises an error since "ᵛⁱ" is defined twice as an abbreviation.
                    error = TextFileError()
                    error.msgid = "ETR-ERRORID004"
                    error.msg = "Ill-formed file : " \
                        f"Duplicate tag key '{tag.group('key')}'"
                    error.fals = fals
                    self.errors.append(error)
                else:
                    self.read_tags[tag.group("name")][tag.group("key")] = \
                        tag.group("value")

                    if tag.group("name") == "abbreviation" and tag.group("value") is None:
                        # (pimydoc)error::ETR-ERRORID009
                        # ⋅Abbreviations must be defined with a key and its value.
                        # ⋅
                        # ⋅By example, the following lines...
                        # ⋅  :abbreviation: N : nominative
                        # ⋅  :abbreviation: V
                        # ⋅... will raise an error since abbreviation "V" has no value.
                        error = TextFileWarn()
                        error.msgid = "ETR-ERRORID009"
                        error.msg = f"Can't read abbreviation '{tag.group('key')}' : empty content."
                        error.fals = fals
                        self.errors.append(error)

                    elif tag.group("name") == "flag" and tag.group("value") is None:
                        # (pimydoc)error::ETR-ERRORID010
                        # ⋅Flags must be defined with a key and its value.
                        # ⋅
                        # ⋅By example, the following lines...
                        # ⋅  :flag: ĸ : little_k
                        # ⋅  :flag: ł
                        # ⋅... will raise an error since flag "ł" has no value.
                        error = TextFileWarn()
                        error.msgid = "ETR-ERRORID010"
                        error.msg = f"Can't read flag '{tag.group('key')}' : empty content."
                        error.fals = fals
                        self.errors.append(error)

            else:
                # (pimydoc)error::ETR-ERRORID005
                # ⋅This error will be raised if a tag name is declared when it is not an
                # ⋅authorized name.
                # ⋅
                # ⋅By example, if .options["authorised tags(json)"] is
                # ⋅('abbreviation',), then
                # ⋅  :abbreviation: ᵛⁱ : something else
                # ⋅  :XYZ: ᵛⁱ          : v+i
                # ⋅
                # ⋅... raises an error since 'XYZ' isn't defined in
                # ⋅.options["authorised tags(json)"].
                error = TextFileError()
                error.msgid = "ETR-ERRORID005"
                error.msg = "Ill-formed file : " \
                    f"Unknown tag name '{tag.group('name')}'; " \
                    "Authorized tag names are: " \
                    f"{self.options['authorised tags(json)']}."
                error.fals = fals
                self.errors.append(error)

            return res, tag.group("name"), tag.group("value")

        return res, None, None

    def _parse_read_line__variable(self,
                                   line: str,
                                   fals):
        """
            ETR._parse_read_line__variable()

            Submethod of ETR._parse_read_line()

            Check if <line> contains a variable; if it's the case, modify .read_variables .

            (pimydoc)ETR.read_variables
            ⋅.read_variables[variable_name] = (value, fals)
            ⋅
            ⋅The fals item is the last time the variables has been set.


            ___________________________________________________________________

            ARGUMENTS:
            o  (str)line        : the line where the variable could be read.
            o  (list of FAL)fals: the FALs objects associated to the <line>.

            RETURNED VALUE: ((bool)has a variable been read in <line> ?,
                             (str)variable name,
                             (str)variable value)
        """
        res = False

        variable = re.search(self.options["variable(regex)"],
                             line)
        if variable:
            res = True
            if variable.group("value") is None or variable.group("value") == "":
                # (pimydoc)error::ETR-ERRORID013
                # ⋅A variable's value can't be an empty string.
                # ⋅
                # ⋅By example you can't write something like...
                # ⋅    /variable_name/
                # ⋅... since the value read for 'variable_name' is an empty string.
                error = TextFileError()
                error.msgid = "ETR-ERRORID013"
                error.msg = "A variable value can't be an empty string. " \
                    f"Variable read was '{variable.group('name')}'."
                error.fals = fals
                self.errors.append(error)

            self.read_variables[variable.group("name")] = (variable.group("value"), fals)

            return res, variable.group("name"), variable.group("value")

        return res, None, None

    def _read(self,
              source_filename: str):
        """
            ETR._read()

            Internal method.
            Submethod of ETR.read() : this method may be called recursively by
            ._read2().

            Read <source_filename> and its nested subfiles.

            GENERATOR !


            ___________________________________________________________________

            ARGUMENTS:
            o  (str)source_filename: path to the file to be read

            YIELDED VALUE : - either None if an error occured.
                            - either ETRLine
        """
        # (pimydoc)error::ETR-ERRORID002
        # ⋅This error will be raised if a file F1 tries to import a file F2 and if F2
        # ⋅has already import F1, maybe by means of several intermediate files.
        # ⋅
        # ⋅By example, if F1 only contains the line:
        # ⋅+++F2
        # ⋅And if F2 only contains the line:
        # ⋅+++F1
        # ⋅... this error will be raised.
        # ⋅
        # ⋅By example, if F1 only contains the line:
        # ⋅+++F2
        # ⋅And if F2 only contains the line:
        # ⋅+++F3
        # ⋅And if F3 only contains the line:
        # ⋅+++F1
        # ⋅... this error will be raised.
        if source_filename in self._nested_files:
            error = TextFileError()
            error.msgid = "ETR-ERRORID002"
            error.msg = "Cyclic import in '{source_filename}' ." \
                f"Parent files already read are f{self._nested_files}"
            self.errors.append(error)
            yield from self._read_action(TLFF(line_inttype=ETRLINE_INTTYPE__NONE))
            return

        self._nested_files.append(source_filename)

        # (pimydoc)error::ETR-ERRORID000
        # ⋅Error raised if the source file to be read is missing.
        if not os.path.exists(source_filename):
            error = TextFileError()
            error.msgid = "ETR-ERRORID000"
            error.msg = "Missing ETR MusaMusa text file '{source_filename}' ."
            self.errors.append(error)
            yield from self._read_action(TLFF(line_inttype=ETRLINE_INTTYPE__NONE))
            return

        # main loop:
        try:
            yield from self._read2(source_filename,
                                   line_to_be_continued=False,
                                   next_line=None)
        except KeyError:
            # (pimydoc)error::ETR-ERRORID003
            # ⋅This error will be raised if `self.options` is wrongly modified during the
            # ⋅reading loop.
            error = TextFileError()
            error.msgid = "ETR-ERRORID003"
            error.msg = f"Can't read '{source_filename}'. " \
                f"Python error is (KeyError)'{traceback.format_exc()}'."
            self.errors.append(error)

            yield from self._read_action(TLFF(line_inttype=ETRLINE_INTTYPE__NONE))

        self._nested_files.pop()

    def _read2(self,
               source_filename,
               line_to_be_continued,
               next_line):
        """
            ETR._read2()

            Internal method.
            Submethod of ETR._read()

            Iterator reading <source_filename> and yielding a list of
            ETRLine objects.

            Nested files declared inside a file may be recursively read through
            this method.


            __________________________________________________________________

            ARGUMENTS:
            o  source_filename      : (str) the path to the file to be read
            o  line_to_be_continued : (bool) True if last read line had the
                                      "tobecontinued_char" symbol.
            o  next_line            : an ETRLine object.

            YIELDED VALUE : - either None if an error occured.
                            - either ETRLine
        """
        # It is not possible for me - for the moment? - to simplify this method
        # and split it into several sub-methods, hence the following lines:
        #
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        # pylint: disable=too-many-locals
        opt = self.options

        with open(source_filename,
                  encoding="utf-8") as content:

            line_index = 0
            for line_index, _line in enumerate(content):

                # ---- warning: tobecontinued_char not at the end of <_line.strip()>
                if self.options["tobecontinued_char"] in _line and \
                   not _line.strip().endswith(self.options["tobecontinued_char"]):
                    # (pimydoc)error::ETR-WARNINGID000
                    # ⋅The tobecontinued_char character (e.g. '⬂') can but shouldn't be placed
                    # ⋅elsewhere than at the end of a string.
                    # ⋅
                    # ⋅By example the following line...
                    # ⋅
                    # ⋅  abc ⬂ def ⬂
                    # ⋅
                    # ⋅...will raise a warning.
                    error = TextFileWarn()
                    error.msgid = "ETR-WARNINGID000"
                    error.msg = "Maybe a problem in a file : " \
                        f"tobecontinued_char '{self.options['tobecontinued_char']}' " \
                        "found elsewhere than at the end of the line where it should have been."
                    error.fals = (FileAndLine(filename=source_filename,
                                              lineindex=line_index+1),)
                    self.errors.append(error)

                # empty lines are ignored and comment lines are ignored:
                if _line.strip() == "" or _line.startswith(opt["comment_lineprefix"]):
                    yield from self._read_action(TLFF(line_inttype=ETRLINE_INTTYPE__COMMENTEMPTY,
                                                      fals=(FileAndLine(filename=source_filename,
                                                                        lineindex=line_index+1),),
                                                      flags=None,
                                                      line=_line.strip()))
                    continue

                # ---- is there a new "options_definition" ? ---------
                optdef = re.search(self.options["options_definition(regex)"],
                                   _line)
                if optdef:
                    self._init_optionsdef(optdef=optdef,
                                          fals=(FileAndLine(filename=source_filename,
                                                            lineindex=line_index+1),))
                    yield from self._read_action(
                        TLFF(line_inttype=ETRLINE_INTTYPE__OPTIONSDEFINITION,
                             fals=(FileAndLine(filename=source_filename,
                                               lineindex=line_index+1),),
                             flags=None,
                             line=_line.strip()))
                    continue

                # ---- is there a new variable definition ? ---------------------------
                is_a_variable, variable_name, variable_value = \
                    self._parse_read_line__variable(
                        line=_line,
                        fals=(FileAndLine(filename=source_filename,
                                          lineindex=line_index+1),))
                if is_a_variable:
                    # yes, it was a variable definition.
                    yield from self._read_action(
                        TLFF(line_inttype=ETRLINE_INTTYPE__VARIABLE,
                             fals=(FileAndLine(filename=source_filename,
                                               lineindex=line_index+1),),
                             flags=None,
                             line=_line.strip()),
                        details={"variable_name": variable_name,
                                 "variable_value": variable_value})
                    continue

                # ---- is there a new tag definition ? --------------------------------
                is_a_tag, tag_name, tag_value = \
                    self._parse_read_line__tag(line=_line,
                                               fals=(FileAndLine(filename=source_filename,
                                                                 lineindex=line_index+1),))

                if is_a_tag:
                    # yes, it was a variable definition.
                    yield from self._read_action(
                        TLFF(line_inttype=ETRLINE_INTTYPE__TAG,
                             fals=(FileAndLine(filename=source_filename,
                                               lineindex=line_index+1),),
                             flags=None,
                             line=_line.strip()),
                        details={"tag_name": tag_name,
                                 "tag_value": tag_value})
                    continue

                # with the "left-spaces syntax" we have to preserve left-spaces string,
                # hence the .rstrip() :
                line = _line.rstrip()

                # a special case : "left-spaces syntax" is enabled and <line> starts with
                # a least one space:
                if opt["allow_leftspaces_syntax(json)"] and line.startswith(" "):
                    # (pimydoc)error::ETR-ERRORID001
                    # ⋅This error is raised if options["allow_leftspaces_syntax(json)"]
                    # ⋅is True and if a line beginning with spaces can't joined to a
                    # ⋅preceding line.
                    # ⋅
                    # ⋅By example, trying to read such a file...
                    # ⋅
                    # ⋅__B     (first line of the file, '_' is a space)
                    # ⋅C
                    # ⋅D       (last line of the file)
                    # ⋅
                    # ⋅...will raise this error.
                    if next_line is None:
                        error = TextFileError()
                        error.msgid = "ETR-ERRORID001"
                        error.msg = "Ill-formed file : " \
                            "first line can't be added to a precedent line " \
                            "since the first character(s) of the first " \
                            "line are spaces " \
                            "and since <allow_leftspaces_syntax(json)> is True." \
                            f" line_index={line_index}"
                        error.fals = (FileAndLine(filename=source_filename,
                                                  lineindex=line_index+1),)
                        self.errors.append(error)
                    else:
                        # let's join <line> to the current <next_line>:
                        if opt["remove left spaces"]:
                            next_line.line += "\n" + line.lstrip()
                        else:
                            next_line.line += "\n" + line

                        next_line.fals.append(FileAndLine(filename=source_filename,
                                                          lineindex=line_index+1))
                        line_to_be_continued = line.endswith(opt["tobecontinued_char"])

                        continue

                if _line.startswith(opt["filetobeincluded_lineprefix"]):
                    # recursive call to read a nested file:
                    new_fname = _line.removeprefix(opt["filetobeincluded_lineprefix"]).strip()
                    # new_fname = source_filename + new_fname
                    new_fname = os.path.join(path_of(source_filename),
                                             new_fname)

                    if next_line:
                        # we have to flush the current <next_line> before reading
                        # a nested file.
                        next_line.line, next_line.flags = self._parse_read_line(
                            line=next_line.line)
                        if next_line.line:  # may be None (see self._parse_read_line())
                            yield from self._read_action(
                                TLFF(line_inttype=ETRLINE_INTTYPE__NORMAL,
                                     fals=tuple(next_line.fals),
                                     flags=next_line.flags,
                                     line=next_line.line))
                        next_line = None

                    # recursive call to self._read():
                    yield from self._read(new_fname)
                    continue

                # From now, the things go on without dealing with the "left-spaces syntax":
                if opt["remove left spaces"]:
                    line = line.lstrip()

                if line_to_be_continued:
                    # a special case : the current <next_line> (=the precedent line) was
                    # ended by ⬂:
                    next_line.line += "\n" + line
                    next_line.fals.append(FileAndLine(filename=source_filename,
                                                      lineindex=line_index+1))
                else:
                    # normal case:
                    # we flush <next_line>:
                    if next_line:
                        next_line.line, next_line.flags = self._parse_read_line(
                            line=next_line.line)
                        if next_line.line:  # may be None (see self._parse_read_line())
                            yield from self._read_action(
                                TLFF(line_inttype=ETRLINE_INTTYPE__NORMAL,
                                     fals=tuple(next_line.fals),
                                     flags=next_line.flags,
                                     line=next_line.line))

                    # we have a new <next_line>:
                    next_line = ETRLine(fals=[FileAndLine(filename=source_filename,
                                                          lineindex=line_index+1), ],
                                        line=line,
                                        line_inttype=ETRLINE_INTTYPE__NORMAL)

                # = does <line> end with ⬂ ?
                line_to_be_continued = line.endswith(opt["tobecontinued_char"])

        # let's flush <next_line>:
        if next_line:
            next_line.line, next_line.flags = self._parse_read_line(
                line=next_line.line)
            if next_line.line:  # may be None (see self._parse_read_line())
                yield from self._read_action(
                    TLFF(line_inttype=ETRLINE_INTTYPE__NORMAL,
                         fals=tuple(next_line.fals),
                         flags=next_line.flags,
                         line=next_line.line))

    def _read_action(self,
                     tlff,
                     details=None):
        """
            ETR._read_action()

            Internal method called when a line has been read.

            What to do when a <line>, <flags> has been read at <fals> ?

            This method may yield ETRLine(<line>) or call a method, depending
            on the content of .options["read line:xxx")


            ___________________________________________________________________

            ARGUMENTS:
            o  tlff                  : a TLFF object (line_inttype, line, flags, fals)

            o  (None|dict)details    : (str:str) details about the read line.
               (pimydoc)ETR._read_action():details
               ⋅<details> is a dict (str:str) allowing to store the last read variable or
               ⋅the last read tag.
               ⋅
               ⋅Known keys are:
               ⋅    o  "variable_name"
               ⋅    o  "variable_value"
               ⋅    o  "tag_name"
               ⋅    o  "tag_value"
               ⋅
               ⋅By example, details["variable_name"] and details["variable_value"] will
               ⋅give the last pair of read variable name/value.

            This method may yield ETRLine objects.
        """
        if tlff.line_inttype == ETRLINE_INTTYPE__NORMAL:
            if self.options["read line:normal:event"]:
                self.options["read line:normal:event"](tlff,
                                                       details)

            if self.options["read line:normal:yield"]:
                yield ETRLine(
                    fals=tlff.fals,
                    flags=tlff.flags,
                    line=tlff.line,
                    line_inttype=tlff.line_inttype)

        elif tlff.line_inttype == ETRLINE_INTTYPE__COMMENTEMPTY:
            if self.options["read line:empty line/comment:event"]:
                self.options["read line:empty line/comment:event"](tlff,
                                                                   details)

            if self.options["read line:empty line/comment:yield"]:
                yield ETRLine(
                    fals=tlff.fals,
                    flags=tlff.flags,
                    line=tlff.line,
                    line_inttype=tlff.line_inttype)

        else:
            # rarest cases:
            yield from self._read_action2(tlff,
                                          details)

    def _read_action2(self,
                      tlff,
                      details=None):
        """
            ETR._read_action2()

            Internal method, submethod of ._read_action2()

            _read_action2() deals with the rarest cases.

            See ._read_action() for more details.

            This method may yield ETRLine(<line>) or call a method, depending
            on the content of .options["read line:xxx")


            ___________________________________________________________________

            ARGUMENTS:
            o  tlff                  : a TLFF object (line_inttype, line, flags, fals)

            o  (None|dict)details    : (str:str) details about the read line.
               (pimydoc)ETR._read_action():details
               ⋅<details> is a dict (str:str) allowing to store the last read variable or
               ⋅the last read tag.
               ⋅
               ⋅Known keys are:
               ⋅    o  "variable_name"
               ⋅    o  "variable_value"
               ⋅    o  "tag_name"
               ⋅    o  "tag_value"
               ⋅
               ⋅By example, details["variable_name"] and details["variable_value"] will
               ⋅give the last pair of read variable name/value.

            This method may yield ETRLine objects.
        """
        if tlff.line_inttype == ETRLINE_INTTYPE__OPTIONSDEFINITION:
            if self.options["read line:options_definition:event"]:
                self.options["read line:options_definition:event"](tlff,
                                                                   details)

            if self.options["read line:options_definition:yield"]:
                yield ETRLine(
                    fals=tlff.fals,
                    flags=tlff.flags,
                    line=tlff.line,
                    line_inttype=tlff.line_inttype)

        elif tlff.line_inttype == ETRLINE_INTTYPE__VARIABLE:
            if self.options["read line:variable:event"]:
                self.options["read line:variable:event"](tlff,
                                                         details)

            if self.options["read line:variable:yield"]:
                yield ETRLine(
                    fals=tlff.fals,
                    flags=tlff.flags,
                    line=tlff.line,
                    line_inttype=tlff.line_inttype)

        elif tlff.line_inttype == ETRLINE_INTTYPE__TAG:
            if self.options["read line:tag:event"]:
                self.options["read line:tag:event"](tlff,
                                                    details)

            if self.options["read line:tag:yield"]:
                yield ETRLine(
                    fals=tlff.fals,
                    flags=tlff.flags,
                    line=tlff.line,
                    line_inttype=tlff.line_inttype)

        elif tlff.line_inttype is ETRLINE_INTTYPE__NONE:
            if self.options["read line:None:event"]:
                self.options["read line:None:event"](tlff,
                                                     details)

            # These lines are superfluous as the value None will be yielded
            # by the method anyway, at the end of the method:
            # if self.options["read line:None:yield"]:
            #     yield None

    def improved_str(self):
        """
            ETR.improved_str()
        """
        return f"{self.errors=}; {self.options=}; {self.read_tags=}; {self._nested_files=}"

    def postread_checks(self):
        """
            ETR.postread_checks()

            Method called at the end of ETR.read() : check that everything is in order
            once the main file and any included files have been read.

            Fill self.errors if necessary.


            ___________________________________________________________________

            no RETURNED VALUE
        """
        for tag_name in self.options["authorised tags(json)"]:
            if tag_name not in self.read_tags or not self.read_tags[tag_name]:
                # (pimydoc)error::ETR-WARNINGID001
                # ⋅No data declared for a tag.
                # ⋅If the read file(s) doesn't read any for a tag, this warning is raised.
                # ⋅
                # ⋅By example...
                # ⋅  %%options_definition(regex)%%°°(?P<name>[^°]+)°°(?P<value>.+)
                # ⋅  °°authorised tags(json)°°["abbreviation", "tag"]
                # ⋅  :tag: Tk : 4
                # ⋅  A
                # ⋅  B
                # ⋅  C
                # ⋅... will raise a warning since there is no data for the "abbreviation"
                # ⋅tag.
                error = TextFileWarn()
                error.msgid = "ETR-WARNINGID001"
                error.msg = "Maybe a problem in the read file(s) : " \
                    "authorised tags " \
                    f"are {self.options['authorised tags(json)']} " \
                    f"but the file(s) doesn't have any data for tag '{tag_name}' ."
                # this warning doesn't concerne one file but concerns all read file(s), i.e. the
                # first file and maybe nested files:
                error.fals = None
                self.errors.append(error)

    def read(self,
             source_filename: str):
        """
            ETR.read()

            Main method to read an etr-like file.

            This method calls ._read() and cannot be recursively called.


            ___________________________________________________________________

            ARGUMENTS:
            o  source_filename      : (str) the path to the file to be read

            no RETURNED VALUE
        """
        self.errors.clear()
        self.read_tags.clear()
        self.read_variables.clear()
        self._nested_files.clear()
        yield from self._read(source_filename)

        self.postread_checks()
