import os
import unittest

from wpexam.exam import Exam

class Test(unittest.TestCase):
     
    def test_exam_directory(self):
        exam = Exam()

        # sub-directory under exam-results that is the node name
        dir_name = "exam_results/%s" % exam.node
        result = os.path.exists(dir_name)
        self.assertTrue(result)

        # That has a sub directory of ???? which is numbers, never
        # overwriting. Check the timestamp to make sure it's created
        # within the past N interval to verify newness
        # Sort directory names in numerical order

        # Sort directory names in numerical order
        sort_dir = os.listdir(dir_name)
        sort_dir = [int(x) for x in sort_dir]
        sort_dir.sort()

        last_dir = "%s/%s" % (dir_name, sort_dir[-1])
        created_time = os.path.getctime(last_dir)
        print "Last by name: %s, %s" % (last_dir, created_time)
        
        import time
        curr_time = time.time()
        # time.time() and os.path.getctime have differing levels of
        # precision on windows. Add some time fudge to make sure the
        # folder is created. This will create false positives if you
        # rapidly create multiple exam folders.
        self.assertLess(created_time-3, curr_time)

        # And has the systeminfo text output in the folder
        sys_info_file = "%s/%s_system_info.txt" % (last_dir,
                                                   sort_dir[-1])
        print "Find file: %s" % sys_info_file
        result = os.path.exists(sys_info_file)
        self.assertTrue(result)
       
    def test_find_last_exam(self):
        import shutil
        temp_root = "temporary_exam_root"
        if os.path.exists(temp_root):
            shutil.rmtree(temp_root)

        self.assertFalse(os.path.exists(temp_root))

        # Create an exam, then delete the director it created, and make
        # sure the find last exam returns the start value of 1
        node_name = "test_node" 
        ex = Exam("to_empty", temp_root, node_name)
        top_level = "%s/%s" % (temp_root, node_name)
        shutil.rmtree(top_level)
        self.assertFalse(os.path.exists(top_level))
        
        fail_find = ex.find_last_exam(temp_root, node_name)
        self.assertEqual("1", fail_find)

        # Enter a random number of pre-existing tests
        import random
        rand_count = random.randint(1, 10)
        for i in range(rand_count):
            full_path = "%s/%s/%s" % (temp_root, node_name, i)
            result = os.makedirs(full_path)
            self.assertTrue(os.path.exists(full_path))


        # Create an exam with the same information, verify that the
        # returned exam directory is one bigger
        ex = Exam("test_name", temp_root, node_name)
        # exam creation calls find_last_exam

        latest = ex.find_last_exam(temp_root, node_name)
        # find last returns the last + 1, 

        full_guess = "%s/%s/%s" % (temp_root, node_name, rand_count+1)
        full_last = "%s/%s/%s" % (temp_root, node_name, latest)
        self.assertEquals(full_guess, full_last)
       
 
        shutil.rmtree(temp_root)

if __name__ == "__main__":
    unittest.main()
