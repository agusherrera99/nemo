from pathlib import Path

def GetProjectRootPath() -> Path:
   projectRootPath = Path(__file__).parent.parent
   return projectRootPath
