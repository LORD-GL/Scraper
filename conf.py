import funcs
class Conf:
    ACCESSORS_LIST = [549745613, 852489448]
    driver = ""

    @classmethod
    def configPage(cls):
        cls.driver = funcs.set_driver()
        funcs.close_windows(cls.driver)
        funcs.setscales(cls.driver)

    @classmethod
    def closePage(cls):
        funcs.close_driver(cls.driver)