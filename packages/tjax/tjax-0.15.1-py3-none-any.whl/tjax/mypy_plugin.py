from mypy.plugin import Plugin
import mypy.plugins.dataclasses

class CustomPlugin(Plugin):
    pass

def plugin(version: str) -> CustomPlugin:
    mypy.plugins.dataclasses.dataclass_makers.add('tjax._src.dataclasses.dataclass.dataclass')
    # mypy.plugins.dataclasses.field_makers.add('tjax._src.dataclasses.helpers.field')
    return CustomPlugin
