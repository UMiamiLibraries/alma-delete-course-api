# alma-delete-course-api

Python script to delete courses in Alma that dont have reading lists. accepts 1 parameter of blackboard term code (ex. 20171) for spring 2017).


## delete_courses.py
the main file. run this, passing in an argument such as "delete_courses.py 20171" and it will delete courses with the course term of 20171 that don't have reading lists. Pulls all courses, searches each course for ones with reading lists, and deletes the ones that don't have a reading list.

### required packages
1. requests
2. lxml

### notes
the course term (ex. 20171) is specific to UM and should be removed for other institutions.

query search (q) did not work at the time I created this, but it might work in the future.

The code takes quite a bit of time to run, perhaps a few hours if you have a few thousand courses.

logging file is optional. beautifulsoup is also optional for printing to a file.


## searchable_id_count.py
test file to get counts.
