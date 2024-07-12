import unittest
import xmlrunner
from test_performance_random import TestWeatherForecastAPIPerformance, TestWeatherForecastAPI

def regression_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestWeatherForecastAPIPerformance))
    suite.addTest(unittest.makeSuite(TestWeatherForecastAPI))
    return suite

if __name__ == '__main__':
    with open('./results/test_results.xml', 'wb') as output:
        runner = xmlrunner.XMLTestRunner(output='./results')
        unittest.TextTestRunner().run(regression_suite())
