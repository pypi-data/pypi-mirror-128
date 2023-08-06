#!/usr/bin/env python

import unittest
from autosubmitAPIwu.components.representations.tree import TreeRepresentation

class TestTreeRepresentation(unittest.TestCase):
  def setUp(self):
      pass
      
  def tearDown(self):
      pass
  
  def test_load(self):    
    tree = TreeRepresentation("a29z") 
    tree.setup()
    tree.distribute_date_member_distribution()
    for key, jobs in tree._date_member_distribution.items():
      print(key)
      for job in jobs:
        print(job.name)
        # print(job.do_print())
    print("Others:")
    for job in tree._no_date_no_member_jobs:
      print(job.name)

if __name__ == '__main__':
  unittest.main()
  

