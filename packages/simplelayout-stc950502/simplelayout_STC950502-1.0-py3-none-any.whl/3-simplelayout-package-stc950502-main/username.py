import os
import re
import sys


repo_name = os.getenv("repo_name")
# print(repo_name)
if repo_name is not None:
    match_obj = re.search(
        r"idrl-assignment/3-simplelayout-package-(.*)", repo_name
    )
    if match_obj:
        user_name = match_obj.group(1)
        print(user_name)
    else:
        sys.exit("No match!")
else:
    sys.exit("No repo name!")
