# -*- coding: utf-8 -*-
from Meta.ClassMetaManager import sunshine_class_meta
from Meta.TypeMeta import PBool
from Preset.Model import PartBaseMeta


@sunshine_class_meta
class UseConfigPartBaseMeta(PartBaseMeta):
    CLASS_NAME = "UseConfigPartBase"
    PROPERTIES = {
        "useConfig": PBool(text="是否导表", sort=100, default=False, group="通用", func=lambda _: {"visible": MC.Controller.studioParam.debug}),
    }


from Preset.Model.PartBase import PartBase

class UseConfigPartBase(PartBase):
    def __init__(self):
        # type: () -> None
        """
        导表零件基类
        """
        pass

