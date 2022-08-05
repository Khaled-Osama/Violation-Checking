


from abc import ABC, abstractmethod

class Block(ABC):

    @abstractmethod
    def execut(self):
        pass

    def onStart(self, blockName, logger):
        logger.info(f'{blockName} is starting')

    def onEnd(self, blockName, logger):
        logger.info(f'{blockName} is finished')