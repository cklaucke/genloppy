from genloppy.parser.filter.package import PackageFilter
from genloppy.parser.filter.regex import RegexFilter

FILTER = dict(package_names=PackageFilter,
              search_reg_exps=RegexFilter)


def create(filter_name, filter_config, **kwargs):
    """Returns a filter instance using filter_name.

    :param filter_name: name of the desired filter
    :param filter_config: filter configuration to initialize the filter with
    :param kwargs: optional keyword arguments to pass to the filter
    :returns a filter instance

    realizes: R-FILTER-001"""
    return FILTER[filter_name](filter_config, **kwargs)
