# Copyright 2006-2007 by Starling Software, K.K.
# This is part of QAM from http://www.starling-software.com.
# For license terms, see the LICENSE.QAM file included with this distribution.

require 'etc'
require 'test/unit/testcase'
require 'test/unit/testsuite'
require 'test/unit/ui/console/testrunner'

module QAM; class TestSuite

    COMMAND_LINE_OPTIONS = ARGV.take_while { |arg| arg.match(/^-/) }
    COMMAND_LINE_ARGUMENTS = ARGV.drop_while { |arg| arg.match(/^-/) }
    QUIET = COMMAND_LINE_OPTIONS.include?('-q')
    VERBOSE = COMMAND_LINE_OPTIONS.include?('-v') && !QUIET

    def self.functional_test_database_setup
	ENV['PGDATABASE'] ||= Etc.getlogin
	ENV['PGSCHEMA_PREFIX'] = 'functional_test'
	d = QAM::Install.new.dirs
	schemas = Dir["#{d.base('src', 'db')}/[a-z]*"].collect {
	    |path| File.basename(path) }
	schemas.each { |schema|
	    env_setup =
		'PGSCHEMA="' + ENV['PGSCHEMA_PREFIX'] + '_' + schema + '"'
	    error("can't load database schema #{schema}.") unless
		system("#{env_setup} \
		    #{QAM.dirs.bin('pg-load-schema')} -t -d \
		    #{d.base('src', 'db')}/#{schema}")
	}
    end

    def initialize(test_base, suite_name = default_suite_name)
	@test_base = test_base
	@suite_name = suite_name
	@requires = []
	@preloads = []
    end

    attr_reader :test_base, :suite_name, :requires, :preloads

    def default_suite_name
	parentdir, thisdir =
	    Install.new.dirs.mine.split(File::SEPARATOR)[-2..-1]
	thisdir == 'webtest' ? parentdir : thisdir
    end

    def require(*libs)
	@requires += libs
	self
    end

    def preload(*files)
	@preloads += files.collect { |f| "#{test_base}/#{f}" }
	self
    end

    def run
	install = test_base + '/Install'
	if File.exists?(install)
	    system("#{install} -q") || fail("Cannot run #{install} (#{$?})")
	end

	requires.each { |lib| Kernel::require lib }

	test_files = preloads + (Dir["#{test_base}/**/*.rt"].sort - preloads)
	test_files.each { |testfile| load testfile }

	pretest_class = nil
	test_classes = []
	test_regex = Regexp.compile('^(.*::)?TC_[^:]+$', Regexp::EXTENDED)
	ObjectSpace.each_object(Class) { |c|
	    pretest_class = c if c.name == 'Pretest'
	    test_classes << c if test_regex.match(c.to_s)
	}
	unless COMMAND_LINE_ARGUMENTS.empty?
	    test_classes = test_classes.select { |c|
		COMMAND_LINE_ARGUMENTS.detect {
		    |a| Regexp.new(a, Regexp::IGNORECASE).match(c.name) }
	    }
	    puts "Testing #{test_classes.join(' ')}" unless QUIET
	end

	verbosity = VERBOSE ? Test::Unit::UI::VERBOSE : Test::Unit::UI::SILENT

	if pretest_class
	    suite = Test::Unit::TestSuite.new("#{suite_name} pretest")
	    suite << pretest_class.suite
	    result = Test::Unit::UI::Console::TestRunner.run(suite, verbosity)
	    show_result(suite, result, QUIET)
	end

	suite = Test::Unit::TestSuite.new(suite_name)
	test_classes.each { |c| suite << c.suite }
	result = Test::Unit::UI::Console::TestRunner.run(suite, verbosity)
	show_result(suite, result, QUIET)
    end

    def show_result(suite, result, quiet = false)
	problems = result.instance_variable_get('@errors') +
	    result.instance_variable_get('@failures')
	if result.passed?
	    puts(suite.name + ": " + result.to_s) unless quiet
	else
	    $stderr.puts("\n" + problems.collect {
		|p| p.to_s }.join("\n\n") + "\n\n")
	    puts(suite.name + ": " + result.to_s)
	    $stderr.puts("***** FAILED")
	    exit(1)
	end
    end

end; end
