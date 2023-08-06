import enum
from collections.abc import MutableMapping
from configparser import ConfigParser, NoOptionError
from json.decoder import JSONDecodeError
import os
import logging
import re
import json
from typing import List


class ObjectValue:

    def __eq__(self, other):
        if isinstance(other, ObjectValue):
            return self._name == other._name and self._value == other._value
        return False

    @classmethod
    def fromString(cls, str_val):
        """
        Creates a ObjectValue object from a given string
        string format must be '{object_name}{object}'
        Example: 'X{"key", "value"}'
        """
        obj_val = cls.parse_string(str_val)
        return cls(name=obj_val[0], value=obj_val[1])

    def parse_string(str_val: str) -> List[str]:
        """
        Parses object value string
        returns: List[str]
            [0] object_name
            [1] object_string (json)
        """
        try:
            obj_val_rgx = r"(\w*)([{].*?[}])$"
            result = re.search(obj_val_rgx, str_val)
            object_name = result.group(1)
            object_string = result.group(2)
            return [object_name, object_string]
        except AttributeError:
            raise AttributeError(f"Cant find an object in the stirng: {str_val}")

    @classmethod
    def is_object_value(cls, str_val) -> bool:
        """
        Checks if a given str_val is an object value
        """
        try:
            result = cls.parse_string(str_val)
            return bool(result[1])
        except:
            return False

    def __init__(self, name="", value="{}") -> None:
        """
        string representation of the object. Value must be parsable to a valid json object {}
        It must containing the surrounding curly brackets. Value cannot be an array, only an object.
        Example: {key1: 42, key3: "Foo"}
        """
        self._name = name

        self._value = value

    def __str__(self) -> str:
        return f"{self._name}{self._value}"

    @property
    def as_dict(self):
        return json.loads(self._value)

    @as_dict.setter
    def as_dict(self, val):
        self._value = json.dumps(val)

    def add(self, key, value, override=True):
        """
        add key/value pair to self._value depending on override flag.
        If override False and value exist return false otherwise true. No error
        """
        dict_val = json.loads(self._value)
        if override:
            dict_val[key] = value
            self.as_dict = dict_val
            return True
        else:
            if key in self.as_dict:
                return False
            else:
                dict_val[key] = value
                self.as_dict = dict_val
                return True


