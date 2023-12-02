import pytest

from genloppy.parser.filter.package import PackageFilter


def test_01_well_formed_packages():
    """Tests that well-formed packages do not raise.

    tests: R-PARSER-FILTER-PACKAGE-001
    tests: R-PARSER-FILTER-PACKAGE-002
    """
    packages = ["www-client/firefox", "glibc", "x11-libs/gtk+", "GTK+"]
    PackageFilter(packages)


def test_02_malformed_packages():
    """Tests that malformed packages raise.

    tests: R-PARSER-FILTER-PACKAGE-001
    tests: R-PARSER-FILTER-PACKAGE-002
    """
    packages = ["www-client//firefox", "www-client/firefox-55", "gcc-8", "glibc-1.0", "-lib"]
    with pytest.raises(RuntimeError) as cm:
        PackageFilter(packages)

    assert cm.match("Malformed packages given")
    for package in packages:
        assert cm.match(package)


def test_03_predicate_case_insensitive():
    """Tests that the predicate returns correct values.

    tests: R-PARSER-FILTER-PACKAGE-001
    tests: R-PARSER-FILTER-PACKAGE-003
    """
    packages = ["www-client/firefox", "glibc", "X11-LIBS/gtk+", "Gtk+"]
    p = PackageFilter(packages)

    assert not p.test(dict())
    assert p.test(dict(atom_base="www-client/firefox"))
    assert p.test(dict(package_name="glibc"))
    assert p.test(dict(atom_base="x11-libs/gtk+"))
    assert p.test(dict(package_name="GTK+"))


def test_04_predicate_case_sensitive():
    """Tests that the predicate returns correct values.

    tests: R-PARSER-FILTER-PACKAGE-001
    tests: R-PARSER-FILTER-PACKAGE-003
    """
    packages = ["www-client/firefox", "glibc", "X11-LIBS/gtk+", "Gtk+"]
    p = PackageFilter(packages, case_sensitive=True)

    assert not p.test(dict())
    assert p.test(dict(atom_base="www-client/firefox"))
    assert p.test(dict(package_name="glibc"))
    assert not p.test(dict(atom_base="x11-libs/gtk+"))
    assert not p.test(dict(package_name="GTK+"))
