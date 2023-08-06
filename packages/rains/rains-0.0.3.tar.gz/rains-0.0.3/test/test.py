from rains.kit.web import *
from rains.common.run_pool import RunPool


class Task01(WebTask):

    def __init__(self):
        self.text = '123'

    def set_function_starting(self):
        self.plant.view.to_url('http://www.baidu.com/')

    def case_01(self):
        print(self.text)
        self.plant.element(
            page='N',
            name='N',
            by_key='xpath',
            by_value='/html/body/div[1]/div[1]/div[5]/div/div/form/span[1]/input'
        ).input.send('测试测试')


# RunPool(
#     cores=[WebCore(), WebCore()],
#     tasks=[Task01, Task01, Task01]
# ).running()

core = WebCore()
core.start_task(Task01)

