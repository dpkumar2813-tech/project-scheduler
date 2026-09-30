import unittest
from scheduler import schedule
class SchedulerTests(unittest.TestCase):
    def test_parallel_and_slack(self):
        tasks=[{'id':'a','duration':2},{'id':'b','duration':4,'dependencies':['a']},{'id':'c','duration':5},{'id':'d','duration':2,'dependencies':['b','c']},{'id':'e','duration':1,'dependencies':['d']}]
        result=schedule(tasks,'2026-09-30',['2026-10-02'])
        self.assertEqual(result['duration'],9)
        self.assertEqual(next(t for t in result['tasks'] if t['id']=='c')['slack'],1)
        self.assertEqual(result['finish'],'2026-10-13')
    def test_cycle(self):
        with self.assertRaisesRegex(ValueError,'Circular'): schedule([{'id':'a','duration':1,'dependencies':['b']},{'id':'b','duration':1,'dependencies':['a']}],'2026-09-30')
    def test_unknown(self):
        with self.assertRaisesRegex(ValueError,'Unknown'): schedule([{'id':'a','duration':1,'dependencies':['x']}],'2026-09-30')
    def test_empty(self): self.assertEqual(schedule([],'2026-09-30')['duration'],0)
if __name__=='__main__': unittest.main()
