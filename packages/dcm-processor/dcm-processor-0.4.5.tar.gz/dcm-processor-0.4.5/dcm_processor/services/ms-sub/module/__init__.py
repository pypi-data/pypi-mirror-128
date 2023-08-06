import os
from .sub import get_dicoms, process
import pydicom
import datetime
DATA = os.getenv("DATA")
dir_path = os.path.dirname(os.path.realpath(__file__))

def sort_lambda(x):
  dt = x.get("studyDate")
  tm = x.get("studyTime")
  try:
    dt_tm = datetime.datetime(int(str(dt)[:4]), int(str(dt)[4:6]), int(str(dt)[6:8]), int(str(tm)[:2]), int(str(tm)[2:4]), int(str(tm)[4:6]))
    return dt_tm
  except:
    return None

def worker(jobName, headers, params, added_params, **kwargs):
  
  if (not DATA is None):
    dcmpath = os.path.join(DATA,headers.get("dcmpath"))
    series = headers.get("seriesIds", [])

    sel_series = []
    for s in series:
      pth = os.path.join(dcmpath, s)
      files = get_dicoms(pth)
      if len(files) > 0:
        ds = pydicom.dcmread(files[0])
        studydate = ds.StudyDate
        studytime = ds.StudyTime
        pps = ds.PerformedProcedureStepDescription
        if str(pps).lower().find("mssub") >= 0 and (len(str(studydate)) >= 8) and (len(str(studytime)) >= 6):
          sel_series.append({"seriesId": s, "studyDate": studydate, "studyTime": studytime})

    sel_series = sorted(sel_series, key=sort_lambda, reverse=False)

    if len(sel_series) >= 2:
      pre_series = sel_series[0].get("seriesId")
      post_series = sel_series[1].get("seriesId")
      conversions = added_params.get("dcm2nii", {}).get("conversions", {})
      sub_file = added_params.get(jobName, {}).get("sub_file")

      if not sub_file is None:
        sub_file = os.path.join(DATA, sub_file)
      
      pre_path = None
      post_path = None

      if str(pre_series) in conversions:
        pre_path = os.path.join(DATA, conversions.get(str(pre_series), {}).get("output"))

      if str(post_series) in conversions:
        post_path = os.path.join(DATA, conversions.get(str(post_series), {}).get("output"))
      
      if (not pre_path is None) and (not post_path is None):
        patient_folder = os.path.join(DATA, 'ms-sub', headers.get("id"))
        
        if not os.path.isdir(patient_folder):
          os.makedirs(patient_folder)

        process(pre_path, post_path, patient_folder, sub_file)