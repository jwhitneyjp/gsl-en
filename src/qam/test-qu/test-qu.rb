# Copyright 2007 by Starling Software, K.K.
# This is part of QAM from http://www.starling-software.com.
# For license terms, see the LICENSE.QAM file included with this distribution.

require 'fileutils'
require 'tempfile'

i = QAM::Install.new; d = i.dirs

qu = d.release('bin', 'qu')
ENV['QAM_TEMPLATE_PROJECTS'] = d.mine('test-qu', 'template_a') + ':' +
    d.mine('test-qu', 'template_b')
FileUtils.chdir(d.mine('test-qu', 'project'))

test_options = [
    '-h',
    '',
    '-r',
    '-d',
    '-r -d',
    '-s atpl,proj srv',
    '-m',
    'top_a_same top_a_projdiff top_a_projmissing',
    'src',
    'src/d2_a_projdiff src/d2_a_projmissing',
    'src/d2_a_projdiff/3_a_projdiff src/d2_a_projdiff/3_a_projmissing src/d2_a_projdiff/3_a_same',
]
test_options.each { |options|
    command = "#{qu} #{options}"
    expected_filename = d.mine('test-qu',
	'expected/out.' + options.gsub(' ', '').gsub('/', ','))
    actual = `#{command}`.
	gsub(d.mine('test-qu'), 'PROJECT_DIR').
	gsub(/\t*\d{4}-\d{2}-\d{2}[ \d:.+]*/, '')
    if options != '-h' && !$?.success?
	$stderr.puts("ERROR: Failed to run \"#{command}\"")
	$stderr.puts("Return code #{$?.exitstatus}, output:")
	$stderr.puts(actual)
	exit(1)
    end

    #File.open(expected_filename, 'w') { |s| s.write(actual) }

    expected = File.open(expected_filename, 'r') { |s| s.read }
    unless expected == actual
	$stderr.puts("ERROR: Output not as expected: #{command}")
	tf = Tempfile.new('qu')
	tf.write(actual)
	tf.close
	system("diff -u '#{expected_filename}' '#{tf.path}'")
	tf.unlink
	exit(1)
    end
}
