from genloppy.processor.base import BaseOutput


class Merge(BaseOutput):
    """List merge processor implementation
    realizes: R-PROCESSOR-MERGE-001
    realizes: R-PROCESSOR-MERGE-002
    """
    HEADER = " * packages merged:\n"

    def __init__(self, **kwargs):
        """Adds callback for 'merge'.
        realizes: R-PROCESSOR-MERGE-003"""
        super().__init__(callbacks={"merge_end": self.process},
                         **kwargs)

    def process(self, properties):
        """Prints merge information.
        realizes: R-PROCESSOR-MERGE-004"""
        self.output.merge_item(properties["timestamp"], properties["atom_base"], properties["atom_version"])
