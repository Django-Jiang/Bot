from .handle import NotificationHandle
from CEACStatusBot.request import query_status
from CEACStatusBot.captcha import CaptchaHandle,OnnxCaptchaHandle
import os,pytz,datetime

class NotificationManager():
    def __init__(self,location:str,number:str,passport_number:str,surname:str,captchaHandle:CaptchaHandle=OnnxCaptchaHandle("captcha.onnx")) -> None:
        self.__handleList = []
        self.__location = location
        self.__number = number
        self.__captchaHandle = captchaHandle
        self.__passport_number = passport_number
        self.__surname = surname

    def addHandle(self, notificationHandle:NotificationHandle) -> None:
        self.__handleList.append(notificationHandle)

    def send(self,) -> None:
        res = query_status(self.__location, self.__number, self.__passport_number, self.__surname, self.__captchaHandle)

        # if res['status'] == "Refused":
        try:
            TIMEZONE = os.environ["TIMEZONE"]
            localTimeZone = pytz.timezone(TIMEZONE)
            localTime = datetime.datetime.now(localTimeZone)
        except pytz.exceptions.UnknownTimeZoneError:
            print("UNKNOWN TIMEZONE Error, use default")
            localTime = datetime.datetime.now()
        except KeyError:
            print("TIMEZONE Error")
            localTime = datetime.datetime.now()

        if localTime.hour < 8 or localTime.hour > 19:
            print("Not working hour")
            return
        if localTime.weekday() >= 5:
            print("In weekend")
            return

        for notificationHandle in self.__handleList:
            notificationHandle.send(res)
