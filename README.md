WPExam - creation of pre-populated exam locations

usage:

    import wpexam
    phd_relay = wpexam.Exam()
    
An exam is another name for 'test', to differentiate from all the test
driven, unittest, and other nomenclature. Provides a unique filesystem
location for the exam test data, pre-populated with useful system
information. This includes a numbered, unique directory structure and
details about the hostname, operating system, etc.
