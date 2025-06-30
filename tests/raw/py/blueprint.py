from plutonkit import Blueprint
import shutil,os
import subprocess
import time

app = Blueprint()


def run(ar):
 folder_name = ar["folder_name"]
 framework = ar["framework"]
 redis= ar["redis"]
 database= ar["database"]

 shutil.move(f"{folder_name}/manage.py", ".")
 os.remove(f"{folder_name}/{folder_name}/urls.py")
 shutil.move(f"{folder_name}/{folder_name}", f"{folder_name}_clone1")
 os.rmdir(f"{folder_name}")
 shutil.move(f"{folder_name}_clone/.env", ".env")

 os.rename(f"{folder_name}_clone1", f"{folder_name}")
 if framework == "None":
  shutil.move(f"{folder_name}_clone/project/default/urls.py", f"{folder_name}")
  shutil.move(f"{folder_name}_clone/health", f"{folder_name}")
  shutil.rmtree(f"{folder_name}_clone")
  subprocess.Popen(f"python scriptload.py setting_app {folder_name} default", shell=True)


 if framework == "django_graphbox":
  shutil.move(f"{folder_name}_clone/project/graphbox/urls.py", f"{folder_name}")
  shutil.move(f"{folder_name}_clone/graph_schema", f"{folder_name}")
  shutil.rmtree(f"{folder_name}_clone")
  subprocess.Popen(f"python scriptload.py setting_app {folder_name} graphbox", shell=True)


 if framework == "django_rest_framework":
  shutil.move(f"{folder_name}_clone/project/drf/urls.py", f"{folder_name}")
  shutil.move(f"{folder_name}_clone/apphealth", f"{folder_name}")
  shutil.rmtree(f"{folder_name}_clone")
  subprocess.Popen(f"python scriptload.py setting_app {folder_name} drf", shell=True)


 if framework == "django_ninja":
  shutil.move(f"{folder_name}_clone/ninja/drf/urls.py", f"{folder_name}")
  shutil.rmtree(f"{folder_name}_clone")

 if database != "none":
  subprocess.Popen(f"python scriptload.py setting_db_app {folder_name} default", shell=True)

 if redis == "yes":
  subprocess.Popen(f"python scriptload.py setting_cache_app {folder_name} default ", shell=True)
 time.sleep(5)
 os.remove("scriptload.py")
