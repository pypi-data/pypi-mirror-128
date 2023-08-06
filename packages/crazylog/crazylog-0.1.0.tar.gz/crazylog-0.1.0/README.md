```python
from crazylog import CrazyLogger

def run_code():
   print('running code ...')

with CrazyLogger() as crazy:
   run_code()


class CustomClass:
   pass

with CrazyLogger() as crazy:
   crazy.exclusively = [CustomClass]
   run_code()
```