from enum import Enum, IntEnum

from strenum import StrEnum
class CarTypes(StrEnum):

    CAR = 'car'
    TRUCK = 'truck'
    VAN = 'van'

IDtoClass = {'0.0': CarTypes.CAR, '2.0': CarTypes.TRUCK, '1.0': CarTypes.VAN}



class CarSpeedLimit:

    speedLimits = {CarTypes.CAR: 120, CarTypes.TRUCK: 60, CarTypes.VAN: 80}

    CAR = 120
    TRUCk = 60
    VAN = 80
    

class CarLegalVisColor:
    colors = {CarTypes.CAR: (255, 0, 0), CarTypes.TRUCK: (0, 255, 0), CarTypes.VAN: (0, 0, 255)}
    CAR = (255, 0, 0) # blue color
    Truck = (0, 255, 0) #green color
    VAN = (0, 0, 255) # red color


if __name__ == '__main__':


    print(CarTypes.VAN)

    print(CarSpeedLimit.VAN)

    print(CarLegalVisColor.VAN)