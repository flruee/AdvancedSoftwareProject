import sys
if len(sys.argv)==2:
    if(sys.argv[1]=="start"):
        from frontend.main import run
        run()

    elif(sys.argv[1]=="test"):
        import pytest
        code = pytest.main(['restAPIConnection'])
        sys.exit(code)

