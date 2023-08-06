from . import ZFPInstructions, ZDSInstructions

class ZFPDSInstructions(ZFPInstructions, ZDSInstructions):
    '''Implements the basic Z-Code instructions'''
    def __init__(self):
        super(ZFPDSInstructions, self).__init__()
