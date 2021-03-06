import re

from genloppy.parser.entry_handler_wrapper import EntryHandlerWrapper
from genloppy.parser.pms import ATOM_BASE_PATTERN
from genloppy.parser.pms import ATOM_PATTERN
from genloppy.parser.pms import PACKAGE_NAME_PATTERN
from genloppy.parser.pms import VERSION_PATTERN


class PackageFilter(EntryHandlerWrapper):
    """
    Filters entry events for given packages.

    realizes: R-PARSER-FILTER-PACKAGE-001
    """

    def __init__(self, packages, **kwargs):
        """Initializes the filter with the given packages.

        realizes: R-PARSER-FILTER-PACKAGE-002
        """
        super().__init__()
        self.case_sensitive = kwargs.get("case_sensitive", False)
        self.atom_bases, self.package_names = self._store_packages(set(packages), self.case_sensitive)

    @staticmethod
    def _store_packages(packages, case_sensitive=False):
        # both pattern are case-insensitive due to their nature: no need to set re.I
        atom_matcher = re.compile(ATOM_PATTERN)
        atom_base_matcher = re.compile(ATOM_BASE_PATTERN)
        package_name_matcher = re.compile(PACKAGE_NAME_PATTERN)
        package_version_matcher = re.compile(PACKAGE_NAME_PATTERN + VERSION_PATTERN)
        atom_bases = []
        package_names = []
        malformed_packages = []

        for package in packages:
            if atom_base_matcher.fullmatch(package) and not atom_matcher.fullmatch(package):
                bucket = atom_bases
            elif package_name_matcher.fullmatch(package) and not package_version_matcher.fullmatch(package):
                bucket = package_names
            else:
                bucket = malformed_packages
            bucket.append(package)

        if malformed_packages:
            raise RuntimeError("Malformed packages given: '{}'. Aborting!"
                               .format(", ".join(malformed_packages)))

        def _adjust_case(iterable):
            return list(iterable if case_sensitive else map(lambda x: str.lower(x), iterable))

        return _adjust_case(atom_bases), _adjust_case(package_names)

    def test(self, properties):
        """Tests for relevant packages

        :param properties: tokens (key-value) of the entry event
        :return: True if any package matches, False otherwise

        realizes: R-PARSER-FILTER-PACKAGE-003
        """
        case_sensitive = self.case_sensitive

        def _lower(name):
            return name.lower() if name and not case_sensitive else name

        atom_base = _lower(properties.get("atom_base"))
        package_name = _lower(properties.get("package_name"))

        return atom_base in self.atom_bases or package_name in self.package_names
