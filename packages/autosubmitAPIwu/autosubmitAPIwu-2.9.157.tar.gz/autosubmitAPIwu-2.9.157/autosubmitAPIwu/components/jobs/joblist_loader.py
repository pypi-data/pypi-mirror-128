#!/usr/bin/env python

from autosubmitAPIwu.components.jobs.joblist_facade import JobListFacade
from autosubmitAPIwu.components.experiment.pkl_organizer import PklOrganizer
from autosubmitAPIwu.components.experiment.configuration_facade import AutosubmitConfigurationFacade
from autosubmitAPIwu.components.jobs.job_factory import StandardJob
from autosubmitAPIwu.database.db_structure import get_structure
from typing import Dict

class JobListLoader(object):
  def __init__(self, expid):
    self.expid = expid
    self.configuration_facade = AutosubmitConfigurationFacade(expid)
    self.pkl_organizer = PklOrganizer(self.configuration_facade.pkl_path)
    self.joblist_facade = JobListFacade(expid, self.pkl_organizer.get_simple_jobs(self.configuration_facade.tmp_path))    
    self._jobs = [] # type : List[StandardJob]
    self._structure_adjacency = {} # type : Dict(str, List[str])
    self._job_dictionary = {} # type : Dict(str, Job)

  def load_jobs(self):
    self.pkl_organizer.identify_dates_members_sections()
    pkl_jobs = self.pkl_organizer.current_content
    self._jobs = [StandardJob().from_pkl(pkl_job) for pkl_job in pkl_jobs]
    self.load_existing_structure_adjacency()
    self.distribute_adjacency_into_list()
    self.assign_packages_to_jobs()
    self.assign_configuration_data_to_jobs()
    self.joblist_facade.update_with_timedata(self._jobs)
    self.configuration_facade.update_years_per_simulated_year_into_jobs(self._jobs)
    self._generate_job_dictionary()

  @property
  def jobs(self):
    return self._jobs

  @property
  def job_dictionary(self):
    return self._job_dictionary

  @property
  def chunk_unit(self):
    return self.configuration_facade.chunk_unit

  @property
  def chunk_size(self):
    return self.configuration_facade.chunk_size

  @property
  def dates(self):
    return self.pkl_organizer.dates

  @property
  def members(self):
    return self.pkl_organizer.members
  
  @property
  def sections(self):
    return self.pkl_organizer.sections
  
  @property
  def date_format(self):
    date_format = ''
    for date in self.pkl_organizer.dates:
      if date.hour > 1:
        date_format = 'H'
      if date.minute > 1:
        date_format = 'M'
    return date_format


  def load_existing_structure_adjacency(self):
    self._structure_adjacency = get_structure(self.expid, self.configuration_facade.structures_path)

  def distribute_adjacency_into_list(self):
    parents_adjacency = {}
    for job in self._jobs:
      job.children_names = set(self._structure_adjacency.get(job.name, []))
      for children_name in job.children_names:
        parents_adjacency.setdefault(children_name, set()).add(job.name)
    for job in self._jobs:
      job.parents_names = set(parents_adjacency.get(job.name, []))
  
  def assign_configuration_data_to_jobs(self):
    section_to_config = {}
    for job in self._jobs:
      if job.section in section_to_config:
        job.ncpus = section_to_config[job.section]["ncpus"]
        job.platform = section_to_config[job.section]["platform"]
        job.qos = section_to_config[job.section]["qos"]
      else:
        job.ncpus = self.configuration_facade.get_section_processors(job.section)
        job.platform = self._determine_platform(job.section)
        job.qos = self._determine_qos(job)
        section_to_config[job.section] = {"ncpus": job.ncpus, "platform": job.platform, "qos": job.qos}

  def _determine_platform(self, section_name):    
    job_platform = self.configuration_facade.get_section_platform(section_name)
    if len(job_platform.strip()) == 0:
      job_platform = self.configuration_facade.get_main_platform()
    return job_platform

  def _determine_qos(self, job):
    if job.package is not None:
      job_qos = self.configuration_facade.get_wrapper_qos()
    else:
      job_qos = self.configuration_facade.get_section_qos(job.section)
    if len(job_qos.strip()) == 0:
      job_qos = self.configuration_facade.get_platform_qos(job.platform)
    return job_qos

  def _generate_job_dictionary(self):
    for job in self._jobs:
      self._job_dictionary[job.name] = job

  def assign_packages_to_jobs(self):
    for job in self._jobs:
      job.package = self.joblist_facade.job_to_package.get(job.name, None)

  def do_print(self):
    for job in self._jobs:
      print(job)





