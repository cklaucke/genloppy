from genloppy.parser.filter.package import PackageFilter

FILTER = dict(package_names=PackageFilter)


def create(filter_name, values, **kwargs):
    return FILTER[filter_name](values, **kwargs)
