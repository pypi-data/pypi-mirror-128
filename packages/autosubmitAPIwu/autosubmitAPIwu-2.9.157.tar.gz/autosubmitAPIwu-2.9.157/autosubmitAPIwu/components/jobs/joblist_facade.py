#!/usr/bin/env python
from autosubmitAPIwu.job.job_list import JobList
from autosubmitAPIwu.database.db_jobdata import JobDataStructure
from autosubmitAPIwu.config.basicConfig import BasicConfig
from autosubmitAPIwu.job.job_utils import datechunk_to_year

class JobListFacade(object):
  def __init__(self, expid, simple_jobs):
    # type : (str, BasicConfig, List[SimpleJob]) -> None
    self.basic_config = BasicConfig # type : BasicConfig
    self.basic_config.read()
    self.job_to_package = {} # type : Dict
    self.package_to_jobs = {} # type : Dict
    self.package_to_package_id = {} # type : Dict
    self.package_to_symbol = {} # type : Dict
    self.job_running_time_to_seconds = {} # type : Dict
    self.job_running_time_to_text = {} # type : Dict
    self._run_id_to_run_object = {} # type : Dict
    self.warning_messages = [] # type : List
    self.expid = expid # type : str
    self.simple_jobs = simple_jobs # type : List
    self._initialize_main_values()

  def _initialize_main_values(self):
    # type : () -> None
    self.job_to_package, self.package_to_jobs, self.package_to_package_id, self.package_to_symbol = JobList.retrieve_packages(
            self.basic_config, self.expid)
    self.job_running_time_to_seconds, self.job_running_time_to_text, self.warning_messages  = JobList.get_job_times_collection(
                self.basic_config, self.simple_jobs, self.expid, self.job_to_package, self.package_to_jobs, timeseconds=True)
    
    
  def update_with_timedata(self, section_jobs):
    """ Update Job information with JobRow (time) data from Historical Database """
    # type : (List[Job]) -> None
    for job in section_jobs:
      if job.name in self.job_running_time_to_seconds:
        job.update_from_jobrow(self.job_running_time_to_seconds[job.name])
  
  def update_with_yps_per_run(self, section_jobs):
    """ Update Job information with Historical Run information: years_per_sim  """
    # type : (List[Job]) -> None
    self._retrieve_current_experiment_runs_required(section_jobs)
    for job in section_jobs:
      job.set_years_per_sim(self._get_yps_per_run_id(job.run_id))
  
  def _retrieve_current_experiment_runs_required(self, section_jobs):
    # type : (List[Job]) -> None
    for job in section_jobs:
      self._add_experiment_run(job.run_id)

  def _get_yps_per_run_id(self, run_id):
    # type : (int) -> float
    experiment_run = self._run_id_to_run_object.get(run_id, None)
    if experiment_run:
      return datechunk_to_year(experiment_run.chunk_unit, experiment_run.chunk_size)
    else:
      return 0.0
  
  def _add_experiment_run(self, run_id):
    # type : (int) -> None
    if run_id and run_id not in self._run_id_to_run_object:
      self._run_id_to_run_object[run_id] = JobDataStructure(self.expid).get_experiment_run_by_id(run_id)





    


