from enum import Enum

from ...icons import icon

CHANNEL_LABELS = ("Red", "Green", "Blue", "Alpha")
CHANNEL_ICONS = ("RGBA_RED", "RGBA_GREEN", "RGBA_BLUE", "RGBA_ALPHA")


class Channel(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2
    ALPHA = 3

    @property
    def label(self) -> str:
        return CHANNEL_LABELS[self.value]

    @property
    def icon(self) -> int:
        return icon(CHANNEL_ICONS[self.value])


def ChannelEnumItems(self, context):
    # Using a function because the icons are only available after register() is executed
    try:
        return ChannelEnumItems._backing
    except AttributeError:
        ChannelEnumItems._backing = tuple((ch.name, ch.label, "", ch.icon, ch.value) for ch in Channel)
        return ChannelEnumItems._backing


def ChannelWithNoneEnumItems(self, context):
    try:
        return ChannelWithNoneEnumItems._backing
    except AttributeError:
        ChannelWithNoneEnumItems._backing = tuple((ch.name, ch.label, "", ch.icon, ch.value) for ch in Channel) + (
            ("NONE", "None", "", "CANCEL", -1),
        )
        return ChannelWithNoneEnumItems._backing


def ChannelEnumFlagItems(self, context):
    # Using a function because the icons are only available after register() is executed
    try:
        return ChannelEnumFlagItems._backing
    except AttributeError:
        ChannelEnumFlagItems._backing = tuple((ch.name, ch.label, "", ch.icon, 1 << ch.value) for ch in Channel)
        return ChannelEnumFlagItems._backing


def attr_domain_size(mesh, attr) -> int:
    match attr.domain:
        case "POINT":
            return len(mesh.vertices)
        case "CORNER":
            return len(mesh.loops)
        case _:
            raise AssertionError(f"Unsupported domain '{attr.domain}'")
