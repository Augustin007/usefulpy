import sys
from usefulpy.IDE import ide, run_path


n = list(sys.argv)
print(n)
if len(n) == 3:
    assert n[1].startswith('-')
    mode = n[1][1:]
    if mode == 'i':
        space = run_path(n[2])
        ide(space)
    else:
        raise RuntimeError('Invalid argument')
elif len(n) == 2:
    run_path(n[1])
elif len(n) == 1:
    ide()
else:
    raise RuntimeError('Error occured')

# eof
