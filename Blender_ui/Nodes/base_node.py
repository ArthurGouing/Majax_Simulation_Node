#############################################################
# Copyright (C) 2025 Arthur Gouinguenet - All Rights Reserved
# This file is part of Majax Simulation Node project which is
# delivered under GNU General Public Liscense.
# For any questions or requests related to the use of this work
# please contact me directly at arthur.gouinguenet@free.fr
#############################################################


# Base class for all custom nodes of the Majax nodetree.
# Defines a poll function to enable instantiation.
class BaseNode:
    bl_width_default = 220

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == "CustomTreeType"