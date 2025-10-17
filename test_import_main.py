import sys
print('sys.path[0]=', sys.path[0])
try:
    import main
    print('main imported ok', main)
except Exception as e:
    import traceback
    traceback.print_exc()
    raise
