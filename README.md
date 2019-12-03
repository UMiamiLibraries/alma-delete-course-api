# alma-delete-course-api

Python script to delete courses in Alma that dont have reading lists. accepts 1 parameter of blackboard term code (ex. 20171) for spring 2017).


## delete_courses.py
the main file. pass in an argument such as "delete_courses.py 20171" and it will delete courses with the course term of 20171 that don't have reading lists. Steps: Pulls all courses, searches each course for ones with reading lists, and deletes the ones that don't have a reading list.

## searchable_id_count.py
test file to get counts.