class OppParser(ConfigParser):

    def __init__(self, **kwargs):
        kwargs.setdefault("interpolation", None)
        kwargs.setdefault("inline_comment_prefixes", "#")
        super().__init__(**kwargs)

    def optionxform(self, optionstr):
        return optionstr

    @classmethod
    def resolve_includes(cls, ini_path, output_path=None, encoding="utf-8"):
        """
        Read and resolve include directives in ini_path and return string representation.
        This will work on the string representation only and wil thus keep comment intact.
        If output_path is given save result as new file
        """
        opp = cls()
        file_content = opp.create_temp_file_with_includes([ini_path])[0]

        if output_path is None:
            return file_content

        # check if output_path is dir and add file name if it is.
        if os.path.isdir(output_path):
            output_path = os.path.join(output_path,
                                       os.path.basename(ini_path))

        with open(output_path, "w") as f:
            f.writelines(file_content)
        return file_content

    def read(self, filenames, encoding=None):

        if isinstance(filenames, (str, bytes, os.PathLike)):
            filenames = [filenames]

        file_contents = self.create_temp_file_with_includes(filenames)

        if len(file_contents) > 1:
            raise ValueError("Only one *.ini file allowed.")

        # TODO allow multiple files
        read_ok = super().read_string(file_contents[0])
        return read_ok

    def create_temp_file_with_includes(self, filenames):

        file_contents = list()

        for f in filenames:
            self.ini_root_path = os.path.dirname(os.path.abspath(f))
            file_content = self.get_file_content_recursively(f)
            file_contents.append(file_content)

        return file_contents

    def get_lines_include(self, filename):

        line_nrs = list()

        with open(filename) as f:
            lines = f.readlines()

        for index in range(len(lines)):
            if lines[index].__contains__("include"):
                line_nrs.append(index)

        return line_nrs

    def has_file_include(self, filename):

        line_nrs = self.get_lines_include(filename)
        if len(line_nrs) == 0:
            return False
        else:
            return True

    def write_sections(self, fp, sections, space_around_delimiters=True):
        """Write an .ini-format representation of the configuration state.

        If `space_around_delimiters' is True (the default), delimiters
        between keys and values are surrounded by spaces.
        """
        if space_around_delimiters:
            d = " {} ".format(self._delimiters[0])
        else:
            d = self._delimiters[0]

        for section in sections:
            self._write_section(fp, section,
                                self._sections[section].items(), d)

    def get_file_content_recursively(self, f_):

        logging.info(f" Relative path found: {f_}")
        f = os.path.join(os.path.abspath(f_))
        logging.info(f"Generate absolute path: {f_} ")

        if os.path.isfile(f):
            logging.info("Set current dir to. \n")
        else:
            f = os.path.abspath(os.path.join(self.current_dir, f_))

            logging.info("No file absolute file path found. \n")
            logging.info(f"Try: {f_} ")

        self.current_dir = os.path.dirname(f)

        with open(f) as f_:
            file_content = f_.read()

        lines = self.get_lines_include(f)

        for l in lines:
            inc_file_name, replace_string = self.get_inc_file_name(f, l)

            print(f"{f} has file include: {self.has_file_include(f)} ({inc_file_name})")

            if self.has_file_include(f):
                file_content = file_content.replace(
                    replace_string, self.get_file_content_recursively(inc_file_name)
                )
                self.current_dir = self.ini_root_path

        return file_content

    def get_inc_file_name(self, filename, index):

        with open(filename) as f:
            lines = f.readlines()

        inc_file = lines[index].split(" ")[-1].split("\n")[0]
        return inc_file, lines[index]


class OppConfigType(enum.Enum):
    """
    Set type on OppConfigFileBase to create read-only configurations if needed.
    """

    READ_ONLY = 1
    EDIT_LOCAL = 2
    EXT_DEL_LOCAL = 3

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        elif type(other) is int:
            return self.value < other
        return NotImplemented

    def __gt__(self, other):
        return self != other and other < self

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        elif type(other) is int:
            return self.value == other
        return NotImplemented

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other


