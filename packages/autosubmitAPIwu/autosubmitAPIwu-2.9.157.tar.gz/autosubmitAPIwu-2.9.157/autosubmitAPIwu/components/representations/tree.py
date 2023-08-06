#!/usr/bin/env python
from autosubmitAPIwu.components.jobs.joblist_loader import JobListLoader

class TreeRepresentation(object):
  def __init__(self, expid):
    self.expid = expid
    self.jobs = []
    self.joblist_loader = JobListLoader(expid)
    self._date_member_distribution = {}
    self._no_date_no_member_jobs = []
  
  def setup(self):
    self.joblist_loader.load_jobs()
    
  def distribute_date_member_distribution(self):
    for job in self.joblist_loader.jobs:
      if job.date is not None and job.member is not None:
        self._date_member_distribution.setdefault((job.date, job.member), []).append(job)
      elif job.date is not None and job.member is None:
        parents_members = {self.joblist_loader.job_dictionary.get(parent_name).member for parent_name in job.parents_names}
        children_members = {self.joblist_loader.job_dictionary.get(children_name).member for children_name in job.children_names}
        intersection_member_parent = self.joblist_loader.members & parents_members
        intersection_member_children = self.joblist_loader.members & children_members
        if len(intersection_member_parent) > 0 or len(intersection_member_children) > 0:
          member = intersection_member_parent[0] if len(intersection_member_parent) > 0 else intersection_member_children[0]        
          self._date_member_distribution.setdefault((job.date, member), []).append(job)
      else:
        self._no_date_no_member_jobs.append(job)
      

    


  
