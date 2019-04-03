from genloppy.parser.filter.package import PackageFilter
from genloppy.parser.filter.regex import RegexFilter

FILTER = dict(package_names=PackageFilter,
              search_reg_exps=RegexFilter)


def create(filter_name, values, **kwargs):
    return FILTER[filter_name](values, **kwargs)