class OppConfigFileBase(MutableMapping):
    """
    Represents an omnetpp.ini file. The extends logic is defined in SimulationManual.pdf p.282 ff.
    Each OppConfigFileBase object has a reference to complete omnetpp.ini configuration file but
    only access's its own options, as well as all options reachable by the search path build
    using the 'extends' option.

    Example(taken form [1]):
    The search path for options for the configuration `SlottedAloha2b` is:
    SlottedAloha2b->SlottedAloha2->SlottedAlohaBase->HighTrafficSettings->General
    ```
    [General]
    ...
    [Config SlottedAlohaBase]
    ...
    [Config LowTrafficSettings]
    ...
    [Config HighTrafficSettings]
    ...

    [Config SlottedAloha1]
    extends = SlottedAlohaBase, LowTrafficSettings
    ...
    [Config SlottedAloha2]
    extends = SlottedAlohaBase, HighTrafficSettings
    ...
    [Config SlottedAloha2a]
    extends = SlottedAloha2
    ...
    [Config SlottedAloha2b]
    extends = SlottedAloha2
    ```
    [1]: https://doc.omnetpp.org/omnetpp/manual/#sec:config-sim:section-inheritance
    """

    @classmethod
    def from_path(
            cls, ini_path, config, cfg_type=OppConfigType.EDIT_LOCAL, is_parent=False
    ):
        _root = OppParser()
        _root.read(ini_path)
        _base_dir = os.path.dirname(ini_path)

        return cls(_root, config, _base_dir, cfg_type, is_parent)

    def __init__(
            self,
            root_cfg: OppParser,
            config_name: str,
            _base_dir: str,
            cfg_type=OppConfigType.EDIT_LOCAL,
            is_parent=False,
    ):
        self._root: OppParser = root_cfg
        self._cfg_type = cfg_type
        self._sec = self._ensure_config_prefix(config_name)
        self._base_dir = _base_dir

        if not self._has_section_(self._sec):
            raise ValueError(f"no section found with name {self._sec}")
        self._parent_cfg = []
        self._section_hierarchy = [self._ensure_config_prefix(self._sec)]
        self._is_parent = is_parent
        if not self._is_parent:
            stack = [iter(self.parents)]
            while stack:
                for p in stack[0]:
                    if p == "":
                        continue
                    _pp = OppConfigFileBase(self._root, p, self._base_dir, is_parent=True)
                    self._parent_cfg.append(_pp)
                    self._section_hierarchy.append(self._ensure_config_prefix(p))
                    if len(_pp.parents) > 0:
                        stack.append(iter(_pp.parents))
                else:
                    stack.pop(0)

        if config_name != "General" and self._has_section_("General"):
            self._parent_cfg.append(
                OppConfigFileBase(self._root, "General", self._base_dir, is_parent=True)
            )
            self.section_hierarchy.append("General")

    @property
    def base_path(self):
        return self._base_dir

    @property
    def all_sections(self):
        return self._root.sections()

    @property
    def section_hierarchy(self):
        return self._section_hierarchy

    def resolve_path(self, key):
        val = self.__getitem__(key)
        p = re.compile('absFilePath\("(.*)"\)')
        m = p.match(val)
        if m:
            return os.path.join(self.base_path, m.group(1))
        else:
            return os.path.join(self.base_path, val.strip('"'))

    def read(self):
        self.read()
        pass

    def writer(self, fp, selected_config_only=False):
        """ write the current state to the given file descriptor. Caller must close file."""
        if selected_config_only:
            # write current section hierarchy with General first (reverse list)
            self._root.write_sections(fp, self.section_hierarchy[::-1])
        else:
            self._root.write(fp)

    @staticmethod
    def _ensure_config_prefix(val):
        """ All omnetpp configurations start with 'Config'. Add 'Config' if it is missing.  """
        if not val.startswith("Config") and val != "General":
            return f"Config {val.strip()}"
        return val

    @property
    def section(self):
        """ Section managed by this OppConfigFileBase object (read-only) """
        return self._sec

    @property
    def parents(self):
        """ local parents i.e all configurations listed in the 'extends' option (read-only) """
        return [
            s.strip()
            for s in self._getitem_local_("extends", default="").strip().split(",")
        ]

    @property
    def type(self):
        return self._cfg_type

    def is_local(self, option):
        """
        Returns True if the given object belongs directly to the current section and False if
        options is contained higher up the hierarchy OR does not exist.
        """
        return self._contains_local_(option)

    def get_config_for_option(self, option):
        """
        Returns the name of the section the option first occurs search order: local --> general
        or None if option does not exist
        """
        if self._contains_local_(option):
            return self.section
        else:
            for p in self._parent_cfg:
                if p._contains_local_(option):
                    return p.get_config_for_option(option)
        return None

    def _is_json_list(self, _str) -> bool:
        # todo: replace with is object value
        obj_rgx = r"[\[].*?[\]]$"
        return bool(re.search(obj_rgx, str(_str)))

    def _has_section_(self, sec):
        """
        True if section exist in the configuration. Note: Returns also True even if given section is not
        in the section_hierarchy if the current section.
        """
        return self._root.has_section(sec)

    def _getitem_local_(self, k, default=None):
        """
        Search for key in local configuration
        """
        try:
            item = self._root.get(self._sec, k)
            if "\n" in item:
                item = item.replace("\n", " ")
            if ObjectValue.is_object_value(item):
                return ObjectValue().fromString(item)
            if self._is_json_list(item):
                return json.loads(item)
            else:
                return self._root.get(self._sec, k)
        except NoOptionError:
            if default is not None:
                return default
            else:
                raise KeyError(f"key not found. Key: {k}")
        except KeyError:
            return self._root.get(self._sec, k)
        except json.JSONDecodeError as e:
            raise KeyError(f"key '{k}' has invalid json value: '{item}' ")

    def _set_local(self, k, v):
        """
        Set new value for key. OppConfigType checks already done
        """
        self._root.set(self._sec, k, v)

    def _contains_local_(self, k):
        """
        True if key exist in current section (parents are not searched) otherwise False
        """
        return self._root.has_option(self._sec, k)

    def _contained_by_parent(self, k):
        """
        True if key exists in any parent. Note key my exist multiple time but only first occurrence of key
        will be returned. See search path.
        """
        return any([k in parent for parent in self._parent_cfg])

    def _delitem_local(self, k):
        """
        Delete local key.
        """
        self._root.remove_option(self._sec, k)

    def __setitem__(self, k, v):
        if self._cfg_type is OppConfigType.READ_ONLY:
            raise NotImplementedError("Cannot set value on read only config")

        if self._contains_local_(k):
            self._set_local(k, v)
        elif self._contained_by_parent(k):
            if self._cfg_type <= OppConfigType.EDIT_LOCAL:
                raise NotImplementedError("Cannot edit value of parent config")
            else:
                for p in self._parent_cfg:
                    if p._contains_local_(k):
                        p._set_local(k, v)
                        return
        else:
            raise KeyError(f"key not found. Key: {k}")

    def __delitem__(self, k):
        if self._cfg_type.value < OppConfigType.EXT_DEL_LOCAL:
            raise ValueError(
                f"current object does not allow deletion. cfg_type={self._cfg_type}"
            )
        if k not in self:
            raise KeyError(f"key not found. Key: {k}")
        if self._contains_local_(k):
            self._root.remove_option(self._sec, k)
        else:
            raise NotImplementedError(
                f"deletion of parent config option not implemented"
            )

    def __getitem__(self, k):
        if k not in self:
            raise KeyError(f"key not found. Key: {k}")

        if self._contains_local_(k):
            return self._getitem_local_(k)
        else:
            for parent in self._parent_cfg:
                try:
                    return parent._getitem_local_(k)
                except KeyError:
                    pass
        raise KeyError(f"key not found. Key: {k}")

    def __contains__(self, k) -> bool:
        if self._contains_local_(k):
            return True
        elif any([k in parent for parent in self._parent_cfg]):
            return True
        else:
            return False

    def __len__(self) -> int:
        _len = 0
        for s in self._section_hierarchy:
            _len += len(self._root.items(s))
        return _len

    def __iter__(self):
        for s in self._section_hierarchy:
            for item in self._root.items(s):
                yield item

    def items(self):
        return list(self.__iter__())

    def keys(self):
        return [k for k, _ in self.__iter__()]

    def values(self):
        return [v for _, v in self.__iter__()]

    def get(self, k):
        return self[k]

    def setdefault(self, k, default=...):
        if k in self:
            return self[k]
        else:
            if self._cfg_type <= OppConfigType.EDIT_LOCAL:
                raise NotImplementedError(
                    "Cannot set value on READ_ONLY or EDIT_LOCAL config. Use EXT_DEL_LOCAL "
                )
            else:
                self._set_local(k, default)
        return default


class OppConfigFile(OppConfigFileBase):
    """
    Helpers to manage OMNeT++ specifics not part of the standard ini-Configuration
    * Read/Write int and doubles
    * specify units (i.e. s, dBm, m)
    * Handle string quotes (are part of the value)
    todo: implement
    """

    def __init__(self, root_cfg: OppParser, config_name: str):
        super().__init__(root_cfg, config_name)


if __name__ == "__main__":
    OppParser.resolve_includes(
        "/home/vm-sts/repos/crownet/crownet/simulations/mucFreiheitLte/omnetpp.ini",
        output_path="/home/vm-sts/repos/crownet/crownet/simulations/mucFreiheitLte/omnetpp_merged.ini"
    )
