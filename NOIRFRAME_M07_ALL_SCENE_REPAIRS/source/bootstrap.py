from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
# M03 controller imports are isolated copies. No original source file is edited.
sys.path.insert(0,str(ROOT/'source/legacy'))
